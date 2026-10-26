# GenerarPagos.pdf

| Campo | Valor |
| --- | --- |
| id | `generarpagos` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 4933401 |
| longitud raw | 123806 |
| longitud limpia | 80172 |
| ratio de cobertura (crudo, legado) | 0.01625 |
| caracteres de texto util | 48552 |
| texto util real (palabras / bytes extraidos) | 60.56% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `77dac0283c54034229f645ac673a18e4351eb8425386e166b4fce46fe7759a79` |

## Resumen jerarquico

- Documento 'GenerarPagos.pdf' (PDF): 80172 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 60.56%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: Código:FT - SL - 00 3 Versión:001 Fecha: 21 / 12 /202 3 FORMATO DE DESARROLLO E INTEGRACIONES FT - SL - 003 - M ódulo_Pago STF GROUP S.A. INFORMATICA – Py. CRED...
- Seccion 2: 21 / 12 /202 3 1. DETALLE TECNICO Ap 1.1 Descripción del Requerimiento: 1.1.1 Requerimiento Realizar todo el proceso de pagos de los créditos realizados con el...
- Seccion 3: Tipo SOLUCION Creditos.Web.Admin Controladores y vistas implementadas para cumplir con el propósito de informar el valor del pago y recibir el valor que quieran...
- Seccion 4: ades 1.3.1 Diagrama de Arquitectura Usar para estos manuales, mejor diagramas de componentes ya que por ser funcionalidades internas los diagramas de arquitectu...
- Seccion 5: o para la consignación. Banco WOMPI Medio de pagos permitidos para registrar el movimiento del RC. MedioPago TX Medio de pagos permitidos para registrar el movi...
- Seccion 6: alor del pago ingresado Pagos El valor ingresado supera el límite del recaudo permitido Agregar el listado de los parametros generales que se usan en el proceso...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | CREDI10 SOFTWARE PROPIO Cali , martes, 15 de septiembre de 2026 Código:FT - SL - 00 3 Versión:001 Fecha: | Credi10 |
| 2 | 1.1.1 Requerimiento Realizar todo el proceso de pagos de los créditos realizados con el cupo de credi10, garantizando el adecuado cobro de los diferentes rubros correspondientes a mora, aval, interés, los impuestos correspondientes y el capital. | Credi10, API |
| 3 | FT - SL - 003 - Módulo_Pago - V5 1.1.2 Flujo del Proceso • Pago en tienda Agregar mockup o capturas del flujo del proceso Código:FT - SL - 00 3 Versión:001 Fecha: | Captura |
| 4 | Creditos.DAL Proyecto encargado de tener el acceso y la interaccióna la base de datos C10_ Credi10NET de la solución . | Credi10 |
| 5 | BASE DE DATOS C10_Credi10NET Tablas y Procedimientos almacenados 1.3 Detallar funcionalidades 1.3.1 Diagrama de Arquitectura Usar para estos manuales, mejor diagramas de componentes ya que por ser funcionalidades internas los diagramas de arquitectura dan una visualizacion muy general Opcional usar: | Credi10, C10_Credi10NET |
| 6 | https://app.diagrams.net/ https://www.youtube.com/watch?app=desktop&v=JF7bH5Xo6ys https://www.ionos.es/digitalguide/paginas - web/desarrollo - web/diagrama - de - componentes/ Código:FT - SL - 00 3 Versión:001 Fecha: | .NET |
| 7 | TipoPago Online Mensaje de las tiendas que ya alcanzaron su límite de recaudo Pagos Lo sentimos, ya se alcanzó el límite de recaudo Mensaje al ingresar un valor no permitido para el pago Pagos El valor del pago está fuera del rango permitido Mensaje mostrado cuando el valor del pago ingresado Pagos El valor ingresado s... | Recaudo |
| 8 | 21 / 12 /202 3 supera el límite de recaudo de la empresa aliada. | Recaudo |
| 9 | Por favor repite el proceso de consulta Oficina para recibir pagos web Pagos 298 SMS - Mensaje Pago Realizado SMS Estimado cliente CREDI10 acabamos de recibir su pago por valor de ${0} con fecha de {1}. | Credi10, SMS |
| 10 | 1.3.4 Proceso Cuando un usuario inicia sesión en la aplicación web de credi10 este va a tener un perfil asignado el cual le concederá permisos para ver y realizar diferentes operaciones dentro del sistema. | Credi10 |
| 11 | 21 / 12 /202 3 Esta vista tiene como ruta https://www.credi10.com.co/Pagos , si se intenta acceder a ella sin iniciar sesión antes será redirigido a la vista de Login Login (credi10.com.co) y si ya ha iniciado sesión y el usuario no tiene los permisos adecuados e intentará acceder directamente por medio de l link , el... | Credi10 |
| 12 | • Pagos En Tienda Al ingresar al índex de pagos en tienda ( https://www.credi10.com.co/Pagos ) llamara al método ValidateSession explicado aquí , que garantiza si el usuario tiene permisos de ingresar al recurso, obtiene y valida la dirección de la ip de conexión para saber si es una tienda específica para que cuando c... | Credi10 |

