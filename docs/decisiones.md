# Decisiones humanas

## Tecnologia

- Se mantuvo Flask, AngularJS y MySQL para respetar el repositorio existente.
- Se creo `api_v2.py` en vez de editar masivamente `api.py`, porque el archivo original queda como evidencia del punto de partida.
- Se creo `db/repository.py` en vez de modificar `db/mysqldb.py`, porque la version original mezcla Python 2, schema y consultas defectuosas.

## Seguridad y roles

- Las contrasenas nuevas se guardan con hash de Werkzeug.
- Las tarjetas se almacenan completas en base de datos para simular pago, pero el API solo devuelve `masked_number` y `last4`.
- CVV se guarda como hash y nunca se devuelve.
- Los reportes, forecast, confirmaciones y reglas de precio requieren sesion de gerente.

## Prevision de demanda

- Se rechazo entrenar un modelo complejo por falta de volumen de datos y por dificultad de explicacion.
- Se usa una regla explicable: ocupacion mensual historica y promedio movil de tres meses.
- La sugerencia de precio no modifica inventario ni precios automaticamente.

## Confirmaciones

- Se implemento bandeja local `Confirmation_Outbox` para demostrar confirmaciones sin depender de SMTP durante la presentacion.
- El codigo de confirmacion usa formato `FH-XXXXXXXX`.

## Pruebas y validacion

- Las pruebas automatizadas requieren MySQL real porque el proyecto usa MySQL desde el origen.
- Si MySQL no esta disponible, los tests se saltan con mensaje explicito en vez de fallar por infraestructura.
- Se documento que en esta maquina Docker Desktop no estaba iniciado durante la verificacion.
