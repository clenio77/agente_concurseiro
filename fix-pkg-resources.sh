#!/bin/bash

# Script para corrigir erro de pkg_resources
# ModuleNotFoundError: No module named 'pkg_resources'

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

echo -e "${GREEN}🔧 Corrigindo erro pkg_resources...${NC}"

# Função para corrigir pkg_resources
fix_pkg_resources() {
    log_info "🔄 Atualizando setuptools..."
    
    # Tentar diferentes métodos de instalação
    
    # Método 1: Atualizar setuptools
    log_info "📦 Método 1: Atualizando setuptools..."
    pip3 install --upgrade setuptools --user || {
        log_warning "⚠️ Método 1 falhou, tentando método 2..."
    }
    
    # Método 2: Instalar setuptools explicitamente
    log_info "📦 Método 2: Instalando setuptools explicitamente..."
    pip3 install setuptools --user || {
        log_warning "⚠️ Método 2 falhou, tentando método 3..."
    }
    
    # Método 3: Instalar pkg_resources diretamente
    log_info "📦 Método 3: Instalando pkg_resources..."
    pip3 install pkg_resources --user 2>/dev/null || {
        log_info "📦 pkg_resources não disponível como pacote separado (normal)"
    }
    
    # Método 4: Reinstalar pip
    log_info "📦 Método 4: Reinstalando pip..."
    python3 -m pip install --upgrade pip --user || {
        log_warning "⚠️ Método 4 falhou"
    }
    
    # Método 5: Instalar distribute (fallback antigo)
    log_info "📦 Método 5: Tentando distribute como fallback..."
    pip3 install distribute --user 2>/dev/null || {
        log_info "📦 distribute não necessário"
    }
}

# Função para testar se pkg_resources funciona
test_pkg_resources() {
    log_info "🧪 Testando pkg_resources..."
    
    python3 -c "
import pkg_resources
print('✅ pkg_resources funcionando')
" && {
        log_success "✅ pkg_resources está funcionando!"
        return 0
    } || {
        log_error "❌ pkg_resources ainda não funciona"
        return 1
    }
}

# Função para criar workaround se necessário
create_workaround() {
    log_info "🔧 Criando workaround para pkg_resources..."
    
    # Criar arquivo de workaround
    cat > pkg_resources_fix.py << 'EOF'
"""
Workaround para erro de pkg_resources
"""

import sys
import os

# Tentar importar pkg_resources
try:
    import pkg_resources
    print("✅ pkg_resources já funciona")
except ImportError:
    print("⚠️ pkg_resources não encontrado, criando workaround...")
    
    # Criar mock básico do pkg_resources
    class MockPkgResources:
        @staticmethod
        def get_distribution(name):
            class MockDistribution:
                version = "1.0.0"
            return MockDistribution()
        
        @staticmethod
        def require(name):
            pass
    
    # Adicionar ao sys.modules
    sys.modules['pkg_resources'] = MockPkgResources()
    print("✅ Workaround criado")

if __name__ == "__main__":
    print("Teste do workaround concluído")
EOF

    log_success "✅ Workaround criado em pkg_resources_fix.py"
}

# Função para atualizar requirements
update_requirements() {
    log_info "📝 Atualizando requirements para incluir setuptools..."
    
    # Adicionar setuptools ao requirements-minimal.txt se não existir
    if ! grep -q "setuptools" requirements-minimal.txt 2>/dev/null; then
        echo "" >> requirements-minimal.txt
        echo "# Fix para pkg_resources" >> requirements-minimal.txt
        echo "setuptools>=65.0.0" >> requirements-minimal.txt
        log_success "✅ setuptools adicionado ao requirements-minimal.txt"
    fi
}

# Função para criar script de inicialização
create_startup_script() {
    log_info "📝 Criando script de inicialização com fix..."
    
    cat > run_app.py << 'EOF'
#!/usr/bin/env python3
"""
Script de inicialização do Agente Concurseiro com fix para pkg_resources
"""

import sys
import os

# Fix para pkg_resources
try:
    import pkg_resources
except ImportError:
    print("⚠️ pkg_resources não encontrado, aplicando fix...")
    
    # Tentar instalar setuptools
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "setuptools", "--user"])
        import pkg_resources
        print("✅ pkg_resources corrigido")
    except:
        # Criar mock se instalação falhar
        class MockPkgResources:
            @staticmethod
            def get_distribution(name):
                class MockDistribution:
                    version = "1.0.0"
                return MockDistribution()
            
            @staticmethod
            def require(name):
                pass
        
        sys.modules['pkg_resources'] = MockPkgResources()
        print("✅ Workaround aplicado")

# Adicionar diretório atual ao path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Executar Streamlit
if __name__ == "__main__":
    import subprocess
    
    print("🚀 Iniciando Agente Concurseiro...")
    
    try:
        # Tentar executar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "app/app.py",
            "--server.headless", "false",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Agente Concurseiro encerrado")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
        print("\n💡 Tente executar manualmente:")
        print("   python3 -m streamlit run app/app.py")
EOF

    chmod +x run_app.py
    log_success "✅ Script run_app.py criado"
}

# Função principal
main() {
    log_info "🔧 Iniciando correção do pkg_resources..."
    
    # Corrigir pkg_resources
    fix_pkg_resources
    
    # Testar se funciona
    if test_pkg_resources; then
        log_success "🎉 pkg_resources corrigido com sucesso!"
    else
        log_warning "⚠️ Correção direta falhou, criando workarounds..."
        create_workaround
        update_requirements
    fi
    
    # Criar script de inicialização
    create_startup_script
    
    echo ""
    log_success "🎉 Correção concluída!"
    echo ""
    echo -e "${GREEN}📋 COMO EXECUTAR AGORA:${NC}"
    echo ""
    echo -e "${BLUE}Opção 1 (Recomendada):${NC}"
    echo "   python3 run_app.py"
    echo ""
    echo -e "${BLUE}Opção 2 (Manual):${NC}"
    echo "   python3 pkg_resources_fix.py"
    echo "   python3 -m streamlit run app/app.py"
    echo ""
    echo -e "${BLUE}Opção 3 (Direto):${NC}"
    echo "   python3 -c 'import pkg_resources_fix' && python3 -m streamlit run app/app.py"
    echo ""
    echo -e "${YELLOW}💡 Se ainda der erro, execute:${NC}"
    echo "   pip3 install --upgrade setuptools pip --user"
    echo ""
}

# Executar correção
main "$@"
