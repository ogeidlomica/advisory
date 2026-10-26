"""Declarative definition of the 7 Zero-Drift phases, their RACI-V leadership,
deliverables, quality gates (QG-0..QG-6) and the report file each produces.

Report builders live in ``phases/builders.py`` and are wired in here lazily by
``load_phases`` so the engine stays decoupled from report content (FEAT-002+).
"""

from __future__ import annotations

from typing import Dict, List

from engine.model import Gate, Phase


# --------------------------------------------------------------------------- #
# Report filenames (00 .. 06) in phase order.
# --------------------------------------------------------------------------- #

REPORT_FILENAMES = {
    "0": "00-higiene-epistemica.md",
    "1": "01-contexto-as-is.md",
    "2": "02-estado-del-arte.md",
    "3": "03-gaps-y-viabilizacion.md",
    "4": "04-diseno-to-be.md",
    "5": "05-roadmap-estimacion-raid.md",
    "6": "06-caso-de-negocio.md",
}

PHASE_ORDER = ["0", "1", "2", "3", "4", "5", "6"]

# Auxiliary generated catalog (FEAT-003): the exhaustive HU/Gherkin catalog for
# ALL Credi10 modules. It is a complement of Phase 4 (not a stage-gated phase),
# written by the orchestrator when running the full pipeline.
CATALOG_FILENAME = "04b-catalogo-historias.md"

# Commercial proposal (report 1, task three-reports): the sales document issued
# by the consultancy (brand Kulgops), written by the orchestrator on `--phase
# all`. Not a stage-gated phase; its builder lives in
# ``phases/commercial_proposal.py``.
PROPOSAL_FILENAME = "1-propuesta-comercial.md"

# Commercial opportunity analysis (task commercial-opportunity): the TWO
# SEPARATE outcomes produced by the bid-management / commercial-offer-design
# expert, governed by the skill ``commercial-opportunity-analysis`` and written
# by the orchestrator on `--phase all` right after the commercial proposal.
# Outcome 1 is the opportunity analysis + the checklist of client-requested
# information + the developed offer content; Outcome 2 is the checklist of items
# to develop + considerations + assumptions + the commercial traceability
# matrix. Their builder lives in ``phases/commercial_opportunity.py``.
COMMERCIAL_OPPORTUNITY_FILENAME = "0-analisis-oportunidad-comercial.md"
COMMERCIAL_CORRELATION_FILENAME = "0b-checklist-oferta-y-correlacion.md"

# Executive/management report (report 2, task three-reports): the executive
# support of the commercial proposal (scope, phases, high-level diagnosis,
# strategy, risks, considerations, prerequisites), written by the orchestrator
# on `--phase all`. Not a stage-gated phase; its builder lives in
# ``phases/executive_report.py``.
EXEC_REPORT_FILENAME = "2-reporte-gerencial.md"

# Technical report (report 3, task three-reports): the multilevel narrative
# technical report, written by the orchestrator on `--phase all` as a tree under
# ``advisory-credi10-2.0/3-informe-tecnico/`` (one subfolder per Zero-Drift
# phase + a master README index). Not a stage-gated phase; its generator lives
# in ``phases/technical_report.py``.
TECH_REPORT_DIRNAME = "3-informe-tecnico"


def _gates() -> Dict[str, Gate]:
    return {
        "0": Gate(
            id="QG-0",
            name="Higiene Epistemica",
            criteria=[
                "Corpus inventariado con trazabilidad (filename, sha256, rol).",
                "Supuestos, conflictos y vacios epistemicos registrados y etiquetados.",
                "Fuentes primarias (RFP, Assessment, 3 diagramas) validadas.",
            ],
            nogo_condition="Existen vacios epistemicos criticos sin registrar o fuentes primarias ilegibles.",
        ),
        "1": Gate(
            id="QG-1",
            name="Contexto AS-IS",
            criteria=[
                "Mapa de capacidades y drivers de negocio establecidos.",
                "Arquitectura AS-IS (contexto, despliegue, AWS) consolidada.",
                "Procesos AS-IS mapeados con evidencia del corpus.",
            ],
            nogo_condition="El AS-IS no es trazable a evidencia primaria del corpus.",
        ),
        "2": Gate(
            id="QG-2",
            name="Estado del Arte",
            criteria=[
                "Benchmarks de industria vinculados a capacidades del AS-IS.",
                "Estado del arte y patrones de referencia documentados.",
            ],
            nogo_condition="Los benchmarks no se conectan con capacidades reales del negocio.",
        ),
        "3": Gate(
            id="QG-3",
            name="Gaps y Viabilizacion",
            criteria=[
                "Pains/gaps identificados y priorizados con relievers.",
                "ABBs y contexto de arquitectura (Fase 3.5) definidos.",
                "Hilo Dorado intacto desde driver hasta reliever.",
            ],
            nogo_condition="Hay gaps sin reliever o relievers sin trazabilidad a un driver.",
        ),
        "4": Gate(
            id="QG-4",
            name="Diseno TO-BE (Dry-Run)",
            criteria=[
                "Arquitectura TO-BE y SBBs definidos.",
                "Specs e historias trazables a gaps.",
                "Dry-Run / Tabletop ejecutado por AM antes del build.",
            ],
            nogo_condition="El Dry-Run revela SBBs sin spec o specs sin historia trazable.",
        ),
        "5": Gate(
            id="QG-5",
            name="Roadmap, Estimacion y RAID",
            criteria=[
                "Olas de entrega y estimacion de tamano definidas.",
                "RAID (Risks, Assumptions, Issues, Dependencies) consolidado.",
                "Modelo operativo y habilitacion del cambio definidos.",
            ],
            nogo_condition="El roadmap carece de estimacion o el RAID omite riesgos criticos.",
        ),
        "6": Gate(
            id="QG-6",
            name="Caso de Negocio",
            criteria=[
                "ROI y outcomes cuantificados contra los indicadores del RFP.",
                "Caso de negocio aprobado por el Comite de Gobierno (ED).",
                "Hilo Dorado completo desde driver hasta ROI.",
            ],
            nogo_condition="El ROI no cierra contra los indicadores del RFP o rompe el Hilo Dorado.",
        ),
    }


