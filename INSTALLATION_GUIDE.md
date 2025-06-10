# 🛠️ Guia de Instalação - Agente Concurseiro

## 🚀 Instalação Rápida (Recomendada)

### **Opção 1: Script Automático**
```bash
# Clonar repositório
git clone https://github.com/seu-usuario/agente-concurseiro.git
cd agente-concurseiro

# Executar instalação automática
chmod +x install.sh
./install.sh

# Ativar ambiente e executar
source venv/bin/activate
streamlit run app/app.py
```

### **Opção 2: Instalação Manual**
```bash
# 1. Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# 2. Atualizar pip
pip install --upgrade pip

# 3. Instalar dependências (tente nesta ordem)
pip install -r requirements-minimal.txt
# ou se der erro:
pip install streamlit pandas plotly requests beautifulsoup4 python-dotenv

# 4. Executar aplicação
streamlit run app/app.py
```

---

## 🔧 Solução de Problemas Comuns

### **❌ Erro: "Could not find a version that satisfies the requirement"**

**Problema**: Versões específicas não disponíveis para sua versão do Python.

**Solução**:
```bash
# Opção 1: Use requirements mínimos
pip install -r requirements-minimal.txt

# Opção 2: Instale sem versões específicas
pip install streamlit pandas plotly requests beautifulsoup4 python-dotenv PyPDF2

# Opção 3: Instale uma por vez
pip install streamlit
pip install pandas
pip install plotly
# ... continue para cada pacote
```

### **❌ Erro: "duckduckgo-search version not found"**

**Problema**: Versão específica do duckduckgo-search não disponível.

**Solução**:
```bash
# Instalar versão mais recente disponível
pip install duckduckgo-search

# Ou versão específica que funciona
pip install "duckduckgo-search>=6.1.0,<7.0.0"

# Se ainda der erro, pule esta dependência
# O sistema funcionará sem ela (busca web limitada)
```

### **❌ Erro: "crewai installation failed"**

**Problema**: CrewAI pode ter dependências conflitantes.

**Solução**:
```bash
# Pular CrewAI inicialmente
pip install streamlit pandas plotly requests beautifulsoup4 python-dotenv

# Tentar instalar CrewAI depois
pip install crewai

# Se falhar, o sistema funciona sem CrewAI
# (funcionalidades de IA limitadas)
```

### **❌ Erro: "psycopg2-binary installation failed"**

**Problema**: Dependência PostgreSQL não necessária para desenvolvimento.

**Solução**:
```bash
# Pular psycopg2-binary para desenvolvimento local
# O sistema usará SQLite automaticamente

# Para produção com PostgreSQL:
# Ubuntu/Debian:
sudo apt-get install libpq-dev python3-dev
pip install psycopg2-binary

# CentOS/RHEL:
sudo yum install postgresql-devel python3-devel
pip install psycopg2-binary

# macOS:
brew install postgresql
pip install psycopg2-binary
```

---

## 🐍 Problemas com Python

### **Versão do Python**
```bash
# Verificar versão
python3 --version

# Deve ser 3.8 ou superior
# Se não tiver Python 3.8+:

# Ubuntu/Debian:
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip

# macOS:
brew install python@3.11

# Windows:
# Baixar de https://python.org
```

### **Múltiplas Versões do Python**
```bash
# Usar versão específica
python3.11 -m venv venv
source venv/bin/activate
python3.11 -m pip install --upgrade pip
```

---

## 🖥️ Problemas por Sistema Operacional

### **🐧 Linux (Ubuntu/Debian)**
```bash
# Instalar dependências do sistema
sudo apt update
sudo apt install python3-pip python3-venv python3-dev build-essential

# Se usar PostgreSQL
sudo apt install libpq-dev

# Executar instalação
./install.sh
```

### **🍎 macOS**
```bash
# Instalar Homebrew se não tiver
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.11

# Executar instalação
./install.sh
```

### **🪟 Windows**
```powershell
# No PowerShell como Administrador

# Instalar Python se não tiver
# Baixar de https://python.org

# Criar ambiente virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements-minimal.txt

# Executar aplicação
streamlit run app/app.py
```

---

## 🔍 Verificação da Instalação

### **Teste Básico**
```bash
# Ativar ambiente
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Testar imports
python -c "
import streamlit
import pandas
import plotly
print('✅ Instalação básica funcionando')
"

# Testar aplicação
streamlit run app/app.py
```

### **Teste Completo**
```bash
# Executar teste de produção
python test_final_production.py

# Deve mostrar:
# ✅ Passou: X/8 testes
```

---

## 🚀 Instalação para Produção

### **Com Docker (Recomendado)**
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Executar deploy
./deploy.sh production
```

### **Sem Docker**
```bash
# Instalar dependências de produção
./install.sh --production

# Ou manualmente:
pip install fastapi uvicorn sqlalchemy redis pydantic bcrypt pyjwt

# Configurar PostgreSQL
sudo apt install postgresql postgresql-contrib
sudo -u postgres createdb agente_concurseiro

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com configurações de produção
```

---

## 📋 Dependências Opcionais

### **Para IA Avançada**
```bash
# OpenAI (requer API key)
pip install openai tiktoken

# Configurar no .env:
# OPENAI_API_KEY=sua-chave-aqui
```

### **Para Análise de Texto**
```bash
# NLTK para processamento de linguagem natural
pip install nltk

# Baixar dados do NLTK
python -c "
import nltk
nltk.download('punkt')
nltk.download('stopwords')
"
```

### **Para Monitoramento**
```bash
# Métricas Prometheus
pip install prometheus-client

# Logs estruturados
pip install structlog
```

---

## 🆘 Suporte

### **Se nada funcionar:**

1. **Instalação mínima absoluta**:
```bash
pip install streamlit pandas requests python-dotenv
streamlit run app/app.py
```

2. **Usar versões específicas que funcionam**:
```bash
pip install streamlit==1.28.0 pandas==2.0.0 plotly==5.15.0
```

3. **Reportar problema**:
   - Criar issue no GitHub com:
     - Versão do Python (`python --version`)
     - Sistema operacional
     - Erro completo
     - Comando que falhou

### **Contato**
- 📧 Email: suporte@agenteconcurseiro.com
- 🐛 Issues: [GitHub Issues](https://github.com/seu-usuario/agente-concurseiro/issues)
- 💬 Discord: [Servidor da Comunidade](https://discord.gg/agenteconcurseiro)

---

## ✅ Checklist de Instalação

- [ ] Python 3.8+ instalado
- [ ] pip atualizado
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas
- [ ] Arquivo .env configurado
- [ ] Aplicação executando
- [ ] Acesso via http://localhost:8501

**🎉 Se todos os itens estão marcados, sua instalação está completa!**
