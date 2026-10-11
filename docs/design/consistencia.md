# Revisión de consistencia (E7) - EcoRecicla AQP

**Herramienta:** Claude (Prompt IA 3 - Auditor de consistencia) · **Fecha:** 10/10/2026
**Archivos auditados:** `clases.puml`, `secuencia-solicitar-recojo.puml`, `estados-solicitud.mmd`, `actividades-ruta-diaria.puml`, `paquetes.puml`.
Regla de oro: la IA propone, el equipo decide y verifica.

## Hallazgos de la IA y verificación del equipo

| # | Regla | Elemento | Hallazgo de la IA | Verificación del equipo | Decisión |
|---|---|---|---|---|---|
| 1 | C2 | `estados-solicitud.mmd` ↔ clase `Solicitud` | Las transiciones `asignar(recicladorId)`, `registrarRecojo()`, `registrarPesaje(pesoKg)` y `acreditarPuntos(puntos)` no existen como operaciones en `clases.puml`. | **Correcto.** Ya se había anotado en E3 y se confirmó en el round-trip (diferencia 8). | Aceptado: agregar las 4 operaciones (y los atributos `recicladorId`, `pesoRealKg`, `puntos`) a `Solicitud`. |
| 2 | C1 | Secuencia, fragmento `loop` + `validarDetalles()` | El criterio de aceptación 3 (sin residuos o peso 0 → error de validación y no se guarda) no aparece en la secuencia: el `loop` llama a `esValido()` pero no hay camino de error ni `ErrorValidacion`; además `validarDetalles()` repite lo que hace el `loop`. | **Correcto.** El checklist de E2 exige cubrir el criterio de error. | Aceptado: `validarDetalles()` itera internamente y se agrega un `alt`/`opt` con `ErrorValidacion` → `400` sin llamar a `guardar`. |
| 3 | C1 | Secuencia, mensaje 4 `crear(vecinoId, direccion, detalles)` | El servicio recibe `textoDireccion: String`, pero `crear` pide un objeto `Direccion` y ningún mensaje lo construye. | **Correcto.** Hay un paso implícito. | Aceptado: agregar el mensaje de creación de `Direccion(textoDireccion)` antes de `crear`. |
| 4 | C1 | Clases: `SolicitarRecojoService ..> ErrorValidacion : lanza` | La excepción la lanza `Solicitud.validarDetalles()`, no el servicio. | **Correcto** (el servicio solo la propaga). | Aceptado: mover la relación a `Solicitud ..> ErrorValidacion`. |
| 5 | C3 | Clases: asociaciones del servicio a los puertos | `SolicitarRecojoService --> "1" SolicitudRepository` (y los otros 2 puertos) solo tiene multiplicidad en un extremo; el checklist de E1 pide ambos. | **Correcto.** | Aceptado: agregar `"1"` en el extremo del servicio. |
| 6 | C5 | `<<port>>`/`<<adapter>>` (clases) vs `<<puerto>>`/`<<adaptador>>` (paquetes) | Estereotipos en idiomas distintos entre diagramas. | **Correcto.** | Aceptado: unificar en `<<puerto>>` y `<<adaptador>>`, como en la guía. |
| 7 | C5 | `asignarSolicitud()` (paquetes) vs `asignar(recicladorId)` (estados) | La misma acción tiene dos nombres. | **Correcto.** | Aceptado: usar `asignar(recicladorId)` como operación de `Solicitud`; en paquetes dejar `asignarSolicitud()` solo si es el contrato público del módulo, y documentar la equivalencia. |
| 8 | C5 / C4 | `acreditarPuntos()` en paquetes (SOL → PUN) y en estados (op. de `Solicitud`) | Mismo nombre para dos cosas: contrato del módulo Puntos y operación de la entidad. | **Parcialmente correcto.** No hay ciclo, pero genera ambigüedad. | Aceptado: renombrar el contrato de PUN a `acreditar(solicitudId, pesoKg, distritoId)`. |
| 9 | C4 | `paquetes.puml`: `PUN` recibe "distrito" | `Solicitud`/`Direccion` no tienen distrito; no se sabe de dónde sale ese dato. | **Correcto.** Vacío de diseño. | Aceptado: obtener `distritoId` vía `IdentidadDistritosService` (SOL → IDE ya existe) o agregarlo a `Direccion`. Decidirlo como equipo. |
| 10 | UML | `estados-solicitud.mmd`: dos transiciones desde `[*]` con guardas | UML solo permite una transición inicial sin evento ni guarda. | **Correcto pero menor** (restricción de usar solo los 6 estados de la enumeración). | Documentado como limitación; opcional: un único `[*] --> PENDIENTE` y `PENDIENTE --> RECHAZADA`. |

## Falsos positivos identificados

| # | Regla | Hallazgo de la IA | Por qué es un falso positivo | Qué habría pasado si se aceptaba |
|---|---|---|---|---|
| FP1 | C1 | "`Solicitud` invoca `DetalleResiduo.esValido()` pero no existe asociación entre ambas." | Falso: existe la composición `Solicitud "1" *-- "1..*" DetalleResiduo : detalles`; la navegación es válida (igual que el Paso 9 de la guía). | Se habría agregado una asociación duplicada o se habría rediseñado una relación que ya era correcta. |
| FP2 | C1 | "El mensaje `crear(...)` no es una operación de instancia de `Solicitud`; el mensaje 4 es inválido." | Falso: `crear` está declarada `{static}` y es la fábrica; en secuencia, un mensaje de creación (`**`) hacia el participante creado es notación válida. | Se habría eliminado la fábrica o cambiado a un constructor, perdiendo la validación centralizada (`validarDetalles`). |
| FP3 | C4 | "`SOL ..> PUN : acreditarPuntos()` y `acreditarPuntos` es de `Solicitud`, por lo tanto `PUN` depende de `SOL` y hay ciclo." | Falso: la flecha es SOL → PUN y `PUN` recibe solo identificadores y peso, sin importar la clase `Solicitud` (nota del diagrama). Recorriendo las flechas: REP → {SOL, RUT, PUN}; RUT → SOL; SOL → {IDE, PUN}; PUN → IDE. No hay ciclo. | Se habría "resuelto" un ciclo inexistente creando un ADR y un puerto innecesarios. |

## Verificación C4 (sin ciclos)

`REP → SOL, RUT, PUN` · `RUT → SOL` · `SOL → IDE, PUN` · `PUN → IDE` · `IDE` no depende de nadie. El grafo es acíclico. Falta confirmar que cada dependencia esté permitida por el ADR-001 del Lab 04.