def load_phases() -> Dict[str, Phase]:
    """Build the declarative phase catalogue and wire report builders."""
    # Imported lazily to avoid a circular import at module load time.
    from phases import BUILDERS

    gates = _gates()
    phases: Dict[str, Phase] = {}

    phases["0"] = Phase(
        id="0",
        name="Fase 0 - Higiene Epistemica",
        leaders=["AM", "TDA", "DRE"],
        verifier="EM",
        deliverables=["E0.1", "E0.2", "E0.3"],
        gate=gates["0"],
        filename=REPORT_FILENAMES["0"],
        accountable="EM",
        consulted=["ED"],
        informed=["EA", "BA"],
    )
    phases["1"] = Phase(
        id="1",
        name="Fase 1 - Contexto AS-IS",
        leaders=["EA", "BA", "PIA", "TDA"],
        verifier="AM",
        deliverables=["E1.1", "E1.2", "E1.3"],
        gate=gates["1"],
        filename=REPORT_FILENAMES["1"],
        accountable="EM",
        consulted=["SME", "DRE"],
        informed=["ED"],
    )
    phases["2"] = Phase(
        id="2",
        name="Fase 2 - Estado del Arte",
        leaders=["EA", "SME", "BA"],
        verifier="AM",
        deliverables=["E2.1", "E2.2"],
        gate=gates["2"],
        filename=REPORT_FILENAMES["2"],
        accountable="EM",
        consulted=["PIA"],
        informed=["ED"],
    )
    phases["3"] = Phase(
        id="3",
        name="Fase 3 + 3.5 - Gaps y Viabilizacion",
        leaders=["EA", "DRE", "PIA"],
        verifier="AM",
        deliverables=["E3.1", "E3.2", "E3.5"],
        gate=gates["3"],
        filename=REPORT_FILENAMES["3"],
        accountable="EM",
        consulted=["SA", "DA"],
        informed=["ED", "FIN"],
    )
    phases["4"] = Phase(
        id="4",
        name="Fase 4 - Diseno TO-BE",
        leaders=["SA", "DA", "PM", "UX"],
        verifier="AM",
        deliverables=["E4.1", "E4.2", "E4.3"],
        gate=gates["4"],
        filename=REPORT_FILENAMES["4"],
        accountable="EM",
        consulted=["AIA", "SEC"],
        informed=["ED"],
    )
    phases["5"] = Phase(
        id="5",
        name="Fase 5 - Roadmap, Estimacion y RAID",
        leaders=["EM", "SA", "PM", "ORG"],
        verifier="AM",
        deliverables=["E5.1", "E5.2", "E5.3"],
        gate=gates["5"],
        filename=REPORT_FILENAMES["5"],
        accountable="EM",
        consulted=["FIN", "SEC"],
        informed=["ED"],
    )
    phases["6"] = Phase(
        id="6",
        name="Fase 6 - Caso de Negocio",
        leaders=["ED", "FIN", "EA"],
        verifier="AM",
        deliverables=["E6.1", "E6.2", "E6.3"],
        gate=gates["6"],
        filename=REPORT_FILENAMES["6"],
        accountable="EM",
        consulted=["ORG"],
        informed=["EM"],
    )

    for pid, phase in phases.items():
        phase.builder = BUILDERS.get(pid)

    return phases


def phases_in_order() -> List[str]:
    return list(PHASE_ORDER)
