# Originacion_API_Inspektor.pdf

| Campo | Valor |
| --- | --- |
| id | `originacion_api_inspektor` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 831033 |
| longitud raw | 13936 |
| longitud limpia | 12445 |
| ratio de cobertura (crudo, legado) | 0.01498 |
| caracteres de texto util | 8626 |
| texto util real (palabras / bytes extraidos) | 69.31% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `5699645db159f4aed9e6e8e3d890cd99b0f3c60127129ca70780bd280e354ce2` |

## Resumen jerarquico

- Documento 'Originacion_API_Inspektor.pdf' (PDF): 12445 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 69.31%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código: ORI - API - 00 1 Versión:001 Fecha: 08/ 11 /202 3 FORMATO DE DESARROLLO E INTEGRACIONES API IN SPEKTOR STF GROUP S.A. INFORMATICA – Py. CREDI10 SOFTWARE...
- Seccion 2: 0 1 Versión:001 Fecha: 08/ 11 /202 3 1. DETALLE TECNICO 1.1 Descripción del Requerimiento: En el presente documento se describe técnicamente como fue desarrolla...
- Seccion 3: estrictivas. 1.2 Detallar componentes existentes SOLUCION Inspektor .Integrator.Api Proyecto que proporciona un conjunto de servicios a otras aplicaciones a tra...
- Seccion 4: 02 3 BASE DE DATOS C10_ Inspektor .dbo.tbl_apps Tablas C10_ Inspektor .dbo.tbl_consulta_ inspektor Tablas C10_ Inspektor .dbo.tbl_parametros Tablas 1.3 Detallar...
- Seccion 5: cion para consumir la API http://192.168.0. xxx / http://192.168.0. xx x / JWT_ISSUER_TOKEN Cliente que podra realizar peticiones a la API http://192.168.0. xxx...
- Seccion 6: estado HTTP 401 (No Autorizado), indicando que la autenticación ha fallado. Este mecanismo de autenticación basado en JWT contribuye a la seguridad de la API al...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | ORI - API - 00 1 Versión:001 Fecha: | API |
| 2 | 08/ 11 /202 3 FORMATO DE DESARROLLO E INTEGRACIONES API IN SPEKTOR STF GROUP S.A. | API |
| 3 | CREDI10 SOFTWARE PROPIO Cali , martes, 15 de septiembre de 2026 Código: | Credi10 |
| 4 | En el presente documento se describe técnicamente como fue desarrollada la API que interviene en el proceso de o riginaci ó n de cupo para Credi 10. | API |
| 5 | a) Consumo del servicio web Inspektor: | Inspektor |
| 6 | La API se conecta de manera segura al servicio proporcionado por INSPEKTOR d onde se obtendrá información de los clientes en listas que ellos administran . | Inspektor, API |
| 7 | La API responde a las solicitudes de los usuarios proporcionando la información de si el cliente se encuentra o no en listas restrictivas. | API |
| 8 | 1.2 Detallar componentes existentes SOLUCION Inspektor .Integrator.Api Proyecto que proporciona un conjunto de servicios a otras aplicaciones a través de una interfaz de programación de aplicaciones (API). | Inspektor, API |
| 9 | Inspektor .Integrator.BLL Proyecto que contiene las clases y métodos que implementan la lógica de negocio de la aplicación, esta biblioteca de clases será el encargado de consumir el servicio web, procesarlo y entregar la información para su posterior envió al usuario final. | Inspektor |
| 10 | Este p royecto se integra con el proyecto API y el proyecto DAL. | API |
| 11 | Inspektor .Integrator.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_ Inspektor de la solución Web Service Inspektor URL CONSUMO: | Inspektor |
| 12 | https://inspektor.datalaft.com:2055/ WSInspektor.asmx URL WSDL: | Inspektor |

