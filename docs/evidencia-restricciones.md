# Evidencia — Restricciones del Proyecto 1

Documento para la defensa: enlaza cada requisito del enunciado con artefactos verificables en GitHub y en el árbol local.

**Repositorio:** https://github.com/Applepie2005/proyecto1-fancy-hotel  
**Última verificación local de pruebas:** 2026-10-28 — `4 passed in 0.69s` (`python -m pytest -q`, MySQL vía Docker).

---

## 1. Repositorio Git

- Remoto público configurado; clon desde `Applepie2005/proyecto1-fancy-hotel`.
- Estructura documentada en [`README.md`](../README.md).

---

## 2. Issues o historias de usuario

| Fuente | Ubicación |
| --- | --- |
| Tabla US01–US09 con criterios, roles y ramas sugeridas | [`historias-issues.md`](historias-issues.md) |
| Resumen en paquete de entrega | [`ENTREGA-Proyecto1-DSaIA.md`](ENTREGA-Proyecto1-DSaIA.md) §4 |

**Gap conocido:** issues aún no creados en GitHub. **Cierre rápido:** [`github-issues-plantilla.md`](github-issues-plantilla.md) (texto listo por US). Alternativa: entregar [`historias-issues.md`](historias-issues.md) como historias equivalentes + captura en [`evidencia-capturas/`](evidencia-capturas/README.md).

---

## 3. Commits identificables

| Commit | Mensaje | Relación con el trabajo |
| --- | --- | --- |
| `6cab9d9` | add | Importación inicial del fork |
| `e69024f` | Document project setup and acceptance tests | README, pytest inicial |
| `6aead48` | Implement Flask APIs for reservation stories | `api_v2.py`, `repository.py` — núcleo US01–US09 en backend |
| `4b72e6a` | Add reservation and manager UI flows | Vistas `*_v2.html`, `controllers_v2.js` |
| `9d417d1` | Document AI usage and human review evidence | Log IA, decisiones, revisión funcional |
| `aa835e5` | Ignore generated Python artifacts | Higiene Git |
| `293c79c` | chore(infra): Docker web stack and local run scripts | Reproducibilidad demo |
| `f490e2d` | feat(ui): modernize Spanish client and manager experience | UI Fancy Hotel 4400 |
| `9df4145` | fix(api): scope request parsers and registration rules | Endurecimiento registro + tests |
| `1f4a4e3` | docs: DSaIA delivery package | ENTREGA, guías |
| `1d00962` | docs(design): product scope and design system | PRODUCT.md, DESIGN.md |

---

## 4. Uso de ramas

Rama activa en remoto: **`main`**.

Ramas **planificadas por historia** (flujo de equipo documentado):

| Historia | Rama sugerida |
| --- | --- |
| US01 | `feature/us-01-pago-guardado` |
| US02 | `feature/us-02-calendario-disponibilidad` |
| … | … |
| US09 | `feature/us-09-precios-demanda` |

**Estado 2026-10-28:** 12 ramas `feature/us-*` en `origin` (US01–US09 @ `6aead48`, UI @ `4b72e6a`, infra @ `293c79c`, docs @ `1f4a4e3`). Captura: [`evidencia-capturas/07-github-pr-o-revision.png`](evidencia-capturas/07-github-pr-o-revision.png). Recrear en otra máquina: [`scripts/create-feature-branches.sh`](../scripts/create-feature-branches.sh) (compatible bash 3.2).

---

## 5. Pull Request o revisión equivalente

| Artefacto | Enlace |
| --- | --- |
| Checklist Reviewer + QA, riesgos | [`revisiones/revision-funcional.md`](revisiones/revision-funcional.md) |
| Decisiones revisadas en revisión | [`decisiones.md`](decisiones.md) |

Equivalente a PR: revisión por pares documentada con checklists marcados y alcance explícito. Evidencia visual de ramas en remoto: [`evidencia-capturas/07-github-pr-o-revision.png`](evidencia-capturas/07-github-pr-o-revision.png).

**Capturas funcionales (demo):** [`evidencia-capturas/README.md`](evidencia-capturas/README.md) (calendario, forecast, 403, tarjetas, confirmación).

---

## 6. Pruebas automatizadas

**Archivo:** [`tests/test_api.py`](../tests/test_api.py)

| Test | Historia / regla de negocio |
| --- | --- |
| `test_customer_login_and_saved_cards_are_masked` | US01, US06 — rol cliente, tarjetas enmascaradas |
| `test_search_uses_date_overlap_to_hide_booked_room` | US02, US04 — solapamiento de fechas |
| `test_manager_can_get_demand_forecast` | US03 — forecast gerente |
| `test_customer_cannot_access_demand_forecast` | US03, US06 — 403 cliente |

**Ejecución:**

```bash
docker compose up -d mysql
source .venv/bin/activate && pip install -r requirements.txt
python -m pytest -q
```

**Salida registrada (entorno local):** `4 passed in 0.70s`

---

## 7. Evidencia del uso de IA

Registro principal: [`ai-development-log.md`](ai-development-log.md) (plantilla del curso: Actividad, Herramienta, Qué se solicitó, Resultado, Decisión humana).

Herramienta declarada: **Cursor** (agente de escritorio).

---

## 8. Ejemplos de respuestas incorrectas de la IA

Ver sección homónima en [`ai-development-log.md`](ai-development-log.md) (ML para forecast, PAN completo al frontend, URL incorrecta del repo base).

---

## 9. Cambios rechazados de la IA

Ver sección “Cambios rechazados” en [`ai-development-log.md`](ai-development-log.md) (React/FastAPI, precios automáticos sin gerente, SMTP obligatorio).

---

## 10. Decisiones tomadas por humanos

Documento dedicado: [`decisiones.md`](decisiones.md) (stack, seguridad, forecast explicable, confirmaciones, pruebas con MySQL real).

---

## Trazabilidad historia → código → prueba

| ID | Evidencia backend / datos | Evidencia UI | Prueba automatizada |
| --- | --- | --- | --- |
| US01 | `repository.py` pagos, `last4` | `payment_v2.html` | `test_customer_login_and_saved_cards_are_masked` |
| US02 | `calendar_availability` | `searchRoom_v2.html` | overlap en búsqueda |
| US03 | `demand_forecast()` | `demandForecast.html` | forecast + 403 |
| US04 | modificar/cancelar reserva | `updateReservation_v2.html`, `cancelReservation_v2.html` | overlap |
| US05 | filtros en búsqueda | `searchRoom_v2.html` | manual QA checklist |
| US06 | sesión Flask, roles | login, rutas gerente | login + 403 |
| US07 | `Confirmation_Outbox` | `confirmations.html` | manual QA |
| US08 | validación estancia | `writeReview_v2.html` | manual QA |
| US09 | reglas de precio | `pricing.html` | manual QA |
