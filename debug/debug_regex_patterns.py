#!/usr/bin/env python3
"""
Debug dos padrões regex para extração de conteúdo
"""

import re

def debug_regex_patterns():
    """Debug dos padrões regex"""
    print("🔍 DEBUG DOS PADRÕES REGEX")
    print("="*50)
    
    # Texto de teste
    edital_texto = """
    CONCURSO PÚBLICO - PREFEITURA MUNICIPAL
    
    CARGO: Contador
    
    MATÉRIAS:
    Português: 20 questões
    Matemática: 15 questões  
    Contabilidade Geral: 25 questões
    
    CONTEÚDO PROGRAMÁTICO:
    
    Português: Interpretação e compreensão de textos de gêneros variados; 
    Reconhecimento de tipos e gêneros textuais; Domínio da ortografia oficial; 
    Emprego das letras; Emprego da acentuação gráfica; Emprego do sinal indicativo de crase;
    Flexão nominal e verbal; Pronomes; Emprego de tempos e modos verbais;
    Vozes do verbo; Concordância nominal e verbal; Regência nominal e verbal;
    Sintaxe do período e da oração; Pontuação; Estilística.
    
    Contabilidade Geral: Conceito, objeto e objetivo da contabilidade;
    Patrimônio: componentes, equação fundamental do patrimônio, situação líquida;
    Contas: conceito, contas de débito e crédito e saldos; Plano de contas;
    Fatos contábeis: conceito, fatos permutativos, modificativos e mistos;
    Balancete de verificação; Balanço patrimonial; Demonstração do resultado do exercício;
    Demonstração de lucros ou prejuízos acumulados; Demonstração das mutações;
    Análise das demonstrações financeiras; Contabilidade de custos; Orçamento público.
    """
    
    content_lower = edital_texto.lower()
    materia = "Contabilidade Geral"
    materia_lower = materia.lower()
    
    print(f"🎯 BUSCANDO CONTEÚDO PARA: {materia}")
    print(f"Matéria em minúsculas: {materia_lower}")
    
    # Testar padrões individualmente
    padroes_teste = [
        # Padrão 1: Matéria: conteúdo até próxima matéria
        rf'{re.escape(materia_lower)}\s*[:\-]\s*([^;]+(?:;[^;]+)*)(?:\s*(?:português|matemática|direito|informática|administração|contabilidade|auditoria|controle)|\s*$)',
        
        # Padrão 2: conteúdo após nome da matéria até próxima seção
        rf'(?:^|\n)\s*{re.escape(materia_lower)}\s*[:\-]\s*(.+?)(?:\n\s*(?:[A-Z][a-záéíóúâêôãõç]+(?:\s+[A-Z][a-záéíóúâêôãõç]+)*)\s*[:\-]|\n\n|$)',
        
        # Padrão 3: seção específica da matéria
        rf'{re.escape(materia_lower)}[:\-\s]*(.{{50,1200}}?)(?:questões?|pontos?|peso|próxima\s+matéria|\n\s*[A-Z][a-z]+\s*[:\-])',
        
        # Padrão 4: CONTEÚDO PROGRAMÁTICO
        rf'conteúdo\s+programático[:\-\s]*.*?{re.escape(materia_lower)}\s*[:\-]\s*(.+?)(?:\n\s*[A-Z][a-z]+\s*[:\-]|\n\n|$)',
        
        # Padrão simples para teste
        rf'{re.escape(materia_lower)}\s*:\s*(.+?)(?=\n\s*[A-Z]|\n\n|$)',
    ]
    
    for i, padrao in enumerate(padroes_teste, 1):
        print(f"\n🧪 TESTANDO PADRÃO {i}:")
        print(f"Regex: {padrao}")
        
        match = re.search(padrao, content_lower, re.IGNORECASE | re.DOTALL | re.MULTILINE)
        
        if match:
            conteudo_extraido = match.group(1).strip()
            print(f"✅ MATCH ENCONTRADO!")
            print(f"Conteúdo extraído ({len(conteudo_extraido)} chars):")
            print(f"'{conteudo_extraido[:200]}{'...' if len(conteudo_extraido) > 200 else ''}'")
            
            # Verificar se contém palavras-chave de contabilidade
            palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
            palavras_encontradas = [p for p in palavras_contabilidade if p in conteudo_extraido.lower()]
            print(f"Palavras-chave encontradas: {palavras_encontradas}")
            
            if palavras_encontradas:
                print("🎉 PADRÃO FUNCIONAL!")
                break
        else:
            print("❌ Nenhum match encontrado")
    
    # Teste manual simples
    print(f"\n🔍 TESTE MANUAL SIMPLES:")
    
    # Buscar a linha que contém "contabilidade geral:"
    linhas = content_lower.split('\n')
    for i, linha in enumerate(linhas):
        if 'contabilidade geral:' in linha:
            print(f"Linha {i}: {linha.strip()}")
            
            # Pegar as próximas linhas até encontrar uma nova matéria
            conteudo_manual = []
            for j in range(i, len(linhas)):
                linha_atual = linhas[j].strip()
                if j > i and any(materia_nome in linha_atual for materia_nome in ['português:', 'matemática:', 'direito:', 'informática:']):
                    break
                if j > i and linha_atual:  # Pular a primeira linha (nome da matéria)
                    conteudo_manual.append(linha_atual)
            
            conteudo_manual_texto = ' '.join(conteudo_manual)
            print(f"Conteúdo manual extraído: {conteudo_manual_texto[:200]}...")
            
            palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
            palavras_encontradas_manual = [p for p in palavras_contabilidade if p in conteudo_manual_texto.lower()]
            print(f"Palavras-chave no conteúdo manual: {palavras_encontradas_manual}")
            
            break

if __name__ == "__main__":
    debug_regex_patterns()
