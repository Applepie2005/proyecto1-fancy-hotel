#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PORT="${FANCYHOTEL_PORT:-5001}"
PY="$ROOT/.venv/bin/python"

mysql_ready() {
  "$PY" - <<'PY' 2>/dev/null
import os, mysql.connector
cfg = dict(
    host=os.environ.get("FANCYHOTEL_DB_HOST", "127.0.0.1"),
    port=int(os.environ.get("FANCYHOTEL_DB_PORT", "3306")),
    user=os.environ.get("FANCYHOTEL_DB_USER", "root"),
    password=os.environ.get("FANCYHOTEL_DB_PASSWORD", "password"),
)
mysql.connector.connect(**cfg).close()
PY
}

ensure_venv() {
  if [ ! -d .venv ]; then
    echo "Creando entorno virtual..."
    python3 -m venv .venv
    "$PY" -m pip install -r requirements.txt
  fi
  if ! "$PY" -c "import flask" 2>/dev/null; then
    echo "Instalando dependencias en .venv..."
    "$PY" -m pip install -r requirements.txt
  fi
}

ensure_venv

if mysql_ready; then
  echo "MySQL accesible."
elif docker info >/dev/null 2>&1; then
  echo "Levantando MySQL con Docker..."
  docker compose up -d mysql
  echo "Esperando MySQL (hasta ~60 s)..."
  ok=0
  for _ in $(seq 1 30); do
    if mysql_ready; then
      ok=1
      break
    fi
    sleep 2
  done
  if [ "$ok" -ne 1 ]; then
    echo "ERROR: MySQL no respondió. Revisa: docker logs fancyhotel-mysql"
    exit 1
  fi
else
  echo "ERROR: No hay MySQL en 127.0.0.1:3306 y Docker no está corriendo."
  echo "Abre Docker Desktop y ejecuta de nuevo: ./run.sh"
  exit 1
fi

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "ERROR: El puerto $PORT ya está en uso. Cierra el otro proceso o usa:"
  echo "  FANCYHOTEL_PORT=5002 ./run.sh"
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN || true
  exit 1
fi

cd fancyhotel
echo ""
echo "=============================================="
echo "  Fancy Hotel en http://127.0.0.1:$PORT"
echo "  NO cierres esta ventana mientras navegas."
echo "  Usa el venv: $PY serve.py"
echo "=============================================="
echo ""
exec "$PY" serve.py
