# B2C.pdf

| Campo | Valor |
| --- | --- |
| id | `b2c` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 2256650 |
| longitud raw | 17919 |
| longitud limpia | 13764 |
| ratio de cobertura (crudo, legado) | 0.00610 |
| caracteres de texto util | 7644 |
| texto util real (palabras / bytes extraidos) | 55.54% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `cde25f1342dbc9b86dd5b45e54e5930701aeffeee32eb40fc03694710abc0c2f` |

## Resumen jerarquico

- Documento 'B2C.pdf' (PDF): 13764 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 55.54%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Portal clientes B2C STF GROUP S.A. INFORMATICA –...
- Seccion 2: /06/2021 1. DETALLE TECNICO 1.1 Descripción del Requerimiento: 1.1.1 Requerimiento Disponer API para suministrar diferente información al portal de clientes cre...
- Seccion 3: CheckoutController Creditos.Web.Admin Controladores y vistas implementadas para cumplir con el propósito de informar el valor del pago y recibir el valor que qu...
- Seccion 4: y Procedimientos almacenados 1.3 Detallar funcionalidades 1.3.1 Diagrama de Componentes 1.3.2 MER Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 Parametriz...
- Seccion 5: ponde a una encriptación del siguiente objeto Al realizar cualquier solicitud a la API de B2CController entrará al método asíncrono llamado b2c, que procesará t...
- Seccion 6: ¨¹¢K" VµN +9E³Ã_faKbZ@/" RquÅÃ~qPccJ]J5$ 2©Â£bbbJRC* OvÆµ3$! 2b¡ÉÖ_{DavBUV$ %sÆñdPP Gh©ÕWd[$9Qo¹èsIeuG`b' ::0p}¶`I;-'" _ztÃ»bP5::00,#%*0²­...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Portal clientes B2C STF GROUP S.A. | Portal, B2C, API |
| 2 | CREDI10 SOFTWARE PROPIO Cali , jueves 19 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 |
| 3 | 1.1.1 Requerimiento Disponer API para suministrar diferente información al portal de clientes credi10 (B2C) . | Credi10, Portal, B2C, API |
| 4 | 1.2 Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con 1 solución desarrollada en .NET Framework 4.8 llamada “Créditos”. | .NET |
| 5 | Se realiza creación del proyecto web API “ Creditos.Web.Servicios ” donde se establece el funcionamiento de los requerimientos correspondientes a Link de recaudo, botón ecommerce e integración B2C. | Recaudo, Ecommerce, Link de Recaudo, B2C, API |
| 6 | Nombre del Componente Descripción SOLUCION C reditos.Web.Servicios API CheckoutController Creditos.Web.Admin Controladores y vistas implementadas para cumplir con el propósito de informar el valor del pago y recibir el valor que quieran aplicar. | API |
| 7 | Creditos.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_Credi10NET de la solución. | Credi10, C10_Credi10NET |
| 8 | BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades 1.3.1 Diagrama de Componentes 1.3.2 MER Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10, C10_Credi10NET |
| 9 | 08/06/2021 Parametrizaciones Descripción Grupo Valor Link conexión consumo API pagos Link https://apicredinet.studiof.c om.co:32448/payment/pay mentLink Código:FT - DG - 00 2 Versión:001 Fecha: | API |
| 10 | 08/06/2021 1.3.3 Proceso Se implementa el componente B2CController encargado de recibir 4 tipos de peticiones diferenciadas por el atributo “operación”. | B2C |
| 11 | Donde el contenido del atributo “datos” corresponde a una encriptación del siguiente objeto Al realizar cualquier solicitud a la API de B2CController entrará al método asíncrono llamado b2c, que procesará todas las solicitudes y, dependiendo de la operación recibida en el cuerpo de la petición, hacer una u otra tarea. | B2C, API |
| 12 | 08/06/2021 El objeto json recibido en la petición se desencripta con claves específicas y se inicia con el proceso validación del usuario y password suministrados en el objeto, si no son correctas las credenciales el sistema retornará “No Autorizado”, en caso de ser correctas, se obtendrá la información necesaria para... | API |

