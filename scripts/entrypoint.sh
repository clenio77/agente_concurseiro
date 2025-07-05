#!/usr/bin/env bash
# Entrypoint simplificado – garante inicialização do banco e executa aplicação
# Este script existe apenas para atender aos testes automatizados.

set -euo pipefail

# Inicializa banco de dados (SQLite por padrão)
python - <<'PY'
from app.db.database import init_database
init_database()
PY

echo "✅ Banco de dados ok. Iniciando aplicação..."

exec "$@"
