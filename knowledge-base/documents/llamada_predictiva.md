# Llamada predictiva.pdf

| Campo | Valor |
| --- | --- |
| id | `llamada_predictiva` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 180654 |
| longitud raw | 73018 |
| longitud limpia | 69197 |
| ratio de cobertura (crudo, legado) | 0.38304 |
| caracteres de texto util | 4949 |
| texto util real (palabras / bytes extraidos) | 7.15% |
| banda de cobertura (por texto util real) | baja |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib+regex (capa de texto PDF) |
| sha256 | `75de074b46dab3babd00ecf877816c3fa41fe29558b18de0c640bcdebf1a6b07` |

## Resumen jerarquico

- Documento 'Llamada predictiva.pdf' (PDF): 69197 caracteres limpios extraidos (zlib+regex), texto util real 7.15%, banda 'baja', clasificacion [VERIFIED-FACT].
- Seccion 1: FORM AT O DE DES A RR OLLO E I NT E GRAC IO NES Integra ción Ll a ma da P re dic ti va STF GROUP S .A. INFORM AT ICA Py . es-MX CR E DI1 0 S OF TW AR E P ROP IO...
- Seccion 2: hivo s Ex c el Lo g4 Net - S is tem a de l og g in g Pa trón de Arquitec tu ra P at rón Repos it o ry - B as eCont ext par a ac c es o a dat os P at rón Se rvic...
- Seccion 3: ip t arR eq ue st .cs : Int erfaz pa ra enc r ipta ci ón Obj e to s de Tra ns fer e nc ia de Da to s (D TO) As ignacionC art e raDTO.cs : Dat os de as ig nac ió...
- Seccion 4: s ific ación y Ca rga de Re gis tros Cuánd o se ej e cu ta : Se g ún exp r es iones CR ON c onf ig ur ada s ( días l ab or ales y sábad os) P roce so : 1. Ve ri...
- Seccion 5: Ca mpa ñas Cuánd o se ej e cu ta : Pr og ram ado d es pués de la c ar ga de r egis tr os P roce so : 1. Ob tiene ag entes ac tiv os de la base de dat os 2. Inic...
- Seccion 6: 3 Repo rt e Tel é fo no a Tel é fo no : GET /api/v2/reports_manager.php?api=campaign_3 Ge s tión de Res ultad os Obte nci ó n de Ti p if ic ac ione s : C onsult...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | NET 8 qu e func iona c om o s ervic io de Wind ow s , dis eñado par a aut om at iza r la g es tió n de c ar g ue de c am pañ as telefónic as pr edic tiv as m ediante el c onsumo de las Apis de la plat a for ma Wo lk vox. | API |
| 2 | DET AL LE T É CN ICO Arqu ite c tu ra Gene ra l Tec nologías Utili za das .NET 8 - Fr am ewor kpri nc ipal Q ua rt z .NET - Pro gramación de t ar eas ( Jo bs ) Micr osoft .Extens ions . | .NET |
| 3 | R egis tr a r es ulta do de d etenc ión Integra ción c on W olk v ox API s Consumi da s I nf o rmaci ó n de Camp añas : | API |
| 4 | GET /api/v2/information.php?api=campaigns I ns e rt ar Re gis t ros : | API |
| 5 | POS T /api/v2/campaign.php?api=add_record Borrar Re gis t ros : | API |
| 6 | DELE TE /api/v2/campaign.php?api= clear_campaign I ni ci ar Camp aña : | API |
| 7 | POST /api/v2/campaign.php?api=start P ara r Camp aña : | API |
| 8 | POST /api/v2/campaign.php?api=stop De t al le Ti pif ic ación : | API |
| 9 | G ET /api/v2/reports_manager.php?api=act_3 Repo rt e Tel é fo no a Tel é fo no : | API |
| 10 | GET /api/v2/reports_manager.php?api=campaign_3 Ge s tión de Res ultad os Obte nci ó n de Ti p if ic ac ione s : | API |
| 11 | sp _consultar_asignacion_cartera Cart e ra por Cupo : | Cartera |
| 12 | sp_ consulta_cartera_por_cupo_creditos Fe chas de Co rt e : | Cartera |

