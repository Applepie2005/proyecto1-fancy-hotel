# Revision funcional equivalente a Pull Request

## Alcance revisado

- Migracion a Python 3 en la ruta activa de la app.
- Nueva capa de datos MySQL con semillas reproducibles.
- Tarjetas guardadas enmascaradas.
- Calendario de disponibilidad.
- Forecast de demanda y reglas de precio para gerente.
- Cancelacion, modificacion, busqueda filtrada, confirmacion y resenas validadas.

## Checklist Reviewer

- [x] El codigo conserva Flask, AngularJS y MySQL.
- [x] El codigo original queda disponible como referencia.
- [x] Los endpoints de reportes y precios validan rol gerente.
- [x] La disponibilidad usa solapamiento real de fechas.
- [x] El API de tarjetas no devuelve CVV ni numero completo.
- [x] El forecast usa una formula explicable para la presentacion.

## Checklist QA

- [x] Login de cliente con `C0001` / `password`.
- [x] Login de gerente con `M0001` / `password`.
- [x] Busqueda de habitaciones con filtros por tipo y precio.
- [x] Calendario de disponibilidad por sede y mes.
- [x] Reserva con tarjeta guardada.
- [x] Confirmacion con codigo y bandeja local.
- [x] Modificacion de reserva con recalculo de costo.
- [x] Cancelacion con politica de reembolso.
- [x] Resena bloqueada si no hay estancia completada.
- [x] Reporte de forecast y regla de precios solo para gerente.
- [x] Cliente recibe 403 al consultar `/api/reports/demandForecast` sin rol gerente.

## Evidencia de pruebas automatizadas

```text
$ python -m pytest -q
....                                                                     [100%]
4 passed in 0.70s
```

(Requiere MySQL activo, p. ej. `docker compose up -d mysql`.)

## Riesgos abiertos

- Sin Docker/MySQL, pytest hace skip o falla al cargar la app; documentar en defensa si la maquina del evaluador no tiene contenedores.
- El correo real queda fuera del alcance; se demuestra con `Confirmation_Outbox`.
- No se implemento pasarela de pago real.
