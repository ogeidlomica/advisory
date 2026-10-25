"""Per-font, ToUnicode-aware PDF text extractor (stdlib only, deterministic).

This module is the executable core of the document-extraction improvement
(task ``task-credi10-font-decoding-extraction``). The legacy extractor in
``engine.corpus`` pulled every ``( ... )`` literal out of every FlateDecode
stream with a single regex. That approach has two fatal problems for the
Credi10 corpus:

  1. It ingests **binary** bytes that merely happen to sit between parentheses
     inside decompressed image / font-program streams, flooding the extracted
     text with multi-kilobyte runs of non-word noise (``ÈÈÈfff¶¶¶...``). This
     crushes the honest useful-text ratio in :mod:`engine.knowledge` to ~1-2%,
     landing real documents in the ``nula`` / ``[EPISTEMIC-VOID]`` band even
     though a perfectly legible Spanish text layer is present.
  2. It applies NO per-font mapping, so text drawn with embedded
     ``Type0 / Identity-H`` fonts (whose glyph codes are mapped to unicode only
     through a ``/ToUnicode`` CMap) is either dropped or emitted as noise.

The extractor here fixes both by being *content-stream aware*:

  * It locates every PDF object and its stream robustly (indirect ``/Length``,
    ``\\r\\n`` / ``\\n`` / ``\\r`` variants) and decodes FlateDecode streams via
    :mod:`zlib`, skipping undecodable ones silently.
  * It parses each embedded font's ``/ToUnicode`` CMap
    (``beginbfchar``/``beginbfrange``, including the ``[<a><b>...]`` array form)
    plus ``/Encoding /Differences`` glyph-name tables, and associates every map
    with the font resource name (``/F1`` ...) through the page ``/Font`` dict.
  * It walks each content stream as a token stream, tracking the ACTIVE font
    via the ``Tf`` operator, and decodes ``Tj`` / ``TJ`` / ``'`` / ``"`` show
    operators (both ``( ... )`` literals with octal escapes and ``< ... >`` hex
    strings), mapping codes through the active font's table. Large negative
    kerning in ``TJ`` arrays inserts a word space.
  * It is **tolerant to failure**: a font with no ``/ToUnicode``, or any parse
    error on a stream or font, degrades to the legacy latin-1 clear-char
    behaviour and never aborts the document.

Everything is stdlib (``re`` + ``zlib``) and deterministic: stable ordering,
no timestamps, no randomness.
"""

from __future__ import annotations

import re
import zlib
from typing import Dict, List, Optional, Tuple


# --------------------------------------------------------------------------- #
# Object / stream location
# --------------------------------------------------------------------------- #

# `N G obj ... endobj`. We capture the object number and the body. The body is
# matched non-greedily up to the next `endobj`.
_OBJ_RE = re.compile(rb"(\d+)\s+\d+\s+obj\b(.*?)\bendobj", re.DOTALL)

# Indirect reference `N G R` inside a dictionary.
_REF_RE = re.compile(rb"(\d+)\s+\d+\s+R\b")

# A stream payload inside an object body. PDF allows the keyword `stream` to be
# followed by CRLF or a bare LF; the payload ends right before `endstream`.
_STREAM_BODY_RE = re.compile(rb"stream\r?\n(.*?)\r?\nendstream", re.DOTALL)
_STREAM_BODY_RE_LF = re.compile(rb"stream\r(.*?)endstream", re.DOTALL)


def _inflate(payload: bytes) -> Optional[bytes]:
    """Best-effort FlateDecode. Returns ``None`` when the payload is not zlib."""
    try:
        return zlib.decompress(payload)
    except Exception:
        # Some producers pad the stream; retry on a trimmed copy.
        try:
            return zlib.decompressobj().decompress(payload)
        except Exception:
            return None


class _PDFObject:
    """A located PDF object: its raw dictionary body and (optional) stream."""

    __slots__ = ("num", "body", "stream_raw")

    def __init__(self, num: int, body: bytes, stream_raw: Optional[bytes]):
        self.num = num
        self.body = body
        self.stream_raw = stream_raw


