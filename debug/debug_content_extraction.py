#!/usr/bin/env python3
"""
Debug específico da extração de conteúdo
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_content_extraction():
    """Debug da extração de conteúdo"""
    print("🔍 DEBUG DA EXTRAÇÃO DE CONTEÚDO")
    print("="*50)
    
    from app.utils.edital_analyzer import EditalAnalyzer
    
    analyzer = EditalAnalyzer()
    
    # Mesmo edital do teste que está falhando
    edital_conteudo = """
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
    
    print("📄 ANALISANDO EDITAL...")
    resultado = analyzer.analisar_edital(edital_conteudo, ['Contador'])
    
    print(f"\n📊 MATÉRIAS ENCONTRADAS: {len(resultado['materias'])}")
    
    for nome_materia, dados in resultado['materias'].items():
        print(f"\n🔸 {nome_materia}:")
        print(f"  Questões: {dados['questoes']}")
        print(f"  Conteúdo ({len(dados['conteudo'])} tópicos):")
        
        conteudo_texto = ' '.join(dados['conteudo']).lower()
        
        for i, topico in enumerate(dados['conteudo'][:5]):
            print(f"    {i+1}. {topico}")
        
        if 'contabilidade' in nome_materia.lower():
            print(f"\n  🔍 ANÁLISE ESPECÍFICA DE CONTABILIDADE:")
            print(f"  Texto do conteúdo: {conteudo_texto[:200]}...")
            
            palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
            palavras_encontradas = [p for p in palavras_contabilidade if p in conteudo_texto]
            
            print(f"  Palavras-chave encontradas: {palavras_encontradas}")
            
            for palavra in palavras_contabilidade:
                presente = palavra in conteudo_texto
                print(f"    '{palavra}': {'✅' if presente else '❌'}")
    
    # Teste direto do método de extração
    print(f"\n🧪 TESTE DIRETO DO MÉTODO _extrair_conteudo_materia:")
    content_lower = edital_conteudo.lower()
    
    conteudo_direto = analyzer._extrair_conteudo_materia(content_lower, "Contabilidade Geral")
    print(f"Conteúdo extraído diretamente: {len(conteudo_direto)} tópicos")
    
    for i, topico in enumerate(conteudo_direto):
        print(f"  {i+1}. {topico}")
    
    conteudo_direto_texto = ' '.join(conteudo_direto).lower()
    palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
    palavras_encontradas_direto = [p for p in palavras_contabilidade if p in conteudo_direto_texto]
    
    print(f"\nPalavras-chave no conteúdo direto: {palavras_encontradas_direto}")

if __name__ == "__main__":
    debug_content_extraction()
