# 📖 Guia do Desenvolvedor - Agente Concurseiro v2.0

Este documento fornece todas as informações técnicas necessárias para entender, manter e expandir o projeto **Agente Concurseiro**.

---

## 🏛️ Arquitetura e Tecnologias

O sistema é construído sobre uma arquitetura modular e escalável, utilizando tecnologias modernas para garantir performance e manutenibilidade.

### Componentes Principais

-   **Interface Web (Frontend)**: Desenvolvida com **Streamlit**, oferece uma experiência de usuário rica e interativa.
-   **API REST (Backend)**: Construída com **FastAPI**, fornece endpoints rápidos e seguros para todas as operações do sistema.
-   **Orquestração de IA**: Utiliza **CrewAI** para gerenciar 8 agentes de IA especializados que executam tarefas complexas como análise de desempenho, geração de conteúdo e mais.
-   **Banco de Dados**: Usa **SQLite** por padrão para simplicidade e pode ser facilmente configurado para **PostgreSQL** em produção. A interação é gerenciada pelo ORM **SQLAlchemy**.
-   **Containerização**: O ambiente é 100% containerizado com **Docker** e **Docker Compose**, permitindo um setup de desenvolvimento e deploy para produção consistentes.

### Estrutura de Diretórios

```
agente_concurseiro/
├── app/                          # Código fonte da aplicação
│   ├── agents/                   # Definição dos Agentes CrewAI
│   ├── api/                      # Endpoints da API FastAPI
│   ├── core/                     # Configurações centrais (env, logging)
│   ├── db/                       # Modelos de dados (SQLAlchemy)
│   ├── pages/                    # Páginas da interface Streamlit
│   ├── schemas/                  # Esquemas de validação (Pydantic)
│   ├── utils/                    # Funções utilitárias (gamificação, analytics)
│   ├── app.py                    # Ponto de entrada da interface Streamlit
│   └── main.py                   # Ponto de entrada da API FastAPI
├── tools/                        # Ferramentas especializadas usadas pelos agentes
├── data/                         # Dados da aplicação (DB, JSONs)
├── tests/                        # Testes automatizados
├── .dockerignore                 # Arquivos a serem ignorados pelo Docker
├── docker-compose.yml            # Orquestração dos containers
├── Dockerfile                    # Definição do container da aplicação
└── requirements.txt              # Dependências Python
```

---

## 🛠️ Setup Avançado e Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto para configurar variáveis de ambiente. Use o `.env.example` como base.

```env
# Configurações da Aplicação
ENVIRONMENT="development" # ou "production"
SECRET_KEY="uma_chave_secreta_forte"

# Banco de Dados
DATABASE_URL="sqlite:///./data/app.db" # Exemplo para PostgreSQL: "postgresql://user:password@host:port/database"

# API da OpenAI
OPENAI_API_KEY="sk-sua-chave-aqui"

# Configurações de E-mail (se aplicável)
SMTP_SERVER="smtp.example.com"
SMTP_PORT=587
SMTP_USER="seu_email"
SMTP_PASSWORD="sua_senha"
```

### Execução com Docker Compose

Para um ambiente de produção ou para simular um, use o Docker Compose:

```bash
# Construir e iniciar os containers em background
docker-compose up --build -d
```

---

## 🗃️ Modelo de Dados

O banco de dados é projetado para suportar todas as funcionalidades do sistema, com as seguintes entidades principais:

-   **User**: Armazena informações dos usuários, incluindo perfil, metas e dados de autenticação.
-   **StudyPlan**: Contém os planos de estudo gerados, com matérias, horários e progresso.
-   **MockExam**: Registra os simulados realizados, respostas e pontuações.
-   **Essay**: Guarda as redações enviadas, temas e as avaliações recebidas.
-   **Gamification**: Tabela para registrar pontos, conquistas e badges de cada usuário.

