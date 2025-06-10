# ❓ FAQ - Perguntas Frequentes

## 🔧 **Problemas de Instalação**

### **❌ "No module named 'pkg_resources'"**

**Problema**: Erro comum relacionado ao setuptools desatualizado.

**Solução**:
```bash
# Método 1: Script automático
./fix-pkg-resources.sh

# Método 2: Manual
pip3 install --upgrade setuptools --user
python3 run_app.py

# Método 3: Reinstalar pip
python3 -m pip install --upgrade pip setuptools --user
```

### **❌ "Command not found: streamlit"**

**Problema**: Streamlit não está no PATH do sistema.

**Solução**:
```bash
# Adicionar ao PATH temporariamente
export PATH=$PATH:$HOME/.local/bin

# Ou usar script que corrige automaticamente
python3 run_app.py

# Para tornar permanente (Linux/Mac)
echo 'export PATH=$PATH:$HOME/.local/bin' >> ~/.bashrc
source ~/.bashrc
```

### **❌ "Could not find a version that satisfies the requirement"**

**Problema**: Versões específicas não disponíveis.

**Solução**:
```bash
# Usar requirements mínimos
pip3 install -r requirements-minimal.txt

# Ou instalar sem versões específicas
pip3 install streamlit pandas plotly requests beautifulsoup4 python-dotenv --user
```

### **❌ "Permission denied"**

**Problema**: Scripts não têm permissão de execução.

**Solução**:
```bash
# Dar permissão aos scripts
chmod +x install-simple.sh install.sh fix-pkg-resources.sh deploy.sh

# Executar
./install-simple.sh
```

---

## 🐍 **Problemas com Python**

### **❌ "Python version too old"**

**Problema**: Python 3.7 ou inferior.

**Solução**:
```bash
# Verificar versão
python3 --version

# Ubuntu/Debian: instalar Python mais novo
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv

# Usar versão específica
python3.11 -m pip install streamlit --user
python3.11 run_app.py
```

### **❌ "Multiple Python versions"**

**Problema**: Conflito entre versões do Python.

**Solução**:
```bash
# Usar versão específica
python3.11 -m venv venv
source venv/bin/activate
python3.11 -m pip install -r requirements-minimal.txt
```

---

## 🖥️ **Problemas por Sistema Operacional**

### **🐧 Linux**

**Problema**: Dependências do sistema faltando.

**Solução**:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-pip python3-venv python3-dev build-essential

# CentOS/RHEL
sudo yum install python3-pip python3-devel gcc

# Executar instalação
./install-simple.sh
```

### **🍎 macOS**

**Problema**: Python não encontrado ou versão antiga.

**Solução**:
```bash
# Instalar Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python@3.11

# Usar Python do Homebrew
/opt/homebrew/bin/python3.11 -m pip install streamlit --user
```

### **🪟 Windows**

**Problema**: Comandos Unix não funcionam.

**Solução**:
```powershell
# PowerShell como Administrador
python -m pip install --upgrade pip setuptools
python -m pip install streamlit pandas plotly requests beautifulsoup4 python-dotenv

# Executar aplicação
python -m streamlit run app/app.py
```

---

## 🚀 **Problemas de Execução**

### **❌ "Address already in use"**

**Problema**: Porta 8501 já está sendo usada.

**Solução**:
```bash
# Usar porta diferente
streamlit run app/app.py --server.port 8502

# Ou matar processo na porta 8501
lsof -ti:8501 | xargs kill -9
```

### **❌ "ModuleNotFoundError: No module named 'app'"**

**Problema**: Python não encontra módulos da aplicação.

**Solução**:
```bash
# Executar do diretório correto
cd agente-concurseiro
python3 run_app.py

# Ou adicionar ao PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)
python3 -m streamlit run app/app.py
```

### **❌ "FileNotFoundError: config.yaml"**

**Problema**: Arquivo de configuração não encontrado.

**Solução**:
```bash
# Criar arquivo .env se não existir
cp .env.example .env

# Ou executar script que cria automaticamente
./install-simple.sh
```

---

## 🔐 **Problemas de Funcionalidade**

### **❌ "OpenAI API not working"**

**Problema**: Funcionalidades de IA não funcionam.

**Solução**:
```bash
# Configurar API key no .env
echo "OPENAI_API_KEY=sua-chave-aqui" >> .env

# Sistema funciona sem OpenAI (com limitações)
# Funcionalidades básicas continuam funcionando
```

### **❌ "Database connection failed"**

**Problema**: Erro de conexão com banco.

**Solução**:
```bash
# Sistema usa SQLite por padrão (não precisa configurar)
# Verificar se diretório data/ existe
mkdir -p data

# Recriar banco se corrompido
rm -f data/agente_concurseiro.db
python3 run_app.py
```

### **❌ "Gamification not working"**

**Problema**: Sistema de conquistas não funciona.

**Solução**:
```bash
# Verificar se dados do usuário existem
ls -la data/users/

# Recriar dados se necessário (perde progresso)
rm -rf data/users/
python3 run_app.py
```

---

## 📊 **Problemas de Performance**

### **❌ "App is slow"**

**Problema**: Interface lenta ou travando.

**Solução**:
```bash
# Limpar cache do Streamlit
streamlit cache clear

# Ou reiniciar aplicação
# Ctrl+C para parar
python3 run_app.py
```

### **❌ "High memory usage"**

**Problema**: Aplicação consumindo muita memória.

**Solução**:
```bash
# Reduzir dados carregados
# Editar app/utils/config.py
# Reduzir CACHE_SIZE e MAX_QUESTIONS

# Ou usar versão mais leve
python3 -c "
import streamlit as st
st.set_page_config(layout='centered')
exec(open('app/app.py').read())
"
```

---

## 🆘 **Quando Nada Funciona**

### **🔥 Instalação de Emergência**

Se todos os métodos falharem:

```bash
# 1. Instalação mínima absoluta
pip3 install streamlit --user

# 2. Criar app mínimo
cat > minimal_app.py << 'EOF'
import streamlit as st
st.title("🎓 Agente Concurseiro - Versão Mínima")
st.write("Sistema funcionando!")
st.write("Instale dependências completas para todas as funcionalidades")
EOF

# 3. Executar versão mínima
python3 -m streamlit run minimal_app.py
```

### **📞 Obter Ajuda**

1. **Verificar logs de erro**:
   ```bash
   python3 run_app.py 2>&1 | tee error.log
   ```

2. **Reportar problema**:
   - Criar issue no GitHub
   - Incluir: SO, versão Python, erro completo
   - Anexar error.log

3. **Contatos**:
   - 🐛 [GitHub Issues](https://github.com/seu-usuario/agente-concurseiro/issues)
   - 📧 suporte@agenteconcurseiro.com
   - 💬 [Discord](https://discord.gg/agenteconcurseiro)

---

## ✅ **Checklist de Diagnóstico**

Antes de reportar problema, verifique:

- [ ] Python 3.8+ instalado (`python3 --version`)
- [ ] pip funcionando (`pip3 --version`)
- [ ] Permissões dos scripts (`ls -la *.sh`)
- [ ] Diretório correto (`ls app/app.py`)
- [ ] Dependências instaladas (`pip3 list | grep streamlit`)
- [ ] Porta disponível (`lsof -i:8501`)
- [ ] Espaço em disco (`df -h`)
- [ ] Memória disponível (`free -h`)

**Se todos os itens estão OK e ainda há problemas, é hora de pedir ajuda!** 🆘
