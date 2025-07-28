# 🤖 GEMINI.md - Visão Geral do Projeto Agente Concurseiro

Este documento fornece uma visão abrangente do projeto "Agente Concurseiro", projetado para que agentes de IA entendam rapidamente seu propósito, arquitetura, funcionalidades e diretrizes operacionais.

## 1. Visão Geral do Projeto

O **Agente Concurseiro** é uma plataforma completa e moderna para preparação de concursos públicos, utilizando **Inteligência Artificial** e **gamificação** para maximizar o aprendizado e a motivação dos candidatos. É projetado para produção, com alta disponibilidade.

**Diferenciais:**
-   **Especialização por Banca**: Avaliação específica para CESPE, FCC, VUNESP, FGV e IBFC.
-   **IA Avançada**: Integração com GPT-4 para análises e recomendações personalizadas.
-   **Gamificação Científica**: Sistema motivacional baseado em psicologia comportamental.
-   **Analytics Profissional**: Predição de desempenho com mais de 85% de acurácia.
-   **Infraestrutura Empresarial**: 100% conteinerizado e escalável.


**Estatísticas do Projeto:**
-   23 Funcionalidades Principais Implementadas
-   5 Bancas Suportadas
-   15 Conquistas + 9 Insígnias Gamificadas
-   Integração real com IA (OpenAI GPT-4)
-   95% de Conclusão

## 2. Funcionalidades Principais

O sistema oferece uma ampla gama de funcionalidades para apoiar os candidatos:

### Sistemas Centrais:
-   **Sistema Avançado de Redação**: Avaliação específica por banca, feedback detalhado, acompanhamento de progresso.
-   **Simulados Adaptativos**: Questões reais de provas anteriores, dificuldade adaptativa, análise detalhada dos resultados.
-   **Analytics & Predição com IA**: Predição de desempenho final, análise de 8 métricas, simulação de cenários "e se", recomendações com IA, gráficos interativos.
-   **Sistema de Gamificação**: 15 conquistas progressivas, 9 insígnias categorizadas, sistema de níveis (XP), streaks motivacionais, ranking.
-   **Planos de Estudo Personalizados**: Cronogramas baseados no perfil do candidato, distribuição inteligente de matérias, adaptação automática ao progresso.
-   **Sistema Inteligente de Notificações**: 7 tipos de notificações contextuais, lembretes personalizados, alertas de desempenho em tempo real, celebração de conquistas.

### Agentes de IA (CrewAI):
-   `SearchAgent`: Busca inteligente de provas anteriores.
-   `StudyPlanAgent`: Criação de plano de estudo personalizado.
-   `MockExamAgent`: Geração de simulados adaptativos.
-   `WritingAgent`: Avaliação automatizada de redações.
-   `CoordinatorAgent`: Coordenação entre componentes.
-   `SpacedRepetitionAgent`: Sistema de repetição espaçada.
-   `PerformancePredictionAgent`: Análise preditiva de desempenho.
-   `QuestionAgent`: Gestão inteligente de questões.

### Ferramentas Avançadas:
-   `MockExamTool`: Simulados realistas conforme padrão das bancas.
-   `WebSearchTool`: Busca inteligente de provas e materiais.
-   `QuestionAPITool`: Banco de questões com 12+ questões reais.
-   `StudyPlanTool`: Planos personalizados por banca e cargo.
-   `SpacedRepetitionTool`: Otimização da memorização.
-   `PerformanceAnalysisTool`: Análise detalhada de desempenho.
-   `WritingTool`: Avaliação de redações com critérios específicos.
-   `RecommendationTool`: Recomendações personalizadas.
-   `ProgressTrackingTool`: Acompanhamento de progresso.
-   `CalendarIntegrationTool`: Integração com calendário.
-   `ExamAnalysisTool`: Análise de padrão de provas.
-   `CoordinationTool`: Coordenação de componentes.
-   `PerformancePredictionTool`: Predições baseadas em dados.

## 3. Instalação & Configuração

O projeto pode ser configurado rapidamente usando scripts ou manualmente.

### Instalação Rápida (3 Comandos):
```bash
# 1. Clonar o repositório
git clone https://github.com/seu-usuario/agente-concurseiro.git
cd agente-concurseiro

# 2. Instalar (simples)
chmod +x install-simple.sh
./install-simple.sh

# 3. Executar
python3 run_app.py
```
Acesse: `http://localhost:8501`

### Instalação Detalhada:
Consulte `INSTALLATION_GUIDE.md` para etapas detalhadas, pré-requisitos (Python 3.11+, Docker, Git) e resolução de problemas.

