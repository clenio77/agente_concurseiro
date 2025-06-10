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
