# Llamada predictiva.pdf

| Campo | Valor |
| --- | --- |
| id | `llamada_predictiva` |
| tipo | pdf |
| rol (prioridad) | secondary |
| tamano (bytes) | 180654 |
| longitud raw | 7569 |
| longitud limpia | 6866 |
| ratio de cobertura (crudo, legado) | 0.03801 |
| caracteres de texto util | 5195 |
| texto util real (palabras / bytes extraidos) | 75.66% |
| banda de cobertura (por texto util real) | alta |
| flag epistemico | [VERIFIED-FACT] |
| metodo de ingesta | zlib + /ToUnicode por fuente (capa de texto nativa PDF) |
| sha256 | `75de074b46dab3babd00ecf877816c3fa41fe29558b18de0c640bcdebf1a6b07` |

## Resumen jerarquico

- Documento 'Llamada predictiva.pdf' (PDF): 6866 caracteres limpios extraidos (zlib + /ToUnicode por fuente), texto util real 75.66%, banda 'alta', clasificacion [VERIFIED-FACT].
- Seccion 1: FORMATO DE DESARROLLO E INTEGRACIONES Integración Llamada Predictiva STF GROUP S.A. INFORMATICA – Py. CREDI10 SOFTWARE PROPIO Cali, martes 6 de enero del 202 6...
- Seccion 2: adaPredictivaBLL para lógica de negocio • Patrón Job - Jobs programados con Quartz • Inyección de Dependencias - Microsoft DI Container 2. COMPONENTES EXISTENTE...
- Seccion 3: • GestionPredictivaDTO.cs : Datos de gestión predictiva • TelefonoTelefonoRequestDTO.cs : Solicitudes teléfono a teléfono Jobs Programados • ClasificacionInserc...
- Seccion 4: o tipificados 5. Inserción en Campañas : Envía registros a Wolkvox por campaña Información que se guarda : • Fecha de asignación de cartera • Tipificación de cl...
- Seccion 5: p?api= clear_campaign • Iniciar Campaña : POST /api/v2/campaign.php?api=start • Parar Campaña : POST /api/v2/campaign.php?api=stop • Detalle Tipificación : • Re...
- Seccion 6: ntes • FechaUltimoCargueWolkvox : Control de última ejecución Sistema de Programación Expresiones CRON • Días Laborales : Configuración específica para L - V •...

## Hechos clave (trazables)

| # | Hecho | Tokens |
| --- | --- | --- |
| 1 | FORMATO DE DESARROLLO E INTEGRACIONES Integración Llamada Predictiva STF GROUP S.A. | Predictiva |
| 2 | CREDI10 SOFTWARE PROPIO Cali, martes 6 de enero del 202 6 I NTRODUCCION La integración de Llamada Predictiva es un Worker Service desarrollado en .NET 8 que funciona como servicio de Windows, diseñado para automatizar la gestión de cargue de campañas telefónicas predictivas mediante el consumo de las Apis de la platafo... | Credi10, .NET, Predictiva, API |
| 3 | DETALLE TÉCNICO Arquitectura General Tecnologías Utilizadas • .NET 8 - Framework principal • Quartz.NET - Programación de tareas (Jobs) • Microsoft.Extensions.Hosting - Servicio de fondo • Microsoft.Data.SqlClient - Conexióna base de datos • System.Text.Json - Serialización JSON • SpreadsheetLight - Generación de archi... | .NET, Predictiva |
| 4 | Punto de entrada, configuración de servicios y programación de Jobs • WorkerLlamadaPredictiva.cs : | Predictiva |
| 5 | Servicio principal de fondo Capa de Lógica de Negocio (BLL) • LlamadaPredictivaBLL.cs : | Predictiva |
| 6 | Manejo de conexiones y consultas a SQL Server • EncriptarRequest.cs : | SQL Server |
| 7 | Interfaz para encriptación Objetos de Transferencia de Datos (DTO) • AsignacionCarteraDTO.cs : | Cartera |
| 8 | Datos de asignación de cartera • AgenteCarteraDTO.cs : | Cartera |
| 9 | Solicitudes de campañas • ResponseApisWolkvox.cs : | WOLKVOX, API |
| 10 | Respuestas de APIs Wolkvox • GestionPredictivaDTO.cs : | WOLKVOX, Predictiva, API |
| 11 | Datos de gestión predictiva • TelefonoTelefonoRequestDTO.cs : | Predictiva |
| 12 | Detención de campañas Integración Externa • WolkvoxConnection.cs : | WOLKVOX |

