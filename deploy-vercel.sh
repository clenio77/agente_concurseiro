#!/bin/bash

# ===================================
# SCRIPT DE DEPLOY PARA VERCEL
# Agente Concurseiro v2.0
# ===================================

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções de log
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════╗"
echo "║     🚀 DEPLOY VERCEL - AGENTE        ║"
echo "║        CONCURSEIRO v2.0              ║"
echo "╚══════════════════════════════════════╝"
echo -e "${NC}"

# Verificar se está no diretório correto
if [ ! -f "streamlit_app.py" ]; then
    log_error "Arquivo streamlit_app.py não encontrado!"
    log_info "Execute este script no diretório raiz do projeto"
    exit 1
fi

# Verificar dependências
log_info "Verificando dependências..."

# Verificar se Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    log_warning "Vercel CLI não encontrado. Instalando..."
    npm install -g vercel
    log_success "Vercel CLI instalado!"
fi

# Verificar se Node.js está instalado
if ! command -v node &> /dev/null; then
    log_error "Node.js não encontrado! Instale Node.js primeiro."
    exit 1
fi

# Preparar arquivos para deploy
log_info "Preparando arquivos para deploy..."

# Copiar requirements otimizado
if [ -f "requirements-vercel.txt" ]; then
    cp requirements-vercel.txt requirements.txt
    log_success "Requirements otimizado copiado"
else
    log_warning "requirements-vercel.txt não encontrado, usando requirements.txt existente"
fi

# Verificar arquivos essenciais
REQUIRED_FILES=(
    "streamlit_app.py"
    "vercel.json"
    "vercel_config.py"
    "vercel_optimizations.py"
    "requirements.txt"
    ".streamlit/config.toml"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        log_success "✓ $file"
    else
        log_error "✗ $file não encontrado!"
        exit 1
    fi
done

# Verificar se app/utils/edital_analyzer.py existe
if [ ! -f "app/utils/edital_analyzer.py" ]; then
    log_error "app/utils/edital_analyzer.py não encontrado!"
    log_info "Este arquivo é essencial para o funcionamento da aplicação"
    exit 1
fi

# Criar .vercelignore se não existir
if [ ! -f ".vercelignore" ]; then
    log_info "Criando .vercelignore..."
    cat > .vercelignore << EOF
# Arquivos desnecessários para Vercel
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git/
.mypy_cache/
.pytest_cache/
.hypothesis/

# Arquivos locais
data/
logs/
backups/
*.db
*.sqlite
*.sqlite3

# Arquivos de desenvolvimento
.env.local
.env.development
debug_*.py
test_*.py
tests/

# Arquivos grandes
*.tar.gz
*.zip
*.pdf

# Arquivos específicos do projeto
app.db
agente-concurseiro-*.tar.gz
requirements-dev.txt
docker-compose.yml
Dockerfile
EOF
    log_success ".vercelignore criado"
fi

# Configurar variáveis de ambiente
log_info "Configurando variáveis de ambiente..."

echo ""
log_warning "IMPORTANTE: Configure as seguintes variáveis no Vercel:"
echo ""
echo "1. 🗄️  DATABASE_URL (obrigatório)"
echo "   Exemplo: postgresql://user:pass@host:5432/db"
echo ""
echo "2. 🤖 OPENAI_API_KEY (opcional)"
echo "   Para funcionalidades de IA"
echo ""
echo "3. 🔧 ENVIRONMENT (opcional)"
echo "   Valor: production"
echo ""

read -p "Pressione Enter para continuar com o deploy..."

# Fazer login no Vercel (se necessário)
log_info "Verificando login no Vercel..."
if ! vercel whoami &> /dev/null; then
    log_info "Fazendo login no Vercel..."
    vercel login
fi

# Deploy
log_info "Iniciando deploy no Vercel..."

# Deploy de produção
if vercel --prod; then
    log_success "🎉 Deploy realizado com sucesso!"
    echo ""
    log_info "🔗 Sua aplicação estará disponível em breve"
    log_info "📊 Acesse o dashboard: https://vercel.com/dashboard"
    echo ""
    
    # Instruções pós-deploy
    echo -e "${YELLOW}"
    echo "📋 PRÓXIMOS PASSOS:"
    echo "1. Configure as variáveis de ambiente no dashboard do Vercel"
    echo "2. Teste a aplicação na URL fornecida"
    echo "3. Configure um banco PostgreSQL (Supabase recomendado)"
    echo "4. Monitore os logs em caso de problemas"
    echo -e "${NC}"
    
else
    log_error "Falha no deploy!"
    echo ""
    log_info "💡 DICAS PARA RESOLVER PROBLEMAS:"
    echo "1. Verifique se todos os arquivos estão presentes"
    echo "2. Confirme se as dependências estão corretas"
    echo "3. Verifique os logs do Vercel para mais detalhes"
    echo "4. Execute 'vercel logs' para ver erros específicos"
    exit 1
fi

# Limpeza
log_info "Limpando arquivos temporários..."
# Restaurar requirements original se necessário
if [ -f "requirements-vercel.txt" ] && [ -f "requirements-original.txt" ]; then
    mv requirements-original.txt requirements.txt
    log_success "Requirements original restaurado"
fi

log_success "🚀 Deploy concluído!"
echo ""
echo -e "${GREEN}Obrigado por usar o Agente Concurseiro v2.0!${NC}"
