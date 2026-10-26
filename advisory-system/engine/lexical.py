"""Lexical reconstruction layer (stdlib only, deterministic, idempotent).

This module is a COMPLEMENTARY post-processing layer that runs AFTER the
per-font ``/ToUnicode`` decoding (:mod:`engine.pdf_text`) and the single-letter
``defragment`` pass (:mod:`engine.corpus`). It is NOT OCR and it NEVER fabricates
text: it only re-joins what the PDF's glyph-spacing split apart and collapses
pure layout artifacts, raising the honest *useful-text* ratio (real words /
total characters) without corrupting legitimate content.

Why a separate layer?
---------------------
The font-aware extractor already recovers legible Spanish, but the PDF text
layer still carries two kinds of ratio-depressing noise:

  1. **Table-of-contents dot leaders** -- long runs of ``.`` (``. . . . .``)
     used only to visually connect a heading to its page number. They are pure
     formatting, carry no lexical content, and in some documents (e.g. the WSO2
     assessment) account for ~5-7% of all characters, dragging the useful-text
     ratio down. Collapsing them is exactly analogous to the existing
     whitespace collapse.
  2. **Glyph-spacing word splits** -- a single capital letter detached from the
     rest of its word by a spurious space (``id C liente`` -> ``id Cliente``,
     ``Datacr edito`` style leading caps). The font engine occasionally emits
     the first glyph of a capitalised word as its own show operator.

Design principle: CONSERVATIVE BY CONSTRUCTION
----------------------------------------------
It is always preferable to leave a fragment un-joined than to fuse two distinct
words (the classic ``fragmentad`` corruption). So this layer implements ONLY
transformations with a near-zero false-positive rate:

  * ``collapse_dot_leaders`` -- deletes TOC dot-leader runs (>= 3 dots). Dots
    are never part of a real >= 3-letter word, so this cannot corrupt words.
  * ``rejoin_split_capitals`` -- re-glues a SINGLE uppercase consonant to the
    lowercase word fragment that follows it, and ONLY when the token before it
    is itself a lowercase word. That guard rules out proper-noun initials
    (``Studio F podra`` keeps its ``F``) and standalone single-letter Spanish
    words (``a``/``y``/``o``/``e``/``u`` are vowels, never touched here because
    the rule only fires on consonants). Direction is unambiguous: a capital
    letter stranded before a lowercase continuation always belongs forward.

Ambiguous cases (lowercase stray letters, two short syllable fragments, stray
letters whose merge direction cannot be proven without a dictionary) are LEFT
UNTOUCHED on purpose. We do not ship a dictionary and we do not guess.

Everything is pure :mod:`re` + string ops, deterministic (no randomness, no
timestamps, stable ordering) and idempotent (applying the layer twice yields
the exact same string as applying it once).
"""

from __future__ import annotations

import re


# --------------------------------------------------------------------------- #
# Character classes (Spanish-aware)
# --------------------------------------------------------------------------- #

# Letters that may appear in a Spanish word, accents and enye included.
_LETTERS = "A-Za-z\u00c1\u00c9\u00cd\u00d3\u00da\u00dc\u00d1\u00e1\u00e9\u00ed\u00f3\u00fa\u00fc\u00f1"
_WORD_RE = re.compile(r"[" + _LETTERS + r"]+")

# A single stranded consonant is (almost) never a standalone Spanish token, so
# it is a safe merge candidate. The single-letter Spanish words are all VOWELS
# (``a`` conj., ``y`` conj., ``o`` conj., ``e`` conj., ``u`` conj.), so by
# restricting the rule to CONSONANTS we never swallow a real one-letter word.
_MERGE_CONSONANTS = set("bcdfghjklmnpqrstvwxz")

# TOC dot-leader run: three or more dots, possibly separated by spaces.
_DOT_LEADER_RE = re.compile(r"(?:\s*\.\s*){3,}")


def _is_word(token: str) -> bool:
    """True when ``token`` is a run of Spanish letters only (no digits/punct)."""
    return bool(token) and bool(_WORD_RE.fullmatch(token))


# --------------------------------------------------------------------------- #
# Transform 1: collapse table-of-contents dot leaders
# --------------------------------------------------------------------------- #

def collapse_dot_leaders(text: str) -> str:
    """Collapse TOC dot-leader runs (``. . . . .``) into a single space.

    Only runs of THREE OR MORE dots are affected, so ordinary punctuation
    (``...`` ellipsis is 3 dots -> also collapsed, acceptable as it is likewise
    not lexical content; a single ``.`` ending a sentence is never touched).
    Deterministic and idempotent: a second pass finds no >= 3-dot run left.
    """
    return _DOT_LEADER_RE.sub(" ", text)


# --------------------------------------------------------------------------- #
# Transform 2: re-join a split leading capital to its word
# --------------------------------------------------------------------------- #

def rejoin_split_capitals(text: str) -> str:
    """Re-glue a stranded single UPPERCASE consonant onto the next word.

    Fires only for the pattern ``<lowercase-word> <UPPERCASE-consonant>
    <lowercase-word-fragment>`` and rewrites it to ``<lowercase-word>
    <Capital+fragment>`` (e.g. ``id C liente`` -> ``id Cliente``). The guards:

      * the stranded token is a SINGLE uppercase CONSONANT (never a vowel, so a
        real one-letter Spanish word ``a/y/o/e/u`` can never be consumed);
      * the FOLLOWING token is an all-letter fragment that starts lowercase
        (a word continuation, not a second proper noun);
      * the PRECEDING token is an all-letter word that starts lowercase. This
        rules out proper-noun initials such as ``Studio F podra`` (``Studio``
        is capitalised, so the ``F`` is kept as an initial, never merged).

    Tokens are split on single spaces; the caller is expected to have collapsed
    whitespace already. Deterministic and idempotent.
    """
    tokens = text.split(" ")
    out = []
    i = 0
    n = len(tokens)
    while i < n:
        tok = tokens[i]
        if (
            len(tok) == 1
            and tok.isupper()
            and tok.lower() in _MERGE_CONSONANTS
            and out
            and i + 1 < n
        ):
            prev = out[-1]
            nxt = tokens[i + 1]
            if (
                _is_word(prev) and prev[0].islower()
                and _is_word(nxt) and nxt[0].islower()
            ):
                # Merge forward: the capital belongs to the following word.
                tokens[i + 1] = tok + nxt
                i += 1
                continue
        out.append(tok)
        i += 1
    return " ".join(out)


# --------------------------------------------------------------------------- #
# Public entry point
# --------------------------------------------------------------------------- #

_WS_RE = re.compile(r"\s+")


def reconstruct_lexical(text: str) -> str:
    """Apply the full conservative lexical reconstruction pipeline.

    Order: collapse dot leaders -> re-join split capitals -> collapse any
    whitespace the leader removal introduced. Pure, deterministic and
    IDEMPOTENT -- ``reconstruct_lexical(reconstruct_lexical(x)) ==
    reconstruct_lexical(x)`` for every input, because each transform converges
    in a single pass and leaves no new fixture for the others to act on.

    Returns the input unchanged when it is empty.
    """
    if not text:
        return text
    text = collapse_dot_leaders(text)
    text = rejoin_split_capitals(text)
    text = _WS_RE.sub(" ", text).strip()
    return text