def _parse_objects(data: bytes) -> Dict[int, _PDFObject]:
    """Locate every ``N G obj ... endobj`` and its stream (if any).

    Robust to CRLF/LF variants. When an object appears more than once (updated
    PDFs), the LAST definition wins, matching the PDF xref-update semantics
    closely enough for text extraction.
    """
    objects: Dict[int, _PDFObject] = {}
    for m in _OBJ_RE.finditer(data):
        try:
            num = int(m.group(1))
        except (ValueError, TypeError):
            continue
        body = m.group(2)
        stream_raw: Optional[bytes] = None
        sm = _STREAM_BODY_RE.search(body)
        if sm is None:
            sm = _STREAM_BODY_RE_LF.search(body)
        if sm is not None:
            stream_raw = sm.group(1)
            # The dictionary is everything before the `stream` keyword.
            body = body[: sm.start()]
        objects[num] = _PDFObject(num, body, stream_raw)
    return objects


def _resolve_ref(body: bytes, key: bytes) -> Optional[int]:
    """Return the object number referenced by ``/key N 0 R`` inside ``body``."""
    # Find `/key` then the following `N 0 R`.
    km = re.search(re.escape(key) + rb"\s*", body)
    if km is None:
        return None
    rm = _REF_RE.match(body, km.end())
    if rm is None:
        # The value might not be adjacent (e.g. `/ToUnicode 1109 0 R`); search a
        # short window after the key.
        window = body[km.end(): km.end() + 24]
        rm2 = _REF_RE.search(window)
        if rm2 is None:
            return None
        return int(rm2.group(1))
    return int(rm.group(1))


# --------------------------------------------------------------------------- #
# ToUnicode CMap parsing
# --------------------------------------------------------------------------- #

_CODESPACE_RE = re.compile(
    rb"begincodespacerange(.*?)endcodespacerange", re.DOTALL)
_BFCHAR_RE = re.compile(rb"beginbfchar(.*?)endbfchar", re.DOTALL)
_BFRANGE_RE = re.compile(rb"beginbfrange(.*?)endbfrange", re.DOTALL)
_HEX_RE = re.compile(rb"<([0-9A-Fa-f]*)>")
_BRACKET_RE = re.compile(rb"\[(.*?)\]", re.DOTALL)


def _hex_to_unicode(h: bytes) -> str:
    """Decode a ToUnicode destination hex string into a Python str.

    Destinations may encode one or several UTF-16BE code units (ligatures).
    """
    if not h:
        return ""
    if len(h) % 2:
        h = h + b"0"
    try:
        raw = bytes.fromhex(h.decode("ascii"))
    except ValueError:
        return ""
    try:
        return raw.decode("utf-16-be")
    except Exception:
        # Fall back to treating each byte as latin-1.
        try:
            return raw.decode("latin-1")
        except Exception:
            return ""


class ToUnicodeMap:
    """A per-font code -> unicode table parsed from a ``/ToUnicode`` CMap."""

    __slots__ = ("mapping", "code_bytes")

    def __init__(self, mapping: Dict[int, str], code_bytes: int):
        self.mapping = mapping
        self.code_bytes = code_bytes

    def __bool__(self) -> bool:
        return bool(self.mapping)


