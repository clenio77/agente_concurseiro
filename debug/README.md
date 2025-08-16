# 🐛 Debug Scripts - Agente Concurseiro v2.0

## 📁 Scripts de Debug e Desenvolvimento

Este diretório contém scripts utilizados durante o desenvolvimento para debug, análise e resolução de problemas específicos.

### **📋 Scripts Disponíveis**

#### **Análise de Editais**
- `debug_edital_analyzer.py` - Debug do analisador de editais
- `debug_analisar_edital.py` - Análise específica de editais
- `debug_content_extraction.py` - Extração de conteúdo
- `debug_text_structure.py` - Estrutura de texto
- `debug_limpar_conteudo.py` - Limpeza de conteúdo

#### **Análise de Cargos**
- `debug_cargo_comparison.py` - Comparação de cargos
- `debug_cargo_especifico.py` - Análise de cargo específico
- `debug_padroes_cargo.py` - Padrões de cargos

#### **Processamento de Dados**
- `debug_detectar_materias.py` - Detecção de matérias
- `debug_regex_patterns.py` - Padrões de regex
- `debug_edital.py` - Debug geral de editais

#### **Fluxo Completo**
- `debug_full_flow.py` - Debug do fluxo completo
- `debug_step_by_step.py` - Análise passo a passo

---

## 🚀 Como Usar

### **Executar Script de Debug**
```bash
# Executar script específico
python debug/debug_edital_analyzer.py

# Com argumentos
python debug/debug_content_extraction.py --file edital.pdf

# Com debug verbose
python debug/debug_full_flow.py --verbose
```

### **Configuração de Ambiente**
```bash
# Configurar variáveis para debug
export DEBUG=true
export LOG_LEVEL=DEBUG
export ENVIRONMENT=development
```

---

## 🔧 Funcionalidades dos Scripts

### **Debug do Analisador de Editais**
```python
# debug_edital_analyzer.py
def debug_edital_analyzer():
    """Debug completo do analisador"""
    - Testa extração de texto
    - Valida regex patterns
    - Verifica conversões de dados
    - Analisa estrutura do PDF
```

### **Debug de Extração de Conteúdo**
```python
# debug_content_extraction.py
def debug_content_extraction():
    """Debug da extração de conteúdo"""
    - Analisa estrutura do PDF
    - Testa diferentes métodos de extração
    - Valida limpeza de texto
    - Verifica encoding
```

### **Debug de Padrões Regex**
```python
# debug_regex_patterns.py
def debug_regex_patterns():
    """Debug dos padrões de regex"""
    - Testa todos os padrões
    - Valida matches
    - Analisa falsos positivos
    - Otimiza performance
```

---

## 📊 Logs e Saída

### **Formato de Log**
```
[DEBUG] 2025-08-04 20:30:15 - debug_edital_analyzer.py:45
Testando extração de texto do PDF...
✅ Texto extraído com sucesso: 1234 caracteres

[DEBUG] 2025-08-04 20:30:16 - debug_regex_patterns.py:23
Testando padrão de cargo: r'cargo[:\s]+([^.\n]+)'
✅ Match encontrado: 'Analista Judiciário'
```

### **Arquivos de Saída**
Os scripts podem gerar arquivos de debug:
- `debug_output.txt` - Saída detalhada
- `extracted_text.txt` - Texto extraído
- `regex_matches.json` - Matches encontrados
- `error_log.txt` - Erros encontrados

---

## 🐛 Resolução de Problemas

### **Problemas Comuns**

#### **Erro de Importação**
```bash
# Adicionar ao PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Ou executar do diretório raiz
python -m debug.debug_edital_analyzer
```

#### **Arquivo PDF Não Encontrado**
```bash
# Verificar se o arquivo existe
ls -la edital.pdf

# Usar caminho absoluto
python debug/debug_edital_analyzer.py --file /path/to/edital.pdf
```

#### **Erro de Encoding**
```python
# Forçar encoding UTF-8
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()
```

---

## 📝 Desenvolvimento

### **Criar Novo Script de Debug**
```python
#!/usr/bin/env python3
"""
Debug para [funcionalidade específica]
"""

import sys
import os
from pathlib import Path

# Adicionar raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def debug_functionality():
    """Debug da funcionalidade"""
    print("🐛 Iniciando debug...")
    
    try:
        # Código de debug aqui
        pass
    except Exception as e:
        print(f"❌ Erro: {e}")
    else:
        print("✅ Debug concluído com sucesso")

if __name__ == "__main__":
    debug_functionality()
```

### **Convenções**
- Nome do arquivo: `debug_[funcionalidade].py`
- Função principal: `debug_[funcionalidade]()`
- Logs claros com emojis
- Tratamento de erros
- Documentação inline

---

## ⚠️ Importante

### **Uso Apenas para Desenvolvimento**
- ❌ **NÃO usar em produção**
- ❌ **NÃO commitar dados sensíveis**
- ❌ **NÃO incluir no deploy**

### **Dados de Teste**
- Use apenas dados de exemplo
- Não inclua informações pessoais
- Remova arquivos temporários após uso

### **Performance**
- Scripts podem ser lentos (debug mode)
- Use apenas para análise pontual
- Não execute em loops contínuos

---

**📅 Última atualização:** 04/08/2025  
**🐛 Mantido por:** Equipe de Desenvolvimento  
**📧 Contato:** dev@agenteconcurseiro.com