### Configuração no GitHub:
O projeto pode ser adicionado ao GitHub usando `setup-github.sh` ou manualmente. Veja `COMO_ADICIONAR_AO_GITHUB.md` e `GITHUB_SETUP.md` para instruções sobre criação de repositório, configuração do Git e autenticação (usando Personal Access Token).

### Salvando Localmente:
Para salvar o projeto localmente, utilize download direto, `git clone` ou cópia manual. Veja `COMO_SALVAR_LOCALMENTE.md` para métodos e etapas de verificação.

## 4. Uso

### Acessando o Sistema:
-   **Interface Streamlit**: Abra `http://localhost:8501` no navegador.
-   **API FastAPI**: Acesse `http://localhost:8000`.

### Primeiros Passos:
1.  Faça login ou crie uma conta.
2.  Configure seu perfil e plano de estudos.
3.  Realize simulados e redações.
4.  Acompanhe seu progresso no dashboard.
5.  Utilize recomendações e notificações para melhorar.

## 5. Especificações Técnicas

### Arquitetura:
O sistema possui arquitetura modular, utilizando:
-   **CrewAI**: Orquestração inteligente de agentes.
-   **Streamlit**: Interface web interativa.
-   **FastAPI**: API REST moderna.
-   **SQLAlchemy**: ORM para interação com banco de dados.
-   **Pydantic**: Validação de dados.
-   **Altair**: Visualizações interativas.
-   **Pandas**: Manipulação de dados.

### Estrutura de Diretórios:
```
agente_concurseiro/
├── app/                          # Aplicação principal
│   ├── agents/                   # Agentes CrewAI
│   ├── api/                      # API FastAPI
│   ├── core/                     # Configurações centrais
│   ├── db/                       # Modelos de banco de dados
│   ├── pages/                    # Páginas Streamlit
│   ├── schemas/                  # Schemas Pydantic
│   ├── utils/                    # Utilidades
│   ├── app.py                    # Interface Streamlit
│   └── main.py                   # API FastAPI
├── tools/                        # Ferramentas especializadas
├── data/                         # Dados e configurações
│   ├── questions/                # Banco de questões
│   ├── dashboard/                # Dados do dashboard
│   └── previous_exams/           # Provas anteriores
├── tests/                        # Testes automatizados
└── requirements.txt              # Dependências
```

### Banco de Dados:
Utiliza SQLite por padrão (`sqlite:///./data/app.db`), podendo ser configurado para PostgreSQL.

### Configuração de IA:
Chave da OpenAI e outros parâmetros são configurados via variáveis de ambiente (`.env`) e `app/ai/config.py`.

## 6. Solução de Problemas & FAQ

Problemas comuns e soluções estão detalhados em `FAQ.md` e na seção de Troubleshooting do `README.md`.

**Exemplos:**
-   "No module named 'pkg_resources'": Execute `./fix-pkg-resources.sh`.
-   "Permission denied": Dê permissão de execução (`chmod +x *.sh`).
-   "Address already in use": Use outra porta (`streamlit run app/app.py --server.port 8502`).
-   Problemas com API da OpenAI, lentidão na interface Streamlit, problemas de conexão com banco de dados também são abordados.

## 7. Roadmap & Melhorias Futuras

### Melhorias Implementadas (Alta & Média Prioridade):
-   **Alta Prioridade**: Refatoração do MockExamTool, WebSearchTool com busca real, interface Streamlit renovada.
-   **Média Prioridade**: Sistema de gamificação completo, análise preditiva avançada, sistema de recomendações com IA aprimorado, página de analytics completa, sistema inteligente de notificações, dashboard gamificado.

### Roadmap Futuro:
-   **Versão 2.1 (Próxima)**: Integração real com API de questões, notificações push, backup em nuvem, modo offline.
-   **Versão 2.2**: Grupos de estudo colaborativos, mentoria com IA, correção de redações em tempo real com IA, gamificação avançada.
-   **Versão 3.0**: Machine Learning para adaptação, Realidade Aumentada para estudos, integração com wearables, marketplace de conteúdos.

## 8. Contribuição

Contribuições são bem-vindas. Veja `GITHUB_SETUP.md` e `app/README.md` para diretrizes sobre fork, criação de branch, commits e Pull Requests.

## 9. Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para detalhes.

## 10. Contato & Suporte

-   **Email**: suporte@agenteconcurseiro.com / clenioti@gmail.com
-   **Discord**: [Servidor da Comunidade](https://discord.gg/agenteconcurseiro)
-   **GitHub Issues**: [Reportar Problemas](https://github.com/clenio77/agente_concurseiro/issues)
-   **GitHub Discussions**: [Discussões](https://github.com/clenio77/agente_concurseiro/discussions)
