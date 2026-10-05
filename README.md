# EcoRecicla AQP — Laboratorio 04: Fundamentos de arquitectura de software
Construcción de Software · EPIS-UNSA · 2026-B · Grupo 10

## Integrantes
| Nombre | Rol en el laboratorio |
|--------|-----------------------|
| Condori Caira Antony Beltran | Redactor de drivers y de ADR-001; responsable del README |
| Sencia Ale Bryan Daniel | Matriz de decisión y diagramador (Mermaid y PlantUML) |
| Yauli Merma Diego Raul | Redactor de ADR-002 y ADR-003; vista de despliegue y verificador de IA |

## Caso
EcoRecicla AQP es una plataforma para el recojo de residuos reciclables con recicladores formalizados en distritos de Arequipa. Los vecinos solicitan recojos y canjean puntos, los recicladores consultan su ruta del día y registran el peso recogido, y la municipalidad consulta reportes de toneladas recicladas. El MVP debe estar en producción en 1 mes con 3 desarrolladores (Node.js y PostgreSQL) y presupuesto bajo. El atributo de calidad crítico es la **modificabilidad**: incorporar un nuevo distrito o una nueva regla de puntos en ≤ 2 días-persona, sin modificar los demás módulos.

## Arquitectura elegida
```mermaid
flowchart TB
    VE["Vecino"]
    RE["Reciclador"]
    MU["Municipalidad"]
    subgraph APP["EcoRecicla AQP — Monolito modular (un solo despliegue)"]
        API["Capa de presentación: API REST + PWA"]
        M1["Identidad<br/>y distritos"]
        M2["Solicitudes<br/>de recojo"]
        M3["Rutas<br/>del día"]
        M4["Puntos<br/>y canjes"]
        M5["Reportes"]
        INF["Capa de infraestructura: repositorios y adaptadores externos"]
    end
    DB[("PostgreSQL<br/>(un esquema por módulo)")]
    MAP["Servicio de mapas<br/>y geocodificación"]
    VE & RE & MU --> API
    API --> M1 & M2 & M3 & M4 & M5
    M1 & M2 & M3 & M4 & M5 --> INF
    INF --> DB
    INF --> MAP
    classDef mod fill:#E8F5E9,stroke:#2E7D32,color:#000
    classDef ext fill:#F2F2F2,stroke:#7F7F7F,color:#000,stroke-dasharray: 4 3
    classDef usr fill:#FDEDEC,stroke:#C8310E,color:#000
    class M1,M2,M3,M4,M5 mod
    class MAP ext
    class VE,RE,MU usr
```

## Decisiones arquitectónicas
- [ADR-001: Estilo arquitectónico](docs/architecture/adr/001-estilo-arquitectonico.md)
- [ADR-002: Base de datos](docs/architecture/adr/002-base-de-datos.md)
- [ADR-003: PWA para el reciclador](docs/architecture/adr/003-pwa-reciclador.md)

## Reflexión sobre el uso de la IA (5–8 líneas)
Claude nos ayudó a estructurar los entregables, a redactar los borradores de drivers, matriz de decisión, ADR y README, y a repartir el trabajo entre los tres. Sus borradores incluyeron supuestos que no le habíamos dado (conectividad intermitente de los recicladores, aplicación de la Ley 29733 y uso de un servicio de mapas), que documentamos como supuestos S-01 a S-03 en `drivers.md`. Recalculamos los totales de la matriz con un script y comprobamos que la segunda mejor alternativa es el monolito en capas, no microservicios como en el ejemplo de la guía, por lo que la alternativa descartada que diagramamos es capas. La crítica adversarial señaló riesgos reales del monolito modular (erosión de límites, punto único de falla, duplicados por la sincronización sin conexión) y los incorporamos como mitigaciones en los ADR. Aprendimos que la IA propone, pero cada supuesto y cada cálculo debe contrastarse con nuestras restricciones: plazo de 1 mes, 3 desarrolladores y presupuesto bajo. El detalle está en la [bitácora de uso de IA](docs/architecture/bitacora-ia.md).


## Vista de despliegue (E6)

[Diagrama y reproducción](docs/architecture/diagramas/README.md). Se incluye una vista alternativa PlantUML porque no se pudo instalar Graphviz; el PNG adjunto se renderizó localmente con Pillow. El script también admite Python Diagrams, pendiente de ejecución con sus dependencias instaladas.
