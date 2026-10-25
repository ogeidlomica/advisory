# Envio de RCL y RCR.pdf

| Campo | Valor |
| --- | --- |
| id | `envio_de_rcl_y_rcr` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 330050 |
| longitud raw | 16829 |
| longitud limpia | 11655 |
| ratio de cobertura (crudo, legado) | 0.03531 |
| caracteres de texto util | 7742 |
| texto util real (palabras / bytes extraidos) | 66.43% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib+regex (capa de texto PDF) |
| sha256 | `8a5b0becf5b4a0f87f2450a4da700c1fda0561abb55d45217cfb0d7c8a31e5c7` |

## Resumen jerarquico

- Documento 'Envio de RCL y RCR.pdf' (PDF): 11655 caracteres limpios extraidos (zlib+regex), texto util real 66.43%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: FORMATO DE DESARROLLO E INTEGRACIONES Integración envió de RCL y RCR a UnoE STF GROUP S.A. INFORMATICA – Py. CREDI10 SOFTWARE PROPIO Cali, viernes 28 de noviemb...
- Seccion 2: s del mes inmediatamente anterior, agrupado por banco y tipo de transacción. Dejar este día configu rable en parámetros 4 - Crear el documento con la fecha del...
- Seccion 3: BI A CG BANCOLO MBIA TX CB1 NC CSG CREDI10 AV BANCOLOMBI A TX Otros valores del conector F357_ID_CAJA = 02 F350_ID_TERCERO = CREDI10 F351_ID_TERCERO_OTRO_ING =...
- Seccion 4: Parametros> </Consulta> Ejemplo de plano RCL – PayU 0000002035700020010001RCL000314832024053010 20240530CREDI10 COP+000003130808880.0000COP+000003130808880.0000...
- Seccion 5: 02001001RCR00052322CA3+000000000153000.0000 00000000 20240715 20240715 CGS CREDI10 1143876497 NC BANCOLOMBIA - CG 0000002035700020011001RCR000519942024073102 20...
- Seccion 6: e requiere enviar la información. Hacer esto para los RC L de consignacióny de RCL de PayU 10 - Configurar para que el RCL que se crea con los pagos de PayU tam...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | FORMATO DE DESARROLLO E INTEGRACIONES Integración envió de RCL y RCR a UnoE STF GROUP S.A. | RCL, RCR |
| 2 | CREDI10 SOFTWARE PROPIO Cali, viernes 28 de noviembre del 2025 DETALLE TECNICO 1.1 Descripción del Requerimiento: | Credi10 |
| 3 | Un servicio que generé y envié recibos consolidados RCL (Recibos de caja payu) y RCR (recibos de consignaciones) al sistema UnoE de manera programada, garantizando la integración contable de los pagos electrónicos y consignaciones bancarias procesadas en el sistema de Credi10. | Credi10, PayU, RCL, RCR |
| 4 | 1.1.1 Requerimiento 1 - Crear un servicio que se encargue de las integraciones a UNOEE, Creación de los XML y manejo de los consecutivos manuales. | UnoEE, UNOEE |
| 5 | 2 - Crear un log en la tabla de C10_Database que permita registrar el proceso de los envíos 3 - Crear proceso que se ejecute automáticamente cada día4 del mes, donde se cree un documento de tipo RCL para cargar el valor consolidado de las consignaciones del mes inmediatamente anterior, agrupado por banco y tipo de tran... | C10_Database, RCL |
| 6 | t ipo_transaccion PLANO => f358_id_me dios_pago PLANO => f358_docto _banco_cg PLANO => *f358_nro_alt_ docto_banco *f350_notas AV VILLAS CG CA3 CG CSG CREDI10 AV VILLAS CG AV VILLAS TX CA3 NC CSG CREDI10 AV VILLAS TX BANCOLO MBIA CG CB1 CG CSG CREDI10 BANCOLOMBI A CG BANCOLO MBIA TX CB1 NC CSG CREDI10 AV BANCOLOMBI A TX... | Credi10, UnoEE, UNOEE, PayU, Recaudo, RCL, RCR |
| 7 | Hacer esto para los RC L de consignacióny de RCL de PayU 10 - Configurar para que el RCL que se crea con los pagos de PayU también se ejecute el dia 4 del mes automáticamente 1.1.2 Flujo del Proceso El WorkerConsolidadoRCL ejecuta 6 procesos principales programados: | PayU, RCL |
| 8 | Generación de Recibos RCL Consolidados - Agrupa pagos electrónicos por períodos 2. | RCL |
| 9 | Control de Recibos RCL - Verifica la creación exitosa en UnoE 3. | RCL |
| 10 | Reprocesamiento de RCL - Reenvía recibos fallidos 4. | RCL |
| 11 | Generación de Recibos RCR (Consignaciones) - Procesa consignaciones bancarias 5. | RCR |
| 12 | Control de Recibos RCR - Verifica consignaciones en UnoE 6. | RCR |

