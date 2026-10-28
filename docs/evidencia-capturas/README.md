# Capturas para la defensa

Generadas 2026-10-28 (app en `http://127.0.0.1:5001`). Referenciar en [`presentacion.md`](../presentacion.md).

| Archivo | Qué demuestra | Restricción |
| --- | --- | --- |
| `01-calendario-disponibilidad.png` | Búsqueda + calendario Atlanta (US02) | US02 |
| `02-forecast-gerente.png` | Previsión demanda como M0001 | US03 |
| `03-cliente-403-forecast.png` | API: `Manager role required` con C0001 | US03, US06 |
| `04-tarjetas-enmascaradas.png` | `************1111`, sin CVV en listado | US01 |
| `05-confirmacion-fh.png` | Outbox con código `FH-25491F5A` | US07 |
| `06-github-issues.png` | Issues abiertos = 0 (pendiente crear US01–US09) | Restricción 2 |
| `07-github-pr-o-revision.png` | Ramas `feature/us-*` en GitHub | Restricción 4–5 |

**Nota restricción 2:** mientras no existan issues en GitHub, usar junto con esta carpeta la tabla [`historias-issues.md`](../historias-issues.md) y la plantilla [`github-issues-plantilla.md`](../github-issues-plantilla.md).
