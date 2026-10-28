# AI Development Log

| Actividad | Herramienta IA | Que se solicito | Resultado | Decision humana |
| --- | --- | --- | --- | --- |
| Analisis inicial | Cursor | Analizar el repositorio elegido antes de modificar codigo | Detecto Flask, AngularJS, MySQL, Python 2 y errores de disponibilidad | Aceptada. Se documento en `docs/analisis-inicial.md`. |
| Arquitectura | Cursor | Proponer una forma de cumplir las historias sin reescribir la app | Sugirio crear una API modernizada y una capa de datos nueva | Aceptada parcialmente. Se mantuvo el codigo original como referencia y se apunto `serve.py` a `api_v2.py`. |
| Base local | Cursor | Hacer runnable el proyecto en Windows con MySQL | Propuso `requirements.txt`, `docker-compose.yml` y semillas | Aceptada. Se agregaron credenciales demo y tests. |
| Disponibilidad | Cursor | Revisar la consulta de disponibilidad | Identifico que la condicion original no detectaba solapamientos parciales | Aceptada. Se cambio a `checkin < checkout_buscado AND checkout > checkin_buscado`. |
| Forecast | Cursor | Crear prevision de demanda | Propuso usar un modelo predictivo complejo | Rechazada. Se uso media movil y promedio historico por mes por ser explicable en clase. |
| Seguridad de tarjetas | Cursor | Implementar tarjetas guardadas | Inicialmente podia devolver el numero completo para reservar | Rechazada. Se usan tarjetas enmascaradas y el backend resuelve por ultimos 4 digitos. |
| Testing | Cursor | Crear pruebas automatizadas | Genero pruebas de login, tarjeta enmascarada, disponibilidad y forecast | Aceptada. Quedan en `tests/test_api.py`. |
| Debug | Cursor | Ejecutar pruebas | Docker Desktop no estaba iniciado y MySQL no pudo levantarse | Se documento limitacion. Las pruebas saltan si MySQL no esta disponible. |

## Ejemplos de respuestas incorrectas de la IA

1. Proponer una red neuronal para la prevision de demanda. Era innecesaria, dificil de explicar y sin datos suficientes.
2. Recomendar devolver el numero completo de tarjeta al frontend para simplificar la reserva. Se rechazo por seguridad.
3. Intentar tratar el enlace `HotelReservation-System` como valido. Se verifico que el repositorio real usa `Hotel-Reservation-System`.

## Cambios rechazados de la IA

- Migrar a React o FastAPI. El proyecto exige modificar una aplicacion existente; se conservaron Flask y AngularJS.
- Automatizar ajuste de precios sin confirmacion humana. El gerente confirma cada regla.
- Usar correo SMTP obligatorio. Se dejo una bandeja local demostrable y SMTP queda opcional.
