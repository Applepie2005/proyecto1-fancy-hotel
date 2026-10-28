# Historias de usuario e issues

Cada historia se desarrollo con una rama sugerida y criterios de aceptacion. Roles fijos: **Developer** David Bustamante, **Reviewer** Fernando Delgado, **QA** Allisson Ortega.

| Issue | Rama | Historia | Developer | Reviewer | QA | Criterios de aceptacion |
| --- | --- | --- | --- | --- | --- | --- |
| US01 | `feature/us-01-pago-guardado` | Como usuario recurrente, quiero reservar directamente usando mis datos guardados, para no tener que rellenar el formulario de pago en cada compra. | David Bustamante | Fernando Delgado | Allisson Ortega | La reserva lista tarjetas guardadas enmascaradas, no expone CVV y permite reservar usando los ultimos 4 digitos. |
| US02 | `feature/us-02-calendario-disponibilidad` | Como cliente, quiero ver un calendario dinamico con los dias disponibles y ocupados, para elegir mi fecha rapidamente sin intentos fallidos. | David Bustamante | Fernando Delgado | Allisson Ortega | La pantalla de reserva muestra disponibilidad diaria por sede con estados disponible/parcial/lleno. |
| US03 | `feature/us-03-prevision-demanda` | Como administrador del sistema, quiero ver graficos de prevision de la demanda basados en el historico, para ajustar los precios y el inventario de forma inteligente. | David Bustamante | Fernando Delgado | Allisson Ortega | El gerente ve forecast de ocupacion y grafico. Clientes reciben 403 en endpoints de reportes. |
| US04 | `feature/us-04-cancelar-modificar` | Como cliente, quiero cancelar o modificar una reserva existente, para ajustar mis planes sin contactar al administrador. | David Bustamante | Fernando Delgado | Allisson Ortega | Modificar recalcula costo y valida disponibilidad con solapamiento. Cancelar aplica politica de reembolso. |
| US05 | `feature/us-05-filtros-busqueda` | Como cliente, quiero filtrar habitaciones o servicios por fecha, precio y tipo, para encontrar una opcion sin revisar todo el catalogo. | David Bustamante | Fernando Delgado | Allisson Ortega | La busqueda filtra por sede, fechas, tipo y precio maximo. |
| US06 | `feature/us-06-rol-administrador` | Como administrador, quiero iniciar sesion con un rol distinto al del cliente, para que solo yo vea reportes y cambie precios. | David Bustamante | Fernando Delgado | Allisson Ortega | Login devuelve rol y Flask guarda sesion. Reportes y precios requieren rol `manager`. |
| US07 | `feature/us-07-confirmacion-reserva` | Como cliente, quiero recibir una confirmacion con codigo de reserva, para tener un comprobante de lo que reserve. | David Bustamante | Fernando Delgado | Allisson Ortega | Crear reserva genera `confirmation_code` y guarda mensaje en `Confirmation_Outbox`. |
| US08 | `feature/us-08-resenas-validadas` | Como cliente, quiero dejar una resena despues de mi estancia, para orientar a otros usuarios. | David Bustamante | Fernando Delgado | Allisson Ortega | Solo clientes con estancia finalizada y no cancelada en esa sede pueden publicar resena. |
| US09 | `feature/us-09-precios-demanda` | Como administrador, quiero ajustar precios por temporada o por ocupacion, para aplicar la prevision de demanda al inventario. | David Bustamante | Fernando Delgado | Allisson Ortega | El gerente crea reglas por sede, tipo y fechas. La busqueda usa el precio ajustado vigente. |

## Pruebas automatizadas

- `tests/test_api.py::test_customer_login_and_saved_cards_are_masked`
- `tests/test_api.py::test_search_uses_date_overlap_to_hide_booked_room`
- `tests/test_api.py::test_manager_can_get_demand_forecast`
- `tests/test_api.py::test_customer_cannot_access_demand_forecast`

## Credenciales demo

- Cliente: `C0001` / `password`
- Gerente: `M0001` / `password`
