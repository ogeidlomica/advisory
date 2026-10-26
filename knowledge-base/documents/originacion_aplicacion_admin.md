# Originacion_Aplicacion_ADMIN.pdf

| Campo | Valor |
| --- | --- |
| id | `originacion_aplicacion_admin` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 874196 |
| longitud raw | 17886 |
| longitud limpia | 16203 |
| ratio de cobertura (crudo, legado) | 0.01853 |
| caracteres de texto util | 11415 |
| texto util real (palabras / bytes extraidos) | 70.45% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `1e1e01d8565d388f0b33fd58f37cc11e3c84fb432976828a3ecf6387d64b2209` |

## Resumen jerarquico

- Documento 'Originacion_Aplicacion_ADMIN.pdf' (PDF): 16203 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 70.45%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES Originacion Aplicación Admin STF GROUP S.A. INFORMATICA – Py. CREDI10...
- Seccion 2: . Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 1. DETALLE TECNICO 1.1 Descripción del Requerimiento: Realizar la primera parte del proceso de inscripción...
- Seccion 3: • ServiciosController.cs • InspektorServices.cs • CentralesServices.cs • NotificationController.cs • SecurityUtil.cs • RestUtil.cs Clases implementadas para rea...
- Seccion 4: n Tablas C10_Credi10NET.dbo.tbl_cliente_correos Tablas C10_Credi10NET.dbo.tbl_cliente_direccio nes Tablas C10_Credi10NET.dbo.tbl_cliente_fotos Tablas C10_Credi1...
- Seccion 5: Componentes 1.3.2 MER Usar para estos manuales, mejor diagramas de componentes ya que por ser funcionalidades internas los diagramas de arquitectura dan una vis...
- Seccion 6: , se notifica por sms, si esta en false no. • Tbl_parametros, Campo Key, Valor EncendidoValidacionCorreo: Sirve para encender o apagar la validación del correo...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES Originacion Aplicación Admin STF GROUP S.A. | Originacion |
| 2 | CREDI10 SOFTWARE PROPIO Cali , Viernes, 17 de noviembre de 2023 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 |
| 3 | Capturar los datos básicos del cliente para la validación del ejercicio 2. | Captura |
| 4 | Realizar validaciones de Inspektor, Datacredito 3. | Inspektor, Datacredito |
| 5 | Creditos.BLL • Prospectos.cs • CuposController.cs • OriginacionController.cs • ServiciosController.cs • InspektorServices.cs • CentralesServices.cs • NotificationController.cs • SecurityUtil.cs • RestUtil.cs Clases implementadas para realizar las consultas a DataCredito, Inspecktor, validaciones de identidad como: | Inspektor, Datacredito, Originacion |
| 6 | Creditos.DTO • CentralesRequest • CentralesLoginRequest • InspektorLoginRequest • InspektorRequest • SolicitudFormularioDTO • AceptacionReferenciasDTO • HabeasDataDTO • PagareDTO Clases de transferencia de datos StyleLoader.css , Estilos pantalla carga Código:FT - DG - 00 2 Versión:001 Fecha: | Inspektor |
| 7 | BASE DE DATOS C10_Credi10NET.dbo.tbl_calificacion Tablas C10_Credi10NET.dbo.tbl_cliente_correos Tablas C10_Credi10NET.dbo.tbl_cliente_direccio nes Tablas C10_Credi10NET.dbo.tbl_cliente_fotos Tablas C10_Credi10NET.dbo.tbl_cliente_telefono s Tablas C10_Credi10NET.dbo.tbl_clientes Tablas C10_Credi10NET.dbo.tbl_cupos Tabla... | Credi10, Inspektor, Datacredito, C10_Credi10NET, C10_Inspektor, C10_Datacredito, Foto |
| 8 | https://app.diagrams.net/ https://www.youtube.com/watch?app=des ktop&v=JF7bH5Xo6ys https://www.ionos.es/digitalguide/paginas - web/desarrollo - web/diagrama - de - componentes/ Código:FT - DG - 00 2 Versión:001 Fecha: | .NET |
| 9 | • Tbl_parametros, Campo Key, Valor EncendidoInspektor: | Inspektor |
| 10 | • Tbl_parametros, Campo Key, Valor EncendidoSMS: | SMS |
| 11 | Sirve para encender o apagar el envió de sms con el otp de aceptación del cupo Asi: | SMS |
| 12 | ”Para continuar con la solicitud su otp es el siguiente {0}.” si esta en True, se notifica por sms, si esta en false no. | SMS |

