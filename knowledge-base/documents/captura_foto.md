# Captura Foto.pdf

| Campo | Valor |
| --- | --- |
| id | `captura_foto` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 846421 |
| longitud raw | 14899 |
| longitud limpia | 13318 |
| ratio de cobertura (crudo, legado) | 0.01573 |
| caracteres de texto util | 8798 |
| texto util real (palabras / bytes extraidos) | 66.06% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `694c1d2001962cbaf2d5f203ee2ca371a98e11f591d7b7fedea032f639d0e9e7` |

## Resumen jerarquico

- Documento 'Captura Foto.pdf' (PDF): 13318 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 66.06%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES CAPTURA FOTO STF GROUP S.A. INFORMATICA – Py. CREDI10 SOFTWARE PROPIO...
- Seccion 2: e pruebas un itarias realizadas a la solución . NOTA: El desarrollo de cualquier solución de requerimiento debe seguir los estándares de desarrollo que define A...
- Seccion 3: sión:001 Fecha: 08/06/2021 Creditos.Web. Admin • Controladores o Desembolso Controller.cs • Vistas o Index.cshtml o Create.cshtml o Camara .cshtml Clases y vist...
- Seccion 4: et/ https://www.youtube.com/watch?app=desktop&v=JF7bH5Xo6ys https://www.ionos.es/digitalguide/paginas - web/desarrollo - web/diagrama - de - componentes/ Código...
- Seccion 5: la foto. Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 En el proceso de captura de fotos, el input relevante es de tipo texto #NumeroDocumento , donde se...
- Seccion 6: retorna un objeto OperationResponse . Código:FT - DG - 00 2 Versión:001 Fecha: 08/06/2021 El endpo i nt ValidacionInicialDesembolsar a través de DesembolsosServ...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | 08/06/2021 FORMATO DE DESARROLLO E INTEGRACIONES CAPTURA FOTO STF GROUP S.A. | Captura, Foto |
| 2 | CREDI10 SOFTWARE PROPIO Cali , lunes , 29 de enero de 202 4 Código:FT - DG - 00 2 Versión:001 Fecha: | Credi10 |
| 3 | 1.1.1 Requerimiento Validar que el cliente tenga foto, si no , r ealizar la captura de la foto del cliente en el proceso antes de ingresar al formulario, también permitir recaptura en el formulario . | Captura, Foto |
| 4 | 1.1.2 Flujo del Proceso Index.cshtml Se ingresa la información de la tienda y el cliente Camara.cshtml Se presiona en capturar para visualizar la foto que se captura en la parte derecha, si la foto sale mal puede volver a dar en capturar para actualizar la foto y la visualización Camara.cshtml Se presiona en guardar pa... | Captura, Foto |
| 5 | Admin • Controladores o Desembolso Controller.cs • Vistas o Index.cshtml o Create.cshtml o Camara .cshtml Clases y vista implementada para la captura de la foto . | Captura, Foto |
| 6 | Creditos.BLL • Desembolsos Service s .cs Clase implementada para realizar la validación de cliente tiene foto . | Foto |
| 7 | Bootstrap Librería para el front v5.1.3 BASE DE DATOS tbl_clientes Tabla tbl_cliente_fotos Tabla Código:FT - DG - 00 2 Versión:001 Fecha: | Foto |
| 8 | https://app.diagrams.net/ https://www.youtube.com/watch?app=desktop&v=JF7bH5Xo6ys https://www.ionos.es/digitalguide/paginas - web/desarrollo - web/diagrama - de - componentes/ Código:FT - DG - 00 2 Versión:001 Fecha: | .NET |
| 9 | ‘ClienteSinFoto’, ‘FotoGuardada’, ‘FotoNoGuardada’ - Los anteriores registros son los mensajes que se muestran en el proceso de captura de la foto. | Captura, Foto |
| 10 | 1.3.4 Proceso La generación del crédito inicia con Index.cshtml del controlador Desembolso Controller.cs , en esta vista se lan zan una serie de validaciones con el consumo de un endpoint incluida la validación de la existencia de al menos una foto del cliente . | Foto |
| 11 | Index.cshtml tiene los inputs correspondientes a la tienda , el cliente y adicionalmente contiene un modal #mdCamara que es el que permite visualizar la vista Camara.cshtml para realizar la cap tura de la foto. | Foto |
| 12 | 08/06/2021 En el proceso de captura de fotos, el input relevante es de tipo texto #NumeroDocumento , donde se ingresa el número de documento del cliente. | Captura, Foto |

