#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

if ! docker info >/dev/null 2>&1; then
  echo "Abre Docker Desktop y vuelve a ejecutar: ./up.sh"
  exit 1
fi

echo "Construyendo e iniciando MySQL + Fancy Hotel..."
docker compose up -d --build

echo "Esperando respuesta HTTP..."
for _ in $(seq 1 45); do
  if curl -sf -o /dev/null "http://127.0.0.1:5001/"; then
    echo ""
    echo "Listo: http://127.0.0.1:5001"
    echo "Login demo: C0001 / password"
    echo "Logs: docker compose logs -f web"
    echo "Detener: docker compose down"
    exit 0
  fi
  sleep 2
done

echo "ERROR: el contenedor web no respondió. Revisa:"
docker compose ps
docker compose logs web --tail 40
exit 1
