#!/usr/bin/env bash
# Arranca Fancy Hotel en segundo plano (para que curl/navegador funcionen en otra terminal).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"
PORT="${FANCYHOTEL_PORT:-5001}"
PIDFILE="$ROOT/.fancyhotel-server.pid"
LOG="$ROOT/fancyhotel-server.log"
PY="$ROOT/.venv/bin/python"

if [ -f "$PIDFILE" ]; then
  oldpid="$(cat "$PIDFILE")"
  if kill -0 "$oldpid" 2>/dev/null; then
    echo "El servidor ya está corriendo (PID $oldpid)."
    echo "URL: http://127.0.0.1:$PORT"
    echo "Log: $LOG"
    exit 0
  fi
  rm -f "$PIDFILE"
fi

if lsof -nP -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
  echo "ERROR: puerto $PORT ocupado."
  lsof -nP -iTCP:"$PORT" -sTCP:LISTEN || true
  exit 1
fi

if [ ! -x "$PY" ]; then
  echo "Ejecuta primero: ./run.sh (una vez) para crear .venv, o:"
  echo "  python3 -m venv .venv && .venv/bin/pip install -r requirements.txt"
  exit 1
fi

# MySQL + venv (misma lógica que run.sh, sin bloquear)
if ! "$PY" -c "import mysql.connector; mysql.connector.connect(host='127.0.0.1',port=3306,user='root',password='password').close()" 2>/dev/null; then
  if docker info >/dev/null 2>&1; then
    docker compose up -d mysql
    for _ in $(seq 1 30); do
      if "$PY" -c "import mysql.connector; mysql.connector.connect(host='127.0.0.1',port=3306,user='root',password='password').close()" 2>/dev/null; then
        break
      fi
      sleep 2
    done
  else
    echo "ERROR: MySQL no disponible. Abre Docker Desktop y vuelve a intentar."
    exit 1
  fi
fi

cd "$ROOT/fancyhotel"
FANCYHOTEL_DEBUG=0 FANCYHOTEL_RELOAD=0 nohup "$PY" serve.py >>"$LOG" 2>&1 &
echo $! >"$PIDFILE"
sleep 2

if ! kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "ERROR: el servidor no arrancó. Revisa el log:"
  tail -30 "$LOG"
  rm -f "$PIDFILE"
  exit 1
fi

if ! curl -sf -o /dev/null "http://127.0.0.1:$PORT/"; then
  echo "ERROR: proceso vivo pero no responde HTTP. Log:"
  tail -30 "$LOG"
  exit 1
fi

echo "Servidor OK en http://127.0.0.1:$PORT (PID $(cat "$PIDFILE"))"
echo "Log: $LOG"
echo "Detener: ./stop-server.sh"
