Online Hotel Reservation System group project for CS 4400
---------------------------------------------------------
Download Mysql from [here]http://dev.mysql.com/downloads/mysql/

Download MySql Workbench from [here](http://dev.mysql.com/downloads/file/?id=459911)

Downlad MySql Community Server from [here](http://dev.mysql.com/downloads/file/?id=459870)

go to fancyhotel folder

run 'python serve.py' 

open 'localhost:5000' in the broswer 


We have to use MySql (per project requirements), going to use it with the MySQL connector for Python. 

UI won't get us any extra points, so feel free to do what you want, but don't waste your time on it if there are other things to do.

Things to be done:
* Create login abilities
* Carry logged-in account to do things
* Pretty much all requests, while being logged in
* regex to disallow bad input from registering users

Project 1 updated version
-------------------------

This repository was modernized for Proyecto 1 de Topicos Especiales II: desarrollo asistido por IA con herramientas de escritorio.

## Ejecutar localmente

1. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

2. Start MySQL:

```bash
docker compose up -d mysql
```

3. Start Flask:

```bash
cd fancyhotel
python serve.py
```

4. Open <http://localhost:5000>.

## Credenciales demo

- Cliente: `C0001` / `password`
- Gerente: `M0001` / `password`

## Pruebas

Run:

```bash
python -m pytest -q
```

The tests use the MySQL-backed Flask app. If Docker Desktop or MySQL is unavailable, they skip with an explicit reason.

## Historias implementadas

- Pago con datos guardados, devolviendo tarjetas enmascaradas y sin CVV.
- Calendario dinamico de disponibilidad por sede y mes.
- Grafico y tabla de prevision de demanda para gerentes.
- Cancelacion y modificacion de reservas.
- Filtros de busqueda por tipo y precio maximo.
- Rol administrador con reportes y precios protegidos por sesion.
- Confirmacion con codigo y bandeja local.
- Resenas permitidas solo tras una estancia finalizada.
- Reglas de precio por ocupacion confirmadas por gerente.
