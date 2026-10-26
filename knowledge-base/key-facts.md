# Hechos clave consolidados (con trazabilidad)

Cada hecho se extrae de la capa de texto del documento fuente mediante coincidencia de tokens de dominio Credi10. La columna **Fuente** garantiza la trazabilidad al documento original.

| # | Hecho | Fuente | Tokens |
| --- | --- | --- | --- |
| 1 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES API Integrador Atención Al Cliente STF GROUP S.A. | Api Integrador Atencion al cliente.pdf | integrador, API |
| 2 | CREDI10 SOFTWARE PROPIO Cali , viernes 26 de diciembre del 202 5 Código:FT - DG - 00 2 Versión:001 Fecha: | Api Integrador Atencion al cliente.pdf | Credi10 |
| 3 | DETALLE TECNICO Requerimiento Disponer API para suministrar información de los clientes de C redi10 y generación de certificados PDF . | Api Integrador Atencion al cliente.pdf | API |
| 4 | Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con una solución desarrollada en .NET Framework 4.8 . | Api Integrador Atencion al cliente.pdf | .NET |
| 5 | Se realiza creación del proyecto web API “ Creditos.Integrador.AtencionCiente ” donde se establece el funcionamiento de los requerimientos correspondientes a la generación de los certificados anteriormente mencionados . | Api Integrador Atencion al cliente.pdf | integrador, API |
| 6 | Nombre del Componente Descripción SOLUCION Creditos.Integrador.AtencionCiente API proporciona los endpoint . | Api Integrador Atencion al cliente.pdf | integrador, API |
| 7 | BLL.AtencionClienteApiController Controlador implementad o para evaluar la viabilidad de la generación del certificado para el cliente, creacion del archivo PD F, envió del archivo por correo electrónico. | Api Integrador Atencion al cliente.pdf | API |
| 8 | Este proyecto se integra con el proyecto Creditos.Integrador.AtencionCiente, el proyecto DAL y el proyecto DTO. | Api Integrador Atencion al cliente.pdf | integrador |
| 9 | Creditos.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_Credi10NET de la solución. | Api Integrador Atencion al cliente.pdf | Credi10, C10_Credi10NET |
| 10 | 08/06/2021 Rotativa Herramienta de línea de comandos para representar HTML en PDF, encargado de crear los PDF de los certificados BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.1.2. | Api Integrador Atencion al cliente.pdf | Credi10, C10_Credi10NET |
| 11 | Detallar funcionalidades Diagrama de Componentes Arquitectura por Capas Capa Web (Creditos.Integrador.AtencionCiente) Responsabilidad : | Api Integrador Atencion al cliente.pdf | integrador |
| 12 | • ServicioAtencionClienteWolkvoxController.cs: | Api Integrador Atencion al cliente.pdf | WOLKVOX |
| 13 | Credi10 corre sobre .NET Framework 4.8 en IIS 10; | Arquitectura_Aplicacion_Despliegue_Credi10.png | Credi10, .NET, IIS |
| 14 | integradores en .NET y Windows Services en .NET Core 8 y .NET 4.8. | Arquitectura_Aplicacion_Despliegue_Credi10.png | .NET, integrador |
| 15 | Bases de datos SQL Server 2019 Enterprise: | Arquitectura_Aplicacion_Despliegue_Credi10.png | SQL Server |
| 16 | C10_Credi10NET, C10_Inspektor, C10_Datacredito y C10_Database. | Arquitectura_Aplicacion_Despliegue_Credi10.png | Credi10, Inspektor, Datacredito, C10_Credi10NET, C10_Inspektor, C10_Datacredito, C10_Database |
| 17 | El modulo B2C usa Node.js + React + Wordpress sobre Apache con MariaDB. | Arquitectura_Aplicacion_Despliegue_Credi10.png | MariaDB, Node.js, React, Wordpress, Apache, B2C |
| 18 | Link de Recaudo en .NET Core 3.1. | Arquitectura_Aplicacion_Despliegue_Credi10.png | .NET, Recaudo, Link de Recaudo |
| 19 | Servidores on-prem nombrados Coatlanta, Codallas y Comumbai. | Arquitectura_Aplicacion_Despliegue_Credi10.png | Coatlanta, Codallas, Comumbai |
| 20 | Diagrama de infraestructura AWS en la region us-east-2. | Arquitectura_Infraestructura_AWS_Credi10.png | AWS |
| 21 | VPC 'STUDIO F' con WAF -> ALB -> instancias EC2 privadas, almacenamiento S3, monitoreo CloudWatch, NAT Gateway y Bastion host. | Arquitectura_Infraestructura_AWS_Credi10.png | VPC, WAF, ALB, EC2, S3, CloudWatch, Bastion, Studio F |
| 22 | Conectividad hibrida mediante VPN IPSec de Telmex hacia el centro de datos on-prem 'Cokioto'. | Arquitectura_Infraestructura_AWS_Credi10.png | VPN, IPSec, Telmex, Cokioto |
| 23 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Portal clientes B2C STF GROUP S.A. | B2C.pdf | Portal, B2C, API |
| 24 | CREDI10 SOFTWARE PROPIO Cali , jueves 19 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | B2C.pdf | Credi10 |
| 25 | 1.1.1 Requerimiento Disponer API para suministrar diferente información al portal de clientes credi10 (B2C) . | B2C.pdf | Credi10, Portal, B2C, API |
| 26 | 1.2 Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con 1 solución desarrollada en .NET Framework 4.8 llamada “Créditos”. | B2C.pdf | .NET |
| 27 | Se realiza creación del proyecto web API “ Creditos.Web.Servicios ” donde se establece el funcionamiento de los requerimientos correspondientes a Link de recaudo, botón ecommerce e integración B2C. | B2C.pdf | Recaudo, Ecommerce, Link de Recaudo, B2C, API |
| 28 | Nombre del Componente Descripción SOLUCION C reditos.Web.Servicios API CheckoutController Creditos.Web.Admin Controladores y vistas implementadas para cumplir con el propósito de informar el valor del pago y recibir el valor que quieran aplicar. | B2C.pdf | API |
| 29 | Creditos.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_Credi10NET de la solución. | B2C.pdf | Credi10, C10_Credi10NET |
| 30 | BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades 1.3.1 Diagrama de Componentes 1.3.2 MER Código:FT - DG - 00 2 Versión:001 Fecha: | B2C.pdf | Credi10, C10_Credi10NET |
| 31 | 08/06/2021 Parametrizaciones Descripción Grupo Valor Link conexión consumo API pagos Link https://apicredinet.studiof.c om.co:32448/payment/pay mentLink Código:FT - DG - 00 2 Versión:001 Fecha: | B2C.pdf | API |
| 32 | 08/06/2021 1.3.3 Proceso Se implementa el componente B2CController encargado de recibir 4 tipos de peticiones diferenciadas por el atributo “operación”. | B2C.pdf | B2C |
| 33 | Donde el contenido del atributo “datos” corresponde a una encriptación del siguiente objeto Al realizar cualquier solicitud a la API de B2CController entrará al método asíncrono llamado b2c, que procesará todas las solicitudes y, dependiendo de la operación recibida en el cuerpo de la petición, hacer una u otra tarea. | B2C.pdf | B2C, API |
| 34 | 08/06/2021 El objeto json recibido en la petición se desencripta con claves específicas y se inicia con el proceso validación del usuario y password suministrados en el objeto, si no son correctas las credenciales el sistema retornará “No Autorizado”, en caso de ser correctas, se obtendrá la información necesaria para... | B2C.pdf | API |
| 35 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Botón Ecommerce Credi10 STF GROUP S.A. | BotonEcommerce.pdf | Credi10, Ecommerce, API |
| 36 | CREDI10 SOFTWARE PROPIO Cali , jueves 19 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | BotonEcommerce.pdf | Credi10 |
| 37 | 1.1.1 Requerimiento Disponer API para suministrar informacióna paginas ecommerce del cupo que tienen los clientes con credi10 y poder realizar la compra por este medio de pago. | BotonEcommerce.pdf | Credi10, Ecommerce, API |
| 38 | Se han establecido múltiples requerimientos donde cada uno presenta funcionalidades y procesos específicos que permitan la generación de información para link de recaudos. | BotonEcommerce.pdf | Recaudo, Link de Recaudo |
| 39 | ● Crear parámetros de configuración para las APIs de Credi10 . | BotonEcommerce.pdf | Credi10, API |
| 40 | ● Crear endpoint para consultar información del cliente , valide si tiene cupo con credi10, genere OTP de compra y lo envié por correo y SMS para seguir con el proceso de compra desde el ecommerce. | BotonEcommerce.pdf | Credi10, Ecommerce, SMS |
| 41 | ● Crear endpoint para crear el pagare de la compra realizada desde el ecommerce. | BotonEcommerce.pdf | Ecommerce |
| 42 | 1.2 Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con 1 solución desarrollada en .Net Framework 4.8 llamada “Créditos”. | BotonEcommerce.pdf | .NET |
| 43 | Se realiza creación del proyecto web API “ Creditos.Web.Servicios ” donde se establece el funcionamiento de los requerimientos correspondientes a Link de recaudo, botón ecommerce e integración B2C. | BotonEcommerce.pdf | Recaudo, Ecommerce, Link de Recaudo, B2C, API |
| 44 | Nombre del Componente Descripción SOLUCION C reditos.Web.Servicios API CheckoutController Creditos.Web.Admin Controladores y vistas implementadas para cumplir con el propósito de informar el valor del pago y recibir el valor que quieran aplicar. | BotonEcommerce.pdf | API |
| 45 | 08/06/2021 Creditos.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_Credi10NET de la solución. | BotonEcommerce.pdf | Credi10, C10_Credi10NET |
| 46 | BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades 1.3.1 Diagrama de Componentes 1.3.2 MER Código:FT - DG - 00 2 Versión:001 Fecha: | BotonEcommerce.pdf | Credi10, C10_Credi10NET |
| 47 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES CAPTURA FOTO STF GROUP S.A. | Captura Foto.pdf | Captura, Foto |
| 48 | CREDI10 SOFTWARE PROPIO Cali , lunes , 29 de enero de 202 4 Código:FT - DG - 00 2 Versión:001 Fecha: | Captura Foto.pdf | Credi10 |
| 49 | 1.1.1 Requerimiento Validar que el cliente tenga foto, si no , r ealizar la captura de la foto del cliente en el proceso antes de ingresar al formulario, también permitir recaptura en el formulario . | Captura Foto.pdf | Captura, Foto |
| 50 | 1.1.2 Flujo del Proceso Index.cshtml Se ingresa la información de la tienda y el cliente Camara.cshtml Se presiona en capturar para visualizar la foto que se captura en la parte derecha, si la foto sale mal puede volver a dar en capturar para actualizar la foto y la visualización Camara.cshtml Se presiona en guardar pa... | Captura Foto.pdf | Captura, Foto |
| 51 | Admin • Controladores o Desembolso Controller.cs • Vistas o Index.cshtml o Create.cshtml o Camara .cshtml Clases y vista implementada para la captura de la foto . | Captura Foto.pdf | Captura, Foto |
| 52 | Creditos.BLL • Desembolsos Service s .cs Clase implementada para realizar la validación de cliente tiene foto . | Captura Foto.pdf | Foto |
| 53 | Bootstrap Librería para el front v5.1.3 BASE DE DATOS tbl_clientes Tabla tbl_cliente_fotos Tabla Código:FT - DG - 00 2 Versión:001 Fecha: | Captura Foto.pdf | Foto |
| 54 | https://app.diagrams.net/ https://www.youtube.com/watch?app=desktop&v=JF7bH5Xo6ys https://www.ionos.es/digitalguide/paginas - web/desarrollo - web/diagrama - de - componentes/ Código:FT - DG - 00 2 Versión:001 Fecha: | Captura Foto.pdf | .NET |
| 55 | ‘ClienteSinFoto’, ‘FotoGuardada’, ‘FotoNoGuardada’ - Los anteriores registros son los mensajes que se muestran en el proceso de captura de la foto. | Captura Foto.pdf | Captura, Foto |
| 56 | 1.3.4 Proceso La generación del crédito inicia con Index.cshtml del controlador Desembolso Controller.cs , en esta vista se lan zan una serie de validaciones con el consumo de un endpoint incluida la validación de la existencia de al menos una foto del cliente . | Captura Foto.pdf | Foto |
| 57 | Index.cshtml tiene los inputs correspondientes a la tienda , el cliente y adicionalmente contiene un modal #mdCamara que es el que permite visualizar la vista Camara.cshtml para realizar la cap tura de la foto. | Captura Foto.pdf | Foto |
| 58 | 08/06/2021 En el proceso de captura de fotos, el input relevante es de tipo texto #NumeroDocumento , donde se ingresa el número de documento del cliente. | Captura Foto.pdf | Captura, Foto |
| 59 | Diagrama de contexto C4 de Credi10. | Diagrama_Contexto_Credi10.png | Credi10 |
| 60 | Aplicacion web central CREDI10 en .NET integrada con UNOEE/Siesa (ERP), PENTAHO (BI/ETL), CROSSCORE -> INSPEKTOR -> DICTUM/Datacredito (originacion y riesgo), Numrot, Cobranza, B2C, Link de Recaudo -> PayU, VTEX (ecommerce), WOLKVOX (contact center), ICOMMARKETING y B2CHAT. | Diagrama_Contexto_Credi10.png | Credi10, Siesa, UnoEE, UNOEE, CrossCore, Inspektor, Datacredito, DICTUM, PayU, WOLKVOX, VTEX, Pentaho, Numrot, B2CHAT, ICOMMARKETING, .NET, Originacion, Cobranza, Recaudo, Ecommerce, Link de Recaudo, B2C |
| 61 | Muestra el sistema Credi10 como nucleo .NET rodeado de integraciones externas de originacion, pagos, ecommerce y atencion al cliente. | Diagrama_Contexto_Credi10.png | Credi10, .NET, Originacion, Ecommerce |
| 62 | FORMATO DE DESARROLLO E INTEGRACIONES Integración envió de RCL y RCR a UnoE STF GROUP S.A. | Envio de RCL y RCR.pdf | RCL, RCR |
| 63 | CREDI10 SOFTWARE PROPIO Cali, viernes 28 de noviembre del 2025 DETALLE TECNICO 1.1 Descripción del Requerimiento: | Envio de RCL y RCR.pdf | Credi10 |
| 64 | Un servicio que generé y envié recibos consolidados RCL (Recibos de caja payu) y RCR (recibos de consignaciones) al sistema UnoE de manera programada, garantizando la integración contable de los pagos electrónicos y consignaciones bancarias procesadas en el sistema de Credi10. | Envio de RCL y RCR.pdf | Credi10, PayU, RCL, RCR |
| 65 | 1.1.1 Requerimiento 1 - Crear un servicio que se encargue de las integraciones a UNOEE, Creación de los XML y manejo de los consecutivos manuales. | Envio de RCL y RCR.pdf | UnoEE, UNOEE |
| 66 | 2 - Crear un log en la tabla de C10_Database que permita registrar el proceso de los envíos 3 - Crear proceso que se ejecute automáticamente cada día4 del mes, donde se cree un documento de tipo RCL para cargar el valor consolidado de las consignaciones del mes inmediatamente anterior, agrupado por banco y tipo de tran... | Envio de RCL y RCR.pdf | C10_Database, RCL |
| 67 | t ipo_transaccion PLANO => f358_id_me dios_pago PLANO => f358_docto _banco_cg PLANO => *f358_nro_alt_ docto_banco *f350_notas AV VILLAS CG CA3 CG CSG CREDI10 AV VILLAS CG AV VILLAS TX CA3 NC CSG CREDI10 AV VILLAS TX BANCOLO MBIA CG CB1 CG CSG CREDI10 BANCOLOMBI A CG BANCOLO MBIA TX CB1 NC CSG CREDI10 AV BANCOLOMBI A TX... | Envio de RCL y RCR.pdf | Credi10, UnoEE, UNOEE, PayU, Recaudo, RCL, RCR |
| 68 | Hacer esto para los RC L de consignacióny de RCL de PayU 10 - Configurar para que el RCL que se crea con los pagos de PayU también se ejecute el dia 4 del mes automáticamente 1.1.2 Flujo del Proceso El WorkerConsolidadoRCL ejecuta 6 procesos principales programados: | Envio de RCL y RCR.pdf | PayU, RCL |
| 69 | Generación de Recibos RCL Consolidados - Agrupa pagos electrónicos por períodos 2. | Envio de RCL y RCR.pdf | RCL |
| 70 | Control de Recibos RCL - Verifica la creación exitosa en UnoE 3. | Envio de RCL y RCR.pdf | RCL |
| 71 | Reprocesamiento de RCL - Reenvía recibos fallidos 4. | Envio de RCL y RCR.pdf | RCL |
| 72 | Generación de Recibos RCR (Consignaciones) - Procesa consignaciones bancarias 5. | Envio de RCL y RCR.pdf | RCR |
| 73 | Control de Recibos RCR - Verifica consignaciones en UnoE 6. | Envio de RCL y RCR.pdf | RCR |
| 74 | CREDI10 SOFTWARE PROPIO Cali , martes, 15 de septiembre de 2026 Código:FT - SL - 00 3 Versión:001 Fecha: | GenerarPagos.pdf | Credi10 |
| 75 | 1.1.1 Requerimiento Realizar todo el proceso de pagos de los créditos realizados con el cupo de credi10, garantizando el adecuado cobro de los diferentes rubros correspondientes a mora, aval, interés, los impuestos correspondientes y el capital. | GenerarPagos.pdf | Credi10, API |
| 76 | FT - SL - 003 - Módulo_Pago - V5 1.1.2 Flujo del Proceso • Pago en tienda Agregar mockup o capturas del flujo del proceso Código:FT - SL - 00 3 Versión:001 Fecha: | GenerarPagos.pdf | Captura |
| 77 | Creditos.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_ Credi10NET de la solución . | GenerarPagos.pdf | Credi10 |
| 78 | BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades 1.3.1 Diagrama de Arquitectura Usar para estos manuales, mejor diagramas de componentes ya que por ser funcionalidades internas los diagramas de arquitectura dan una visualizacion muy general Opcional usar: | GenerarPagos.pdf | Credi10, C10_Credi10NET |
| 79 | https://app.diagrams.net/ https://www.youtube.com/watch?app=desktop&v=JF7bH5Xo6ys https://www.ionos.es/digitalguide/paginas - web/desarrollo - web/diagrama - de - componentes/ Código:FT - SL - 00 3 Versión:001 Fecha: | GenerarPagos.pdf | .NET |
| 80 | TipoPago Online Mensaje de las tiendas que ya alcanzaron su límite de recaudo Pagos Lo sentimos, ya se alcanzó el límite de recaudo Mensaje al ingresar un valor no permitido para el pago Pagos El valor del pago está fuera del rango permitido Mensaje mostrado cuando el valor del pago ingresado Pagos El valor ingresado s... | GenerarPagos.pdf | Recaudo |
| 81 | 21 / 12 /202 3 supera el límite de recaudo de la empresa aliada. | GenerarPagos.pdf | Recaudo |
| 82 | Por favor repite el proceso de consulta Oficina para recibir pagos web Pagos 298 SMS - Mensaje Pago Realizado SMS Estimado cliente CREDI10 acabamos de recibir su pago por valor de ${0} con fecha de {1}. | GenerarPagos.pdf | Credi10, SMS |
| 83 | 1.3.4 Proceso Cuando un usuario inicia sesión en la aplicación web de credi10 este va a tener un perfil asignado el cual le concederá permisos para ver y realizar diferentes operaciones dentro del sistema. | GenerarPagos.pdf | Credi10 |
| 84 | 21 / 12 /202 3 Esta vista tiene como ruta https://www.credi10.com.co/Pagos , si se intenta acceder a ella sin iniciar sesión antes será redirigido a la vista de Login Login (credi10.com.co) y si ya ha iniciado sesión y el usuario no tiene los permisos adecuados e intentará acceder directamente por medio de l link , el... | GenerarPagos.pdf | Credi10 |
| 85 | • Pagos En Tienda Al ingresar al índex de pagos en tienda ( https://www.credi10.com.co/Pagos ) llamara al método ValidateSession explicado aquí , que garantiza si el usuario tiene permisos de ingresar al recurso, obtiene y valida la dirección de la ip de conexión para saber si es una tienda específica para que cuando c... | GenerarPagos.pdf | Credi10 |
| 86 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 011 - APIs Link de recaudos Credi10 STF GROUP S.A. | LinkDePagos.pdf | Credi10, Recaudo, Link de Recaudo, API |
| 87 | CREDI10 SOFTWARE PROPIO Cali , jueves 16 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | LinkDePagos.pdf | Credi10 |
| 88 | 1.1.1 Requerimiento Disponer API para suministrar información al link de recaudos de credi10 y aplicar el pago respectivo. | LinkDePagos.pdf | Credi10, Recaudo, Link de Recaudo, API |
| 89 | Se han establecido múltiples requerimientos donde cada uno presenta funcionalidades y procesos específicos que permitan la generación de información para link de recaudos. | LinkDePagos.pdf | Recaudo, Link de Recaudo |
| 90 | ● Crear parámetros de configuración para las APIs de Credi10 . | LinkDePagos.pdf | Credi10, API |
| 91 | ● Crear endpoint para consultar información del cliente y enviar al link de recaudos . | LinkDePagos.pdf | Recaudo, Link de Recaudo |
| 92 | ● Crear endpoint para procesar el pago del link de recaudos . | LinkDePagos.pdf | Recaudo, Link de Recaudo |
| 93 | 1.2 Detallar componentes existentes Para el desarrollo de los requerimientos se cuenta con 1 solución desarrollada en .Net Framework 4.8 llamada “Créditos”. | LinkDePagos.pdf | .NET |
| 94 | Se realiza creación del proyecto web API “ Creditos.Web.Servicios ” donde se establece el funcionamiento de los requerimientos correspondientes a Link de recaudo, botón ecommerce e integración B2C. | LinkDePagos.pdf | Recaudo, Ecommerce, Link de Recaudo, B2C, API |
| 95 | 08/06/2021 base de datos C10_Credi10NET de la solución. | LinkDePagos.pdf | Credi10, C10_Credi10NET |
| 96 | BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades 1.3.1 Diagrama de Componentes . | LinkDePagos.pdf | Credi10, C10_Credi10NET |
| 97 | Inténtalo de nuevo más tarde Oficina para recibir pagos web (Sucursal) Pagos 298 SMS - Mensaje Pago Realizado SMS Estimado cliente CREDI10 acabamos de recibir su pago por valor de ${0} con fecha de {1}. | LinkDePagos.pdf | Credi10, SMS |
| 98 | FORMATO DE DESARROLLO E INTEGRACIONES Integración Llamada Predictiva STF GROUP S.A. | Llamada predictiva.pdf | Predictiva |
| 99 | CREDI10 SOFTWARE PROPIO Cali, martes 6 de enero del 202 6 I NTRODUCCION La integración de Llamada Predictiva es un Worker Service desarrollado en .NET 8 que funciona como servicio de Windows, diseñado para automatizar la gestión de cargue de campañas telefónicas predictivas mediante el consumo de las Apis de la platafo... | Llamada predictiva.pdf | Credi10, .NET, Predictiva, API |
| 100 | DETALLE TÉCNICO Arquitectura General Tecnologías Utilizadas • .NET 8 - Framework principal • Quartz.NET - Programación de tareas (Jobs) • Microsoft.Extensions.Hosting - Servicio de fondo • Microsoft.Data.SqlClient - Conexióna base de datos • System.Text.Json - Serialización JSON • SpreadsheetLight - Generación de archi... | Llamada predictiva.pdf | .NET, Predictiva |
| 101 | Punto de entrada, configuración de servicios y programación de Jobs • WorkerLlamadaPredictiva.cs : | Llamada predictiva.pdf | Predictiva |
| 102 | Servicio principal de fondo Capa de Lógica de Negocio (BLL) • LlamadaPredictivaBLL.cs : | Llamada predictiva.pdf | Predictiva |
| 103 | Manejo de conexiones y consultas a SQL Server • EncriptarRequest.cs : | Llamada predictiva.pdf | SQL Server |
| 104 | Interfaz para encriptación Objetos de Transferencia de Datos (DTO) • AsignacionCarteraDTO.cs : | Llamada predictiva.pdf | Cartera |
| 105 | Datos de asignación de cartera • AgenteCarteraDTO.cs : | Llamada predictiva.pdf | Cartera |
| 106 | Solicitudes de campañas • ResponseApisWolkvox.cs : | Llamada predictiva.pdf | WOLKVOX, API |
| 107 | Respuestas de APIs Wolkvox • GestionPredictivaDTO.cs : | Llamada predictiva.pdf | WOLKVOX, Predictiva, API |
| 108 | Datos de gestión predictiva • TelefonoTelefonoRequestDTO.cs : | Llamada predictiva.pdf | Predictiva |
| 109 | Detención de campañas Integración Externa • WolkvoxConnection.cs : | Llamada predictiva.pdf | WOLKVOX |
| 110 | ORI - API - 00 1 Versión:001 Fecha: | Originacion_API_Datacredito.pdf | API |
| 111 | 08/ 11 /202 3 FORMATO DE DESARROLLO E INTEGRACIONES API DATACREDITO STF GROUP S.A. | Originacion_API_Datacredito.pdf | Datacredito, API |
| 112 | CREDI10 SOFTWARE PROPIO Cali , martes, 15 de septiembre de 2026 Código: | Originacion_API_Datacredito.pdf | Credi10 |
| 113 | En el presente documento se describe técnicamente como fue desarrollada la API que interviene en el proceso de o riginaci ó n de cupo. | Originacion_API_Datacredito.pdf | API |
| 114 | La API se conecta de manera segura al servicio proporcionado por Datacrédito Experian donde se obtendrá los datos crediticios de personas naturales según los datos de la solicitud de entrada. | Originacion_API_Datacredito.pdf | API |
| 115 | La API responde a las solicitudes de los usuarios proporcionando la información crediticia detallada yfácilmente interp r etable para quien realiza la solicitud. | Originacion_API_Datacredito.pdf | API |
| 116 | Este requerimiento se basa en la necesidad de acceder de manera eficiente a la información crediticia de individuos para tomar una decisión puntual en el proceso de originación en el aplicativo de credi10, teniendo en cuenta la escalabilidad que este pueda tener a futuro. | Originacion_API_Datacredito.pdf | Credi10 |
| 117 | 1.2 Detallar componentes existentes SOLUCION Datacredito.Integrator.Api Proyecto que proporciona un conjunto de servicios a otras aplicaciones a través de una interfaz de programación de aplicaciones (API). | Originacion_API_Datacredito.pdf | Datacredito, API |
| 118 | Datacredito.Integrator.BLL Proyecto que contiene las clases y métodos que implementan la lógica de negocio de la aplicación, esta biblioteca de clases será el encargado de consumir el servicio web, procesarlo y entregar la información para su posterior envió al usuario final. | Originacion_API_Datacredito.pdf | Datacredito |
| 119 | Este p royecto se integra con el proyecto API y el proyecto DAL. | Originacion_API_Datacredito.pdf | API |
| 120 | Datacredito.Integrator.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_Datacredito de la solución Web Service Produccion Historia de crédito + URL CONSUMO: | Originacion_API_Datacredito.pdf | Datacredito, C10_Datacredito |
| 121 | https://servicesesb.datacredito.com .co/wss/dhws3/services/DHServicePlus Código: | Originacion_API_Datacredito.pdf | Datacredito, S3 |
| 122 | ORI - API - 00 1 Versión:001 Fecha: | Originacion_API_Inspektor.pdf | API |
| 123 | 08/ 11 /202 3 FORMATO DE DESARROLLO E INTEGRACIONES API IN SPEKTOR STF GROUP S.A. | Originacion_API_Inspektor.pdf | API |
| 124 | CREDI10 SOFTWARE PROPIO Cali , martes, 15 de septiembre de 2026 Código: | Originacion_API_Inspektor.pdf | Credi10 |
| 125 | En el presente documento se describe técnicamente como fue desarrollada la API que interviene en el proceso de o riginaci ó n de cupo para Credi 10. | Originacion_API_Inspektor.pdf | API |
| 126 | a) Consumo del servicio web Inspektor: | Originacion_API_Inspektor.pdf | Inspektor |
| 127 | La API se conecta de manera segura al servicio proporcionado por INSPEKTOR d onde se obtendrá información de los clientes en listas que ellos administran . | Originacion_API_Inspektor.pdf | Inspektor, API |
| 128 | La API responde a las solicitudes de los usuarios proporcionando la información de si el cliente se encuentra o no en listas restrictivas. | Originacion_API_Inspektor.pdf | API |
| 129 | 1.2 Detallar componentes existentes SOLUCION Inspektor .Integrator.Api Proyecto que proporciona un conjunto de servicios a otras aplicaciones a través de una interfaz de programación de aplicaciones (API). | Originacion_API_Inspektor.pdf | Inspektor, API |
| 130 | Inspektor .Integrator.BLL Proyecto que contiene las clases y métodos que implementan la lógica de negocio de la aplicación, esta biblioteca de clases será el encargado de consumir el servicio web, procesarlo y entregar la información para su posterior envió al usuario final. | Originacion_API_Inspektor.pdf | Inspektor |
| 131 | Este p royecto se integra con el proyecto API y el proyecto DAL. | Originacion_API_Inspektor.pdf | API |
| 132 | Inspektor .Integrator.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_ Inspektor de la solución Web Service Inspektor URL CONSUMO: | Originacion_API_Inspektor.pdf | Inspektor |
| 133 | https://inspektor.datalaft.com:2055/ WSInspektor.asmx URL WSDL: | Originacion_API_Inspektor.pdf | Inspektor |
| 134 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES Originacion Aplicación Admin STF GROUP S.A. | Originacion_Aplicacion_ADMIN.pdf | Originacion |
| 135 | CREDI10 SOFTWARE PROPIO Cali , Viernes, 17 de noviembre de 2023 Código:FT - DG - 00 2 Versión:001 Fecha: | Originacion_Aplicacion_ADMIN.pdf | Credi10 |
| 136 | Capturar los datos básicos del cliente para la validación del ejercicio 2. | Originacion_Aplicacion_ADMIN.pdf | Captura |
| 137 | Realizar validaciones de Inspektor, Datacredito 3. | Originacion_Aplicacion_ADMIN.pdf | Inspektor, Datacredito |
| 138 | Creditos.BLL • Prospectos.cs • CuposController.cs • OriginacionController.cs • ServiciosController.cs • InspektorServices.cs • CentralesServices.cs • NotificationController.cs • SecurityUtil.cs • RestUtil.cs Clases implementadas para realizar las consultas a DataCredito, Inspecktor, validaciones de identidad como: | Originacion_Aplicacion_ADMIN.pdf | Inspektor, Datacredito, Originacion |
| 139 | Creditos.DTO • CentralesRequest • CentralesLoginRequest • InspektorLoginRequest • InspektorRequest • SolicitudFormularioDTO • AceptacionReferenciasDTO • HabeasDataDTO • PagareDTO Clases de transferencia de datos StyleLoader.css , Estilos pantalla carga Código:FT - DG - 00 2 Versión:001 Fecha: | Originacion_Aplicacion_ADMIN.pdf | Inspektor |
| 140 | BASE DE DATOS C10_Credi10NET.dbo.tbl_calificacion Tablas C10_Credi10NET.dbo.tbl_cliente_correos Tablas C10_Credi10NET.dbo.tbl_cliente_direccio nes Tablas C10_Credi10NET.dbo.tbl_cliente_fotos Tablas C10_Credi10NET.dbo.tbl_cliente_telefono s Tablas C10_Credi10NET.dbo.tbl_clientes Tablas C10_Credi10NET.dbo.tbl_cupos Tabla... | Originacion_Aplicacion_ADMIN.pdf | Credi10, Inspektor, Datacredito, C10_Credi10NET, C10_Inspektor, C10_Datacredito, Foto |
| 141 | https://app.diagrams.net/ https://www.youtube.com/watch?app=des ktop&v=JF7bH5Xo6ys https://www.ionos.es/digitalguide/paginas - web/desarrollo - web/diagrama - de - componentes/ Código:FT - DG - 00 2 Versión:001 Fecha: | Originacion_Aplicacion_ADMIN.pdf | .NET |
| 142 | • Tbl_parametros, Campo Key, Valor EncendidoInspektor: | Originacion_Aplicacion_ADMIN.pdf | Inspektor |
| 143 | • Tbl_parametros, Campo Key, Valor EncendidoSMS: | Originacion_Aplicacion_ADMIN.pdf | SMS |
| 144 | Sirve para encender o apagar el envió de sms con el otp de aceptación del cupo Asi: | Originacion_Aplicacion_ADMIN.pdf | SMS |
| 145 | ”Para continuar con la solicitud su otp es el siguiente {0}.” si esta en True, se notifica por sms, si esta en false no. | Originacion_Aplicacion_ADMIN.pdf | SMS |
| 146 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES ORIGINACION CROSSCORE STF GROUP S.A. | Originacion_CrossCore.pdf | CrossCore, Originacion |
| 147 | CREDI10 SOFTWARE PROPIO Cali , viernes , 16 de febrero de 202 4 Código:FT - DG - 00 2 Versión:001 Fecha: | Originacion_CrossCore.pdf | Credi10 |
| 148 | Capturar los datos básicos del cliente 2. | Originacion_CrossCore.pdf | Captura |
| 149 | Realizar proceso de Aceptación de tratamiento de datos con la captura de fotos al documento de identidad y una selfie. | Originacion_CrossCore.pdf | Captura, Foto |
| 150 | Realizar validaciones de Inspektor, Datacredito , Fecha de Expedición de documento, Correo Electrónico, Celular 4. | Originacion_CrossCore.pdf | Inspektor, Datacredito |
| 151 | Crosscore • Controladores o Registro Controller.cs o AceptacionCupoController.cs • Vistas o Registro.cshtml o CapturaFotos.cshtml o ValidarTokenAceptacion.cshtml o HabeasData.cshtml Clases y vistas implementadas para cumplir con el propósito registrar un prospecto, validar mediante el servicio de Crosscore , crear y ac... | Originacion_CrossCore.pdf | CrossCore, Captura, Foto |
| 152 | Creditos.BLL • Prospectos.cs • CuposController.cs • OriginacionController.cs • ServiciosController.cs • InspektorServices.cs • CentralesServices.cs • NotificationController.cs • SecurityUtil.cs • RestUtil.cs Clases implementadas para realizar las consultas a DataCredito, Inspecktor, validaciones de identidad como: | Originacion_CrossCore.pdf | Inspektor, Datacredito, Originacion |
| 153 | 08/06/2021 Creditos.DTO • CentralesRequest • CentralesLoginRequest • InspektorLoginRequest • InspektorRequest • SolicitudFormularioDTO • AceptacionReferenciasDTO • HabeasDataDTO • PagareDTO Clases de transferencia de datos StyleLoader.cs s Estilos pantalla carga StylesRegistro.css Estilos vista registro AutoNumeric Lib... | Originacion_CrossCore.pdf | Inspektor |
| 154 | BASE DE DATOS C10_Credi10NET.dbo. | Originacion_CrossCore.pdf | Credi10, C10_Credi10NET |
| 155 | tbl_calificacion Tablas C10_Credi10NET.dbo. | Originacion_CrossCore.pdf | Credi10, C10_Credi10NET |
| 156 | tbl_cliente_correos Tablas C10_Credi10NET.dbo. | Originacion_CrossCore.pdf | Credi10, C10_Credi10NET |
| 157 | tbl_cliente_direcciones Tablas C10_Credi10NET.dbo. | Originacion_CrossCore.pdf | Credi10, C10_Credi10NET |
| 158 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 004 - Módulo_Cartera STF GROUP S.A. | ProcesoCorteCartera.pdf | Cartera |
| 159 | CREDI10 SOFTWARE PROPIO C ali , lunes 12 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | ProcesoCorteCartera.pdf | Credi10 |
| 160 | 1.1.1 Requerimiento Realizar los procesos saldos al corte, presupuesto, facturación , estados de cuenta y creación del reporte de facturas en las fechas adecuadas para los cortes establecidos por credi10. | ProcesoCorteCartera.pdf | Credi10 |
| 161 | 08/06/2021 1.2 Detallar componentes existentes SOLUCION CarteraWindowsServices Proyecto de tipo servicio de Windows que se ejecuta automáticamente en fechas establecidas que realiza el proceso de cada corte en credi10. | ProcesoCorteCartera.pdf | Credi10, Cartera |
| 162 | Quartz.NET Librería que ejecuta tareas en segundo plano en una hora y fecha determinada. | ProcesoCorteCartera.pdf | .NET |
| 163 | BASE DE DATOS C10_ Credi10_NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades Código:FT - DG - 00 2 Versión:001 Fecha: | ProcesoCorteCartera.pdf | Credi10 |
| 164 | 1.3.3 Parametrizaciones Descripción Grupo Valor Correo origen estado cuenta Email credi10estadocuenta@cr edi10.com.co Valor IdEmpresa para crear la facturación Cartera 1 Correo al que le enviara el reporte de la facturación creada Facturacion Correo Ruta archivos de reportes de facturación Facturacion \ \ COATLANTA \ C... | ProcesoCorteCartera.pdf | Credi10, Cartera, Coatlanta, Email |
| 165 | 08/06/2021 Url Estados de cuenta clientes EstadosDeCuenta https://www.credi10.com. | ProcesoCorteCartera.pdf | Credi10 |
| 166 | co/EstadosCuenta/Estad oCuentaPersonalizado/ Url Facturas clientes Facturacion https://www.credi10.com. | ProcesoCorteCartera.pdf | Credi10 |
| 167 | co/Facturas/FacturaPers onalizada/ Parámetro WS SIESA - WSDL FacturacionElectronica http://192.168.0. | ProcesoCorteCartera.pdf | Siesa |
| 168 | xxx /WSU NOEE/WSUNOEE.asmx Parámetro WS SIESA - Usuario FacturacionElectronica interfaz_ecommerce Parámetro WS SIESA - Clave FacturacionElectronica LvH4GYi3 Parámetro WS SIESA - Nombre de Conexión FacturacionElectronica STFColombia Notas de Reclasificación de Saldos FacturacionElectronica NCR Cantidad UVT Mínimo Factur... | ProcesoCorteCartera.pdf | Siesa, UnoEE, UNOEE, Ecommerce |
| 169 | 08/06/2021 porque no se ha enviado la facturacion porque no se ha enviado la facturación del corte HTML para envió de la factura POS al cliente Email Html HTML para reporte de facturacion creada Email Html HTML para envió estado de cuenta link Email Html 1.3.4 Proceso • Proceso automático en cada corte Para cumplir con... | ProcesoCorteCartera.pdf | Cartera, Email |
| 170 | 2269 Acopi - Yumbo SOLICITUD DE OFERTA (RFP) No: | RFP_CREDI10_2_0.pdf | RFP |
| 171 | 00 1 PROYECTO DE CREDI10 2.0 STF GROUP S.A. | RFP_CREDI10_2_0.pdf | Credi10 |
| 172 | 2269 Acopi - Yumbo CAPITULO 1 INSTRUCCIONES A LOS OFERENTES 1. | RFP_CREDI10_2_0.pdf | API |
| 173 | quien para efectos del presente documento se denominará LA EMPRESA , tiene el gusto de invitarlo a participar en la convocatoria que se llevará a cabo para la presentación de propuestas para “ PROYECTO CREDI10 2.0 ” 1.2 OBJETO DE LA SOLICITUD Seleccionar el proponente que ofrezca las mejores condiciones para el proyect... | RFP_CREDI10_2_0.pdf | Credi10 |
| 174 | 1.3 ALCANCE La propuesta presentada por el oferente debe contemplar el cumplimiento a cabalidad de los requerimientos solicitados por LA EMPRESA para “ PROYECTO CREDI10 2.0 ”. | RFP_CREDI10_2_0.pdf | Credi10 |
| 175 | 2269 Acopi - Yumbo CAPITULO 2 ELABORACIÓNY PRESENTACIÓN DE LA OFERTA 1. | RFP_CREDI10_2_0.pdf | API |
| 176 | 1 de Octubre de 202 6 , hora y fecha límites para el recibo de las mismas, sin importar si la entrega se hace física ovía email . | RFP_CREDI10_2_0.pdf | Email |
| 177 | Concepto Descripción Necesidad del proyecto Credi10 cuenta actualmente con un ecosistema tecnológico compuesto por aplicaciones, servicios Windows, APIs, integradores, bases de datos, componentes de procesamiento, plataformas web ymúltiples integraciones con sistemas internos y proveedores externos . | RFP_CREDI10_2_0.pdf | Credi10, integrador, API |
| 178 | La arquitectura actual presenta componentes desarrollados sobre diferentes generaciones tecnológicas, incluyendo soluciones basadas en .NET Framework 4.8.1, .NET 8, .NET Core 3.1, Node.js y React, entre otras tecnologías. | RFP_CREDI10_2_0.pdf | .NET, Node.js, React |
| 179 | Adicionalmente, la plataforma mantiene dependencias e integraciones con sistemas y servicios como Cegid/UnoEE, VTEX, PayU, Datacrédito, Inspector, Jumio, CrossCore, Wolkvox, B2Chat, Icommarketing, Pentaho , Numrot y demás componentes identificados durante el diagnóstico. | RFP_CREDI10_2_0.pdf | UnoEE, UNOEE, CrossCore, PayU, WOLKVOX, VTEX, Pentaho, Numrot, B2CHAT, ICOMMARKETING, B2C |
| 180 | 2269 Acopi - Yumbo En este contexto, se requiere realizar un assessment integral de la arquitectura tecnológica actual de Credi10, con el propósito de identificar riesgos, deuda técnica, obsolescencia tecnológica, oportunidades de optimización, restricciones de escalabilidad, disponibilidad, seguridad, mantenibilidad,... | RFP_CREDI10_2_0.pdf | Credi10 |
| 181 | A rquitectura tecnológica objetivo denominada Credi10 2.0 , que incorpore las oportunidades de mejora, hallazgos y recomendaciones identificadas durante el diagnóstico, orientada a fortalecer la escalabilidad, disponibilidad, seguridad, rendimiento, mantenibilidad y sostenibilidad tecnológica de la plataforma. | RFP_CREDI10_2_0.pdf | Credi10 |
| 182 | Gestionar todas las APIs de manera Centralizada 19 5.3. | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | API |
| 183 | Objetivo del Documento Evaluar el contexto actual de Studio F para analizar las oportunidades de mejora y en su arquitectura, donde las soluciones WSO2 API Platform y WSO2 Integration Platform pueden ayudar a modernizar su ecosistema, además de proporcionar beneficios de gobernanza y gestión para las API e integracione... | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | WSO2, Studio F, API |
| 184 | Contexto de Negócio Studio F cuenta con una arquitectura fragmentada y un ecosistema de sistemas y aplicaciones desactualizados, compuestos por más de 150 aplicaciones .NET y 200 bases de datos con informaciones duplicadas e inconsistentes. | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | .NET, Studio F |
| 185 | Actualmente, el ecosistema depende de integraciones "punto a punto" y procesos batch (archivos planos) hacia su ERP Siesa. | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | Siesa |
| 186 | Para revertir esta situación, Studio F busca centralizar y estandarizar sus integraciones bajo un modelo de gobernanza clara, con el fin de eliminar la duplicidad de funciones y mejorar la eficiencia operativa, reduciendo significativamente el Time - to - Market y la carga operativa manual. | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | Studio F |
| 187 | ○ ERP Siesa - las integraciones con su ERP sónrígidas, mediante archivos planos y un único WebServices para todas las operaciones. | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | Siesa |
| 188 | ● Falta de Gobernanza y Control ○ Varias aplicaciones .NET desarrolladas de forma desordenada para resolver problemas puntuales y muchas de ellas con funciones duplicadas . | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | .NET |
| 189 | Arquitectura Actual Hoy, el escenario de Studio F puede ser representado de acuerdo con los diagramas abajo: | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | Studio F |
| 190 | # Origen Destino Protocolo Descripción 1 Devoluciones Automáticas VTEX JSON/HTTP Consulta Devoluciones y Crea GiftCards 2 Devoluciones Automáticas Siesa Unoee XML/SOAP Crea Notas de Crédito 3 Gestor de Pedidos Siesa Unoee XML/SOAP Crea RQI 4 Auto Registro Siesa Unoee XML/SOAP Fideliza Cliente 5 Generic Transfer WMS Sie... | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | Credi10, Siesa, UnoEE, UNOEE, VTEX, Pentaho, Numrot, Ecommerce, SMS, Email |
| 191 | Para el API Manager, se ha seleccionado el Patrón 1 (Pattern 1: | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | API |
| 192 | All - in - One High Availability), el cual consta de dos nodos idénticos que integran todos los componentes del API Manager: | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | API |
| 193 | API Gateway y Control Plane (API Publisher, Developer Portal, Traffic Manager y Key Manager). | WSO2 y Studio F - Assessment Mayo2026-Final.pdf | Portal, API |

**Total de hechos clave trazables:** 193.

