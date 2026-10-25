# ProcesoCorteCartera.pdf

| Campo | Valor |
| --- | --- |
| id | `procesocortecartera` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 4672023 |
| longitud raw | 47426 |
| longitud limpia | 44100 |
| ratio de cobertura (crudo, legado) | 0.00944 |
| caracteres de texto util | 23746 |
| texto util real (palabras / bytes extraidos) | 53.85% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `c5058d4fb7bac933c6b1b535b4a095bbedcd89534f0faf774ba86e59d83cf281` |

## Resumen jerarquico

- Documento 'ProcesoCorteCartera.pdf' (PDF): 44100 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 53.85%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 004 - Módulo_Cartera STF GROUP S.A. INFORMATICA – Py. CREDI1...
- Seccion 2: o s casos de pruebas un itarias realizadas a la solución . NOTA: El desarrollo de cualquier solución de requerimiento debe seguir los estándares de desarrollo q...
- Seccion 3: o plano en una hora y fecha determinada. BASE DE DATOS C10_ Credi10_NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades Código:FT - DG - 00 2 V...
- Seccion 4: i10.com. co/Facturas/FacturaPers onalizada/ Parámetro WS SIESA - WSDL FacturacionElectronica http://192.168.0. xxx /WSU NOEE/WSUNOEE.asmx Parámetro WS SIESA - U...
- Seccion 5: ta para el corte Ya se envió estados de cuenta anteriormente Estados de Cuenta El proceso de envió del estado de cuenta ya se realizó anteriormente No se puede...
- Seccion 6: da corte como una tarea en segundo plano. Para esto en el proyecto se utilizó la librería Quartz.NET que se encarga de ejecutar tareas en segundo plano en un mo...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 004 - Módulo_Cartera STF GROUP S.A. | Cartera |
| 2 | CREDI10 SOFTWARE PROPIO C ali , lunes 12 de febrero del 2024 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 |
| 3 | 1.1.1 Requerimiento Realizar los procesos saldos al corte, presupuesto, facturación , estados de cuenta y creación del reporte de facturas en las fechas adecuadas para los cortes establecidos por credi10. | Credi10 |
| 4 | 08/06/2021 1.2 Detallar componentes existentes SOLUCION CarteraWindowsServices Proyecto de tipo servicio de Windows que se ejecuta automáticamente en fechas establecidas que realiza el proceso de cada corte en credi10. | Credi10, Cartera |
| 5 | Quartz.NET Librería que ejecuta tareas en segundo plano en una hora y fecha determinada. | .NET |
| 6 | BASE DE DATOS C10_ Credi10_NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 |
| 7 | 1.3.3 Parametrizaciones Descripción Grupo Valor Correo origen estado cuenta Email credi10estadocuenta@cr edi10.com.co Valor IdEmpresa para crear la facturación Cartera 1 Correo al que le enviara el reporte de la facturación creada Facturacion Correo Ruta archivos de reportes de facturación Facturacion \ \ COATLANTA \ C... | Credi10, Cartera, Coatlanta, Email |
| 8 | 08/06/2021 Url Estados de cuenta clientes EstadosDeCuenta https://www.credi10.com. | Credi10 |
| 9 | co/EstadosCuenta/Estad oCuentaPersonalizado/ Url Facturas clientes Facturacion https://www.credi10.com. | Credi10 |
| 10 | co/Facturas/FacturaPers onalizada/ Parámetro WS SIESA - WSDL FacturacionElectronica http://192.168.0. | Siesa |
| 11 | xxx /WSU NOEE/WSUNOEE.asmx Parámetro WS SIESA - Usuario FacturacionElectronica interfaz_ecommerce Parámetro WS SIESA - Clave FacturacionElectronica LvH4GYi3 Parámetro WS SIESA - Nombre de Conexión FacturacionElectronica STFColombia Notas de Reclasificación de Saldos FacturacionElectronica NCR Cantidad UVT Mínimo Factur... | Siesa, UnoEE, UNOEE, Ecommerce |
| 12 | 08/06/2021 porque no se ha enviado la facturacion porque no se ha enviado la facturación del corte HTML para envió de la factura POS al cliente Email Html.... | Email |

