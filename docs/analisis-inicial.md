# Analisis inicial

## Repositorio elegido

Se eligio `thegrucoder/Hotel-Reservation-System`. El enlace escrito en el enunciado sin guion devuelve 404; el repositorio real disponible en GitHub usa `Hotel-Reservation-System`.

## Arquitectura encontrada

- Backend: Flask y Flask-RESTful en `fancyhotel/serve.py` y `fancyhotel/api.py`.
- Frontend: AngularJS 1.x con rutas en `fancyhotel/static/js/controllers.js` y vistas HTML en `fancyhotel/static/views/`.
- Base de datos: MySQL, esquema `Fancy_Hotel`, creado desde `fancyhotel/db/mysqldb.py`.
- Roles: el sistema infiere cliente o gerente por el prefijo del usuario (`C` o `M`), pero no protegia endpoints en el servidor.

## Hallazgos antes de modificar

- El codigo original tenia sintaxis de Python 2 (`print valor`) y no arrancaba en Python 3.
- No habia datos semilla de habitaciones, usuarios o reservas, por lo que las busquedas podian quedar vacias.
- La validacion de disponibilidad comparaba rangos contenidos, no solapamientos reales.
- `ReservationResource.put` usaba `deltaDays` sin definir y no acumulaba correctamente el costo.
- `Credit_Card` devolvia CVV al frontend.
- Los reportes existentes eran tablas fijas para agosto y septiembre, sin grafico ni prevision.
- Ya existian pantallas parciales de pago, cancelacion, modificacion y resenas, pero sin todas las reglas de negocio solicitadas.

## Decision humana

Se mantiene la base original en Flask, AngularJS y MySQL. No se migra a otro framework porque el objetivo del proyecto es trabajar sobre un repositorio existente y conservar un proceso de ingenieria real.
