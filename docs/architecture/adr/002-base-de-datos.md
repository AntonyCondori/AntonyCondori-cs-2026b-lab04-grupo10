# ADR-002: Usar PostgreSQL con un esquema por módulo

- Estado: Aceptado
- Fecha: 2026-10-04
- Decisores: Condori Caira Antony Beltran, Sencia Ale Bryan Daniel, Yauli Merma Diego Raul

## Contexto
El sistema acredita y canjea puntos (RF-04, RF-05), por lo que necesita consistencia al registrar cada movimiento. Los reportes de toneladas por distrito y periodo (RF-06) son consultas agregadas. El equipo domina PostgreSQL (R-02, R-05), el presupuesto es bajo (R-03) y los datos personales de vecinos requieren control de acceso (QA-02, R-04). Además, ADR-001 exige límites claros entre módulos (QA-01).

## Alternativas consideradas
1. Base de datos documental (por ejemplo, MongoDB): esquema flexible; exigiría evaluar otro modelo de persistencia y aprender una tecnología fuera de R-05. La elección no presupone que una base documental carezca de transacciones.
2. PostgreSQL con un esquema por módulo: modelo relacional con transacciones, consultas SQL para reportes y separación lógica entre módulos.

## Decisión
Usaremos PostgreSQL como única base de datos, con un esquema por módulo (identidad, solicitudes, rutas, puntos, reportes). Los módulos no harán consultas directas a esquemas ajenos; usarán las interfaces públicas definidas en ADR-001.

## Consecuencias
- Positivas: transacciones para acreditar y canjear puntos sin inconsistencias; reportes con SQL estándar; el equipo ya domina la tecnología; un solo motor de base de datos que operar y respaldar.
- Negativas / riesgos: los cambios de estructura requieren migraciones controladas; la separación entre esquemas depende de la disciplina del equipo y no solo de la tecnología; no se podrán usar joins directos entre módulos. Además, una sola base concentra los datos personales de los vecinos, por lo que la visibilidad de las direcciones se limitará por rol (QA-02).

## Aplicación y verificación propuesta
- Cada módulo mantiene sus migraciones y repositorios; Reportes obtiene los datos mediante las interfaces públicas y conserva sus propias proyecciones. La separación por esquemas no reemplaza la autorización por rol.
- La confirmación del recojo y la acreditación se coordinan mediante servicios públicos dentro de una transacción PostgreSQL compartida: se confirman ambas operaciones o ninguna, sin consultar tablas ajenas desde los repositorios.
- El identificador de operación de ADR-003 tiene una restricción única; una repetición no vuelve a acreditar puntos. Los canjes deben comprobar y actualizar el saldo de forma atómica para evitar saldos negativos ante concurrencia.
- Se proponen pruebas de rollback, reintentos y canjes concurrentes, más restauración de respaldos. Son criterios de implementación del MVP; aún no son pruebas ejecutadas sobre una aplicación.
