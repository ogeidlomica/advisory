# Reglas de negocio, excepciones y NFR base

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 3 + 3.5 - Gaps y Viabilizacion**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../03-gaps-y-viabilizacion.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

Preservar las **reglas de negocio** (RN-01..04) es un requisito duro del RFP, y la matriz de excepciones (Exception Storming) captura los casos borde del flujo de credito antes de diseñar. Junto con el perfil base de NFR (ISO 25010) y los limites de integracion legada, esta seccion define **que no puede romperse** durante la transformacion.

La narrativa de calidad es central: las excepciones y los NFR son donde los proyectos subestiman esfuerzo. Hacerlos explicitos aqui evita la sorpresa clasica de 'el happy path estaba, pero los casos borde duplicaron el trabajo'.

## Reglas de negocio a preservar

| Regla | Descripcion | Preservacion (requisito RFP) |
| --- | --- | --- |
| RN-01 | El estudio de credito encadena CrossCore, luego Inspektor y finalmente Datacredito/Dictum antes de decidir | Preservar regla existente [VERIFIED-FACT] |
| RN-02 | Una solicitud rechazada en cualquier buro detiene el flujo | Preservar regla existente |
| RN-03 | El desembolso genera RCL/RCR en UnoEE y se timbra con Numrot | Preservar regla existente |
| RN-04 | El recaudo solo se marca aplicado tras confirmacion de PayU | Preservar regla existente |

## Matriz de excepciones (Exception Storming)

| ID | Evento / caso borde (flujo estudio de credito) | Causa | Respuesta esperada TO-BE |
| --- | --- | --- | --- |
| EX-01 | CrossCore no responde o agota timeout | Indisponibilidad del buro | Reintento con backoff; si persiste, encolar y notificar sin perder la solicitud |
| EX-02 | Inspektor devuelve datos incompletos | Respuesta parcial del servicio | Marcar estudio como pendiente de revision manual, no aprobar |
| EX-03 | Datacredito/Dictum reporta no-hit | Cliente sin historial | Aplicar regla de negocio alterna de scoring, registrar [DOC-ASSUMPTION] |
| EX-04 | Escritura a Siesa falla (WS lento o caido) | Limite del WS unico | Publicar evento y reintentar via Data Services; nunca escribir directo a la BD del ERP |
| EX-05 | Solicitud duplicada del mismo cliente | Reenvio o doble clic | Idempotencia por clave de solicitud; rechazar duplicado |

### Por que las excepciones mueven la aguja

Cada excepcion (buro caido, respuesta parcial, no-hit, fallo de escritura a Siesa, duplicados) es trabajo real de resiliencia e idempotencia que rara vez cabe en una estimacion ingenua. Catalogarlas desde la Fase 3 permite que la estimacion por modulo las incluya en lugar de descubrirlas en construccion.

## Perfil base de NFR y limites legacy

| Caracteristica ISO 25010 | NFR base | Objetivo | Driver |
| --- | --- | --- | --- |
| Fiabilidad (disponibilidad) | Disponibilidad de servicios criticos | 90% -> 99% | DRV-001 |
| Eficiencia de desempenio | Latencia del estudio de credito y recaudo | Instrumentar SLOs (hoy sin medicion) [EPISTEMIC-VOID] | DRV-002 |
| Mantenibilidad | Reglas de negocio centralizadas y sin duplicar | Reducir logica duplicada | DRV-004 |
| Seguridad | Zero-trust, cifrado y trazabilidad de errores | Cerrar brechas de gobernanza | DRV-005 |
| Portabilidad | Runtime contenerizado .NET 8 | Cloud-native | DRV-004 |
| Compatibilidad | Integracion estandarizada (APIs + eventos) | Retirar archivos planos y WS unico | DRV-002 |

| Sistema legado | Limite de integracion | Impacto | Gap |
| --- | --- | --- | --- |
| ERP Siesa/UnoEE | Un UNICO Web Service para todas las operaciones | Cuello de botella y punto unico de falla | GAP-001 |
| ERP Siesa/UnoEE | Integraciones por archivos planos en modo batch | Falta de sincronizacion, latencia alta | GAP-001 |
| ERP Siesa/UnoEE | Lectura/escritura directa a la BD por lentitud del WS | Riesgo de integridad; acoplamiento a esquema | GAP-002 |
| Integraciones Windows/cronjobs | Sin gestion centralizada ni trazabilidad de errores | Incidentes opacos, MTTR alto | GAP-004 |
| Portal B2C | Wordpress/XAMPP en produccion | Superficie de ataque y operacion fragil | GAP-005 |
## Implicaciones para la estimacion

Los NFR y las excepciones son multiplicadores de esfuerzo: un modulo con muchos casos borde y NFR exigentes de disponibilidad se talla mas grande. El factor de riesgo de integracion (1,25) de la Fase 5 captura parte de este efecto.

## Implicaciones para la estrategia de implementacion

La estrategia introduce pruebas de **equivalencia funcional** para garantizar que las reglas RN-01..04 se preservan al modernizar, y trata los limites legacy (WS unico, batch) como fronteras a desacoplar de forma incremental (Strangler Fig).

## Riesgos e incertidumbre

El riesgo mayor es alterar inadvertidamente una regla de negocio al migrar. Se mitiga con una base de casos de prueba de equivalencia como prerrequisito (PRE-006). [DOC-ASSUMPTION]

