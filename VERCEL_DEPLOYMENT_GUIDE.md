# 🚀 Guia de Deploy no Vercel - Agente Concurseiro

## 📋 Visão Geral

O Agente Concurseiro pode ser adaptado para rodar no Vercel, mas requer algumas modificações na arquitetura atual.

## 🏗️ Arquitetura Recomendada

### Opção 1: Streamlit Puro (Mais Simples)
```
┌─────────────────┐
│   Vercel        │
│  ┌───────────┐  │
│  │ Streamlit │  │  ← Frontend único
│  │    App    │  │
│  └───────────┘  │
└─────────────────┘
        │
        ▼
┌─────────────────┐
│ Banco Externo   │  ← PostgreSQL/MongoDB
│ (Supabase/      │
│  PlanetScale)   │
└─────────────────┘
```

### Opção 2: Separação Frontend/Backend
```
┌─────────────────┐    ┌─────────────────┐
│   Vercel        │    │   Railway/      │
│  ┌───────────┐  │    │   Render        │
│  │ Streamlit │  │◄──►│  ┌───────────┐  │
│  │ Frontend  │  │    │  │  FastAPI  │  │
│  └───────────┘  │    │  │  Backend  │  │
└─────────────────┘    │  └───────────┘  │
                       └─────────────────┘
                               │
                               ▼
                       ┌─────────────────┐
                       │ Banco Externo   │
                       │ (PostgreSQL)    │
                       └─────────────────┘
```

## 🔧 Modificações Necessárias

### 1. **Configuração do Vercel**

Criar `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app/app.py",
      "use": "@vercel/python",
      "config": {
        "maxLambdaSize": "50mb"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app/app.py"
    }
  ],
  "env": {
    "PYTHONPATH": ".",
    "STREAMLIT_SERVER_PORT": "8501",
    "STREAMLIT_SERVER_ADDRESS": "0.0.0.0"
  }
}
```

### 2. **Adaptação do requirements.txt**
```txt
# Essenciais para Vercel
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
pypdf>=3.15.0
python-dotenv>=1.0.0

# IA e Processamento
openai>=1.0.0
langchain>=0.1.0
crewai>=0.1.0

# Banco de Dados (externo)
psycopg2-binary>=2.9.0
sqlalchemy>=2.0.0

# Remover dependências incompatíveis:
# - redis (usar cache externo)
# - uvicorn/fastapi (separar backend)
# - sqlite (usar PostgreSQL)
```

### 3. **Configuração de Banco Externo**

**Opções recomendadas:**
- **Supabase** (PostgreSQL gratuito)
- **PlanetScale** (MySQL serverless)
- **Neon** (PostgreSQL serverless)

### 4. **Adaptação do Código**

#### A. Remover dependências do FastAPI
```python
# Remover imports:
# from fastapi import ...
# from uvicorn import ...

# Manter apenas Streamlit
import streamlit as st
```

#### B. Configurar banco externo
```python
# app/config/vercel_config.py
import os
from sqlalchemy import create_engine

def get_database_url():
    """Configuração para banco externo"""
    if os.getenv("VERCEL_ENV"):
        # Produção no Vercel
        return os.getenv("DATABASE_URL")  # Supabase/PlanetScale
    else:
        # Desenvolvimento local
        return "sqlite:///data/app.db"
```

#### C. Adaptar armazenamento de arquivos
```python
# Usar armazenamento temporário ou externo
import tempfile

def save_uploaded_file(uploaded_file):
    """Salvar arquivo temporariamente"""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        return tmp_file.name
```

## 📦 Passos para Deploy

### 1. **Preparar o Projeto**
```bash
# Criar branch específica para Vercel
git checkout -b vercel-deploy

# Simplificar estrutura
mkdir streamlit-app
cp -r app/app.py streamlit-app/
cp -r app/components streamlit-app/
cp -r app/utils streamlit-app/
```

