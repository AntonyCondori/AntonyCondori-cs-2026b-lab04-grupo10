# Round-trip (E6) - Módulo Solicitudes de recojo

**Flujo:** `clases.puml` → IA (Prompt IA 2, ingeniería directa) → `src/solicitudes/dominio.py` → `pyreverse` (ingeniería inversa) → `classes_solicitudes.puml` → comparación humana.

```bash
pip install pylint
pyreverse -o puml -p solicitudes src/solicitudes   # classes_solicitudes.puml
pyreverse -o png  -p solicitudes src/solicitudes   # classes_solicitudes.png
```

Resultado: `docs/design/classes_solicitudes.puml` y `docs/design/img/classes_solicitudes.png`.
Se verificó el código con un script de prueba: los criterios de aceptación 1, 2 y 3 de HU-01 se cumplen y el ciclo completo PENDIENTE → PUNTOS_ACREDITADOS funciona.

## Tabla de diferencias (diagrama de diseño vs diagrama obtenido del código)

| # | Diferencia observada | Causa | Acción |
|---|---|---|---|
| 1 | No aparecen las composiciones `Solicitud *-- DetalleResiduo` ni `Direccion *-- Coordenadas`, ni la asociación `Solicitud --> EstadoSolicitud`. Solo se infiere `Solicitud --> Direccion`. | pyreverse no infiere asociaciones desde colecciones tipadas (`list[DetalleResiduo]`) ni desde uniones (`Coordenadas \| None`, `EstadoSolicitud \| None`). | Ninguna: limitación de la herramienta. El diagrama de diseño se mantiene. |
| 2 | No hay multiplicidades (`1..*`, `0..1`). | El código no expresa multiplicidades. | Se refuerza C3 en código: `validar_detalles()` exige al menos un detalle con peso > 0. El `0..1` queda como `Coordenadas \| None`. |
| 3 | `MapasGeocodificacionPort`, `SolicitudRepository` y `NotificacionPort` aparecen como clases, no como interfaces `<<port>>`; `GoogleMapsAdapter.geocodificar` figura como `{abstract}` aunque lanza `NotImplementedError`. Se pierden los estereotipos. | Python implementa interfaces con ABC; pyreverse no lee estereotipos. El adaptador aún no está implementado. | Aceptable en Python; se documenta. |
| 4 | `EstadoSolicitud` aparece como clase con un atributo `name`, sin sus 6 valores. | pyreverse no lista los miembros de un `Enum`. | Ninguna: el diagrama de diseño es la fuente de verdad de los valores. |
| 5 | Se pierde la visibilidad (`-`/`+`): todos los atributos aparecen sin modificador. | Python no tiene atributos privados reales. | Documentar la convención: los atributos del diagrama `-` son atributos de instancia no expuestos fuera de la clase. |
| 6 | Se pierden las dependencias `..>` (`SolicitarRecojoService ..> Solicitud : crea`, `..> ErrorValidacion : lanza`, `Port ..> ErrorGeocodificacion`). | pyreverse solo dibuja asociaciones por atributo y herencia, no usos dentro de métodos. | Ninguna: limitación de la herramienta. |
| 7 | Nombres en snake_case (`solicitar_recojo`, `marcar_pendiente`) frente a camelCase del diagrama. | Convención de Python (PEP 8). El stack del ADR-001 es Node.js, donde se usaría camelCase. | Aceptable; se documenta la equivalencia (C5). |
| 8 | El código tiene atributos que el diagrama no tiene: `reciclador_id`, `peso_real_kg`, `puntos`; y `estado` es `EstadoSolicitud \| None`. | La IA los agregó para implementar `asignar()`, `registrar_pesaje()` y `acreditar_puntos()` (operaciones de E3 que faltaban en `clases.puml`). `None` representa "recién creada" porque el diagrama no define estado inicial. | **Corregir el diagrama:** agregar esos atributos y las 4 operaciones a `Solicitud` en `clases.puml` (cierra C2). |
| 9 | La notificación al vecino es una llamada síncrona. | El diagrama de secuencia la marca asíncrona (`->>`); el esqueleto no usa `async`/colas. | Documentar la limitación; en la implementación real (Node.js) se emitirá sin `await`/por evento. |
| 10 | El esqueleto está en Python y el stack del ADR-001 es Node.js. | La guía permite Python o Java para E6 (pyreverse). | Documentar: el esqueleto valida el diseño, no es código de producción. |

## Pendiente de corregir en `clases.puml` (resultado del round-trip)

```plantuml
class Solicitud {
  ' ... atributos existentes ...
  - recicladorId: String
  - pesoRealKg: Number
  - puntos: Integer
  ' ... operaciones existentes ...
  + asignar(recicladorId: String): void
  + registrarRecojo(): void
  + registrarPesaje(pesoKg: Number): void
  + acreditarPuntos(puntos: Integer): void
}
```
