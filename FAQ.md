# ❓ FAQ - Perguntas Frequentes

## Instalação

**❌ "No module named 'pkg_resources'"**
- Execute `./fix-pkg-resources.sh` ou veja o [Guia de Instalação](INSTALLATION_GUIDE.md).

**❌ "Command not found: streamlit"**
- Adicione ao PATH: `export PATH=$PATH:$HOME/.local/bin`.

**❌ "Permission denied" ao rodar scripts**
- Dê permissão: `chmod +x install-simple.sh install.sh deploy.sh`.

**❌ "Python version too old"**
- Use Python 3.11+. Veja instruções detalhadas no [Guia de Instalação](INSTALLATION_GUIDE.md).

## Execução

**❌ "Address already in use"**
- Use outra porta: `streamlit run app/app.py --server.port 8502`.
- Ou mate o processo: `lsof -ti:8501 | xargs kill -9`.

**❌ "ModuleNotFoundError: No module named 'app'"**
- Execute do diretório correto: `cd agente-concurseiro`.

**❌ "FileNotFoundError: config.yaml"**
- Crie o arquivo `.env` ou rode `./install-simple.sh`.

## Uso

**Como criar conta?**
- Acesse `http://localhost:8501` e clique em "Criar Conta".

**Como redefinir senha?**
- Use a opção "Esqueci minha senha" na tela de login.

**Como atualizar o sistema?**
- Faça pull do repositório e rode novamente o script de instalação.

## Suporte

- Consulte o [Guia de Instalação](INSTALLATION_GUIDE.md) para problemas detalhados.
- Reporte bugs em [GitHub Issues](https://github.com/seu-usuario/agente-concurseiro/issues).
