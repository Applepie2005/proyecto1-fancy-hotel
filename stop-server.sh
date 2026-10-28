#!/usr/bin/env bash
ROOT="$(cd "$(dirname "$0")" && pwd)"
PIDFILE="$ROOT/.fancyhotel-server.pid"
if [ ! -f "$PIDFILE" ]; then
  echo "No hay PID guardado (.fancyhotel-server.pid)."
  exit 0
fi
pid="$(cat "$PIDFILE")"
if kill -0 "$pid" 2>/dev/null; then
  kill "$pid"
  echo "Servidor detenido (PID $pid)."
else
  echo "El proceso $pid ya no existe."
fi
rm -f "$PIDFILE"
