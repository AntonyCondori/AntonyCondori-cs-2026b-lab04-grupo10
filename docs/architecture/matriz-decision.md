# Matriz de decisión — EcoRecicla AQP

## Alternativas
- **A. Monolito en capas:** un solo despliegue en Node.js organizado en presentación, lógica de negocio y acceso a datos. Es lo más simple y rápido de construir, pero las funciones (solicitudes, rutas, puntos, reportes) quedan mezcladas dentro de cada capa.
- **B. Monolito modular:** un solo despliegue dividido en módulos de dominio (Identidad y distritos, Solicitudes, Rutas, Puntos y canjes, Reportes) que se comunican por interfaces explícitas y tienen su propio esquema en PostgreSQL.
- **C. Microservicios:** un servicio independiente por dominio, cada uno con su base de datos y un API Gateway. Máxima independencia entre partes, pero exige varios despliegues y operación distribuida.

## Criterios y pesos (deben sumar 100 %)
| Criterio                | Peso | Justificación (driver relacionado)                                                         |
|-------------------------|------|--------------------------------------------------------------------------------------------|
| Modificabilidad         | 30 % | QA-01: es el atributo crítico (nuevo distrito o regla de puntos en ≤ 2 días-persona)       |
| Tiempo de entrega       | 20 % | R-01: el MVP debe estar en producción en 1 mes                                             |
| Simplicidad operativa   | 20 % | R-02: solo 3 desarrolladores deben construir y operar el sistema                           |
| Costo operativo         | 15 % | R-03: presupuesto de infraestructura bajo (un solo servidor)                               |
| Seguridad de datos      | 15 % | QA-02 y R-04: protección de direcciones y datos personales de los vecinos                  |
| **Total**               | 100 %|                                                                                            |

## Matriz (puntaje 1 = muy malo … 5 = excelente)
| Criterio (peso)             | A. Capas | B. Monolito modular | C. Microservicios |
|-----------------------------|----------|---------------------|-------------------|
| Modificabilidad (30 %)      | 2        | 4                   | 5                 |
| Tiempo de entrega (20 %)    | 5        | 4                   | 2                 |
| Simplicidad operativa (20 %)| 5        | 4                   | 1                 |
| Costo operativo (15 %)      | 5        | 5                   | 2                 |
| Seguridad de datos (15 %)   | 3        | 4                   | 3                 |
| **Total ponderado**         | **3,80** | **4,15**            | **2,85**          |

Total ponderado = Σ (peso × puntaje).
- A: 0,30×2 + 0,20×5 + 0,20×5 + 0,15×5 + 0,15×3 = 3,80
- B: 0,30×4 + 0,20×4 + 0,20×4 + 0,15×5 + 0,15×4 = 4,15
- C: 0,30×5 + 0,20×2 + 0,20×1 + 0,15×2 + 0,15×3 = 2,85

## Conclusión
Elegimos **B. Monolito modular** porque combina buena modificabilidad (el atributo crítico, QA-01) con un solo despliegue y un costo acorde a R-01, R-02 y R-03. La segunda mejor alternativa es **A. Monolito en capas (3,80)**, que se documenta como descartada en `diagramas/alternativa.puml`; los microservicios (2,85) exceden la capacidad operativa de 3 desarrolladores en 1 mes. Ver [ADR-001](adr/001-estilo-arquitectonico.md).
