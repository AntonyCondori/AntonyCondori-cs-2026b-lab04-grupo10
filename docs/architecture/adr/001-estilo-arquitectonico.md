# ADR-001: Adoptar un monolito modular para el MVP de EcoRecicla AQP

- Estado: Aceptado
- Fecha: 2026-10-04
- Decisores: Condori Caira Antony Beltran, Sencia Ale Bryan Daniel, Yauli Merma Diego Raul

## Contexto
EcoRecicla AQP debe estar en producción en 1 mes (R-01) con 3 desarrolladores que dominan Node.js y PostgreSQL (R-02, R-05) y una infraestructura de bajo costo (R-03). El atributo de calidad crítico es la modificabilidad (QA-01): incorporar un nuevo distrito o una nueva regla de puntos en ≤ 2 días-persona sin modificar los demás módulos. Los requisitos RF-01 a RF-08 se agrupan naturalmente en dominios (identidad, solicitudes, rutas, puntos, reportes).

## Alternativas consideradas
1. Monolito en capas (3,80): simple y rápido, pero las funciones quedarían acopladas dentro de cada capa y cambiar reglas de puntos tocaría varios módulos.
2. Microservicios (2,85): máxima modificabilidad, pero exige varios despliegues, bases de datos y operación distribuida, excesivo para 3 desarrolladores en 1 mes.
3. Monolito modular (4,15): elegido.

## Decisión
Usaremos un monolito modular en Node.js con cinco módulos (Identidad y distritos, Solicitudes de recojo, Rutas, Puntos y canjes, Reportes). Los módulos se comunican solo mediante interfaces públicas (servicios de aplicación) y cada uno tiene su propio esquema en PostgreSQL. Las reglas de puntos por distrito se implementan como componentes intercambiables dentro del módulo Puntos, y las integraciones externas como adaptadores (puertos y adaptadores).

## Consecuencias
- Positivas: un solo despliegue y bajo costo; entrega dentro de 1 mes; agregar un distrito o regla de puntos queda acotado al módulo Puntos (QA-01); los módulos pueden extraerse como servicios en el futuro si la carga lo exige.
- Negativas / riesgos: una falla grave o un despliegue defectuoso afecta a todo el sistema, y los límites entre módulos pueden erosionarse con el tiempo si el equipo no los respeta.
- Mitigaciones: verificar los límites entre módulos en la CI con una herramienta como dependency-cruiser y prohibir consultas entre esquemas; hacer respaldos automáticos diarios de PostgreSQL y mantener un procedimiento de reversión (rollback) del despliegue; aislar cada regla de puntos por distrito en su propio componente con pruebas propias.
