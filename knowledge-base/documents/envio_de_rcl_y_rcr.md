# Envio de RCL y RCR.pdf

| Campo | Valor |
| --- | --- |
| id | `envio_de_rcl_y_rcr` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 330050 |
| longitud raw | 175952 |
| longitud limpia | 161351 |
| ratio de cobertura (crudo, legado) | 0.48887 |
| caracteres de texto util | 6668 |
| texto util real (palabras / bytes extraidos) | 4.13% |
| banda de cobertura (por texto util real) | baja |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib+regex (capa de texto PDF) |
| sha256 | `8a5b0becf5b4a0f87f2450a4da700c1fda0561abb55d45217cfb0d7c8a31e5c7` |

## Resumen jerarquico

- Documento 'Envio de RCL y RCR.pdf' (PDF): 161351 caracteres limpios extraidos (zlib+regex), texto util real 4.13%, banda 'baja', clasificacion [VERIFIED-FACT].
- Seccion 1: FORM A TO DE DESARRO LL O E INTEGRACIONES I ntegrac i ón en vi ó de RCLy RCR a Un oE STF GROUP S . A . IN FORM A TICA Py . es-MX CREDI 10 SOF TWA RE PROPIO C al...
- Seccion 2: e lo s envíos es-CL es-CL es-CL 3 es-CL - Cr earp roce so que se e jecu te au to m á tic amen te cada d í a 4 del mes , donde se cree un documento de tip o RCL...
- Seccion 3: u entas inf luye en f358 _ id_ med ios_ p ago es-CL es-CL es-CL es-CL es-CL tb l_ c ompr obantes . ba nc o_ c on s igna c ion tb l_ c omprobantes . t ipo_ trans...
- Seccion 4: na cio n es-CL es-CL es-CL es-CL 7 es-CL - Ag reg ar co lu mna de re cibo _ unoee en tbl_ca rgues _ pagos_ deta ll e , en el cu al se co loq ue ca da con se cut...
- Seccion 5: L es-CL E jemplo de p la no es-CL es-CL RC L PayU es-CL es-CL 0000002035700020010001 RC L000314832024053010 20240530C REDI1 0 COP + 000003130808880 .0000 CO P +...
- Seccion 6: 240715C REDI1 0 COP + 000000000153000 .0000 CO P + 000000000153000 .0000000699 110201 0001310C GS CREDI1 0 1143876497 13050504 CR E DI1 0 22208 0 es-CL es-CL 00...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | FORM A TO DE DESARRO LL O E INTEGRACIONES I ntegrac i ón en vi ó de RCLy RCR a Un oE STF GROUP S . | RCL, RCR |
| 2 | es-CL es-CL es-CL 2 es-CL - Cr earun lo g en la tabla de C1 0 _ Dat aba se que pe rm ita re g istrar el p roce so de lo s envíos es-CL es-CL es-CL 3 es-CL - Cr earp roce so que se e jecu te au to m á tic amen te cada d í a 4 del mes , donde se cree un documento de tip o RCL pa ra ca rga rel va lor co nso li dado de las... | RCL |
| 3 | t ipo_ trans acc ion P LA NO => f35 8 _ id _ me dios _ pa go P LA NO => f35 8 _ docto _ ba nc o_ cg P LA NO => *f35 8 _ nro _ a lt_ docto_ba nc o *f35 0 _ not as AV VILLAS CG CA3 CG CSG CREDI1 0 AV VILLAS CG AV VILLAS TX CA3 NC CSG CREDI1 0 AV VILLAS TX BA NC OL OMB IA CG CB1 CG CSG CREDI1 0 BA NC OL OMBI A CG BA NC OL... | UnoEE, UNOEE, PayU, RCL, RCR |
| 4 | Hace re sto pa ra lo sRCL de con sig na ció n y de RCL de Pa yU es-CL es-CL 10 es-CL - Con fig u rar pa ra que el RC L que se cre a co n lospagos de Pa yU también se e jecu te eldia 4 del mesautom á tica men te es-CL es-CL 1 .1 . | RCL |
| 5 | Reproc esa mie nt o de RC R - Ree nvía con sig na cion esfa ll id as 1 .2 Deta ll ar c omponente s ex is tentes S OLUC IO N Wo rkerC onso li dado RC L P roye cto de t ipo Wo rk er Se rvi ce (.NET Core 3 . | .NET |
| 6 | Qu a rtz.NET L ibre ría que e jecu ta ta rea s p rog ra madas en se gundo p lan o u sa ndo e xp re sion es CR ON pa ra de fin ir ho rari os específ icos de e jecu ción . | .NET |
| 7 | 2 Pa ra me triza c ione s Des c rip ci ón Grupo Va lor E xp resió n CR ON pa ra RCL Con so li da do Cr onE xp ressio n Con so l ida do 0 0 9 4 , 20 * ? * E xp resió n CR ON pa ra Con tro l RCL Cr onE xp ressio n Con tro lR e cibo 0 20 ,59 9 - 23 4 , 20 * ? * E xp resió n CR ON pa ra Rep roce so RCL Cr onE xp ressio n R... | RCL, RCR |
| 8 | \ Cr ed it1 0 \ XML \ Rut a a rchivo s XML RCR Rut a _ Recib o _ Co n sign a cion es C: | RCR |
| 9 | 3 P roc eso P roc eso a ut omá tic o progra ma do Pa ra cu mp li r co n el re que ri m ie n to se cre ó un Wo rker Se rvi ce que ut il iza Qu a rtz.NET pa ra eje cu tar6 jo bsprog ra madosque manejan la gene ració n , co n tr oly rep roce sa m ie n to de re cibo s RCL y RCR . | .NET, RCL, RCR |
| 10 | Co nc e os de Q ua rtz.NET util iza dos: | .NET |
| 11 | Ge ne ra re cibo s co n so li dados RCL ag ru pando pagos e lect rón icos por períodos (1 - 15 y 16 - fin de me s) 2. | RCL |
| 12 | Ve ri fica que lo s re ci bos RCL se ha ya n crea do co rr e cta men te en Un oE 3. | RCL |

