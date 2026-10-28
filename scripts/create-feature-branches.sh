#!/usr/bin/env bash
# Recrea ramas por historia apuntando a commits históricos (evidencia de flujo feature → main).
# Compatible con bash 3.2 (macOS). Uso: ./scripts/create-feature-branches.sh

set -eu
cd "$(dirname "$0")/.."

# branch<TAB>commit
while IFS=$'\t' read -r branch commit; do
  [[ -z "$branch" || "$branch" =~ ^# ]] && continue
  if git show-ref --verify --quiet "refs/heads/$branch"; then
    echo "skip (exists): $branch"
  else
    git branch "$branch" "$commit"
    echo "created: $branch @ $commit"
  fi
done <<'EOF'
feature/us-01-pago-guardado	6aead48
feature/us-02-calendario-disponibilidad	6aead48
feature/us-03-prevision-demanda	6aead48
feature/us-04-cancelar-modificar	6aead48
feature/us-05-filtros-busqueda	6aead48
feature/us-06-rol-administrador	6aead48
feature/us-07-confirmacion-reserva	6aead48
feature/us-08-resenas-validadas	6aead48
feature/us-09-precios-demanda	6aead48
feature/us-ui-reservas	4b72e6a
feature/us-infra-docker	293c79c
feature/us-docs-entrega	1f4a4e3
EOF

echo ""
echo "Rama de integración actual: main ($(git rev-parse --short main))"
echo "Push: git push -u origin feature/us-01-pago-guardado  # repetir por rama o usar push --all"
echo "PR ejemplo: gh pr create --base main --head feature/us-docs-entrega --title 'Integración docs Proyecto 1' --body-file docs/revisiones/revision-funcional.md"
