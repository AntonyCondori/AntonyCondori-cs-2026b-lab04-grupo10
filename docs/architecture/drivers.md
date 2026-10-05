# Drivers arquitectónicos — EcoRecicla AQP

## 1. Requisitos funcionales clave
| ID | Requisito | Actor | Prioridad |
|---|---|---|---|
| RF-01 | Crear y cancelar una solicitud con distrito, dirección, fecha y materiales; cancelar solo antes del inicio del recojo. | Vecino | Alta |
| RF-02 | Activar distritos, zonas y horarios desde configuración; el distrito activo aparece en solicitudes sin cambios en su código. | Municipalidad | Alta |
| RF-03 | Registrar recicladores formalizados y asignar solicitudes a uno autorizado para la zona. | Municipalidad | Alta |
| RF-04 | Consultar la ruta del día como lista ordenada de paradas; abrir una dirección en un proveedor externo de mapas. | Reciclador | Alta |
| RF-05 | Confirmar el recojo y registrar peso decimal en kg por material; rechazar valores negativos y confirmaciones duplicadas. | Reciclador | Alta |
| RF-06 | Consultar puntos y canjear un beneficio con saldo suficiente; un canje no admite saldo negativo. | Vecino | Alta |
| RF-07 | Configurar reglas de puntos versionadas por distrito/material y vigencia; el histórico conserva la versión aplicada. | Municipalidad | Alta |
| RF-08 | Obtener reporte por distrito, material y período; toneladas = suma de kg confirmados / 1000. | Municipalidad | Alta |
| RF-09 | Acceder con permisos de vecino, reciclador o municipalidad; solo se muestra información autorizada. | Todos | Alta |

## 2. Atributos de calidad (ordenados por prioridad)
1. **QA-01 — Mantenibilidad: modificabilidad.** Atributo crítico: incorporar un distrito o regla en ≤ 2 días-persona sin modificar otros módulos.
2. **QA-02 — Fiabilidad: integridad.** Los reintentos no deben duplicar puntos, pesos ni canjes.
3. **QA-03 — Seguridad.** Las direcciones y saldos requieren autorización por rol y propietario.
4. **QA-04 — Eficiencia de desempeño.** La lista de recojos debe poder consultarse durante la jornada con carga moderada.
5. **QA-05 — Capacidad de interacción.** Vecinos y recicladores necesitan flujos cortos utilizables desde celulares.

## 3. Restricciones
| ID | Tipo | Restricción |
|---|---|---|
| R-01 | Plazo | MVP en producción en 1 mes. Obligatoria según guía; evitar infraestructura distribuida inicial. |
| R-02 | Equipo | 3 integrantes del grupo 10, dentro del máximo de la guía. Tecnologías dominadas pendientes de confirmación; Django/PostgreSQL siguen como propuesta provisional. |
| R-03 | Presupuesto | Presupuesto bajo. Obligatoria; un VPS propuesto, sin importes inventados; cotizar hosting, dominio y respaldo antes del despliegue. |
| R-04 | Modificabilidad | Un distrito o una regla nuevos en ≤ 2 días-persona sin modificar los demás módulos. Obligatoria según el caso; interfaces estables y configuración por datos. |
| R-05 | Operación | Solo recicladores formalizados pueden recibir asignaciones. Derivada del caso; la municipalidad verifica la formalización por un procedimiento por definir. |
| R-06 | Integración | No depender de una API municipal ni de mapas contratada. Decisión de alcance: mapa externo como enlace de navegación; la ruta básica sigue disponible sin él. |
| R-07 | Confidencialidad | Repositorio público sin datos reales de vecinos ni credenciales. Derivada de la entrega pública y la regla de confidencialidad de la guía; usar datos sintéticos. |

## 4. Escenarios de atributos de calidad
Las metas siguientes son criterios de aceptación propuestos, no resultados de pruebas del MVP.

| ID | Atributo | Fuente | Estímulo | Entorno | Artefacto | Respuesta | Medida |
|---|---|---|---|---|---|---|---|
| EC-01 | Modificabilidad (QA-01) | Responsable municipal y desarrollador | Incorporar un distrito o una nueva regla de puntos | Desarrollo y ensayo previo al despliegue con pruebas de regresión | Distritos o Puntos, sus contratos y configuración | Configurar el distrito o añadir estrategia de puntos manteniendo contratos públicos | Cada cambio ≤ 16 horas-persona (2 jornadas de 8 h), 0 archivos modificados en otros módulos, 100 % de regresión aprobada |
| EC-02 | Fiabilidad (QA-02) | Celular del reciclador | Reenviar 100 veces la misma confirmación de recojo, incluidas 10 peticiones simultáneas | Operación normal con fallos intermitentes de red | Recolección y Puntos, transacción y restricciones únicas | Registrar un recojo y un abono; responder al duplicado con el resultado original | 1 recojo confirmado, 1 abono por identificador de recojo, 0 duplicados en 100 reintentos |
| EC-03 | Seguridad (QA-03) | Vecino autenticado | Intentar leer/modificar solicitudes y saldo de otro vecino, o usar funciones municipales | Operación normal con dos cuentas de prueba y tres roles | API, autorización y repositorios | Denegar acceso sin exponer ni cambiar datos ajenos; registrar el intento sin contenido sensible | 100 de 100 intentos ajenos denegados con 403/404; 0 datos expuestos y 0 cambios no autorizados |