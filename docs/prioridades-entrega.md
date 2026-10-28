# Prioridades de entrega — Proyecto 1 DSaIA

Orden sugerido antes de la defensa. Lo marcado con ✅ ya está cubierto en el repositorio; ⚠️ requiere acción del grupo; 🔶 opcional pero suma puntos en proceso.

---

## Prioridad 1 — Bloqueantes de la rúbrica (restricciones 1–10)

| Orden | Restricción | Estado | Acción concreta |
| --- | --- | --- | --- |
| 1 | Repositorio Git | ✅ | Enlace: https://github.com/Applepie2005/proyecto1-fancy-hotel |
| 2 | Issues o historias | ⚠️ | Tabla en [`historias-issues.md`](historias-issues.md). **Acción:** copiar 9 issues desde [`github-issues-plantilla.md`](github-issues-plantilla.md) (~15 min) o adjuntar captura de la tabla en el PDF de entrega. |
| 3 | Commits identificables | ✅ | Mensajes `feat` / `fix` / `docs` / `chore`; ver matriz de trazabilidad. |
| 4 | Uso de ramas | ✅ | 12 ramas `feature/us-*` en local y `origin` (2026-10-28). Script: [`scripts/create-feature-branches.sh`](../scripts/create-feature-branches.sh) (bash 3.2). Captura: [`evidencia-capturas/07-github-pr-o-revision.png`](evidencia-capturas/07-github-pr-o-revision.png). |
| 5 | PR o revisión equivalente | ✅ parcial | [`revisiones/revision-funcional.md`](revisiones/revision-funcional.md) + ramas remotas (`07-github-pr-o-revision.png`). **Opcional:** PR `feature/us-docs-entrega` → `main` con ese checklist. |
| 6 | Pruebas automatizadas | ✅ | `tests/test_api.py` — 4 tests (ver salida en [`evidencia-restricciones.md`](evidencia-restricciones.md)). |
| 7–10 | IA + humanos | ✅ | [`ai-development-log.md`](ai-development-log.md) (tabla + incorrectas + rechazadas + resumen humano) + [`decisiones.md`](decisiones.md). Verificado 2026-10-28. |

---

## Prioridad 2 — Documento de entrega al campus

| Orden | Tarea | Estado |
| --- | --- | --- |
| 1 | Completar nombres y cédulas en [`ENTREGA-Proyecto1-DSaIA.md`](ENTREGA-Proyecto1-DSaIA.md) §1 | ⚠️ |
| 2 | Entregar PDF o enlace al repo según indique el profesor | ⚠️ |
| 3 | Revisar que `DSaIA-Proyecto1.pdf` / enunciado coincida con lo implementado | ✅ |

---

## Prioridad 3 — Demo y presentación (5–8 min)

| Orden | Tarea | Referencia |
| --- | --- | --- |
| 1 | `./up.sh` + Docker Desktop encendido | [`README.md`](../README.md) |
| 2 | Guión cliente + gerente | [`presentacion.md`](presentacion.md) |
| 3 | Cambio en vivo (umbrales forecast) | `fancyhotel/db/repository.py` → `demand_forecast()` |
| 4 | Mencionar 2 rechazos de IA (ML, PAN completo) | Log § incorrectas / rechazadas |

---

## Prioridad 4 — Calidad opcional

- Capturas en [`docs/evidencia-capturas/`](evidencia-capturas/README.md) — hecho (commitear PNG si el profesor pide repo completo).
- Diapositivas (Canva/PPT) enlazadas en §1 de ENTREGA.
- Issue en GitHub por cada US01–US09 con criterios de aceptación copiados de la tabla.

---

## Qué NO priorizar ahora

- Migrar a React/FastAPI (rechazado y fuera de enunciado).
- SMTP real (bandeja local es suficiente para demo).
- Más historias allá de US09 (ya hay 3 obligatorias + 6 adicionales).
