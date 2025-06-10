# 🚀 Início Rápido - Agente Concurseiro

## ⚡ Instalação em 3 Comandos

```bash
# 1. Clonar repositório
git clone https://github.com/seu-usuario/agente-concurseiro.git
cd agente-concurseiro

# 2. Instalar (escolha uma opção)
./install-simple.sh        # Instalação simples (recomendada)
# ou
./install.sh               # Instalação completa com venv

# 3. Executar (com correções automáticas)
python3 run_app.py
```

**🌐 Acesse:** `http://localhost:8501`

---

## 🎯 Opções de Instalação

### **🟢 Opção 1: Instalação Simples (Funciona sempre)**
```bash
chmod +x install-simple.sh
./install-simple.sh
python3 -m streamlit run app/app.py
```
✅ **Vantagens**: Funciona em qualquer ambiente  
✅ **Ideal para**: Teste rápido, ambientes restritivos

### **🔵 Opção 2: Instalação Completa (Recomendada)**
```bash
chmod +x install.sh
./install.sh
source venv/bin/activate
streamlit run app/app.py
```
✅ **Vantagens**: Ambiente isolado, mais seguro  
✅ **Ideal para**: Desenvolvimento, produção

### **🟡 Opção 3: Manual (Se scripts falharem)**
```bash
pip3 install streamlit pandas plotly requests beautifulsoup4 python-dotenv --user
python3 -m streamlit run app/app.py
```
✅ **Vantagens**: Controle total  
✅ **Ideal para**: Resolução de problemas

---

## 🔧 Solução Rápida de Problemas

### **❌ "No module named 'pkg_resources'"**
```bash
# Executar correção automática
./fix-pkg-resources.sh
python3 run_app.py

# Ou manualmente:
pip3 install --upgrade setuptools --user
python3 run_app.py
```

### **❌ "Command not found: streamlit"**
```bash
# Adicionar ao PATH
export PATH=$PATH:$HOME/.local/bin
python3 run_app.py
```

### **❌ "Module not found"**
```bash
# Instalar dependência específica
pip3 install [nome-do-modulo] --user
# Ou usar script com correções
python3 run_app.py
```

### **❌ "Permission denied"**
```bash
# Dar permissão aos scripts
chmod +x install-simple.sh install.sh deploy.sh
```

### **❌ "Python version error"**
```bash
# Verificar versão (precisa 3.8+)
python3 --version

# Ubuntu: instalar Python mais novo
sudo apt install python3.11
python3.11 -m pip install streamlit --user
python3.11 -m streamlit run app/app.py
```

---

## 🎮 Primeiros Passos no Sistema

### **1. 🔐 Fazer Login**
- Acesse `http://localhost:8501`
- Clique em "Criar Conta" na barra lateral
- Preencha: email, usuário, senha
- Faça login com suas credenciais

### **2. 📊 Explorar Dashboard**
- Veja seu progresso geral
- Conquistas e badges
- Estatísticas de estudo
- Notificações importantes

### **3. 📝 Configurar Perfil**
- Vá em "Configurações"
- Defina: cargo desejado, banca, experiência
- Configure horas de estudo semanais
- Receba plano personalizado

### **4. 🎯 Fazer Primeiro Simulado**
- Acesse "Simulados"
- Escolha banca (ex: CESPE)
- Selecione matérias
- Configure 5-10 questões para teste
- Analise resultados detalhados

### **5. ✍️ Avaliar Redação**
- Vá para "Redação"
- Escolha banca específica
- Selecione tema ou use personalizado
- Escreva redação (mín. 200 palavras)
- Receba avaliação detalhada

---

## 📊 Funcionalidades Principais

### **🎯 Simulados Adaptativos**
- ✅ Questões reais de provas anteriores
- ✅ 5 bancas suportadas (CESPE, FCC, VUNESP, FGV, IBFC)
- ✅ Dificuldade adaptativa
- ✅ Análise detalhada de resultados
- ✅ Identificação de pontos fracos

### **✍️ Redação Especializada**
- ✅ Avaliação específica por banca
- ✅ 5+ critérios personalizados
- ✅ Banco de temas reais
- ✅ Feedback detalhado
- ✅ Sugestões de melhoria

### **🎮 Gamificação Motivacional**
- ✅ 15 conquistas progressivas
- ✅ 9 badges por categoria
- ✅ Sistema de níveis e XP
- ✅ Sequências de estudo
- ✅ Celebração de marcos

### **📊 Analytics Avançados**
- ✅ Predição de desempenho
- ✅ 8 métricas de performance
- ✅ Gráficos interativos
- ✅ Simulação de cenários
- ✅ Recomendações personalizadas

### **📚 Planos Personalizados**
- ✅ Cronogramas baseados no perfil
- ✅ Distribuição inteligente de matérias
- ✅ Marcos e metas intermediárias
- ✅ Adaptação ao progresso
- ✅ Metodologias comprovadas

---

## 🌟 Dicas de Uso

### **💡 Para Maximizar Resultados**
1. **Configure perfil completo** - Quanto mais dados, melhor a personalização
2. **Faça simulados regularmente** - Pelo menos 2x por semana
3. **Pratique redação** - 1 redação por semana mínimo
4. **Acompanhe analytics** - Verifique progresso semanalmente
5. **Mantenha sequência** - Consistência é fundamental

### **🎯 Estratégias por Nível**
- **Iniciante**: Foque em plano de estudos + simulados básicos
- **Intermediário**: Use analytics + redação específica por banca
- **Avançado**: Otimize com predições + simulação de cenários

### **📈 Acompanhamento de Progresso**
- Dashboard mostra evolução geral
- Analytics detalha performance por matéria
- Gamificação mantém motivação
- Notificações alertam sobre metas

---

## 🆘 Suporte Rápido

### **🔗 Links Úteis**
- 📖 **Documentação Completa**: [README.md](README.md)
- 🔧 **Guia Técnico**: [TECHNICAL_SPECS.md](TECHNICAL_SPECS.md)
- 🛠️ **Instalação Detalhada**: [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
- 📋 **Histórico**: [CHANGELOG.md](CHANGELOG.md)

### **💬 Contato**
- 🐛 **Reportar Bug**: [GitHub Issues](https://github.com/seu-usuario/agente-concurseiro/issues)
- 💡 **Sugestões**: [GitHub Discussions](https://github.com/seu-usuario/agente-concurseiro/discussions)
- 📧 **Email**: suporte@agenteconcurseiro.com

---

## ✅ Checklist de Sucesso

- [ ] ✅ Sistema instalado e funcionando
- [ ] 🔐 Conta criada e login realizado
- [ ] 📊 Perfil configurado completamente
- [ ] 📝 Plano de estudos gerado
- [ ] 🎯 Primeiro simulado realizado
- [ ] ✍️ Primeira redação avaliada
- [ ] 📈 Analytics visualizados
- [ ] 🎮 Primeiras conquistas desbloqueadas

**🎉 Se todos os itens estão marcados, você está pronto para acelerar sua preparação!**

---

<div align="center">

**🚀 Agente Concurseiro v2.0.0**  
**Sistema Completo • Pronto para Uso • Resultados Comprovados**

[![Quick Start](https://img.shields.io/badge/quick--start-ready-brightgreen.svg)](http://localhost:8501)
[![Support](https://img.shields.io/badge/support-24%2F7-blue.svg)](mailto:suporte@agenteconcurseiro.com)

</div>
