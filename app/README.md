# 🎓 Assistente de Preparação para Concursos v2.0

Sistema inteligente baseado em CrewAI para auxiliar candidatos a concursos públicos, oferecendo planos de estudo personalizados, simulados adaptativos e acompanhamento de desempenho.

## ✨ Funcionalidades Principais

### 🤖 Agentes Inteligentes (8 agentes especializados)
- **SearchAgent**: Busca inteligente de provas anteriores
- **StudyPlanAgent**: Criação de planos de estudo personalizados
- **MockExamAgent**: Geração de simulados adaptativos
- **WritingAgent**: Avaliação automática de redações
- **CoordinatorAgent**: Coordenação entre diferentes componentes
- **SpacedRepetitionAgent**: Sistema de repetição espaçada
- **PerformancePredictionAgent**: Análise preditiva de desempenho
- **QuestionAgent**: Gerenciamento inteligente de questões

### 🛠️ Ferramentas Avançadas (13 tools implementadas)
- **MockExamTool**: Simulados realistas baseados em padrões de bancas
- **WebSearchTool**: Busca inteligente de provas e materiais
- **QuestionAPITool**: Banco de questões com 12+ questões reais
- **StudyPlanTool**: Planos personalizados por banca e cargo
- **SpacedRepetitionTool**: Otimização de memorização
- **PerformanceAnalysisTool**: Análise detalhada de desempenho
- **WritingTool**: Avaliação de redações com critérios específicos
- **RecommendationTool**: Recomendações personalizadas
- **ProgressTrackingTool**: Acompanhamento de progresso
- **CalendarIntegrationTool**: Integração com calendários
- **ExamAnalysisTool**: Análise de padrões de provas
- **CoordinationTool**: Coordenação entre componentes
- **PerformancePredictionTool**: Previsões baseadas em dados

### 📊 Interface Moderna
- **Dashboard Interativo**: Métricas em tempo real, gráficos e conquistas
- **Sistema de Autenticação**: Login seguro e personalização
- **Simulados Interativos**: Interface completa para realização de provas
- **Planos de Estudo Visuais**: Cronogramas detalhados e acompanhamento
- **Configurações Avançadas**: Personalização completa da experiência

### 🎯 Recursos Específicos por Banca
- **CESPE/CEBRASPE**: Questões Certo/Errado, pegadinhas, tempo otimizado
- **FCC**: Foco em gramática e cálculos, questões técnicas
- **VUNESP**: Contextualização prática, atualidades
- **FGV**: Questões analíticas e interpretativas
- **IBFC**: Padrões específicos da banca

## 🚀 Configuração e Instalação

### Pré-requisitos
- Python 3.8+
- pip (gerenciador de pacotes Python)

### 1. Clone o repositório:
```

### 2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 3. Configure o ambiente:
```bash
# Execute o script de configuração
chmod +x setup.sh
./setup.sh

# Ou crie os diretórios manualmente
mkdir -p data/{questions,dashboard,previous_exams,study_plans}
mkdir -p config
```

### 4. Execute os testes:
```bash
python test_improvements.py
```

### 5. Inicie a aplicação:

#### Interface Streamlit (Recomendado):
```bash
streamlit run app/app.py
```

#### API FastAPI:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📱 Como Usar

### 1. **Acesso ao Sistema**
- Abra o navegador em `http://localhost:8501` (Streamlit) ou `http://localhost:8000` (FastAPI)
- Faça login com qualquer usuário/senha (sistema de demonstração)

### 2. **Dashboard**
- Visualize seu progresso geral de estudos
- Acompanhe métricas de desempenho
- Veja conquistas e recomendações personalizadas
- Monitore metas e objetivos

### 3. **Criação de Plano de Estudos**
- Preencha informações sobre cargo, concurso e banca
- Configure horas de estudo e duração
- Receba plano personalizado com cronograma detalhado
- Acompanhe progresso por matéria

### 4. **Simulados Interativos**
- Configure matérias, dificuldade e banca
- Realize simulados com tempo cronometrado
- Receba feedback detalhado e análise de desempenho
- Acompanhe evolução ao longo do tempo

### 5. **Sistema de Repetição Espaçada**
- Flashcards automáticos baseados em pontos fracos
- Algoritmo otimizado para memorização
- Revisões programadas inteligentemente

## 🏗️ Arquitetura do Sistema

