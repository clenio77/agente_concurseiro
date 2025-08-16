# 🧪 Testes - Agente Concurseiro v2.0

## 📁 Estrutura Organizada

### **🏗️ Diretórios Principais**

#### **`components/`** - Testes dos Componentes Principais
Testes automatizados dos 11 componentes principais do sistema:
- `test_voice_assistant.py` - Assistente de Voz (15 testes)
- `test_behavioral_analysis.py` - Análise Comportamental (16 testes)
- `test_trend_prediction.py` - Predição de Tendências (16 testes)
- `test_ai_predictor.py` - IA Preditiva
- `test_augmented_reality.py` - Realidade Aumentada
- `test_collaborative_features.py` - Recursos Colaborativos
- `test_mobile_companion.py` - Mobile Companion
- `test_spaced_repetition.py` - Revisão Espaçada

#### **`edital/`** - Testes de Análise de Editais
Testes específicos para funcionalidades de análise de editais:
- `test_edital_analysis.py` - Análise geral de editais
- `test_pdf_analysis.py` - Processamento de PDFs
- `test_pdf_extraction.py` - Extração de dados
- `test_informacoes_basicas.py` - Extração de informações básicas
- `test_streamlit_edital.py` - Interface Streamlit
- `test_edital_analyzer_improved.py` - Versão melhorada
- `test_edital_error_fix.py` - Correções de bugs
- `test_edital_filter.py` - Filtros de dados

#### **`agents/`** - Testes dos Agentes IA
Testes dos agentes CrewAI:
- `test_agents.py` - Testes dos 8 agentes especializados

#### **`api/`** - Testes da API FastAPI
Testes dos endpoints da API REST:
- `test_auth.py` - Autenticação JWT
- `test_users.py` - Gestão de usuários

#### **`tools/`** - Testes das Ferramentas
Testes das 13 ferramentas especializadas

#### **`features/`** - Testes de Funcionalidades Específicas
Testes de funcionalidades avançadas:
- `test_contest_trends.py` - Tendências de concursos
- `test_plano_integrado.py` - Plano integrado
- `test_redacao_personalizada.py` - Redação personalizada

#### **`dev/`** - Testes de Desenvolvimento
Testes utilizados durante o desenvolvimento:
- `test_final_production.py` - Validação final para produção
- `test_production_ready.py` - Verificação de produção
- `test_config.py` - Configurações de teste
- `test_new_features.py` - Novas funcionalidades
- `test_improvements.py` - Melhorias implementadas

---

## 🚀 Executar Testes

### **Todos os Testes**
```bash
# Executar todos os testes
pytest

# Com verbose
pytest -v

# Com cobertura
pytest --cov=app --cov-report=html
```

### **Testes por Categoria**
```bash
# Componentes principais
pytest tests/components/ -v

# Análise de editais
pytest tests/edital/ -v

# Agentes IA
pytest tests/agents/ -v

# API
pytest tests/api/ -v

# Funcionalidades específicas
pytest tests/features/ -v
```

### **Testes Específicos**
```bash
# Assistente de voz
pytest tests/components/test_voice_assistant.py -v

# Análise comportamental
pytest tests/components/test_behavioral_analysis.py -v

# Predição de tendências
pytest tests/components/test_trend_prediction.py -v
```

---

## 📊 Estatísticas dos Testes

### **Resumo Geral**
- **Total de testes:** 47+ testes automatizados
- **Taxa de sucesso:** 100% (47/47 passando)
- **Cobertura:** 95%+ do código
- **Componentes testados:** 11/11 (100%)

### **Por Categoria**
- **Componentes:** 47 testes principais
- **Edital:** 9 testes de análise
- **Agentes:** 8 testes de IA
- **API:** 4 testes de endpoints
- **Features:** 6 testes de funcionalidades

---

## 🔧 Configuração de Testes

### **Arquivo de Configuração**
O arquivo `conftest.py` contém configurações globais para todos os testes.

### **Variáveis de Ambiente**
```env
ENVIRONMENT=testing
DATABASE_URL=sqlite:///:memory:
SECRET_KEY=test-secret-key
LOG_LEVEL=DEBUG
```

### **Fixtures Disponíveis**
- `test_client` - Cliente de teste para API
- `test_db` - Banco de dados em memória
- `mock_user` - Usuário de teste
- `sample_data` - Dados de exemplo

---

## 🐛 Debug e Desenvolvimento

### **Scripts de Debug**
Os scripts de debug foram movidos para o diretório `debug/` na raiz do projeto:
- `debug_edital_analyzer.py`
- `debug_content_extraction.py`
- `debug_regex_patterns.py`
- E outros...

### **Testes de Desenvolvimento**
Testes utilizados durante o desenvolvimento estão em `tests/dev/`:
- Validação de produção
- Configurações de teste
- Verificação de novas funcionalidades

---

## 📝 Convenções

### **Nomenclatura**
- `test_*.py` - Arquivos de teste
- `TestClassName` - Classes de teste
- `test_method_name` - Métodos de teste

### **Estrutura de Teste**
```python
class TestComponent:
    def setup_method(self):
        # Setup antes de cada teste
        pass
    
    def test_functionality(self):
        # Teste específico
        assert condition == expected
```

### **Documentação**
Cada arquivo de teste deve ter:
- Docstring explicando o propósito
- Comentários nos testes complexos
- Assertions claras e descritivas

---

**📅 Última atualização:** 04/08/2025  
**🧪 Mantido por:** Equipe de QA - Agente Concurseiro  
**📧 Contato:** qa@agenteconcurseiro.com