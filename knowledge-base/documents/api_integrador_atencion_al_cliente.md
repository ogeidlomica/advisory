# Api Integrador Atencion al cliente.pdf

| Campo | Valor |
| --- | --- |
| id | `api_integrador_atencion_al_cliente` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 910137 |
| longitud raw | 17167 |
| longitud limpia | 15395 |
| ratio de cobertura (crudo, legado) | 0.01692 |
| caracteres de texto util | 9901 |
| texto util real (palabras / bytes extraidos) | 64.31% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `230c3c9a38f8a8dbd25ffa205504ce39fb2817ee7b3fa7e5948051982dde6a31` |

## Resumen jerarquico

- Documento 'Api Integrador Atencion al cliente.pdf' (PDF): 15395 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 64.31%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES API Integrador Atención Al Cliente STF GROUP S.A. INFORMATICA – Py. CR...
- Seccion 2: rtificado Al Día ................................ ................................ ................................ . 9 Generar Certificado de Deuda ..............
- Seccion 3: /o Comentarios ................................ ................................ ....... 13 2. CASOS DE PRUEBAS UNITARIAS 17 Código:FT - DG - 00 2 Versión:001 F...
- Seccion 4: tificado paz y salvo ● Crear endpoint para c rear y enviar certificado tributario ● Crear endpoint para crear y enviar certificado de cliente al día ● Crear end...
- Seccion 5: on del archivo PD F, envió del archivo por correo electrónico. Creditos.BLL Proyecto que contiene las clases y métodos que implementan la lógica de negocio de l...
- Seccion 6: validación de entrada, manejo de respuestas HTTP • AccountController.cs: Autenticación JWT . • ServicioAtencionClienteWolkvoxController.cs: Endpoints principale...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES API Integrador Atención Al Cliente STF GROUP S.A. | integrador, API |
| 2 | CREDI10 SOFTWARE PROPIO Cali , viernes 26 de diciembre del 202 5 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 |
| 3 | DETALLE TECNICO Requerimiento Disponer API para suministrar información de los clientes de C redi10 y generación de certificados PDF . | API |
| 4 | Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con una solución desarrollada en .NET Framework 4.8 . | .NET |
| 5 | Se realiza creación del proyecto web API “ Creditos.Integrador.AtencionCiente ” donde se establece el funcionamiento de los requerimientos correspondientes a la generación de los certificados anteriormente mencionados . | integrador, API |
| 6 | Nombre del Componente Descripción SOLUCION Creditos.Integrador.AtencionCiente API proporciona los endpoint . | integrador, API |
| 7 | BLL.AtencionClienteApiController Controlador implementad o para evaluar la viabilidad de la generación del certificado para el cliente, creacion del archivo PD F, envió del archivo por correo electrónico. | API |
| 8 | Este proyecto se integra con el proyecto Creditos.Integrador.AtencionCiente, el proyecto DAL y el proyecto DTO. | integrador |
| 9 | Creditos.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_Credi10NET de la solución. | Credi10, C10_Credi10NET |
| 10 | 08/06/2021 Rotativa Herramienta de línea de comandos para representar HTML en PDF, encargado de crear los PDF de los certificados BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.1.2. | Credi10, C10_Credi10NET |
| 11 | Detallar funcionalidades Diagrama de Componentes Arquitectura por Capas Capa Web (Creditos.Integrador.AtencionCiente) Responsabilidad : | integrador |
| 12 | • ServicioAtencionClienteWolkvoxController.cs: | WOLKVOX |

