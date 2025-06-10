#!/bin/bash

# Script para criar backup completo do Agente Concurseiro
# Versão: 2.0.0

set -e

# Cores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${GREEN}📦 Criando backup do Agente Concurseiro v2.0.0${NC}"

# Nome do arquivo de backup
BACKUP_NAME="agente-concurseiro-v2.0.0-$(date +%Y%m%d)"

# Criar diretório temporário
TEMP_DIR="/tmp/agente-concurseiro-backup"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

echo -e "${BLUE}📁 Copiando arquivos...${NC}"

# Lista de arquivos e diretórios para incluir no backup
items_to_backup=(
    "README.md"
    "QUICK_START.md"
    "INSTALLATION_GUIDE.md"
    "FAQ.md"
    "TECHNICAL_SPECS.md"
    "CHANGELOG.md"
    "EXECUTIVE_SUMMARY.md"
    "DOCS_INDEX.md"
    "COMO_ADICIONAR_AO_GITHUB.md"
    "GITHUB_SETUP.md"
    "COMO_SALVAR_LOCALMENTE.md"
    "requirements.txt"
    "requirements-minimal.txt"
    "requirements-prod.txt"
    "Dockerfile"
    "docker-compose.yml"
    "install-simple.sh"
    "install.sh"
    "fix-pkg-resources.sh"
    "setup-github.sh"
    "download-projeto.sh"
    "criar-backup.sh"
    "deploy.sh"
    "run_app.py"
    "test_final_production.py"
    "test_improvements.py"
    "app/"
    "tools/"
    "data/"
    "config/"
    "scripts/"
    "monitoring/"
    "nginx/"
    ".github/"
)

# Copiar arquivos existentes
for item in "${items_to_backup[@]}"; do
    if [ -e "$item" ]; then
        cp -r "$item" "$TEMP_DIR/" 2>/dev/null || true
        echo "✅ $item"
    fi
done

# Criar arquivo .env.example se não existir
if [ ! -f "$TEMP_DIR/.env.example" ]; then
    cat > "$TEMP_DIR/.env.example" << 'EOF'
# Configuração do Agente Concurseiro
ENVIRONMENT=development
DEBUG=true

# Banco de dados
DATABASE_URL=sqlite:///data/agente_concurseiro.db

# OpenAI (opcional)
# OPENAI_API_KEY=your-openai-api-key-here

# Configurações da aplicação
APP_NAME=Agente Concurseiro
APP_VERSION=2.0.0
LOG_LEVEL=INFO
EOF
fi

# Criar arquivo de informações do backup
cat > "$TEMP_DIR/BACKUP_INFO.txt" << EOF
AGENTE CONCURSEIRO - BACKUP v2.0.0
==================================

Data do Backup: $(date)
Versão: 2.0.0
Status: Produção

CONTEÚDO:
- Sistema completo de preparação para concursos
- 23 funcionalidades principais
- Interface Streamlit moderna
- Sistema de gamificação
- Analytics e predição IA
- Avaliação de redação por banca
- Infraestrutura Docker
- Documentação completa (100KB+)

COMO USAR:
1. Extrair arquivos
2. Executar: ./install-simple.sh
3. Executar: python3 run_app.py
4. Acessar: http://localhost:8501

REQUISITOS:
- Python 3.8+
- pip3
- 50MB espaço livre

SUPORTE:
- README.md - Documentação completa
- FAQ.md - Perguntas frequentes
- QUICK_START.md - Início rápido
EOF

echo -e "${BLUE}📦 Criando arquivo compactado...${NC}"

# Criar tar.gz
cd /tmp
tar -czf "${BACKUP_NAME}.tar.gz" agente-concurseiro-backup/

# Mover para diretório original
mv "${BACKUP_NAME}.tar.gz" "$OLDPWD/"

# Limpar temporário
rm -rf "$TEMP_DIR"

echo -e "${GREEN}✅ Backup criado com sucesso!${NC}"
echo ""
echo "📄 Arquivo: ${BACKUP_NAME}.tar.gz"
echo "📊 Tamanho: $(ls -lh ${BACKUP_NAME}.tar.gz | awk '{print $5}')"
echo "📁 Localização: $(pwd)/${BACKUP_NAME}.tar.gz"
echo ""
echo "🚀 Para usar o backup:"
echo "1. tar -xzf ${BACKUP_NAME}.tar.gz"
echo "2. cd agente-concurseiro-backup"
echo "3. ./install-simple.sh"
echo "4. python3 run_app.py"
