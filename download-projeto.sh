#!/bin/bash

# Script para baixar/copiar Agente Concurseiro para máquina local
# Versão: 2.0.0

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

# Banner
echo -e "${GREEN}"
cat << "EOF"
   ____                      _                 _   
  |  _ \  _____      ___ __ | | ___   __ _  __| |  
  | | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |  
  | |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  
  |____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|  
                                                   
   _                    _         ____                                   _           
  / \   __ _  ___ _ __ | |_ ___  / ___|___  _ __   ___ _   _ _ __ ___  ___(_)_ __ ___  
 / _ \ / _` |/ _ \ '_ \| __/ _ \| |   / _ \| '_ \ / __| | | | '__/ __|/ _ \ | '__/ _ \ 
/ ___ \ (_| |  __/ | | | ||  __/| |__| (_) | | | | (__| |_| | |  \__ \  __/ | | | (_) |
\_/   \_\__, |\___|_| |_|\__\___|\____\___/|_| |_|\___|\__,_|_|  |___/\___|_|_|  \___/ 
        |___/                                                                         
EOF
echo -e "${NC}"

log_info "💾 Download do Agente Concurseiro v2.0.0"

# Função para obter diretório de destino
get_destination() {
    log_info "📁 Configurando diretório de destino..."
    
    # Sugerir localizações baseadas no OS
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        default_dir="$HOME/Projetos/agente-concurseiro"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        default_dir="$HOME/Projects/agente-concurseiro"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
        default_dir="$HOME/Documents/Projetos/agente-concurseiro"
    else
        default_dir="$HOME/agente-concurseiro"
    fi
    
    echo "📍 Diretório sugerido: $default_dir"
    read -p "Usar este diretório? (y/n) ou digite outro caminho: " user_input
    
    if [[ $user_input =~ ^[Yy]$ ]]; then
        destination_dir="$default_dir"
    elif [[ $user_input =~ ^[Nn]$ ]]; then
        read -p "Digite o caminho completo: " destination_dir
    else
        destination_dir="$user_input"
    fi
    
    log_info "📂 Destino: $destination_dir"
}

# Função para criar estrutura de diretórios
create_structure() {
    log_info "🏗️ Criando estrutura de diretórios..."
    
    # Criar diretório principal
    mkdir -p "$destination_dir"
    cd "$destination_dir"
    
    # Criar estrutura completa
    mkdir -p app/{api,auth,db,ai,monitoring,backup,pages,utils}
    mkdir -p tools
    mkdir -p data/{users,questions,dashboard}
    mkdir -p config
    mkdir -p scripts
    mkdir -p monitoring
    mkdir -p nginx
    mkdir -p .github/workflows
    mkdir -p logs
    mkdir -p backups
    
    log_success "✅ Estrutura criada em: $destination_dir"
}

# Função para detectar método de cópia
detect_copy_method() {
    log_info "🔍 Detectando método de cópia..."
    
    # Verificar se estamos no ambiente de desenvolvimento
    if [ -f "README.md" ] && [ -f "app/app.py" ]; then
        copy_method="local"
        source_dir="$(pwd)"
        log_info "📁 Projeto encontrado localmente: $source_dir"
    else
        log_warning "⚠️ Projeto não encontrado no diretório atual"
        echo "Opções disponíveis:"
        echo "1. Copiar de outro diretório local"
        echo "2. Baixar do GitHub (se disponível)"
        echo "3. Criar estrutura básica"
        
        read -p "Escolha uma opção (1-3): " option
        
        case $option in
            1)
                copy_method="local"
                read -p "Digite o caminho do projeto: " source_dir
                if [ ! -d "$source_dir" ]; then
                    log_error "Diretório não encontrado: $source_dir"
                    exit 1
                fi
                ;;
            2)
                copy_method="github"
                read -p "Digite a URL do repositório: " github_url
                ;;
            3)
                copy_method="basic"
                ;;
            *)
                log_error "Opção inválida"
                exit 1
                ;;
        esac
    fi
}

# Função para copiar arquivos localmente
copy_local_files() {
    log_info "📋 Copiando arquivos do diretório local..."
    
    # Lista de arquivos e diretórios para copiar
    items_to_copy=(
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
        "requirements*.txt"
        "Dockerfile"
        "docker-compose.yml"
        "*.sh"
        "*.py"
        "app/"
        "tools/"
        "data/"
        "config/"
        "scripts/"
        "monitoring/"
        "nginx/"
        ".github/"
        ".env.example"
    )
    
    copied_count=0
    
    for item in "${items_to_copy[@]}"; do
        if [ -e "$source_dir/$item" ]; then
            cp -r "$source_dir/$item" . 2>/dev/null || true
            ((copied_count++))
        fi
    done
    
    # Dar permissões aos scripts
    chmod +x *.sh 2>/dev/null || true
    chmod +x *.py 2>/dev/null || true
    
    log_success "✅ $copied_count itens copiados"
}

# Função para baixar do GitHub
download_from_github() {
    log_info "🌐 Baixando do GitHub..."
    
    if command -v git &> /dev/null; then
        # Usar git clone
        git clone "$github_url" temp_repo
        cp -r temp_repo/* .
        rm -rf temp_repo
        log_success "✅ Projeto clonado do GitHub"
    else
        log_error "Git não encontrado. Instale o Git primeiro."
        exit 1
    fi
}

# Função para criar estrutura básica
create_basic_structure() {
    log_info "📝 Criando estrutura básica..."
    
    # Criar README básico
    cat > README.md << 'EOF'
# 🎓 Agente Concurseiro

Sistema completo de preparação para concursos públicos com IA.

## 🚀 Como Usar

1. Instalar dependências:
   ```bash
   pip install streamlit pandas plotly requests beautifulsoup4 python-dotenv
   ```

2. Executar aplicação:
   ```bash
   streamlit run app/app.py
   ```

3. Acessar: http://localhost:8501

## 📚 Documentação

Para documentação completa, baixe o projeto completo do GitHub.
EOF

    # Criar app básico
    mkdir -p app
    cat > app/app.py << 'EOF'
import streamlit as st

st.title("🎓 Agente Concurseiro")
st.write("Sistema de preparação para concursos públicos")
st.info("Esta é uma versão básica. Para funcionalidades completas, baixe o projeto completo.")
EOF

    # Criar requirements básico
    cat > requirements.txt << 'EOF'
streamlit>=1.28.0
pandas>=2.0.0
plotly>=5.15.0
requests>=2.31.0
beautifulsoup4>=4.12.0
python-dotenv>=1.0.0
EOF

    log_success "✅ Estrutura básica criada"
}

# Função para verificar integridade
verify_integrity() {
    log_info "🔍 Verificando integridade do projeto..."
    
    essential_files=(
        "README.md"
        "app/app.py"
        "requirements.txt"
    )
    
    missing_files=()
    
    for file in "${essential_files[@]}"; do
        if [ ! -f "$file" ]; then
            missing_files+=("$file")
        fi
    done
    
    if [ ${#missing_files[@]} -eq 0 ]; then
        log_success "✅ Todos os arquivos essenciais presentes"
        return 0
    else
        log_warning "⚠️ Arquivos faltando:"
        for file in "${missing_files[@]}"; do
            echo "   ❌ $file"
        done
        return 1
    fi
}

# Função para instalar dependências
install_dependencies() {
    log_info "📦 Instalando dependências..."
    
    if command -v python3 &> /dev/null; then
        if [ -f "install-simple.sh" ]; then
            ./install-simple.sh
        else
            pip3 install -r requirements.txt --user 2>/dev/null || {
                log_warning "⚠️ Falha na instalação automática"
                echo "Execute manualmente: pip3 install streamlit pandas plotly requests beautifulsoup4 python-dotenv --user"
            }
        fi
        log_success "✅ Dependências instaladas"
    else
        log_warning "⚠️ Python3 não encontrado. Instale Python 3.8+ primeiro."
    fi
}

# Função para criar script de execução
create_run_script() {
    log_info "📝 Criando script de execução..."
    
    cat > run.sh << 'EOF'
#!/bin/bash
echo "🚀 Iniciando Agente Concurseiro..."

if [ -f "run_app.py" ]; then
    python3 run_app.py
elif [ -f "app/app.py" ]; then
    python3 -m streamlit run app/app.py
else
    echo "❌ Arquivo principal não encontrado"
    exit 1
fi
EOF

    chmod +x run.sh
    log_success "✅ Script de execução criado: ./run.sh"
}

# Função para mostrar instruções finais
show_final_instructions() {
    echo ""
    log_success "🎉 Download/cópia concluída com sucesso!"
    echo ""
    echo -e "${GREEN}📋 COMO USAR:${NC}"
    echo ""
    echo -e "${BLUE}1. Navegar para o diretório:${NC}"
    echo "   cd \"$destination_dir\""
    echo ""
    echo -e "${BLUE}2. Executar aplicação:${NC}"
    if [ -f "run.sh" ]; then
        echo "   ./run.sh"
    elif [ -f "run_app.py" ]; then
        echo "   python3 run_app.py"
    else
        echo "   python3 -m streamlit run app/app.py"
    fi
    echo ""
    echo -e "${BLUE}3. Acessar no navegador:${NC}"
    echo "   http://localhost:8501"
    echo ""
    echo -e "${YELLOW}💡 DICAS:${NC}"
    echo "• Leia o README.md para documentação completa"
    echo "• Use ./install-simple.sh se tiver problemas de dependências"
    echo "• Configure .env para personalizar configurações"
    echo ""
    echo -e "${GREEN}📊 ESTATÍSTICAS:${NC}"
    echo "   📁 Localização: $destination_dir"
    echo "   📄 Arquivos: $(find . -type f | wc -l)"
    echo "   📂 Diretórios: $(find . -type d | wc -l)"
    echo "   💾 Tamanho: $(du -sh . | cut -f1)"
    echo ""
    echo -e "${GREEN}🎯 Projeto salvo com sucesso!${NC}"
}

# Função principal
main() {
    get_destination
    create_structure
    
    cd "$destination_dir"
    
    detect_copy_method
    
    case $copy_method in
        "local")
            copy_local_files
            ;;
        "github")
            download_from_github
            ;;
        "basic")
            create_basic_structure
            ;;
    esac
    
    verify_integrity
    install_dependencies
    create_run_script
    show_final_instructions
}

# Executar script
main "$@"
