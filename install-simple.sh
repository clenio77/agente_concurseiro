#!/bin/bash

# Script de instalação simples do Agente Concurseiro
# Para ambientes onde python3-venv não está disponível

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

echo -e "${GREEN}🚀 Instalação Simples - Agente Concurseiro v2.0.0${NC}"

# Verificar Python
log_info "🐍 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 não encontrado"
    exit 1
fi
log_success "✅ Python encontrado"

# Verificar pip
log_info "📦 Verificando pip..."
if ! command -v pip3 &> /dev/null; then
    log_error "pip3 não encontrado"
    exit 1
fi
log_success "✅ pip encontrado"

# Atualizar pip e setuptools (fix para pkg_resources)
log_info "⬆️ Atualizando pip e setuptools..."
pip3 install --upgrade pip setuptools --user

# Instalar dependências essenciais
log_info "📚 Instalando dependências essenciais..."

ESSENTIAL_DEPS=(
    "streamlit"
    "pandas"
    "numpy"
    "plotly"
    "requests"
    "beautifulsoup4"
    "python-dotenv"
)

for dep in "${ESSENTIAL_DEPS[@]}"; do
    log_info "📦 Instalando $dep..."
    pip3 install "$dep" --user || {
        log_warning "⚠️ Falha ao instalar $dep"
    }
done

# Tentar instalar dependências opcionais
log_info "🔧 Instalando dependências opcionais..."

OPTIONAL_DEPS=(
    "PyPDF2"
    "altair"
)

for dep in "${OPTIONAL_DEPS[@]}"; do
    log_info "📦 Tentando instalar $dep..."
    pip3 install "$dep" --user || {
        log_warning "⚠️ $dep não instalado (opcional)"
    }
done

# Criar diretórios
log_info "📁 Criando diretórios..."
mkdir -p data/users data/questions data/dashboard config logs backups

# Criar arquivo .env
log_info "⚙️ Criando configuração..."
if [ ! -f ".env" ]; then
    cat > .env << EOF
# Configuração do Agente Concurseiro
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite:///data/agente_concurseiro.db
APP_NAME=Agente Concurseiro
APP_VERSION=2.0.0
LOG_LEVEL=INFO
EOF
    log_success "✅ Arquivo .env criado"
fi

# Testar instalação
log_info "🧪 Testando instalação..."
python3 -c "
import streamlit
import pandas
import plotly
import requests
print('✅ Dependências principais funcionando')
" && log_success "✅ Teste passou" || log_warning "⚠️ Alguns módulos podem não estar funcionais"

# Criar script de execução com fix
log_info "📝 Criando script de execução..."
cat > run_app.py << 'EOF'
#!/usr/bin/env python3
import sys
import os

# Fix para pkg_resources se necessário
try:
    import pkg_resources
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools", "--user"])

# Executar Streamlit
if __name__ == "__main__":
    import subprocess
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/app.py"])
EOF
chmod +x run_app.py

# Instruções finais
echo ""
log_success "🎉 Instalação simples concluída!"
echo ""
echo -e "${GREEN}📋 COMO EXECUTAR:${NC}"
echo ""
echo -e "${BLUE}Opção 1 (Recomendada):${NC}"
echo "   python3 run_app.py"
echo ""
echo -e "${BLUE}Opção 2 (Manual):${NC}"
echo "   python3 -m streamlit run app/app.py"
echo ""
echo -e "${BLUE}3. Acessar no navegador:${NC}"
echo "   http://localhost:8501"
echo ""
echo -e "${YELLOW}💡 NOTA:${NC}"
echo "• Instalação feita no usuário (--user)"
echo "• Script run_app.py inclui correções automáticas"
echo "• Se der erro de módulo, tente: export PATH=\$PATH:\$HOME/.local/bin"
echo ""
echo -e "${GREEN}🚀 Agente Concurseiro pronto para uso!${NC}"
