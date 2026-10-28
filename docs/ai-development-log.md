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
| UI / marca | Cursor | Modernizar interfaz sin cambiar AngularJS | Propuso rail lateral, vistas en espanol y tokens Fancy Hotel 4400 | Aceptada parcialmente. Se revisaron textos y flujos; no se cambio el stack. |
| Infra Docker | Cursor | Empaquetar app + MySQL para demo en clase | `docker-compose.yml`, `Dockerfile`, scripts `up.sh` / `run.sh` | Aceptada. Puerto 5001 y variables documentadas en README. |
| Registro API | Cursor | Endurecer registro de usuarios | Genero parsers por endpoint y validacion de email | Aceptada con ajustes manuales en mensajes de error y codigos HTTP. |
| Documentacion entrega | Cursor | Armar paquete DSaIA (restricciones 1-10) | ENTREGA, matriz de evidencia, prioridades | Aceptada. Grupo: David Bustamante, Allisson Ortega, Fernando Delgado (ENTREGA §1). |
| Diseno producto | Cursor | Capturar alcance y design system | PRODUCT.md, DESIGN.md, guia de tokens | Aceptada como soporte de presentacion; no es criterio CS 4400 original. |
| Capa de datos | Cursor | Reescribir consultas MySQL y semillas | `db/repository.py` con solapamiento, forecast, reglas de precio | Aceptada. Se dejo `mysqldb.py` intacto como contraste con Python 2. |
| Sesion y roles | Cursor | Proteger endpoints de gerente | Decoradores / comprobacion de rol en `api_v2.py` | Aceptada. QA manual: cliente 403 en `/api/reports/demandForecast`. |
| Politica de precios sugeridos | Cursor | Traducir forecast a accion comercial | Umbrales 60%/80% → `+8%`, `+15%`, `0%` en `demand_forecast()` | Aceptada con ajuste humano: solo sugerencia textual, sin aplicar precios solos. |
| Entrega DSaIA | Cursor | Prioridades, matriz restricciones 1–10, ampliar log IA | `prioridades-entrega.md`, `evidencia-restricciones.md`, plantilla issues | Aceptada. Issues en GitHub siguen opcionales; integrantes identificados en ENTREGA §1. |
| Revision de trazabilidad | Cursor | Verificar US → codigo → pytest | Tabla en `evidencia-restricciones.md`; 4 tests en verde (MySQL Docker) | Aceptada. US05, US07–US09 siguen con QA manual documentado en revision funcional. |

## Ejemplos de respuestas incorrectas de la IA

1. Proponer una red neuronal para la prevision de demanda. Era innecesaria, dificil de explicar y sin datos suficientes.
2. Recomendar devolver el numero completo de tarjeta al frontend para simplificar la reserva. Se rechazo por seguridad.
3. Intentar tratar el enlace `HotelReservation-System` como valido. Se verifico que el repositorio real usa `Hotel-Reservation-System`.
4. Sugerir reemplazar todos los `window.alert` en ingles sin revisar controladores v2. Parte de los mensajes quedaron en ingles en rutas secundarias; se corrigio lo visible en demo (login/registro) y se dejo mejora como deuda menor.
5. Proponer eliminar `api.py` y `mysqldb.py` para "limpiar" el repo. Se rechazo: el enunciado pide partir de codigo existente y conservar evidencia del antes/despues.
6. Sugerir mocks in-memory de MySQL para “evitar Docker”. Se rechazo: el proyecto original es MySQL; los tests usan skip explicito si la BD no levanta, no una BD falsa que oculte regresiones SQL.
7. Proponer aplicar automaticamente `price_suggestion` del forecast sobre `Room.price`. Se rechazo: US09 exige reglas confirmadas por el gerente en `Price_Rule`, no un batch nocturno opaco.
8. Diagnosticar “403 en forecast” como bug de CORS. Era control de acceso por rol; la prueba `test_customer_cannot_access_demand_forecast` lo fija como comportamiento esperado.

## Cambios rechazados de la IA

- Migrar a React o FastAPI. El proyecto exige modificar una aplicacion existente; se conservaron Flask y AngularJS.
- Automatizar ajuste de precios sin confirmacion humana. El gerente confirma cada regla.
- Usar correo SMTP obligatorio. Se dejo una bandeja local demostrable y SMTP queda opcional.
- Sustituir AngularJS por un SPA moderno “para impresionar en la demo”. Fuera de alcance y contradice el enunciado de modificar el repo existente.
- Unificar `api.py` y `api_v2.py` borrando la version antigua. Se mantienen ambos: trazabilidad del antes/despues para la defensa.
- Generar 20+ tests E2E con Selenium sin tiempo de CI. Se priorizaron 4 pruebas de API que cubren historias obligatorias y reglas de seguridad.

## Decisiones humanas (resumen rapido)

| Tema | Que decidio el grupo | Donde se ve |
| --- | --- | --- |
| Stack | Flask + AngularJS + MySQL | `serve.py`, vistas `*_v2.html` |
| Forecast | Media movil + mismo mes historico, sin ML | `repository.py` → `demand_forecast()` |
| Tarjetas | PAN en BD demo; API solo enmascarado + last4 | `get_credit_cards`, tests de payment |
| Integracion Git | Commits por capa en `main`; ramas US documentadas | `historias-issues.md`, script `scripts/create-feature-branches.sh` |
| Proceso IA | Registrar prompts que cambiaron el producto, no cada autocompletado | Este archivo + [`decisiones.md`](decisiones.md) |

Detalle extendido: [`decisiones.md`](decisiones.md).