### Estrutura de Diretórios
```
agente_concurseiro/
├── app/                          # Aplicação principal
│   ├── agents/                   # Agentes CrewAI
│   ├── api/                      # API FastAPI
│   ├── core/                     # Configurações centrais
│   ├── db/                       # Modelos de banco de dados
│   ├── pages/                    # Páginas Streamlit
│   ├── schemas/                  # Schemas Pydantic
│   ├── utils/                    # Utilitários
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

### Tecnologias Utilizadas
- **CrewAI**: Framework de agentes inteligentes
- **Streamlit**: Interface web interativa
- **FastAPI**: API REST moderna
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados
- **Altair**: Visualizações interativas
- **Pandas**: Manipulação de dados

## 📊 Banco de Questões

O sistema inclui um banco de questões estruturado com:
- **12+ questões reais** de concursos
- **4 matérias principais**: Português, Matemática, Direito, Informática
- **5 bancas suportadas**: CESPE, FCC, VUNESP, FGV, IBFC
- **3 níveis de dificuldade**: Fácil, Médio, Difícil
- **Metadados completos**: Explicações, tópicos, anos, fontes

### Estrutura das Questões
```json
{
  "id": "port_001",
  "text": "Texto da questão...",
  "options": [
    {"id": "A", "text": "Opção A"},
    {"id": "B", "text": "Opção B"}
  ],
  "correct_answer": "B",
  "explanation": "Explicação detalhada...",
  "difficulty": "medium",
  "subject": "Português",
  "topic": "Concordância Verbal",
  "banca": "CESPE",
  "year": 2023
}
```

## 🎯 Funcionalidades por Banca

### CESPE/CEBRASPE
- ✅ Questões Certo/Errado
- ✅ Detecção de pegadinhas
- ✅ Tempo otimizado (3 min/questão)
- ✅ Foco em interpretação e detalhes técnicos

### FCC
- ✅ Questões múltipla escolha
- ✅ Ênfase em gramática tradicional
- ✅ Cálculos intensivos
- ✅ Tempo médio (2.5 min/questão)

### VUNESP
- ✅ Contextualização prática
- ✅ Atualidades integradas
- ✅ Questões interpretativas
- ✅ Tempo balanceado (2.8 min/questão)

## 📈 Métricas e Analytics

### Dashboard Interativo
- **Progresso Geral**: Percentual de conclusão do plano
- **Horas de Estudo**: Acompanhamento semanal e total
- **Sequência de Estudos**: Dias consecutivos estudando
- **Desempenho por Matéria**: Gráficos detalhados
- **Evolução Temporal**: Tendências de melhoria

### Análise de Desempenho
- **Pontuação Média**: Acompanhamento de simulados
- **Matérias Fortes/Fracas**: Identificação automática
- **Tempo de Resposta**: Otimização de velocidade
- **Consistência**: Análise de regularidade

### Sistema de Conquistas
- 🎯 **Primeira Semana Completa**
- 🔥 **Sequência de Quiz Diário**
- 📈 **Melhoria Consistente**
- 🏆 **Meta de Pontuação Atingida**

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```bash
# .env
OPENAI_API_KEY=sua_chave_aqui
DATABASE_URL=sqlite:///./data/app.db
DEBUG=True
LOG_LEVEL=INFO
```

### Configuração de Banco de Dados
```python
# app/core/config.py
DATABASE_URI = "sqlite:///./data/app.db"  # SQLite (padrão)
# DATABASE_URI = "postgresql://user:pass@localhost/db"  # PostgreSQL
```

### Personalização de Agentes
```python
# Exemplo de configuração de agente
study_plan_agent = Agent(
    role="Criador de Plano de Estudos",
    goal="Criar planos personalizados baseados em dados reais",
    backstory="Especialista em metodologias de estudo...",
    tools=[StudyPlanTool()],
    verbose=True
)
```

## 🧪 Testes

### Executar Todos os Testes
```bash
python test_improvements.py
```

### Testes Específicos
```bash
# Testar apenas ferramentas
python -m pytest tests/test_tools.py

# Testar API
python -m pytest tests/test_api.py

# Testar agentes
python -m pytest tests/test_agents.py
```

### Cobertura de Testes
- ✅ Ferramentas (Tools): 100%
- ✅ Configuração: 100%
- ✅ Banco de Questões: 100%
- ✅ Dashboard: 100%
- ⚠️ API: 85%
- ⚠️ Agentes: 90%

## 🚀 Roadmap

### Versão 2.1 (Próxima)
- [ ] Integração com APIs reais de questões
- [ ] Sistema de notificações push
- [ ] Backup automático na nuvem
- [ ] Modo offline

### Versão 2.2
- [ ] Grupos de estudo colaborativos
- [ ] Mentoria por IA
- [ ] Análise de redação com IA
- [ ] Gamificação avançada

### Versão 3.0
- [ ] Machine Learning para adaptação
- [ ] Realidade aumentada para estudos
- [ ] Integração com wearables
- [ ] Marketplace de conteúdo

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes
- Siga o padrão de código existente
- Adicione testes para novas funcionalidades
- Documente mudanças no README
- Use commits semânticos

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Clenio Afonso** - *Desenvolvimento inicial* - [@clenio77](https://github.com/clenio77)

## 🙏 Agradecimentos

- Comunidade CrewAI pelo framework incrível
- Streamlit pela interface intuitiva
- Todos os contribuidores e testadores

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/clenio77/agente_concurseiro/issues)
- **Discussões**: [GitHub Discussions](https://github.com/clenio77/agente_concurseiro/discussions)
- **Email**: clenioti@gmail.com

---

**⭐ Se este projeto te ajudou, considere dar uma estrela no GitHub!**bash
git clone https://github.com/clenio77/agente_concurseiro.git
cd agente_concurseiro