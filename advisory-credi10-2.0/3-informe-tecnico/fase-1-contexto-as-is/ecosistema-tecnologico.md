# Ecosistema tecnologico y de datos AS-IS

> Tema del **informe tecnico multinivel** de Credi10 2.0, dentro de **Fase 1 - Contexto AS-IS**. Vista narrativa que reorganiza y **enriquece** el informe plano de respaldo ([vista compacta de la fase](../../01-contexto-as-is.md)); aqui el foco es la **interpretacion** de los hallazgos y sus implicaciones para la **estimacion**, la **estrategia de implementacion** y los **riesgos**.

> **Etiquetas epistemicas:** **[VERIFIED-FACT]** evidencia explicita del corpus; **[DOC-ASSUMPTION]** supuesto razonable a validar; **[DOC-CONFLICT]** tension entre fuentes; **[EPISTEMIC-VOID]** sin base documental (no se fabrica evidencia).

> **Hilo Dorado:** la trazabilidad end-to-end encadena Driver (DRV) -> Capability (CAP) -> Benchmark (BMK) -> Gap (GAP) -> Reliever (REL) -> ABB -> SBB -> Ola (WAV) -> ROI/Outcome, de modo que cada decision tecnica de este informe es trazable hasta un indicador de retorno del RFP.

## Que estamos mirando y por que importa

El inventario tecnologico y de datos es la **radiografia del terreno** sobre el que se construira. Credi10 corre sobre .NET Framework 4.8 e IIS, con integradores en .NET, Link de Recaudo en .NET Core 3.1, workers mixtos y un canal B2C sobre Node.js/React y Wordpress/XAMPP. Los datos viven en SQL Server 2019 Enterprise y MariaDB. Conocer cada pieza con precision es lo que convierte una estimacion en algo mas que una corazonada.

La lectura narrativa es que conviven **dos generaciones tecnologicas**: componentes modernos (.NET 8 en algunos workers) junto a marcos fuera de soporte (.NET 4.8, .NET Core 3.1, Wordpress). Esa heterogeneidad encarece el mantenimiento y es el corazon del driver de evolucion (DRV-004) y licenciamiento (DRV-005).

## Inventario tecnologico

| Capa | Componente | Tecnologia (AS-IS) | Evidencia |
| --- | --- | --- | --- |
| Aplicacion | Plataforma Credi10 | .NET Framework 4.8 sobre IIS 10 | Despliegue |
| Aplicacion | Integradores (CrossCore, Inspektor, Datacredito, Servicios) | .NET | Despliegue |
| Aplicacion | Web Service UnoEE | .NET | Despliegue |
| Aplicacion | Link de Recaudo | .NET Core 3.1 | Despliegue |
| Workers | Llamada predictiva, Indicador Robot, API SAC, Worker Consolidado, Corte/Cartera, Cobranza SMS/WhatsApp/Email/Scheduler | .NET Core 8 y .NET Framework 4.8 | Despliegue |
| Canales | Portal B2C | API Node.js + React; Wordpress sobre Apache (XAMPP) | Despliegue |
| Infra | Servidores on-prem | Windows Server 2019 Datacenter (Coatlanta, Codallas, Comumbai) | Despliegue |
| Infra | Nube | AWS us-east-2, VPC STUDIO F, WAF->ALB->EC2, S3, CloudWatch, NAT, Bastion, VPN IPSec (Telmex) a on-prem Cokioto | Infra AWS |

## Inventario de datos

| Base de datos | Motor | Uso | Evidencia |
| --- | --- | --- | --- |
| C10_Credi10NET | SQL Server 2019 Enterprise | BD principal de Credi10 | Despliegue |
| C10_Inspektor | SQL Server 2019 Enterprise | Integrador Inspektor | Despliegue |
| C10_Datacredito | SQL Server 2019 Enterprise | Integrador Datacredito | Despliegue |
| C10_Database | SQL Server 2019 Enterprise | Link de Recaudo | Despliegue |
| UnoEE_studiof (principal + espejo), Siesa Unoee | SQL Server | ERP Siesa/UnoEE | Despliegue |
| C10_B2C_Wordpress, C10_B2C | MariaDB 10.4.32 | Portal B2C | Despliegue |

### Lo que implica el inventario de datos

La dispersion de bases de datos (y, a nivel grupo, las +200 BDs duplicadas) anticipa un frente de **consolidacion de datos** que la Fase 4 resuelve con una fuente unica de verdad por dominio. Es uno de los frentes de mayor incertidumbre porque el corpus no detalla el esquema real de cada base.
## Implicaciones para la estimacion

El inventario permite tallar el esfuerzo de **migracion de runtime** (cuantos componentes salen de .NET 4.8 / Core 3.1) y de **consolidacion de datos**. Ambos frentes se marcan con factores de acople legado en la tabla parametrica de la Fase 5.

## Implicaciones para la estrategia de implementacion

La estrategia modera el riesgo migrando por dominio (no big-bang) y retirando primero los componentes fuera de soporte, que son los de mayor riesgo de seguridad y licenciamiento.

## Riesgos e incertidumbre

El riesgo es la **deuda tecnica oculta**: esquemas de datos no documentados y dependencias implicitas entre componentes legados. Se mitiga con un inventario y clasificacion previos como prerrequisito. [DOC-ASSUMPTION]

