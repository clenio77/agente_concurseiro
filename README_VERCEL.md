# 🚀 Agente Concurseiro v2.0 - Vercel Edition

## 📋 Visão Geral

Versão otimizada do Agente Concurseiro para deploy no **Vercel**, mantendo todas as funcionalidades principais de análise de editais com performance otimizada para ambiente serverless.

## ✨ Funcionalidades

### 🎯 **Principais:**
- 📋 **Análise Inteligente de Editais** - Upload e processamento de PDFs
- 🏠 **Dashboard Interativo** - Métricas e estatísticas em tempo real
- 📊 **Visualizações** - Gráficos interativos com Plotly
- ⚙️ **Configurações** - Personalização da aplicação

### 🔧 **Otimizações para Vercel:**
- ⏱️ **Controle de Timeout** - Processamento dentro dos limites
- 💾 **Gestão de Memória** - Otimização automática
- 📁 **Arquivos Temporários** - Gerenciamento seguro
- 🗄️ **Banco Externo** - Suporte a PostgreSQL

## 🚀 Deploy Rápido

### **1. Pré-requisitos**
```bash
# Node.js (para Vercel CLI)
node --version

# Git
git --version
```

### **2. Deploy Automatizado**
```bash
# Executar script de deploy
./deploy-vercel.sh
```

### **3. Configurar Banco de Dados**

**Opção A: Supabase (Recomendado)**
1. Acesse [supabase.com](https://supabase.com)
2. Crie novo projeto
3. Vá em Settings > Database
4. Copie a Connection String
5. Configure no Vercel como `DATABASE_URL`

**Opção B: PlanetScale**
1. Acesse [planetscale.com](https://planetscale.com)
2. Crie novo banco
3. Obtenha URL de conexão
4. Configure no Vercel

### **4. Variáveis de Ambiente**

No dashboard do Vercel, adicione:

| Variável | Obrigatório | Exemplo |
|----------|-------------|---------|
| `DATABASE_URL` | ✅ | `postgresql://user:pass@host:5432/db` |
| `OPENAI_API_KEY` | ❌ | `sk-...` |
| `ENVIRONMENT` | ❌ | `production` |

## 📁 Estrutura do Projeto

```
agente_concurseiro/
├── streamlit_app.py          # Aplicação principal
├── vercel.json              # Configuração Vercel
├── vercel_config.py         # Configuração de ambiente
├── vercel_optimizations.py  # Otimizações de performance
├── requirements-vercel.txt  # Dependências otimizadas
├── deploy-vercel.sh         # Script de deploy
├── .streamlit/
│   └── config.toml         # Configuração Streamlit
└── app/
    └── utils/
        └── edital_analyzer.py  # Analisador de editais
```

## 🔧 Desenvolvimento Local

### **1. Configurar Ambiente**
```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements-vercel.txt
```

### **2. Configurar Banco Local**
```bash
# Usar SQLite para desenvolvimento
export DATABASE_URL="sqlite:///data/app.db"
```

### **3. Executar Aplicação**
```bash
streamlit run streamlit_app.py
```

## 📊 Monitoramento

### **Performance Monitor**
A aplicação inclui monitoramento automático:
- ⏱️ Tempo de execução
- 💾 Uso de memória
- 🔄 Operações realizadas
- ⚠️ Warnings de performance

### **Logs no Vercel**
```bash
# Ver logs em tempo real
vercel logs

# Ver logs de uma função específica
vercel logs --follow
```

## 🐛 Solução de Problemas

### **Erro: "Module not found"**
```bash
# Verificar se todos os arquivos estão presentes
ls -la streamlit_app.py vercel_config.py app/utils/edital_analyzer.py
```

### **Erro: "Database connection failed"**
```bash
# Verificar variável DATABASE_URL no Vercel
vercel env ls
```

### **Timeout Error**
- Arquivos PDF muito grandes (>10MB)
- Processamento demorado
- **Solução:** Usar arquivos menores ou otimizar código

### **Memory Error**
- Múltiplos uploads simultâneos
- Cache muito grande
- **Solução:** Reiniciar aplicação ou otimizar memória

## 📈 Limites do Vercel

| Recurso | Hobby | Pro |
|---------|-------|-----|
| **Timeout** | 10s | 60s |
| **Memória** | 1GB | 1GB |
| **Tamanho** | 50MB | 50MB |
| **Bandwidth** | 100GB | 1TB |

## 🔄 Atualizações

### **Deploy de Nova Versão**
```bash
# Fazer alterações no código
git add .
git commit -m "Nova funcionalidade"

# Deploy automático (se conectado ao Git)
git push origin main

# Ou deploy manual
vercel --prod
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- 📧 **Email:** suporte@agenteconcurseiro.com
- 💬 **Discord:** [Comunidade](https://discord.gg/agenteconcurseiro)
- 🐛 **Issues:** [GitHub Issues](https://github.com/clenio77/agente_concurseiro/issues)

---

**Desenvolvido com ❤️ para concurseiros brasileiros**

🚀 **Deploy no Vercel em menos de 5 minutos!**
