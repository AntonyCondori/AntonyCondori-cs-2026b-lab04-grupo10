# HU-01: Solicitar el recojo de residuos reciclables

Como vecino, quiero solicitar el recojo de mis residuos reciclables desde la aplicación ingresando mi dirección y el detalle de mis residuos, para que un reciclador pueda asignar mi solicitud a su ruta diaria.

**Criterios de aceptación:**

1. **Dado** que un vecino autenticado ingresa una dirección válida y al menos un detalle de residuo, **cuando** envía la solicitud, **entonces** la solicitud queda en estado PENDIENTE, se guarda en el sistema y se obtienen las coordenadas de la dirección mediante el servicio de mapas.
2. **Dado** que el vecino intenta enviar la solicitud, **cuando** el servicio de mapas no responde o la dirección es inválida, **entonces** la solicitud es RECHAZADA y se notifica al vecino del error de ubicación.
3. **Dado** que un vecino está creando una solicitud, **cuando** intenta enviarla sin agregar ningún detalle de los residuos (lista de residuos vacía o peso en 0), **entonces** el sistema muestra un error de validación y la solicitud no se procesa ni se guarda.