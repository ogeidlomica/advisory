# Originacion_API_Datacredito.pdf

| Campo | Valor |
| --- | --- |
| id | `originacion_api_datacredito` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 1070575 |
| longitud raw | 18721 |
| longitud limpia | 16775 |
| ratio de cobertura (crudo, legado) | 0.01567 |
| caracteres de texto util | 11542 |
| texto util real (palabras / bytes extraidos) | 68.80% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `d3e307f9ec7482661d3910ce307bde920e50ba6a657409c2c77b535a5bb7d7f2` |

## Resumen jerarquico

- Documento 'Originacion_API_Datacredito.pdf' (PDF): 16775 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 68.80%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código: ORI - API - 00 1 Versión:001 Fecha: 08/ 11 /202 3 FORMATO DE DESARROLLO E INTEGRACIONES API DATACREDITO STF GROUP S.A. INFORMATICA – Py. CREDI10 SOFTWAR...
- Seccion 2: 00 1 Versión:001 Fecha: 08/ 11 /202 3 1. DETALLE TECNICO 1.1 Descripción del Requerimiento: En el presente documento se describe técnicamente como fue desarroll...
- Seccion 3: ble para quien realiza la solicitud. Este requerimiento se basa en la necesidad de acceder de manera eficiente a la información crediticia de individuos para to...
- Seccion 4: gado de tener el acceso y la interaccióna la base de datos C10_Datacredito de la solución Web Service Produccion Historia de crédito + URL CONSUMO: https://serv...
- Seccion 5: 8/ 11 /202 3 1.3.2 MER 1.3.3 Parametrizaciones La aplicación cuenta con 18 parámetros que pueden cambiar dependiente del ambiente que se este utilizando o las r...
- Seccion 6: o del client e 805003626 805003626 DenialCaus eKey Caus a de dene gació n CAUSAL CAUSAL Código: ORI - API - 00 1 Versión:001 Fecha: 08/ 11 /202 3 DnsIdentity Id...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | ORI - API - 00 1 Versión:001 Fecha: | API |
| 2 | 08/ 11 /202 3 FORMATO DE DESARROLLO E INTEGRACIONES API DATACREDITO STF GROUP S.A. | Datacredito, API |
| 3 | CREDI10 SOFTWARE PROPIO Cali , martes, 15 de septiembre de 2026 Código: | Credi10 |
| 4 | En el presente documento se describe técnicamente como fue desarrollada la API que interviene en el proceso de o riginaci ó n de cupo. | API |
| 5 | La API se conecta de manera segura al servicio proporcionado por Datacrédito Experian donde se obtendrá los datos crediticios de personas naturales según los datos de la solicitud de entrada. | API |
| 6 | La API responde a las solicitudes de los usuarios proporcionando la información crediticia detallada yfácilmente interp r etable para quien realiza la solicitud. | API |
| 7 | Este requerimiento se basa en la necesidad de acceder de manera eficiente a la información crediticia de individuos para tomar una decisión puntual en el proceso de originación en el aplicativo de credi10, teniendo en cuenta la escalabilidad que este pueda tener a futuro. | Credi10 |
| 8 | 1.2 Detallar componentes existentes SOLUCION Datacredito.Integrator.Api Proyecto que proporciona un conjunto de servicios a otras aplicaciones a través de una interfaz de programación de aplicaciones (API). | Datacredito, API |
| 9 | Datacredito.Integrator.BLL Proyecto que contiene las clases y métodos que implementan la lógica de negocio de la aplicación, esta biblioteca de clases será el encargado de consumir el servicio web, procesarlo y entregar la información para su posterior envió al usuario final. | Datacredito |
| 10 | Este p royecto se integra con el proyecto API y el proyecto DAL. | API |
| 11 | Datacredito.Integrator.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_Datacredito de la solución Web Service Produccion Historia de crédito + URL CONSUMO: | Datacredito, C10_Datacredito |
| 12 | https://servicesesb.datacredito.com .co/wss/dhws3/services/DHServicePlus Código: | Datacredito, S3 |

