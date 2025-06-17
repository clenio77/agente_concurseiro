# 🛠️ Guia de Instalação Detalhado

## Instalação Completa

### Pré-requisitos
- Python 3.11+
- Docker e Docker Compose (opcional para produção)
- Git 2.0+

### Passos Detalhados

```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/agente-concurseiro.git
cd agente-concurseiro

# 2. Instalação completa
chmod +x install.sh
./install.sh

# 3. Ativar ambiente virtual
source venv/bin/activate

# 4. Executar aplicação
streamlit run app/app.py
```

### Instalação Manual (Alternativa)
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements-minimal.txt
streamlit run app/app.py
```

### Deploy em Produção (Docker)
```bash
chmod +x deploy.sh
./deploy.sh production
```

---

## Troubleshooting Avançado

- Problemas de dependências: `pip install -r requirements-minimal.txt`
- Erro de permissão: `chmod +x *.sh`
- Python antigo: instale Python 3.11+
- Streamlit não encontrado: `export PATH=$PATH:$HOME/.local/bin`
- Porta ocupada: `streamlit run app/app.py --server.port 8502`
- Banco de dados: use SQLite por padrão ou configure PostgreSQL no .env

Para dúvidas rápidas, consulte a [FAQ](FAQ.md).
Para instalação simplificada, veja o [Quick Start](QUICK_START.md).

---

## Instruções por Sistema Operacional

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip git
```

### macOS
```bash
brew install python@3.11 git
```

### Windows
- Instale Python 3.11 pelo instalador oficial
- Use o PowerShell para comandos

---

## Variáveis de Ambiente (.env)

Exemplo:
```
ENVIRONMENT=production
DATABASE_URL=sqlite:///data/agente_concurseiro.db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET_KEY=sua-chave-secreta
```

---

Se persistirem problemas, reporte em [GitHub Issues](https://github.com/seu-usuario/agente-concurseiro/issues).
