#\!/bin/bash

# Entrypoint script para Agente Concurseiro
set -e

echo "🚀 Iniciando Agente Concurseiro..."

# Função para aguardar serviços
wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3
    
    echo "⏳ Aguardando $service_name ($host:$port)..."
    
    while \! nc -z $host $port; do
        echo "⏳ $service_name não está pronto. Aguardando..."
        sleep 2
    done
    
    echo "✅ $service_name está pronto\!"
}

# Executar migrações do banco
echo "🔄 Executando migrações do banco..."
python -c "
from app.db.database import init_database, seed_database
print('Inicializando banco...')
if init_database():
    print('✅ Banco inicializado\!')
    print('🌱 Populando dados iniciais...')
    seed_database()
    print('✅ Dados iniciais inseridos\!')
else:
    print('❌ Falha na inicialização\!')
    exit(1)
"

echo "✅ Inicialização concluída\!"
echo "🚀 Iniciando aplicação..."

# Executar comando passado como argumento
exec "$@"
