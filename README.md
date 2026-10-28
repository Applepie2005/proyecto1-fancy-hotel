# Fancy Hotel — Proyecto 1 DSaIA

Sistema de reservas en línea para **Fancy Hotel**, modernizado sobre el repositorio open source [thegrucoder/Hotel-Reservation-System](https://github.com/thegrucoder/Hotel-Reservation-System) (Flask + AngularJS + MySQL).

**Curso:** Tópicos Especiales II — Desarrollo asistido por IA (Prof. Regis Rivera)  
**Repositorio del grupo:** https://github.com/Applepie2005/proyecto1-fancy-hotel  
**Documento de entrega (entregar en campus):** [`docs/ENTREGA-Proyecto1-DSaIA.md`](docs/ENTREGA-Proyecto1-DSaIA.md)

---

## Inicio rápido (Docker — recomendado)

1. Inicia **Docker Desktop**.
2. En la raíz del proyecto:

```bash
chmod +x up.sh
./up.sh
```

3. Abre **http://127.0.0.1:5001**

4. Detener:

```bash
docker compose down
```

### Credenciales demo

| Rol | Usuario | Contraseña |
| --- | --- | --- |
| Cliente | `C0001` | `password` |
| Gerente | `M0001` | `password` |

---

## Desarrollo local (solo MySQL en Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d mysql
cd fancyhotel && python serve.py
```

Variables útiles: `FANCYHOTEL_PORT` (default `5001`), `FANCYHOTEL_DB_HOST`, `FANCYHOTEL_DB_PASSWORD`.

En macOS también puedes usar `FancyHotel.command` o `./start-server.sh` / `./stop-server.sh`.

---

## Pruebas automatizadas

```bash
source .venv/bin/activate
pip install -r requirements.txt
docker compose up -d mysql
python -m pytest -q
```

Las pruebas ejercitan la API con MySQL real. Si la base no está disponible, se **omiten** con un mensaje claro (no fallan por infraestructura).

Casos principales en `tests/test_api.py`:

- Login cliente y tarjetas enmascaradas (sin CVV ni PAN completo).
- Búsqueda con solapamiento de fechas (habitación ocupada excluida).
- Forecast de demanda accesible solo para gerente (`403` para cliente).

---

## Historias de usuario implementadas

### Obligatorias (enunciado)

1. **Pago con datos guardados** — tarjetas enmascaradas, reserva por últimos 4 dígitos.
2. **Calendario dinámico** — disponibilidad por sede y mes en la búsqueda de habitaciones.
3. **Previsión de demanda** — gráfico y tabla para gerentes; fórmula documentada en entrega.

### Adicionales (6)

4. Cancelación y modificación de reservas (política de reembolso, recálculo de costo).  
5. Filtros de búsqueda (tipo, precio máximo).  
6. Rol administrador con sesión y endpoints protegidos.  
7. Confirmación con código `FH-…` y bandeja local.  
8. Reseñas solo tras estancia completada.  
9. Reglas de precio por ocupación/demanda confirmadas por gerente.

Detalle, criterios de aceptación y ramas sugeridas: [`docs/historias-issues.md`](docs/historias-issues.md)

**Prioridades de entrega y matriz de evidencia (restricciones 1–10):** [`docs/prioridades-entrega.md`](docs/prioridades-entrega.md) · [`docs/evidencia-restricciones.md`](docs/evidencia-restricciones.md) · [`docs/github-issues-plantilla.md`](docs/github-issues-plantilla.md)

---

## Estructura del código

```
proyecto1-fancy-hotel/
├── docker-compose.yml      # MySQL + app web
├── Dockerfile
├── up.sh                   # Levantar stack completo
├── fancyhotel/
│   ├── serve.py            # Entrada Flask
│   ├── api_v2.py           # API activa (REST)
│   ├── api.py              # API original (referencia)
│   ├── db/
│   │   ├── repository.py   # MySQL, semillas, reglas de negocio
│   │   └── mysqldb.py      # Capa original (referencia)
│   ├── static/             # AngularJS, vistas *_v2, CSS
│   └── templates/index.html
├── tests/test_api.py
└── docs/                   # Entrega, IA, decisiones, presentación
```

---

## API REST (resumen)

| Método | Ruta | Descripción | Rol |
| --- | --- | --- | --- |
| POST | `/api/login` | Inicio de sesión | Público |
| POST | `/api/logout` | Cierre de sesión | Autenticado |
| POST | `/api/register` | Registro cliente (`C####`) | Público |
| GET | `/api/searchRoom` | Buscar habitaciones | Cliente |
| GET | `/api/availability/calendar` | Calendario mensual | Cliente |
| POST | `/api/reservation/create` | Crear reserva + código | Cliente |
| PUT | `/api/reservation` | Modificar reserva | Cliente |
| GET | `/api/reservation/<id>/cancel` | Cancelar | Cliente |
| GET/POST | `/api/payment` | Tarjetas guardadas | Cliente |
| POST | `/api/review` | Reseñas | Cliente |
| GET | `/api/reports/demandForecast` | Forecast | **Gerente** |
| GET/POST | `/api/price-rules` | Reglas de precio | **Gerente** |
| GET | `/api/confirmations` | Bandeja confirmaciones | **Gerente** |
| GET | `/api/reports/*` | Otros reportes | **Gerente** |

---

## Evidencia DSaIA (proceso, no solo código)

| Tema | Archivo |
| --- | --- |
| Análisis antes de tocar código | [`docs/analisis-inicial.md`](docs/analisis-inicial.md) |
| Log de uso de IA | [`docs/ai-development-log.md`](docs/ai-development-log.md) |
| Decisiones humanas | [`docs/decisiones.md`](docs/decisiones.md) |
| Revisión funcional (tipo PR) | [`docs/revisiones/revision-funcional.md`](docs/revisiones/revision-funcional.md) |
| Guion de presentación | [`docs/presentacion.md`](docs/presentacion.md) |
| **Paquete de entrega** | [`docs/ENTREGA-Proyecto1-DSaIA.md`](docs/ENTREGA-Proyecto1-DSaIA.md) |

Enunciado PDF: `fancyhotel/DSaIA-Proyecto1.pdf`

---

## Notas técnicas

- **Stack fijo:** no se migró a React/FastAPI para cumplir el requisito de trabajar sobre la aplicación existente.
- **Contraseñas:** hash Werkzeug en usuarios nuevos; demo `password` en semillas.
- **Registro:** validación `C` + 4 caracteres alfanuméricos (front `ng-pattern` + API); email y longitud mínima de contraseña en servidor.
- **Confirmaciones:** bandeja `Confirmation_Outbox` en lugar de SMTP para la demo en aula.

---

## Créditos

Proyecto base: CS 4400 Online Hotel Reservation System (Georgia Tech lineage).  
Modernización y historias DSaIA: grupo Fancy Hotel 4400 — ver commits en `main`.
