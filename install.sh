#!/bin/bash

# Script de instalação do Agente Concurseiro
# Versão: 2.0.0

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

# Banner
echo -e "${BLUE}"
cat << "EOF"
    ___                    __           ______                                   _           
   /   |  ____ ____  ____  / /____      / ____/___  ____  _______  ______________(_)___  
  / /| | / __ `/ _ \/ __ \/ __/ _ \    / /   / __ \/ __ \/ ___/ / / / ___/ ___/ _ \/ / __ \ 
 / ___ |/ /_/ /  __/ / / / /_/  __/   / /___/ /_/ / / / / /__/ /_/ / /  (__  )  __/ / /_/ / 
/_/  |_|\__, /\___/_/ /_/\__/\___/    \____/\____/_/ /_/\___/\__,_/_/  /____/\___/_/\____/  
       /____/                                                                               
EOF
echo -e "${NC}"

log_info "🚀 Instalando Agente Concurseiro v2.0.0"
log_info "📋 Sistema completo de preparação para concursos públicos"

# Verificar Python
check_python() {
    log_info "🐍 Verificando Python..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 não encontrado. Instale Python 3.8+ primeiro."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    REQUIRED_VERSION="3.8"
    
    if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
        log_error "Python $PYTHON_VERSION encontrado. Requer Python $REQUIRED_VERSION ou superior."
        exit 1
    fi
    
    log_success "✅ Python $PYTHON_VERSION encontrado"
}

# Verificar pip
check_pip() {
    log_info "📦 Verificando pip..."
    
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 não encontrado. Instale pip primeiro."
        exit 1
    fi
    
    log_success "✅ pip encontrado"
}

# Criar ambiente virtual
create_venv() {
    log_info "🔧 Criando ambiente virtual..."
    
    if [ -d "venv" ]; then
        log_warning "⚠️ Ambiente virtual já existe. Removendo..."
        rm -rf venv
    fi
    
    python3 -m venv venv
    log_success "✅ Ambiente virtual criado"
}

# Ativar ambiente virtual
activate_venv() {
    log_info "🔄 Ativando ambiente virtual..."
    source venv/bin/activate
    log_success "✅ Ambiente virtual ativado"
}

# Atualizar pip
upgrade_pip() {
    log_info "⬆️ Atualizando pip..."
    pip install --upgrade pip
    log_success "✅ pip atualizado"
}

# Instalar dependências core
install_core_deps() {
    log_info "📚 Instalando dependências principais..."
    
    # Instalar uma por vez para melhor controle de erros
    CORE_DEPS=(
        "streamlit>=1.28.0"
        "pandas>=2.0.0"
        "numpy>=1.24.0"
        "plotly>=5.15.0"
        "requests>=2.31.0"
        "beautifulsoup4>=4.12.0"
        "python-dotenv>=1.0.0"
        "PyPDF2>=3.0.0"
    )
    
    for dep in "${CORE_DEPS[@]}"; do
        log_info "📦 Instalando $dep..."
        pip install "$dep" || {
            log_warning "⚠️ Falha ao instalar $dep, tentando versão mais antiga..."
            # Tentar sem versão específica
            dep_name=$(echo "$dep" | cut -d'>' -f1 | cut -d'=' -f1)
            pip install "$dep_name" || log_error "❌ Falha ao instalar $dep_name"
        }
    done
    
    log_success "✅ Dependências principais instaladas"
}

# Instalar dependências opcionais
install_optional_deps() {
    log_info "🔧 Instalando dependências opcionais..."
    
    OPTIONAL_DEPS=(
        "crewai"
        "crewai-tools"
        "duckduckgo-search"
        "altair"
    )
    
    for dep in "${OPTIONAL_DEPS[@]}"; do
        log_info "📦 Tentando instalar $dep..."
        pip install "$dep" || {
            log_warning "⚠️ Falha ao instalar $dep (opcional)"
        }
    done
    
    log_success "✅ Dependências opcionais processadas"
}

# Instalar dependências de produção (opcional)
install_production_deps() {
    if [ "$1" = "--production" ]; then
        log_info "🏭 Instalando dependências de produção..."
        
        PROD_DEPS=(
            "fastapi>=0.100.0"
            "uvicorn>=0.20.0"
            "sqlalchemy>=2.0.0"
            "redis>=4.5.0"
            "pydantic>=2.0.0"
            "bcrypt>=4.0.0"
            "pyjwt>=2.8.0"
        )
        
        for dep in "${PROD_DEPS[@]}"; do
            log_info "📦 Instalando $dep..."
            pip install "$dep" || {
                log_warning "⚠️ Falha ao instalar $dep"
            }
        done
        
        # Tentar instalar psycopg2-binary (pode falhar em alguns sistemas)
        log_info "📦 Tentando instalar psycopg2-binary..."
        pip install psycopg2-binary || {
            log_warning "⚠️ Falha ao instalar psycopg2-binary. Instale PostgreSQL dev headers se necessário."
        }
        
        log_success "✅ Dependências de produção processadas"
    fi
}

# Criar diretórios necessários
create_directories() {
    log_info "📁 Criando diretórios necessários..."
    
    DIRS=(
        "data/users"
        "data/questions"
        "data/dashboard"
        "config"
        "logs"
        "backups"
    )
    
    for dir in "${DIRS[@]}"; do
        mkdir -p "$dir"
    done
    
    log_success "✅ Diretórios criados"
}

# Criar arquivo de configuração
create_config() {
    log_info "⚙️ Criando arquivo de configuração..."
    
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Configuração do Agente Concurseiro
ENVIRONMENT=development
DEBUG=true

# Banco de dados (SQLite para desenvolvimento)
DATABASE_URL=sqlite:///data/agente_concurseiro.db

# OpenAI (opcional)
# OPENAI_API_KEY=your-openai-api-key-here

# Configurações da aplicação
APP_NAME=Agente Concurseiro
APP_VERSION=2.0.0

# Logs
LOG_LEVEL=INFO
EOF
        log_success "✅ Arquivo .env criado"
    else
        log_info "📄 Arquivo .env já existe"
    fi
}

# Testar instalação
test_installation() {
    log_info "🧪 Testando instalação..."
    
    # Testar imports principais
    python3 -c "
import streamlit
import pandas
import numpy
import plotly
import requests
print('✅ Imports principais funcionando')
" || {
        log_error "❌ Falha nos imports principais"
        return 1
    }
    
    # Testar se o app pode ser importado
    python3 -c "
import sys
sys.path.append('.')
try:
    from app.utils.config import load_config
    print('✅ Configuração carregada')
except ImportError as e:
    print(f'⚠️ Alguns módulos podem não estar disponíveis: {e}')
" || {
        log_warning "⚠️ Alguns módulos podem não estar totalmente funcionais"
    }
    
    log_success "✅ Teste de instalação concluído"
}

# Mostrar instruções finais
show_instructions() {
    log_success "🎉 Instalação concluída com sucesso!"
    
    echo ""
    echo -e "${GREEN}📋 PRÓXIMOS PASSOS:${NC}"
    echo ""
    echo -e "${BLUE}1. Ativar ambiente virtual:${NC}"
    echo "   source venv/bin/activate"
    echo ""
    echo -e "${BLUE}2. Executar aplicação:${NC}"
    echo "   streamlit run app/app.py"
    echo ""
    echo -e "${BLUE}3. Acessar no navegador:${NC}"
    echo "   http://localhost:8501"
    echo ""
    echo -e "${BLUE}4. Para deploy em produção:${NC}"
    echo "   ./deploy.sh production"
    echo ""
    echo -e "${YELLOW}💡 DICAS:${NC}"
    echo "• Configure OPENAI_API_KEY no arquivo .env para IA avançada"
    echo "• Use './install.sh --production' para instalar deps de produção"
    echo "• Consulte README.md para documentação completa"
    echo ""
    echo -e "${GREEN}🚀 Agente Concurseiro v2.0.0 pronto para uso!${NC}"
}

# Função principal
main() {
    check_python
    check_pip
    create_venv
    activate_venv
    upgrade_pip
    install_core_deps
    install_optional_deps
    install_production_deps "$1"
    create_directories
    create_config
    test_installation
    show_instructions
}

# Executar instalação
main "$@"
