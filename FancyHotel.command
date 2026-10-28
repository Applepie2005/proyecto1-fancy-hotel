#!/usr/bin/env bash
cd "$(dirname "$0")"
chmod +x up.sh 2>/dev/null || true
./up.sh
echo ""
read -r -p "Pulsa Enter para cerrar (los contenedores siguen en Docker)."
