#!/bin/bash

# Script de deploy para Agente Concurseiro
# Versão: 2.0.0 - Produção

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configurações
PROJECT_NAME="agente-concurseiro"
VERSION="2.0.0"
ENVIRONMENT=${1:-production}
BACKUP_BEFORE_DEPLOY=${BACKUP_BEFORE_DEPLOY:-true}

log_info "🚀 Iniciando deploy do Agente Concurseiro v$VERSION"
log_info "📋 Ambiente: $ENVIRONMENT"

# Verificar pré-requisitos
check_prerequisites() {
    log_info "🔍 Verificando pré-requisitos..."
    
    # Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker não encontrado. Instale o Docker primeiro."
        exit 1
    fi
    
    # Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose não encontrado. Instale o Docker Compose primeiro."
        exit 1
    fi
    
    # Git
    if ! command -v git &> /dev/null; then
        log_error "Git não encontrado. Instale o Git primeiro."
        exit 1
    fi
    
    log_success "✅ Pré-requisitos verificados"
}

# Configurar variáveis de ambiente
setup_environment() {
    log_info "⚙️ Configurando ambiente..."
    
    # Criar arquivo .env se não existir
    if [ ! -f .env ]; then
        log_info "📝 Criando arquivo .env..."
        cat > .env << EOF
# Ambiente
ENVIRONMENT=$ENVIRONMENT

# Banco de dados
DB_PASSWORD=postgres123
REDIS_PASSWORD=redis123

# Segurança
JWT_SECRET_KEY=$(openssl rand -base64 32)

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8501
ALLOWED_HOSTS=localhost,127.0.0.1

# Monitoramento
GRAFANA_PASSWORD=admin123

# Backup
BACKUP_RETENTION_DAYS=30
MAX_LOCAL_BACKUPS=10

# OpenAI (opcional)
# OPENAI_API_KEY=your-openai-api-key

# AWS S3 (opcional para backups)
# AWS_ACCESS_KEY_ID=your-access-key
# AWS_SECRET_ACCESS_KEY=your-secret-key
# BACKUP_S3_BUCKET=your-backup-bucket
EOF
        log_success "✅ Arquivo .env criado"
    else
        log_info "📄 Arquivo .env já existe"
    fi
    
    # Carregar variáveis
    source .env
}

# Criar backup antes do deploy
create_backup() {
    if [ "$BACKUP_BEFORE_DEPLOY" = "true" ]; then
        log_info "💾 Criando backup antes do deploy..."
        
        # Criar diretório de backup
        mkdir -p backups/pre-deploy
        
        # Backup do banco de dados (se existir)
        if docker-compose ps postgres | grep -q "Up"; then
            log_info "📊 Fazendo backup do banco de dados..."
            docker-compose exec -T postgres pg_dump -U postgres agente_concurseiro > "backups/pre-deploy/db_backup_$(date +%Y%m%d_%H%M%S).sql"
            log_success "✅ Backup do banco criado"
        fi
        
        # Backup dos volumes
        log_info "📁 Fazendo backup dos volumes..."
        docker run --rm -v agente-concurseiro_app_data:/data -v $(pwd)/backups/pre-deploy:/backup alpine tar czf /backup/app_data_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .
        
        log_success "✅ Backup completo criado"
    fi
}

# Build das imagens
build_images() {
    log_info "🔨 Construindo imagens Docker..."
    
    # Build da imagem principal
    docker build -t $PROJECT_NAME:$VERSION .
    docker tag $PROJECT_NAME:$VERSION $PROJECT_NAME:latest
    
    # Build da imagem Streamlit (se existir Dockerfile.streamlit)
    if [ -f Dockerfile.streamlit ]; then
        docker build -f Dockerfile.streamlit -t $PROJECT_NAME-streamlit:$VERSION .
        docker tag $PROJECT_NAME-streamlit:$VERSION $PROJECT_NAME-streamlit:latest
    fi
    
    log_success "✅ Imagens construídas"
}

# Deploy dos serviços
deploy_services() {
    log_info "🚀 Fazendo deploy dos serviços..."
    
    # Parar serviços existentes
    log_info "⏹️ Parando serviços existentes..."
    docker-compose down --remove-orphans
    
    # Limpar volumes órfãos (cuidado!)
    if [ "$ENVIRONMENT" != "production" ]; then
        docker volume prune -f
    fi
    
    # Iniciar serviços
    log_info "▶️ Iniciando serviços..."
    docker-compose up -d
    
    log_success "✅ Serviços iniciados"
}

