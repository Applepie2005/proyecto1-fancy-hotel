# Plantilla — Issues en GitHub (US01–US09)

Copiar cada bloque como **New issue** en https://github.com/Applepie2005/proyecto1-fancy-hotel/issues  
Etiquetas sugeridas: `historia`, `US0X` (si el repo tiene labels).

---

## US01 — Pago con datos guardados

**Como** usuario recurrente **quiero** reservar con tarjetas guardadas **para** no rellenar el formulario de pago en cada compra.

**Rama sugerida:** `feature/us-01-pago-guardado`

**Criterios de aceptación**

- [ ] La API lista tarjetas con `masked_number` y `last4`; no expone CVV ni PAN completo.
- [ ] La reserva acepta `card_last4` y el backend resuelve la tarjeta del usuario.
- [ ] Prueba: `tests/test_api.py::test_customer_login_and_saved_cards_are_masked`

---

## US02 — Calendario de disponibilidad

**Como** cliente **quiero** un calendario dinámico **para** elegir fechas sin intentos fallidos.

**Rama sugerida:** `feature/us-02-calendario-disponibilidad`

**Criterios de aceptación**

- [ ] Por sede y mes: estados `available`, `partial`, `full`.
- [ ] Endpoint `GET /api/availability/calendar`.
- [ ] UI en `searchRoom_v2.html`.

---

## US03 — Previsión de demanda

**Como** administrador **quiero** gráficos de previsión **para** ajustar precios e inventario.

**Rama sugerida:** `feature/us-03-prevision-demanda`

**Criterios de aceptación**

- [ ] Gerente accede a forecast; cliente recibe 403.
- [ ] Fórmula explicable (histórico + promedio móvil), no ML opaco.
- [ ] Pruebas: `test_manager_can_get_demand_forecast`, `test_customer_cannot_access_demand_forecast`

---

## US04 — Cancelar o modificar reserva

**Rama sugerida:** `feature/us-04-cancelar-modificar`

**Criterios de aceptación**

- [ ] Modificar recalcula costo y valida solapamiento de fechas.
- [ ] Cancelar aplica política de reembolso documentada en UI.

---

## US05 — Filtros de búsqueda

**Rama sugerida:** `feature/us-05-filtros-busqueda`

**Criterios de aceptación**

- [ ] Filtros por sede, fechas, tipo de habitación y precio máximo.

---

## US06 — Rol administrador

**Rama sugerida:** `feature/us-06-rol-administrador`

**Criterios de aceptación**

- [ ] Login devuelve `role`; sesión Flask en rutas protegidas.
- [ ] Reportes y precios requieren rol `manager`.

---

## US07 — Confirmación con código

**Rama sugerida:** `feature/us-07-confirmacion-reserva`

**Criterios de aceptación**

- [ ] Código `FH-XXXXXXXX` al crear reserva.
- [ ] Registro en `Confirmation_Outbox` (bandeja local).

---

## US08 — Reseñas validadas

**Rama sugerida:** `feature/us-08-resenas-validadas`

**Criterios de aceptación**

- [ ] Solo estancia completada y no cancelada en la sede permite reseña.

---

## US09 — Precios por demanda

**Rama sugerida:** `feature/us-09-precios-demanda`

**Criterios de aceptación**

- [ ] Gerente crea reglas por sede, tipo y rango de fechas.
- [ ] La búsqueda aplica el precio ajustado vigente.

---

## Cierre del requisito “Issues”

Tras crear los 9 issues, enlazar en [`ENTREGA-Proyecto1-DSaIA.md`](ENTREGA-Proyecto1-DSaIA.md) §5 una fila “Issues GitHub” con el rango `#1–#9` o la URL del filtro `label:historia`.
