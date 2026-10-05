# ADR-003: Construir la interfaz del reciclador como PWA

- Estado: Aceptado
- Fecha: 2026-10-04
- Decisores: Condori Caira Antony Beltran, Sencia Ale Bryan Daniel, Yauli Merma Diego Raul

## Contexto
Los recicladores registran recojos en la calle con celulares de gama baja y señal posiblemente intermitente (QA-03: registro en ≤ 4 toques y sincronización en ≤ 60 s al recuperar señal). El MVP debe estar en 1 mes (R-01) con 3 desarrolladores que dominan tecnologías web (R-02, R-05) y presupuesto bajo (R-03). Las funciones RF-02 y RF-03 son las que usa el reciclador.

## Alternativas consideradas
1. App nativa (Android): mejor acceso a funciones del dispositivo, pero requiere otro stack, publicación en tienda y más tiempo de desarrollo.
2. PWA (Progressive Web App): una sola aplicación web instalable, con almacenamiento local y sincronización posterior, sobre el stack que el equipo ya domina.

## Decisión
Usaremos una PWA para la interfaz del reciclador (y la misma base web para vecino y municipalidad), con almacenamiento local de los registros de recojo y sincronización automática al recuperar la conexión.

## Consecuencias
- Positivas: un solo código para todos los roles; sin publicación en tiendas; reduce el esfuerzo de distribución para R-01; permite diseñar el trabajo sin conexión de QA-03, pendiente de validación en dispositivos reales.
- Negativas / riesgos: acceso limitado a algunas funciones del dispositivo (por ejemplo, tareas en segundo plano); la sincronización exige manejar conflictos y reintentos, lo que añade complejidad de desarrollo y pruebas. Para evitar registros duplicados (por ejemplo, un peso o unos puntos contados dos veces), cada registro llevará un identificador único generado en el dispositivo y el servidor ignorará los repetidos.

## Sincronización y verificación propuesta
- Guardar la ruta necesaria y las operaciones pendientes en IndexedDB; usar un service worker para los recursos estáticos. Mostrar estados «pendiente», «sincronizando» y «confirmado»; eliminar el pendiente solo tras la confirmación del servidor.
- Intentar sincronizar al abrir o recuperar el foco de la PWA, al detectar conexión y mediante una acción manual. Las tareas en segundo plano son una mejora opcional, porque su disponibilidad depende del navegador.
- Reutilizar el mismo UUID en cada reintento. El servidor valida rol, asignación y peso; registra operación y puntos de forma atómica conforme a ADR-002 y devuelve el resultado previo si recibe la misma operación. Un UUID repetido con contenido distinto se rechaza como conflicto.
- Una sesión expirada solicita autenticación sin borrar pendientes. Una solicitud reasignada se marca para revisión; el cliente no sobrescribe el estado del servidor.
- Medir los ≤ 4 toques y los ≤ 60 s de QA-03 con la PWA abierta, sesión válida y API disponible al volver la conexión. El funcionamiento con la aplicación cerrada debe acordarse con el equipo; no se garantiza sincronización en segundo plano.
- Verificar modo avión, recarga, reintentos y conflictos en el dispositivo objetivo. Estas pruebas quedan propuestas, no ejecutadas.