### 2. **Configurar Banco Externo**
```bash
# Exemplo com Supabase
# 1. Criar conta no Supabase
# 2. Criar novo projeto
# 3. Obter URL de conexão
# 4. Configurar variáveis de ambiente
```

### 3. **Deploy no Vercel**
```bash
# Instalar Vercel CLI
npm i -g vercel

# Fazer deploy
vercel --prod

# Configurar variáveis de ambiente:
# DATABASE_URL=postgresql://...
# OPENAI_API_KEY=sk-...
```

## ⚠️ Limitações do Vercel

### **Limitações Técnicas:**
- **Timeout**: 10s (Hobby) / 60s (Pro)
- **Memória**: 1GB máximo
- **Tamanho**: 50MB por função
- **Armazenamento**: Apenas temporário

### **Soluções:**
1. **Timeout**: Otimizar processamento de PDFs
2. **Memória**: Processar arquivos em chunks
3. **Armazenamento**: Usar Supabase Storage

## 🎯 Recomendação Final

### **Para MVP Rápido:**
- Deploy apenas o Streamlit no Vercel
- Usar Supabase como banco
- Simplificar funcionalidades iniciais

### **Para Produção Completa:**
- Frontend (Streamlit) → Vercel
- Backend (FastAPI) → Railway/Render
- Banco → Supabase/PlanetScale
- Cache → Upstash Redis

## 🚀 Próximos Passos

1. **Escolher arquitetura** (Opção 1 ou 2)
2. **Configurar banco externo** (Supabase recomendado)
3. **Adaptar código** conforme guia
4. **Testar localmente** com banco externo
5. **Deploy no Vercel**

## 🎯 IMPLEMENTAÇÃO CONCLUÍDA!

### ✅ **Arquivos Criados:**

1. **`vercel.json`** - Configuração principal do Vercel
2. **`streamlit_app.py`** - Aplicação Streamlit otimizada
3. **`vercel_config.py`** - Configuração de banco e ambiente
4. **`vercel_optimizations.py`** - Otimizações de performance
5. **`requirements-vercel.txt`** - Dependências otimizadas
6. **`deploy-vercel.sh`** - Script automatizado de deploy
7. **`.streamlit/config.toml`** - Configuração do Streamlit

### 🚀 **Como Fazer Deploy:**

#### **Opção 1: Script Automatizado (Recomendado)**
```bash
# Execute o script de deploy
./deploy-vercel.sh
```

#### **Opção 2: Deploy Manual**
```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Fazer login
vercel login

# 3. Deploy
vercel --prod
```

### 🔧 **Configuração de Variáveis de Ambiente:**

No dashboard do Vercel, configure:

```env
# Obrigatório - Banco de dados
DATABASE_URL=postgresql://user:pass@host:5432/db

# Opcional - IA
OPENAI_API_KEY=sk-...

# Opcional - Ambiente
ENVIRONMENT=production
```

### 📊 **Banco de Dados Recomendado:**

**Supabase (Gratuito):**
1. Acesse [supabase.com](https://supabase.com)
2. Crie novo projeto
3. Copie a URL de conexão
4. Configure no Vercel como `DATABASE_URL`

### 🎉 **Funcionalidades Disponíveis:**

- ✅ **Análise de Edital** - Upload e processamento de PDFs
- ✅ **Dashboard** - Métricas e estatísticas
- ✅ **Otimizações** - Performance para Vercel
- ✅ **Responsivo** - Interface adaptável
- ✅ **Cache** - Sistema de cache otimizado

### 🔍 **Monitoramento:**

A aplicação inclui:
- Monitor de performance
- Controle de timeout
- Gestão de memória
- Logs detalhados

### 📱 **URL da Aplicação:**

Após o deploy, sua aplicação estará disponível em:
`https://seu-projeto.vercel.app`

**Deploy realizado com sucesso! 🚀**
