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

## Proceso de equipo (DSaIA)

| Decision | Motivo | Evidencia |
| --- | --- | --- |
| Historias US01–US09 con roles fijos (Developer David, Reviewer Fernando, QA Allisson) | Equivalente planificado a issues de GitHub | [`historias-issues.md`](historias-issues.md) |
| Revision por pares sin PR mergeado en remoto | Tiempo de integracion; checklist formal sustituye el hilo de PR | [`revisiones/revision-funcional.md`](revisiones/revision-funcional.md) |
| Commits identificables por capa (API → UI → infra → docs) | Facilita demo de “commits identificables” aunque `main` sea la rama visible | [`evidencia-restricciones.md`](evidencia-restricciones.md) §3 |
| Log de IA solo para interacciones que alteraron diseno o codigo | Alineado con la plantilla del curso (no registrar cada prompt) | [`ai-development-log.md`](ai-development-log.md) |
| Plantilla para crear 9 issues en GitHub antes de entregar | Cierra gap de restriccion 2 sin reescribir historias | [`github-issues-plantilla.md`](github-issues-plantilla.md) |

## Cambios humanos sobre salida de Cursor (ejemplos concretos)

1. **Umbrales de sugerencia de precio** en forecast: la IA propuso varias escalas; el grupo fijo 60% y 80% de ocupacion predicha para coherencia con la narrativa de demo.
2. **Mensajes de registro**: se ajustaron textos de error en espanol y codigos HTTP tras la primera version generada de parsers en `api_v2.py` (commit `9df4145`).
3. **Enmascarado de tarjeta**: formato fijo `************` + `last4` en lugar de mostrar BIN o longitud variable sugerida por la IA.
4. **Skip de pytest**: decision explicita de no fallar el CI local cuando MySQL no corre; preferible a mocks que no ejecutarian las consultas reales.
