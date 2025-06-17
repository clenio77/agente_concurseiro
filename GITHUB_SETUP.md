# 🐙 Guia GitHub - Agente Concurseiro

## Subindo o Projeto para o GitHub

### 1. Pré-requisitos
- Conta no GitHub
- Git instalado e configurado

### 2. Inicializando o Repositório
```bash
cd /caminho/para/agente_concurseiro
git init
git add .
git commit -m "Initial commit"
```

### 3. Adicionando o Remoto
```bash
git remote add origin https://github.com/SEU_USUARIO/agente-concurseiro.git
git branch -M main
git push -u origin main
```

### 4. Autenticação
- Use token de acesso pessoal ou SSH
- Configure usuário e email:
```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### 5. Dicas de Versionamento
- Commits frequentes e descritivos
- Use branches para novas features
- Pull requests para revisão

---

Para visão geral do projeto, consulte o [README.md](README.md).