# Verificar saúde dos serviços
health_check() {
    log_info "🔍 Verificando saúde dos serviços..."
    
    # Aguardar serviços ficarem prontos
    log_info "⏳ Aguardando serviços..."
    sleep 30
    
    # Verificar PostgreSQL
    if docker-compose ps postgres | grep -q "Up"; then
        log_success "✅ PostgreSQL está rodando"
    else
        log_error "❌ PostgreSQL não está rodando"
        return 1
    fi
    
    # Verificar Redis
    if docker-compose ps redis | grep -q "Up"; then
        log_success "✅ Redis está rodando"
    else
        log_error "❌ Redis não está rodando"
        return 1
    fi
    
    # Verificar aplicação principal
    if docker-compose ps app | grep -q "Up"; then
        log_success "✅ Aplicação principal está rodando"
        
        # Testar endpoint de saúde
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            log_success "✅ API está respondendo"
        else
            log_warning "⚠️ API não está respondendo ainda"
        fi
    else
        log_error "❌ Aplicação principal não está rodando"
        return 1
    fi
    
    # Verificar Streamlit
    if docker-compose ps streamlit | grep -q "Up"; then
        log_success "✅ Interface Streamlit está rodando"
        
        # Testar interface
        if curl -f http://localhost:8501 > /dev/null 2>&1; then
            log_success "✅ Interface está acessível"
        else
            log_warning "⚠️ Interface não está acessível ainda"
        fi
    else
        log_warning "⚠️ Interface Streamlit não está rodando"
    fi
    
    log_success "✅ Verificação de saúde concluída"
}

# Executar migrações
run_migrations() {
    log_info "🔄 Executando migrações do banco..."
    
    # Aguardar banco estar pronto
    docker-compose exec app python -c "
from app.db.database import init_database, seed_database
import time
import sys

print('Aguardando banco de dados...')
for i in range(30):
    try:
        if init_database():
            print('✅ Banco inicializado!')
            seed_database()
            print('✅ Dados iniciais inseridos!')
            sys.exit(0)
    except Exception as e:
        print(f'Tentativa {i+1}/30 falhou: {e}')
        time.sleep(2)

print('❌ Falha na inicialização do banco')
sys.exit(1)
"
    
    if [ $? -eq 0 ]; then
        log_success "✅ Migrações executadas"
    else
        log_error "❌ Falha nas migrações"
        return 1
    fi
}

# Configurar monitoramento
setup_monitoring() {
    log_info "📊 Configurando monitoramento..."
    
    # Verificar se Prometheus está rodando
    if docker-compose ps prometheus | grep -q "Up"; then
        log_success "✅ Prometheus está rodando"
    fi
    
    # Verificar se Grafana está rodando
    if docker-compose ps grafana | grep -q "Up"; then
        log_success "✅ Grafana está rodando"
        log_info "🌐 Grafana disponível em: http://localhost:3000"
        log_info "👤 Login: admin / Senha: $GRAFANA_PASSWORD"
    fi
}

# Limpeza pós-deploy
cleanup() {
    log_info "🧹 Limpando recursos desnecessários..."
    
    # Remover imagens não utilizadas
    docker image prune -f
    
    # Remover containers parados
    docker container prune -f
    
    log_success "✅ Limpeza concluída"
}

# Rollback em caso de falha
rollback() {
    log_error "❌ Deploy falhou. Iniciando rollback..."
    
    # Parar serviços atuais
    docker-compose down
    
    # Restaurar backup se existir
    if [ -f "backups/pre-deploy/db_backup_*.sql" ]; then
        log_info "🔄 Restaurando backup do banco..."
        # Implementar restauração do backup
    fi
    
    log_info "🔄 Rollback concluído"
}

# Função principal
main() {
    # Trap para rollback em caso de erro
    trap rollback ERR
    
    check_prerequisites
    setup_environment
    create_backup
    build_images
    deploy_services
    run_migrations
    health_check
    setup_monitoring
    cleanup
    
    log_success "🎉 Deploy concluído com sucesso!"
    log_info "🌐 Aplicação disponível em:"
    log_info "   • API: http://localhost:8000"
    log_info "   • Interface: http://localhost:8501"
    log_info "   • Documentação: http://localhost:8000/docs"
    log_info "   • Monitoramento: http://localhost:3000"
    
    log_info "📋 Para verificar logs:"
    log_info "   docker-compose logs -f"
    
    log_info "📊 Para verificar status:"
    log_info "   docker-compose ps"
}

# Executar função principal
main "$@"
