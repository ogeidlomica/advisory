# Originacion_API_Inspektor.pdf

| Campo | Valor |
| --- | --- |
| id | `originacion_api_inspektor` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 831033 |
| longitud raw | 13936 |
| longitud limpia | 12636 |
| ratio de cobertura (crudo, legado) | 0.01521 |
| caracteres de texto util | 8626 |
| texto util real (palabras / bytes extraidos) | 68.27% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `5699645db159f4aed9e6e8e3d890cd99b0f3c60127129ca70780bd280e354ce2` |

## Resumen jerarquico

- Documento 'Originacion_API_Inspektor.pdf' (PDF): 12636 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 68.27%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código: ORI - API - 00 1 Versión:001 Fecha: 08/ 11 /202 3 FORMATO DE DESARROLLO E INTEGRACIONES API IN SPEKTOR STF GROUP S.A. INFORMATICA – Py. CREDI10 SOFTWARE...
- Seccion 2: ruebas un itarias realizadas a la solución . NOTA: El desarrollo de cualquier solución de requerimiento debe seguir los estándares de desarrollo que define Arqu...
- Seccion 3: el estudio . c) Retorno de información por listas restrictivas : La API responde a las solicitudes de los usuarios proporcionando la información de si el client...
- Seccion 4: r URL CONSUMO: https://inspektor.datalaft.com:2055/ WSInspektor.asmx URL WSDL: https://inspektor.datalaft.com:2055/ WSInspektor.asmx?WSDL Código: ORI - API - 00...
- Seccion 5: r.da talaft.com:2055/W SInspektor.asmx ServicePassword Contraseña del cliente Inspektor xxx xxx JWT_SECRET_KEY Llave secreta para el JWT xxxxxxx xxxxx JWT_AUDIE...
- Seccion 6: teriormente para autorizar y autenticar las solicitudes subsiguientes del usuario. En caso de que las credenciales recibidas en la soli citud sean inválidas, la...

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