def parse_tounicode_cmap(cmap: bytes) -> ToUnicodeMap:
    """Parse a ToUnicode CMap byte stream into a :class:`ToUnicodeMap`.

    Handles ``beginbfchar`` pairs ``<src> <dst>``, ``beginbfrange`` triples
    ``<lo> <hi> <dstBase>`` and the array form ``<lo> <hi> [<d0> <d1> ...]``.
    The source-code width (1 or 2 bytes) is detected from the codespace range
    or the width of the ``bfchar`` source keys.
    """
    mapping: Dict[int, str] = {}

    # Detect code width from the codespacerange (e.g. `<0000> <FFFF>` -> 2).
    code_bytes = 1
    cs = _CODESPACE_RE.search(cmap)
    if cs is not None:
        hexes = _HEX_RE.findall(cs.group(1))
        if hexes:
            width = max((len(h) + 1) // 2 for h in hexes if h)
            if width >= 1:
                code_bytes = width

    key_width_votes: List[int] = []

    # bfchar blocks: pairs of hex strings.
    for block in _BFCHAR_RE.findall(cmap):
        hexes = _HEX_RE.findall(block)
        for i in range(0, len(hexes) - 1, 2):
            src_h = hexes[i]
            dst_h = hexes[i + 1]
            if not src_h:
                continue
            try:
                src = int(src_h, 16)
            except ValueError:
                continue
            key_width_votes.append((len(src_h) + 1) // 2)
            mapping[src] = _hex_to_unicode(dst_h)

    # bfrange blocks: iterate tokens, supporting both the triple form and the
    # `<lo> <hi> [ ... ]` array form.
    for block in _BFRANGE_RE.findall(cmap):
        _parse_bfrange_block(block, mapping, key_width_votes)

    if key_width_votes:
        # Prefer the observed key width when it is wider than the codespace
        # guess (defensive: some CMaps omit a meaningful codespacerange).
        code_bytes = max(code_bytes, max(key_width_votes))

    return ToUnicodeMap(mapping, code_bytes)


def _parse_bfrange_block(block: bytes, mapping: Dict[int, str],
                         key_width_votes: List[int]) -> None:
    """Parse one ``beginbfrange ... endbfrange`` body into ``mapping``."""
    pos = 0
    n = len(block)
    while pos < n:
        # lo
        lo_m = _HEX_RE.search(block, pos)
        if lo_m is None:
            break
        lo_h = lo_m.group(1)
        # hi
        hi_m = _HEX_RE.search(block, lo_m.end())
        if hi_m is None:
            break
        hi_h = hi_m.group(1)
        # destination: either an array [...] or a single <hex>.
        rest_start = hi_m.end()
        # Find the next significant token start: '[' or '<'.
        bracket_pos = block.find(b"[", rest_start)
        angle_pos = block.find(b"<", rest_start)
        try:
            lo = int(lo_h, 16)
            hi = int(hi_h, 16)
        except ValueError:
            pos = hi_m.end()
            continue
        key_width_votes.append((len(lo_h) + 1) // 2)

        if bracket_pos != -1 and (angle_pos == -1 or bracket_pos < angle_pos):
            # Array form.
            close = block.find(b"]", bracket_pos)
            if close == -1:
                break
            arr = block[bracket_pos + 1: close]
            dsts = _HEX_RE.findall(arr)
            code = lo
            for d in dsts:
                if code > hi:
                    break
                mapping[code] = _hex_to_unicode(d)
                code += 1
            pos = close + 1
        else:
            dst_m = _HEX_RE.search(block, rest_start)
            if dst_m is None:
                break
            dst_h = dst_m.group(1)
            base = _hex_to_unicode(dst_h)
            # Increment the LAST unicode code unit across the range.
            if base and (hi - lo) >= 0:
                base_cp = ord(base[-1]) if base else 0
                prefix = base[:-1]
                for offset in range(0, hi - lo + 1):
                    try:
                        ch = prefix + chr(base_cp + offset)
                    except ValueError:
                        ch = prefix
                    mapping[lo + offset] = ch
            pos = dst_m.end()


# --------------------------------------------------------------------------- #
# /Encoding /Differences (glyph-name) fallback
# --------------------------------------------------------------------------- #

# A compact glyphname -> unicode table covering the common Latin / Spanish set.
# Only a secondary fallback; most corpus fonts use ToUnicode or WinAnsi.
_GLYPH_TO_UNICODE: Dict[str, str] = {}


def _init_glyph_table() -> None:
    import string
    for c in string.ascii_lowercase:
        _GLYPH_TO_UNICODE[c] = c
    for c in string.ascii_uppercase:
        _GLYPH_TO_UNICODE[c] = c
    digit_names = {
        "zero": "0", "one": "1", "two": "2", "three": "3", "four": "4",
        "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9",
    }
    _GLYPH_TO_UNICODE.update(digit_names)
    named = {
        "space": " ", "period": ".", "comma": ",", "colon": ":",
        "semicolon": ";", "hyphen": "-", "parenleft": "(", "parenright": ")",
        "slash": "/", "percent": "%", "plus": "+", "equal": "=",
        "quotesingle": "'", "quotedbl": '"', "exclam": "!", "question": "?",
        "aacute": "á", "eacute": "é", "iacute": "í", "oacute": "ó",
        "uacute": "ú", "ntilde": "ñ", "Ntilde": "Ñ", "udieresis": "ü",
        "Aacute": "Á", "Eacute": "É", "Iacute": "Í", "Oacute": "Ó",
        "Uacute": "Ú", "ampersand": "&", "at": "@", "numbersign": "#",
    }
    _GLYPH_TO_UNICODE.update(named)


_init_glyph_table()

_DIFFERENCES_RE = re.compile(rb"/Differences\s*\[(.*?)\]", re.DOTALL)
_DIFF_TOKEN_RE = re.compile(rb"(\d+)|/([A-Za-z0-9]+)")


def parse_differences(encoding_body: bytes) -> Dict[int, str]:
    """Parse an ``/Encoding << /Differences [ ... ] >>`` into code -> unicode.

    Only glyph names present in :data:`_GLYPH_TO_UNICODE` resolve; unknown names
    are skipped (they fall through to the latin-1 heuristic later).
    """
    dm = _DIFFERENCES_RE.search(encoding_body)
    if dm is None:
        return {}
    mapping: Dict[int, str] = {}
    current = 0
    for tok in _DIFF_TOKEN_RE.finditer(dm.group(1)):
        if tok.group(1) is not None:
            current = int(tok.group(1))
        else:
            name = tok.group(2).decode("latin-1")
            uni = _GLYPH_TO_UNICODE.get(name)
            if uni is not None:
                mapping[current] = uni
            current += 1
    return mapping


# --------------------------------------------------------------------------- #
# Font table assembly
# --------------------------------------------------------------------------- #

class FontInfo:
    """Decoded per-font mapping used while walking a content stream."""

    __slots__ = ("tounicode", "differences")

    def __init__(self, tounicode: Optional[ToUnicodeMap],
                 differences: Optional[Dict[int, str]]):
        self.tounicode = tounicode
        self.differences = differences

    @property
    def has_mapping(self) -> bool:
        return bool(self.tounicode) or bool(self.differences)


def _build_font_info(font_obj: _PDFObject,
                     objects: Dict[int, _PDFObject]) -> FontInfo:
    """Build a :class:`FontInfo` for a single font object (tolerant)."""
    tounicode: Optional[ToUnicodeMap] = None
    differences: Optional[Dict[int, str]] = None

    try:
        tu_ref = _resolve_ref(font_obj.body, b"/ToUnicode")
        if tu_ref is not None:
            tu_obj = objects.get(tu_ref)
            if tu_obj is not None and tu_obj.stream_raw is not None:
                dec = _inflate(tu_obj.stream_raw)
                if dec is None:
                    dec = tu_obj.stream_raw  # some CMaps are not compressed
                if dec:
                    parsed = parse_tounicode_cmap(dec)
                    if parsed:
                        tounicode = parsed
    except Exception:
        tounicode = None

    try:
        # /Encoding may be inline (<< /Differences [...] >>) or an indirect ref.
        if b"/Differences" in font_obj.body:
            differences = parse_differences(font_obj.body) or None
        else:
            enc_ref = _resolve_ref(font_obj.body, b"/Encoding")
            if enc_ref is not None:
                enc_obj = objects.get(enc_ref)
                if enc_obj is not None and b"/Differences" in enc_obj.body:
                    differences = parse_differences(enc_obj.body) or None
    except Exception:
        differences = None

    return FontInfo(tounicode, differences)


def _collect_font_maps(objects: Dict[int, _PDFObject]) -> Dict[str, FontInfo]:
    """Map every font RESOURCE name (``F1`` ...) to its decoded tables.

    We scan every page/XObject ``/Resources ... /Font << /Fx N 0 R ... >>``
    dictionary so a resource name is tied to the right font object. When the
    same name maps to different objects on different pages, any entry carrying a
    usable mapping wins (names are stable within this corpus).
    """
    font_maps: Dict[str, FontInfo] = {}
    # Cache FontInfo by object number so we parse each font once.
    cache: Dict[int, FontInfo] = {}

    font_dict_re = re.compile(rb"/Font\s*<<(.*?)>>", re.DOTALL)
    entry_re = re.compile(rb"/([A-Za-z0-9]+)\s+(\d+)\s+\d+\s+R")

    for obj in objects.values():
        for fm in font_dict_re.finditer(obj.body):
            for em in entry_re.finditer(fm.group(1)):
                name = em.group(1).decode("latin-1")
                try:
                    ref = int(em.group(2))
                except ValueError:
                    continue
                font_obj = objects.get(ref)
                if font_obj is None:
                    continue
                if ref not in cache:
                    cache[ref] = _build_font_info(font_obj, objects)
                info = cache[ref]
                existing = font_maps.get(name)
                if existing is None or (info.has_mapping and not existing.has_mapping):
                    font_maps[name] = info
    return font_maps


# --------------------------------------------------------------------------- #
# Content-stream token walking
# --------------------------------------------------------------------------- #

# Operators / operands we care about, tokenised in document order:
#   - `/Name <num> Tf`           -> switch active font
#   - `( ... ) Tj` / `( ... ) '` -> show a literal string
#   - `< ... > Tj`               -> show a hex string
#   - `[ ... ] TJ`               -> show-array with kerning numbers
# We also recognise `"` (aw ac string) and treat it like a string show.
_TF_RE = re.compile(rb"/([A-Za-z0-9]+)\s+[-\d.]+\s+Tf")
# NOTE: these show-operator patterns avoid the `(?:... | \\.)*` alternation that
# backtracks catastrophically on large (pseudo-)binary streams. A literal/array
# body is matched with a simple negated-class star; embedded escaped parens are
# handled downstream in `_unescape_literal` / `_decode_tj_array` instead of in
# the scanner. Array bodies are length-bounded as a final backtracking guard.
_SHOW_LITERAL_RE = re.compile(rb"\([^()]*\)\s*(?:Tj|'|\")")
_SHOW_HEX_RE = re.compile(rb"<[0-9A-Fa-f\s]*>\s*Tj")
_SHOW_ARRAY_RE = re.compile(rb"\[[^\[\]]{0,20000}\]\s*TJ", re.DOTALL)
_BT_RE = re.compile(rb"\bBT\b")
_ET_RE = re.compile(rb"\bET\b")

# Inner tokens of a TJ array: strings (literal/hex) and kerning numbers.
_ARRAY_TOKEN_RE = re.compile(
    rb"\((?:[^()\\]|\\.)*\)|<[0-9A-Fa-f\s]*>|(-?\d+(?:\.\d+)?)", re.DOTALL)

_LITERAL_RE = re.compile(rb"\((?:[^()\\]|\\.)*\)", re.DOTALL)
_OCTAL_RE = re.compile(rb"\\([0-7]{1,3})")
_SIMPLE_ESC = {
    b"n": b"\n", b"r": b"\r", b"t": b"\t", b"b": b"\b", b"f": b"\f",
    b"(": b"(", b")": b")", b"\\": b"\\",
}

# Large negative kerning (in thousandths of an em) that implies a word break.
_WORD_BREAK_KERN = 200.0


def _unescape_literal(raw: bytes) -> bytes:
    """Unescape a PDF literal string body (without the surrounding parens)."""
    out = bytearray()
    i = 0
    n = len(raw)
    while i < n:
        c = raw[i]
        if c == 0x5C and i + 1 < n:  # backslash
            nxt = raw[i + 1: i + 2]
            if nxt in _SIMPLE_ESC:
                out += _SIMPLE_ESC[nxt]
                i += 2
                continue
            om = _OCTAL_RE.match(raw, i)
            if om is not None:
                out.append(int(om.group(1), 8) & 0xFF)
                i = om.end()
                continue
            if nxt in (b"\n", b"\r"):
                # line-continuation: drop the escaped newline
                i += 2
                continue
            # Unknown escape: keep the following byte literally.
            out += nxt
            i += 2
            continue
        out.append(c)
        i += 1
    return bytes(out)


def _decode_codes(code_bytes_seq: bytes, font: Optional[FontInfo]) -> str:
    """Map a byte string of character codes through the active font table.

    When the font has a ToUnicode map with 2-byte codes, bytes are grouped in
    pairs. When it has 1-byte codes (or only a Differences table), each byte is
    a code. When no mapping exists, degrade to the latin-1 clear-char heuristic.
    """
    if font is not None and font.tounicode and font.tounicode.mapping:
        width = font.tounicode.code_bytes or 1
        mapping = font.tounicode.mapping
        out: List[str] = []
        if width >= 2:
            # Pad an odd trailing byte so we never crash.
            data = code_bytes_seq
            if len(data) % width:
                data = data + b"\x00" * (width - len(data) % width)
            for i in range(0, len(data), width):
                code = int.from_bytes(data[i: i + width], "big")
                mapped = mapping.get(code)
                if mapped is not None:
                    out.append(mapped)
                else:
                    # Unknown glyph code: skip it rather than emit noise.
                    continue
            return "".join(out)
        for b in code_bytes_seq:
            mapped = mapping.get(b)
            if mapped is not None:
                out.append(mapped)
            else:
                out.append(_latin1_clear(bytes([b])))
        return "".join(out)

    if font is not None and font.differences:
        diffs = font.differences
        out = []
        for b in code_bytes_seq:
            mapped = diffs.get(b)
            if mapped is not None:
                out.append(mapped)
            else:
                out.append(_latin1_clear(bytes([b])))
        return "".join(out)

    # No per-font mapping: legacy behaviour (latin-1 of the literal bytes).
    return _latin1_clear(code_bytes_seq)


def _latin1_clear(raw: bytes) -> str:
    """Legacy fallback: decode bytes as latin-1 (clear-char heuristic)."""
    try:
        return raw.decode("latin-1")
    except Exception:
        return ""


def _hex_string_to_bytes(token: bytes) -> bytes:
    """Convert a ``< ... >`` hex-string token into its raw bytes."""
    inner = token.strip()
    if inner.startswith(b"<"):
        inner = inner[1:]
    if inner.endswith(b">"):
        inner = inner[:-1]
    inner = re.sub(rb"\s+", b"", inner)
    if len(inner) % 2:
        inner += b"0"
    try:
        return bytes.fromhex(inner.decode("ascii"))
    except ValueError:
        return b""


def _text_object_regions(dec: bytes) -> List[Tuple[int, int]]:
    """Return ``(start, end)`` spans of each ``BT ... ET`` text object.

    Pairs each ``BT`` with the next ``ET``. Unbalanced ``BT`` (no closing ``ET``)
    is dropped. This keeps text decoding strictly inside text objects so binary
    image data never leaks into the extracted text.
    """
    regions: List[Tuple[int, int]] = []
    bts = [m.start() for m in _BT_RE.finditer(dec)]
    if not bts:
        return regions
    ets = [m.end() for m in _ET_RE.finditer(dec)]
    if not ets:
        return regions
    ei = 0
    n_et = len(ets)
    for bt in bts:
        # advance to the first ET that closes this BT
        while ei < n_et and ets[ei] <= bt:
            ei += 1
        if ei >= n_et:
            break
        regions.append((bt, ets[ei]))
    return regions


def _decode_content_stream(dec: bytes,
                           font_maps: Dict[str, FontInfo]) -> str:
    """Decode one content stream into text, tracking the active font.

    Only bytes shown inside text objects via Tj/TJ/'/" are emitted; everything
    else (binary image data, path ops) is ignored, which is what keeps the
    extracted text clean.
    """
    # Restrict scanning to text objects (`BT ... ET`). Image XObjects and other
    # binary streams can contain `Tj`/`TJ` bytes by coincidence, but they do not
    # carry balanced BT/ET text objects, so this both avoids emitting binary
    # noise and keeps the heavy show-operator regexes off large binary spans.
    regions = _text_object_regions(dec)
    if not regions:
        return ""

    # Build an ordered event list: Tf switches and show operators, each confined
    # to a BT/ET region.
    events: List[Tuple[int, int, re.Match]] = []
    for lo, hi in regions:
        span = dec[lo:hi]
        for m in _TF_RE.finditer(span):
            events.append((lo + m.start(), 0, m))
        for m in _SHOW_LITERAL_RE.finditer(span):
            events.append((lo + m.start(), 1, m))
        for m in _SHOW_HEX_RE.finditer(span):
            events.append((lo + m.start(), 1, m))
        for m in _SHOW_ARRAY_RE.finditer(span):
            events.append((lo + m.start(), 1, m))
    events.sort(key=lambda e: e[0])

    out: List[str] = []
    current_font: Optional[FontInfo] = None
    for _pos, kind, m in events:
        if kind == 0:
            name = m.group(1).decode("latin-1")
            current_font = font_maps.get(name)
            continue
        token = m.group(0)
        if token.lstrip().startswith(b"["):
            out.append(_decode_tj_array(token, current_font))
        elif token.lstrip().startswith(b"<"):
            raw = _hex_string_to_bytes(token[: token.rfind(b">") + 1])
            out.append(_decode_codes(raw, current_font))
        else:
            lm = _LITERAL_RE.search(token)
            if lm is None:
                continue
            body = lm.group(0)[1:-1]
            raw = _unescape_literal(body)
            out.append(_decode_codes(raw, current_font))
        out.append(" ")
    return "".join(out)


def _decode_tj_array(token: bytes, font: Optional[FontInfo]) -> str:
    """Decode a ``[ ... ] TJ`` array, inserting spaces on big negative kerns."""
    # Strip the surrounding brackets and the trailing TJ.
    inner_start = token.find(b"[")
    inner_end = token.rfind(b"]")
    if inner_start == -1 or inner_end == -1 or inner_end <= inner_start:
        return ""
    inner = token[inner_start + 1: inner_end]
    parts: List[str] = []
    for m in _ARRAY_TOKEN_RE.finditer(inner):
        tok = m.group(0)
        if m.group(1) is not None:
            # Kerning number: a large negative value separates words.
            try:
                kern = float(m.group(1))
            except ValueError:
                kern = 0.0
            if -kern >= _WORD_BREAK_KERN:
                parts.append(" ")
            continue
        if tok.startswith(b"("):
            raw = _unescape_literal(tok[1:-1])
            parts.append(_decode_codes(raw, font))
        elif tok.startswith(b"<"):
            raw = _hex_string_to_bytes(tok)
            parts.append(_decode_codes(raw, font))
    return "".join(parts)


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #

def extract_pdf_text_font_aware(data: bytes) -> str:
    """Extract text from PDF ``data`` using per-font ToUnicode decoding.

    Tolerant to failure: any error on a font or stream degrades that unit to the
    latin-1 heuristic and never aborts. Returns the concatenated page text in
    document order (deterministic). On total failure returns ``""`` so the
    caller can fall back to the legacy extractor.
    """
    objects = _parse_objects(data)
    if not objects:
        return ""
    try:
        font_maps = _collect_font_maps(objects)
    except Exception:
        font_maps = {}

    texts: List[str] = []
    for num in sorted(objects.keys()):
        obj = objects[num]
        if obj.stream_raw is None:
            continue
        dec = _inflate(obj.stream_raw)
        if dec is None:
            continue
        # Only decode streams that carry text objects. Image/font-program
        # streams lack BT/ET text objects and are skipped entirely.
        if b"BT" not in dec:
            continue
        try:
            texts.append(_decode_content_stream(dec, font_maps))
        except Exception:
            # Degrade this stream to the legacy literal pull.
            try:
                for lm in _LITERAL_RE.finditer(dec):
                    texts.append(_latin1_clear(_unescape_literal(lm.group(0)[1:-1])))
                    texts.append(" ")
            except Exception:
                continue
    return "".join(texts)
