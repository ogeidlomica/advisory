# LinkDePagos.pdf

| Campo | Valor |
| --- | --- |
| id | `linkdepagos` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 1542583 |
| longitud raw | 13102 |
| longitud limpia | 11303 |
| ratio de cobertura (crudo, legado) | 0.00733 |
| caracteres de texto util | 7606 |
| texto util real (palabras / bytes extraidos) | 67.29% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `b7217bd96e21cbf58b318f06919d3c780c1b80c92e12dc6ec5dad66398b277aa` |

## Resumen jerarquico

- Documento 'LinkDePagos.pdf' (PDF): 11303 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 67.29%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Link de recaudos Credi10 STF GROUP S.A. INFORMATI...
- Seccion 2: a: 08/06/2021 1. DETALLE TECNICO 1.1 Descripción del Requerimiento: 1.1.1 Requerimiento Disponer API para suministrar información al link de recaudos de credi10...
- Seccion 3: lamada “Créditos”. Se realiza creación del proyecto web API “ Creditos.Web.Servicios ” donde se establece el funcionamiento de los requerimientos correspondient...
- Seccion 4: s C10_Credi10NET de la solución. Creditos.DTO Proyecto que contiene los diferentes modelos usados en toda la aplicación. Rotativa Herramienta de línea de comand...
- Seccion 5: ón consumo API pagos Link https://apicredinet.studiof.c om.co:32448/payment/pay mentLink Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 1.3.3 Proceso • Ope...
- Seccion 6: s diferentes a la operación deberán ser enviados encriptados , estos serán la información del cliente y el usuario y la contraseña de quien podrá tener acceso a...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Link de recaudos Credi10 STF GROUP S.A. | Credi10, Recaudo, Link de Recaudo, API |
| 2 | CREDI10 SOFTWARE PROPIO Cali , jueves 16 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 |
| 3 | 1.1.1 Requerimiento Disponer API para suministrar información al link de recaudos de credi10 y aplicar el pago respectivo. | Credi10, Recaudo, Link de Recaudo, API |
| 4 | Se han establecido múltiples requerimientos donde cada uno presenta funcionalidades y procesos específicos que permitan la generación de información para link de recaudos. | Recaudo, Link de Recaudo |
| 5 | ● Crear parámetros de configuración para las APIs de Credi10 . | Credi10, API |
| 6 | ● Crear endpoint para consultar información del cliente y enviar al link de recaudos . | Recaudo, Link de Recaudo |
| 7 | ● Crear endpoint para procesar el pago del link de recaudos . | Recaudo, Link de Recaudo |
| 8 | 1.2 Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con 1 solución desarrollada en .Net Framework 4.8 llamada “Créditos”. | .NET |
| 9 | Se realiza creación del proyecto web API “ Creditos.Web.Servicios ” donde se establece el funcionamiento de los requerimientos correspondientes a Link de recaudo, botón ecommerce e integración B2C. | Recaudo, Ecommerce, Link de Recaudo, B2C, API |
| 10 | 08/06/2021 base de datos C10_Credi10NET de la solución. | Credi10, C10_Credi10NET |
| 11 | BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades 1.3.1 Diagrama de Componentes . | Credi10, C10_Credi10NET |
| 12 | Inténtalo de nuevo más tarde Oficina para recibir pagos web (Sucursal) Pagos 298 SMS - Mensaje Pago Realizado SMS Estimado cliente CREDI10 acabamos de recibir su pago por valor de ${0} con fecha de {1}. | Credi10, SMS |

