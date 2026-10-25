# BotonEcommerce.pdf

| Campo | Valor |
| --- | --- |
| id | `botonecommerce` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 2109944 |
| longitud raw | 23626 |
| longitud limpia | 13995 |
| ratio de cobertura (crudo, legado) | 0.00663 |
| caracteres de texto util | 7011 |
| texto util real (palabras / bytes extraidos) | 50.10% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `7022aa5fb6e89c5b8d695f93ce53aa82c5d41e198e1d4408c9c3199322fb8f1d` |

## Resumen jerarquico

- Documento 'BotonEcommerce.pdf' (PDF): 13995 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 50.10%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Botón Ecommerce Credi10 STF GROUP S.A. INFORMATIC...
- Seccion 2: as. Así como lo s casos de pruebas un itarias realizadas a la solución . NOTA: El desarrollo de cualquier solución de requerimiento debe seguir los estándares d...
- Seccion 3: e OTP de compra y lo envié por correo y SMS para seguir con el proceso de compra desde el ecommerce. ● Crear endpoint para crear el pagare de la compra realizad...
- Seccion 4: blioteca de clases será el encargado de calcular los pagos, procesarlos, generar y enviar el ticket. Este proyecto se integra con el proyecto Web.Admin , el pro...
- Seccion 5: 1.3.3 Proceso Se implementa el componente CheckoutController encargado de recibir por medio de la clase Ecommerce una petición encriptada que tendrá 2 tipos de...
- Seccion 6: , “ correo ” : correo@gmail .c om , “ monto ” : “ 50000 ” , “ plazo ” : ” 1 ” , “usuario”: “xxx”, “password”: “xxx” } Código:FT - DG - 00 2 Versión:001 Fecha: 0...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Botón Ecommerce Credi10 STF GROUP S.A. | Credi10, Ecommerce, API |
| 2 | CREDI10 SOFTWARE PROPIO Cali , jueves 19 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 |
| 3 | 1.1.1 Requerimiento Disponer API para suministrar informacióna paginas ecommerce del cupo que tienen los clientes con credi10 y poder realizar la compra por este medio de pago. | Credi10, Ecommerce, API |
| 4 | Se han establecido múltiples requerimientos donde cada uno presenta funcionalidades y procesos específicos que permitan la generación de información para link de recaudos. | Recaudo, Link de Recaudo |
| 5 | ● Crear parámetros de configuración para las APIs de Credi10 . | Credi10, API |
| 6 | ● Crear endpoint para consultar información del cliente , valide si tiene cupo con credi10, genere OTP de compra y lo envié por correo y SMS para seguir con el proceso de compra desde el ecommerce. | Credi10, Ecommerce, SMS |
| 7 | ● Crear endpoint para crear el pagare de la compra realizada desde el ecommerce. | Ecommerce |
| 8 | 1.2 Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con 1 solución desarrollada en .Net Framework 4.8 llamada “Créditos”. | .NET |
| 9 | Se realiza creación del proyecto web API “ Creditos.Web.Servicios ” donde se establece el funcionamiento de los requerimientos correspondientes a Link de recaudo, botón ecommerce e integración B2C. | Recaudo, Ecommerce, Link de Recaudo, B2C, API |
| 10 | Nombre del Componente Descripción SOLUCION C reditos.Web.Servicios API CheckoutController Creditos.Web.Admin Controladores y vistas implementadas para cumplir con el propósito de informar el valor del pago y recibir el valor que quieran aplicar. | API |
| 11 | 08/06/2021 Creditos.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_Credi10NET de la solución. | Credi10, C10_Credi10NET |
| 12 | BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades 1.3.1 Diagrama de Componentes 1.3.2 MER Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10, C10_Credi10NET |

