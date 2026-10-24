"""Catalogo DECLARATIVO del universo de modulos Credi10 (FEAT-003).

Esta es la **unica fuente de verdad** del listado de modulos del universo
Credi10. Es un dato declarativo (no codigo de la solucion): el builder de la
Fase 4 (``phases/phase4.py``) y el catalogo de historias
(``phases/catalog.py`` -> ``advisory-credi10-2.0/04b-catalogo-historias.md``)
lo renderizan, y la estimacion por modulo de la Fase 5 (FEAT-004) lo importa
para estimar modulo por modulo. Definido una sola vez, reutilizado en todas
partes, de modo que la cobertura sea COMPLETA y TESTEABLE
(``len(MODULES)`` == modulos cubiertos, sin muestreo).

Contenido: documentacion de advisory (historias de usuario + criterios
BDD/Gherkin en espanol). NO es codigo ejecutable de la solucion/producto; son
specs de diseno para la siguiente etapa, consumidas por el motor generador de
informes.

Cada modulo (``Module``) declara:

  * ``id``          identificador estable (p. ej. ``MOD-01``).
  * ``name``        nombre del modulo.
  * ``bounded_context`` contexto DDD al que pertenece (consistente con la
    Fase 3).
  * ``components``  componentes/documentos reales del corpus que lo sustentan.
  * ``source``      documento(s) del corpus que evidencian el modulo (para
    trazar al knowledge base).
  * ``abbs``        ABBs de la Fase 3.5 que lo habilitan (Hilo Dorado).
  * ``stories``     lista de ``UserStory``.

Cada ``UserStory`` declara:

  * ``id``          identificador trazable del Hilo Dorado (p. ej. ``HU-01``).
  * ``rol/quiero/para`` la narrativa "Como <rol> quiero <meta> para <valor>".
  * ``happy``       escenario Gherkin de happy path (``GherkinScenario``).
  * ``edge``        escenario Gherkin de caso borde / excepcion (Exception
    Storming).

Cada ``GherkinScenario`` declara el ``titulo`` y las lineas ``dado`` / ``cuando``
/ ``entonces`` (listas), que el renderizador convierte en
Dado/Cuando/Entonces (con ``Y`` para pasos encadenados).

Determinismo: todo es estatico y ordenado; sin aleatoriedad ni timestamps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class GherkinScenario:
    """Un escenario BDD/Gherkin en espanol (Dado/Cuando/Entonces)."""

    titulo: str
    dado: List[str]
    cuando: List[str]
    entonces: List[str]
    tipo: str = "happy"  # 'happy' | 'edge'


@dataclass(frozen=True)
class UserStory:
    """Historia de usuario con criterios de aceptacion BDD (happy + borde)."""

    id: str
    rol: str
    quiero: str
    para: str
    happy: GherkinScenario
    edge: GherkinScenario


@dataclass(frozen=True)
class Module:
    """Un modulo del universo Credi10 con sus historias y trazabilidad."""

    id: str
    name: str
    bounded_context: str
    components: str
    source: str
    abbs: List[str]
    stories: List[UserStory] = field(default_factory=list)


# --------------------------------------------------------------------------- #
# Catalogo declarativo (unica fuente de verdad). Orden estable = orden de
# render y de estimacion.
# --------------------------------------------------------------------------- #

MODULES: List[Module] = [
    Module(
        id="MOD-01",
        name="Plataforma Credi10 / Administracion de creditos",
        bounded_context="Plataforma / Core",
        components="Aplicacion central Credi10 (.NET), administracion de "
                   "obligaciones y parametrizacion de productos de credito.",
        source="RFP_CREDI10_2_0.pdf",
        abbs=["ABB-004", "ABB-005"],
        stories=[
            UserStory(
                id="HU-01",
                rol="administrador de creditos",
                quiero="parametrizar y administrar los productos de credito y "
                       "sus obligaciones desde una plataforma central",
                para="operar la cartera con reglas de negocio preservadas y "
                     "trazables",
                happy=GherkinScenario(
                    titulo="Alta de un producto de credito (happy path)",
                    dado=["un administrador autenticado en la plataforma Credi10"],
                    cuando=["registra un producto de credito con sus parametros",
                            "guarda la configuracion"],
                    entonces=["el producto queda disponible para originacion",
                              "la operacion queda auditada y trazable"],
                ),
                edge=GherkinScenario(
                    titulo="Parametros invalidos (caso borde)",
                    tipo="edge",
                    dado=["un administrador autenticado"],
                    cuando=["intenta guardar un producto con una tasa fuera de "
                            "rango"],
                    entonces=["la plataforma rechaza el cambio con un mensaje "
                              "claro",
                              "no se altera ninguna obligacion existente"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-02",
        name="Originacion - CrossCore",
        bounded_context="Estudio de Credito",
        components="Orquestacion de buros CrossCore dentro del estudio de "
                   "credito (CrossCore -> Inspektor -> Datacredito).",
        source="Originacion_CrossCore.pdf",
        abbs=["ABB-001", "ABB-004"],
        stories=[
            UserStory(
                id="HU-02",
                rol="motor de originacion",
                quiero="consultar CrossCore como primer eslabon del estudio de "
                       "credito",
                para="validar identidad y riesgo antes de continuar con los "
                     "demas buros",
                happy=GherkinScenario(
                    titulo="CrossCore responde correctamente (happy path)",
                    dado=["una solicitud en estudio de credito"],
                    cuando=["se invoca CrossCore con el documento del cliente"],
                    entonces=["se obtiene la respuesta de CrossCore",
                              "el flujo continua hacia Inspektor"],
                ),
                edge=GherkinScenario(
                    titulo="CrossCore agota el timeout (caso borde, EX-01)",
                    tipo="edge",
                    dado=["una solicitud en estudio de credito"],
                    cuando=["CrossCore no responde dentro del tiempo limite"],
                    entonces=["se aplica reintento con backoff",
                              "si persiste, la solicitud se encola sin perderse"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-03",
        name="Originacion - Inspektor",
        bounded_context="Estudio de Credito",
        components="Consulta al servicio Inspektor como segundo eslabon del "
                   "estudio de credito.",
        source="Originacion_API_Inspektor.pdf",
        abbs=["ABB-001", "ABB-004"],
        stories=[
            UserStory(
                id="HU-03",
                rol="motor de originacion",
                quiero="consultar Inspektor tras CrossCore",
                para="enriquecer el estudio de credito con senales adicionales",
                happy=GherkinScenario(
                    titulo="Inspektor entrega datos completos (happy path)",
                    dado=["una solicitud con CrossCore ya resuelto"],
                    cuando=["se invoca Inspektor"],
                    entonces=["se reciben los datos de Inspektor",
                              "el flujo continua hacia Datacredito"],
                ),
                edge=GherkinScenario(
                    titulo="Inspektor devuelve datos incompletos (caso borde, EX-02)",
                    tipo="edge",
                    dado=["una solicitud con CrossCore ya resuelto"],
                    cuando=["Inspektor devuelve una respuesta parcial"],
                    entonces=["el estudio se marca pendiente de revision manual",
                              "no se aprueba automaticamente"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-04",
        name="Originacion - Datacredito",
        bounded_context="Estudio de Credito",
        components="Consulta al bureau Datacredito/Dictum como eslabon final "
                   "del estudio de credito.",
        source="Originacion_API_Datacredito.pdf",
        abbs=["ABB-001", "ABB-004"],
        stories=[
            UserStory(
                id="HU-04",
                rol="motor de originacion",
                quiero="consultar Datacredito/Dictum al cierre del estudio",
                para="decidir la aprobacion con el historial crediticio del "
                     "cliente",
                happy=GherkinScenario(
                    titulo="Datacredito devuelve historial (happy path)",
                    dado=["una solicitud con CrossCore e Inspektor resueltos"],
                    cuando=["se invoca Datacredito/Dictum"],
                    entonces=["se obtiene el score/historial",
                              "se produce la decision APROBADO/RECHAZADO/REVISION"],
                ),
                edge=GherkinScenario(
                    titulo="Cliente sin historial (no-hit) (caso borde, EX-03)",
                    tipo="edge",
                    dado=["un cliente sin historial en el bureau"],
                    cuando=["Datacredito/Dictum reporta no-hit"],
                    entonces=["se aplica una regla de scoring alterna",
                              "la decision queda registrada como [DOC-ASSUMPTION]"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-05",
        name="Originacion - Aplicacion ADMIN",
        bounded_context="Originacion",
        components="Aplicacion ADMIN de originacion para gestion y revision de "
                   "solicitudes.",
        source="Originacion_Aplicacion_ADMIN.pdf",
        abbs=["ABB-004", "ABB-005"],
        stories=[
            UserStory(
                id="HU-05",
                rol="analista de originacion",
                quiero="revisar y resolver manualmente las solicitudes en cola "
                       "de revision",
                para="decidir casos que el motor dejo en REVISION sin perder "
                     "trazabilidad",
                happy=GherkinScenario(
                    titulo="Resolucion manual de una solicitud (happy path)",
                    dado=["una solicitud en estado REVISION"],
                    cuando=["el analista la aprueba o rechaza con justificacion"],
                    entonces=["la solicitud cambia de estado",
                              "la decision queda auditada con el usuario y motivo"],
                ),
                edge=GherkinScenario(
                    titulo="Solicitud ya resuelta por otro analista (caso borde)",
                    tipo="edge",
                    dado=["dos analistas abren la misma solicitud"],
                    cuando=["el segundo intenta resolverla ya resuelta"],
                    entonces=["se bloquea la doble resolucion (idempotencia)",
                              "se informa el estado actual"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-06",
        name="Pagos / GenerarPagos",
        bounded_context="Pagos",
        components="Generacion de pagos (FT-SL-003) y su registro.",
        source="GenerarPagos.pdf",
        abbs=["ABB-001", "ABB-003"],
        stories=[
            UserStory(
                id="HU-06",
                rol="sistema de pagos",
                quiero="generar la orden de pago de una obligacion",
                para="habilitar el recaudo del cliente",
                happy=GherkinScenario(
                    titulo="Generacion de pago (happy path)",
                    dado=["una obligacion con saldo pendiente"],
                    cuando=["se solicita generar el pago"],
                    entonces=["se crea la orden de pago",
                              "queda lista para el link de recaudo"],
                ),
                edge=GherkinScenario(
                    titulo="Obligacion sin saldo (caso borde)",
                    tipo="edge",
                    dado=["una obligacion con saldo cero"],
                    cuando=["se solicita generar el pago"],
                    entonces=["se rechaza la generacion",
                              "se informa que no hay saldo por cobrar"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-07",
        name="Corte de Cartera",
        bounded_context="Corte / Cartera",
        components="Proceso de corte de cartera (FT-SL-004) y consolidacion de "
                   "saldos/mora.",
        source="ProcesoCorteCartera.pdf",
        abbs=["ABB-004", "ABB-005"],
        stories=[
            UserStory(
                id="HU-07",
                rol="sistema de cartera",
                quiero="ejecutar el corte de cartera periodico",
                para="consolidar saldos y mora para cobranza y reporteria",
                happy=GherkinScenario(
                    titulo="Corte periodico exitoso (happy path)",
                    dado=["la cartera al cierre del periodo"],
                    cuando=["se ejecuta el proceso de corte"],
                    entonces=["se consolidan saldos y estados de mora",
                              "se publican los resultados para cobranza"],
                ),
                edge=GherkinScenario(
                    titulo="Corte interrumpido a mitad de proceso (caso borde)",
                    tipo="edge",
                    dado=["un corte en ejecucion"],
                    cuando=["el proceso falla antes de terminar"],
                    entonces=["el corte es idempotente y reanudable",
                              "no se duplican ni pierden obligaciones"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-08",
        name="Link de Recaudo / APIs de recaudo",
        bounded_context="Recaudo",
        components="Link de Recaudo (FT-SL-011) hacia PayU y conciliacion del "
                   "pago.",
        source="LinkDePagos.pdf",
        abbs=["ABB-001", "ABB-003"],
        stories=[
            UserStory(
                id="HU-08",
                rol="cliente",
                quiero="pagar mi obligacion mediante un link de recaudo",
                para="saldar mi credito de forma simple y segura",
                happy=GherkinScenario(
                    titulo="Pago por link conciliado (happy path)",
                    dado=["un link de recaudo generado para una obligacion"],
                    cuando=["el cliente paga en PayU"],
                    entonces=["PayU confirma el pago",
                              "se publica el evento PagoAplicado y se concilia"],
                ),
                edge=GherkinScenario(
                    titulo="PayU no confirma el pago (caso borde, EX-04)",
                    tipo="edge",
                    dado=["un link de recaudo generado"],
                    cuando=["PayU no entrega confirmacion"],
                    entonces=["el pago NO se marca aplicado (RN-04)",
                              "se reintenta la conciliacion via eventos"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-09",
        name="B2C / Portal de clientes",
        bounded_context="B2C / E-commerce",
        components="Portal B2C (Node.js + React + Wordpress), autoservicio del "
                   "cliente.",
        source="B2C.pdf",
        abbs=["ABB-001", "ABB-006"],
        stories=[
            UserStory(
                id="HU-09",
                rol="cliente",
                quiero="consultar mis obligaciones y pagar desde el portal B2C",
                para="autogestionar mi credito sin llamar a un asesor",
                happy=GherkinScenario(
                    titulo="Autoconsulta y pago en el portal (happy path)",
                    dado=["un cliente autenticado en el portal B2C"],
                    cuando=["consulta sus obligaciones y elige pagar"],
                    entonces=["ve su saldo actualizado",
                              "es redirigido al link de recaudo (PayU)"],
                ),
                edge=GherkinScenario(
                    titulo="Portal sobre Wordpress/XAMPP degradado (caso borde)",
                    tipo="edge",
                    dado=["el canal B2C legado (Wordpress/XAMPP, GAP-005)"],
                    cuando=["el componente legado falla"],
                    entonces=["el portal degrada sin exponer datos sensibles",
                              "se prioriza la migracion a .NET 8 (SBB-006)"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-10",
        name="Boton E-commerce",
        bounded_context="B2C / E-commerce",
        components="Boton de pago e-commerce (integracion VTEX / comercio).",
        source="BotonEcommerce.pdf",
        abbs=["ABB-001", "ABB-003"],
        stories=[
            UserStory(
                id="HU-10",
                rol="comercio aliado",
                quiero="ofrecer el boton de pago e-commerce de Credi10",
                para="permitir compras financiadas en linea",
                happy=GherkinScenario(
                    titulo="Compra financiada con boton (happy path)",
                    dado=["un carrito de compra en el comercio aliado"],
                    cuando=["el cliente paga con el boton e-commerce"],
                    entonces=["se registra la transaccion",
                              "se concilia el recaudo con la obligacion"],
                ),
                edge=GherkinScenario(
                    titulo="Transaccion rechazada por el medio de pago (caso borde)",
                    tipo="edge",
                    dado=["un carrito de compra"],
                    cuando=["el medio de pago rechaza la transaccion"],
                    entonces=["no se genera obligacion",
                              "el cliente recibe un mensaje de rechazo claro"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-11",
        name="Captura Foto",
        bounded_context="Originacion",
        components="Captura fotografica de documentos y soportes en la "
                   "originacion.",
        source="Captura_Foto.pdf",
        abbs=["ABB-004"],
        stories=[
            UserStory(
                id="HU-11",
                rol="asesor de originacion",
                quiero="capturar la foto del documento del cliente",
                para="adjuntar soporte valido a la solicitud",
                happy=GherkinScenario(
                    titulo="Captura y validacion de foto (happy path)",
                    dado=["una solicitud en curso"],
                    cuando=["el asesor captura la foto del documento"],
                    entonces=["la imagen se adjunta a la solicitud",
                              "queda disponible como soporte trazable"],
                ),
                edge=GherkinScenario(
                    titulo="Foto ilegible o de baja calidad (caso borde)",
                    tipo="edge",
                    dado=["una solicitud en curso"],
                    cuando=["la foto capturada es ilegible"],
                    entonces=["el sistema solicita recaptura",
                              "la solicitud no avanza sin soporte valido"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-12",
        name="API Integrador Atencion al Cliente",
        bounded_context="Atencion al Cliente",
        components="API integrador de atencion al cliente (omnicanal Wolkvox / "
                   "B2Chat).",
        source="Api_Integrador_Atencion_al_cliente.pdf",
        abbs=["ABB-001", "ABB-004"],
        stories=[
            UserStory(
                id="HU-12",
                rol="agente de atencion al cliente",
                quiero="consultar el estado del cliente desde una API "
                       "integradora omnicanal",
                para="atender consultas con informacion unificada",
                happy=GherkinScenario(
                    titulo="Consulta omnicanal unificada (happy path)",
                    dado=["un agente en el canal de atencion"],
                    cuando=["consulta al cliente via el API integrador"],
                    entonces=["recibe el estado consolidado del cliente",
                              "atiende sin cambiar de sistema"],
                ),
                edge=GherkinScenario(
                    titulo="Fuente de datos no disponible (caso borde)",
                    tipo="edge",
                    dado=["un agente en el canal de atencion"],
                    cuando=["una fuente del integrador no responde"],
                    entonces=["se devuelve la informacion parcial disponible",
                              "se informa que el dato esta temporalmente incompleto"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-13",
        name="Llamada Predictiva",
        bounded_context="Cobranza",
        components="Marcacion predictiva de cobranza (WOLKVOX).",
        source="Llamada_predictiva.pdf",
        abbs=["ABB-001", "ABB-004"],
        stories=[
            UserStory(
                id="HU-13",
                rol="operacion de cobranza",
                quiero="ejecutar campanas de llamada predictiva",
                para="contactar deudores de forma eficiente para recaudo",
                happy=GherkinScenario(
                    titulo="Campana predictiva conecta al deudor (happy path)",
                    dado=["una lista priorizada de deudores"],
                    cuando=["el marcador predictivo (WOLKVOX) lanza las llamadas"],
                    entonces=["se conecta al agente con el deudor",
                              "se registra el resultado de contacto"],
                ),
                edge=GherkinScenario(
                    titulo="Sin agentes disponibles (caso borde)",
                    tipo="edge",
                    dado=["una campana predictiva en curso"],
                    cuando=["no hay agentes libres al conectar la llamada"],
                    entonces=["se evita la llamada abandonada",
                              "se reprograma el contacto"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-14",
        name="Cobranza (SMS / WhatsApp / Email / Scheduler)",
        bounded_context="Cobranza",
        components="Scheduler de cobranza multicanal (SMS, WhatsApp, Email).",
        source="RFP_CREDI10_2_0.pdf",
        abbs=["ABB-003", "ABB-004"],
        stories=[
            UserStory(
                id="HU-14",
                rol="operacion de cobranza",
                quiero="programar envios de cobranza por SMS/WhatsApp/Email con "
                       "un scheduler",
                para="recordar y gestionar el pago de forma automatica y "
                     "multicanal",
                happy=GherkinScenario(
                    titulo="Envio multicanal programado (happy path)",
                    dado=["una cartera en mora segmentada"],
                    cuando=["el scheduler dispara los mensajes por canal"],
                    entonces=["se envian SMS/WhatsApp/Email segun la segmentacion",
                              "se registra el acuse de cada canal"],
                ),
                edge=GherkinScenario(
                    titulo="Canal caido en el envio (caso borde)",
                    tipo="edge",
                    dado=["un envio multicanal programado"],
                    cuando=["un canal (p. ej. WhatsApp) no esta disponible"],
                    entonces=["se reintenta o se usa un canal alterno",
                              "no se duplican mensajes al mismo deudor"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-15",
        name="Envio RCL y RCR",
        bounded_context="Integracion ERP",
        components="Generacion y envio de RCL/RCR (facturacion electronica en "
                   "UnoEE, timbrado Numrot).",
        source="Envio_de_RCL_y_RCR.pdf",
        abbs=["ABB-002", "ABB-003"],
        stories=[
            UserStory(
                id="HU-15",
                rol="sistema de facturacion",
                quiero="generar y enviar los documentos RCL/RCR tras el "
                       "desembolso",
                para="cumplir la facturacion electronica (timbrado Numrot)",
                happy=GherkinScenario(
                    titulo="RCL/RCR timbrado y enviado (happy path)",
                    dado=["un desembolso confirmado (RN-03)"],
                    cuando=["se generan RCL/RCR en UnoEE"],
                    entonces=["se timbran con Numrot",
                              "se envian al cliente y a la DIAN"],
                ),
                edge=GherkinScenario(
                    titulo="Fallo de timbrado (caso borde)",
                    tipo="edge",
                    dado=["un desembolso confirmado"],
                    cuando=["el timbrado con Numrot falla"],
                    entonces=["se reintenta el timbrado via eventos",
                              "nunca se escribe directo a la BD del ERP (ADR-002)"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-16",
        name="Integracion UnoEE / Siesa",
        bounded_context="Integracion ERP",
        components="Integracion con el ERP Siesa/UnoEE (hoy archivos planos + "
                   "WS unico; TO-BE Data Services + eventos).",
        source="WSO2 y Studio F - Assessment Mayo2026-Final.pdf",
        abbs=["ABB-002", "ABB-003"],
        stories=[
            UserStory(
                id="HU-16",
                rol="plataforma de integracion",
                quiero="sincronizar con el ERP Siesa/UnoEE via Data Services y "
                       "eventos",
                para="eliminar los archivos planos batch y el WS unico como "
                     "cuello de botella (GAP-001)",
                happy=GherkinScenario(
                    titulo="Sincronizacion gobernada con Siesa (happy path)",
                    dado=["un evento de negocio (p. ej. PagoAplicado)"],
                    cuando=["se publica al bus y lo consumen los Data Services"],
                    entonces=["Siesa se actualiza via Data Services gobernados",
                              "no se accede directo a la BD del ERP (ADR-002)"],
                ),
                edge=GherkinScenario(
                    titulo="Data Service de Siesa no disponible (caso borde, EX-04)",
                    tipo="edge",
                    dado=["un evento pendiente de sincronizar"],
                    cuando=["el Data Service de Siesa esta caido"],
                    entonces=["el evento se retiene y se reintenta",
                              "jamas se evade el contrato escribiendo a la BD"],
                ),
            ),
        ],
    ),
    Module(
        id="MOD-17",
        name="Fidelizacion / Pentaho (BI)",
        bounded_context="Cartera",
        components="Fidelizacion y analitica/BI con Pentaho sobre datos de "
                   "cartera.",
        source="RFP_CREDI10_2_0.pdf",
        abbs=["ABB-004", "ABB-005"],
        stories=[
            UserStory(
                id="HU-17",
                rol="analista de negocio",
                quiero="disponer de tableros de fidelizacion y BI (Pentaho)",
                para="tomar decisiones sobre cartera y campanas de fidelizacion",
                happy=GherkinScenario(
                    titulo="Tablero de fidelizacion actualizado (happy path)",
                    dado=["datos de cartera consolidados por el corte"],
                    cuando=["Pentaho procesa y publica los tableros"],
                    entonces=["el analista ve indicadores de fidelizacion",
                              "las cifras trazan al corte de cartera (MOD-07)"],
                ),
                edge=GherkinScenario(
                    titulo="Datos de origen incompletos (caso borde)",
                    tipo="edge",
                    dado=["un corte de cartera parcial"],
                    cuando=["Pentaho detecta datos faltantes"],
                    entonces=["el tablero marca el dato como incompleto",
                              "no se publican indicadores enganiosos"],
                ),
            ),
        ],
    ),
]


# --------------------------------------------------------------------------- #
# Helpers de cobertura (deterministas) - usados por el render y los tests.
# --------------------------------------------------------------------------- #

def module_count() -> int:
    """Numero de modulos declarados (fuente de verdad de la cobertura)."""
    return len(MODULES)


def story_count() -> int:
    """Numero total de historias de usuario declaradas."""
    return sum(len(m.stories) for m in MODULES)


def all_story_ids() -> List[str]:
    """IDs de todas las historias (Hilo Dorado), en orden estable."""
    ids: List[str] = []
    for m in MODULES:
        for s in m.stories:
            ids.append(s.id)
    return ids


def all_module_ids() -> List[str]:
    """IDs de todos los modulos, en orden estable."""
    return [m.id for m in MODULES]