Os modelos SQLAlchemy estão definidos em `app/db/models/`.

---

## 🌐 API Endpoints

A API FastAPI expõe diversos endpoints para interagir com o sistema. A documentação completa da API (gerada pelo Swagger) está disponível em `http://localhost:8000/docs` quando a API está em execução.

### Exemplos de Endpoints

-   `POST /auth/register`: Registra um novo usuário.
-   `POST /auth/login`: Autentica um usuário e retorna um token JWT.
-   `POST /study-plans`: Cria um novo plano de estudos para o usuário autenticado.
-   `GET /analytics/performance`: Retorna as métricas de desempenho do usuário.
-   `GET /analytics/predict`: Retorna a predição de nota para a prova final.

---

## 🧪 Testes

O projeto possui uma suíte de testes para garantir a qualidade e a estabilidade do código.

```bash
# Para executar todos os testes
pytest

# Para executar testes de um arquivo específico
pytest tests/test_api.py

# Para ver o relatório de cobertura de testes
pytest --cov=app
```

---

## 📈 Roadmap de Desenvolvimento

O futuro do Agente Concurseiro é promissor. O roadmap abaixo detalha as próximas fases de desenvolvimento.

### Versão 2.1 (Curto Prazo)

-   [ ] **Integração com API Real de Questões**: Substituir o banco de questões JSON por uma API externa para ter acesso a um volume muito maior de questões atualizadas.
-   [ ] **Notificações Push**: Implementar um sistema de notificações push (web ou mobile) para aumentar o engajamento.
-   [ ] **Backup na Nuvem**: Configurar rotinas automáticas de backup do banco de dados para um serviço de armazenamento em nuvem (S3, Google Cloud Storage).
-   [ ] **Modo Offline**: Permitir que os usuários acessem funcionalidades básicas (como revisão de flashcards) sem conexão com a internet.

### Versão 2.2 (Médio Prazo)

-   [ ] **Grupos de Estudo Colaborativos**: Funcionalidade para que usuários possam criar e participar de grupos de estudo, com chat e compartilhamento de materiais.
-   [ ] **Mentoria com IA**: Um agente de IA dedicado a atuar como mentor, fornecendo conselhos de estudo mais aprofundados e personalizados.
-   [ ] **Correção de Redação em Tempo Real**: Utilizar a IA para fornecer feedback instantâneo sobre a estrutura e gramática da redação enquanto o usuário escreve.
-   [ ] **Gamificação Avançada**: Introduzir competições sazonais, desafios em grupo e um sistema de recompensas mais elaborado.

### Versão 3.0 (Longo Prazo)

-   [ ] **Machine Learning para Adaptação Real**: Implementar um modelo de Machine Learning que aprenda com o desempenho de todos os usuários para otimizar os planos de estudo e as predições de forma ainda mais precisa.
-   [ ] **Integração com Wearables**: Sincronizar com dispositivos como smartwatches para monitorar o tempo de estudo e os níveis de estresse, ajustando as recomendações.
-   [ ] **Marketplace de Conteúdo**: Permitir que especialistas e outros usuários criem e vendam planos de estudo, simulados e outros materiais na plataforma.

---

## 🆘 Troubleshooting

-   **Erro `Address already in use`**: Outro processo está usando a porta `8501` ou `8000`. Use `lsof -ti:PORTA | xargs kill -9` para liberar a porta ou configure uma porta diferente.
-   **Erro de Módulo não Encontrado**: Certifique-se de que as dependências foram instaladas corretamente com `pip install -r requirements.txt` e que você está executando os comandos a partir do diretório raiz do projeto.
-   **Problemas com a API da OpenAI**: Verifique se a sua chave da API (`OPENAI_API_KEY`) está correta no arquivo `.env` e se você tem créditos disponíveis na sua conta OpenAI.

Para outros problemas, sinta-se à vontade para abrir uma **Issue** no repositório do GitHub.
