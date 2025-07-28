"""
Configuração específica para testes
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configurar variáveis de ambiente para testes
os.environ["ENVIRONMENT"] = "testing"
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["DATABASE_URI"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["SQL_DEBUG"] = "false"

# Configurações específicas para testes
TEST_CONFIG = {
    "database_url": "sqlite:///:memory:",
    "secret_key": "test-secret-key",
    "environment": "testing",
    "log_level": "DEBUG"
}

def setup_test_environment():
    """Configura o ambiente para testes"""
    print("🔧 Configurando ambiente de teste...")

    # Criar diretórios necessários
    os.makedirs("data", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    os.makedirs("backups", exist_ok=True)

    print("✅ Ambiente de teste configurado")

if __name__ == "__main__":
    setup_test_environment()
