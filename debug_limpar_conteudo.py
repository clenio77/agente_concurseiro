#!/usr/bin/env python3
"""
Debug do método _limpar_conteudo
"""

import sys
import os
from pathlib import Path
import re

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_limpar_conteudo():
    """Debug do método _limpar_conteudo"""
    print("🔍 DEBUG DO MÉTODO _limpar_conteudo")
    print("="*50)
    
    from app.utils.edital_analyzer import EditalAnalyzer
    
    analyzer = EditalAnalyzer()
    
    # Mesmo edital do teste
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
    
    print("📄 CONTEÚDO ORIGINAL:")
    print("Contém 'Contabilidade Geral:'?", 'Contabilidade Geral:' in edital_conteudo)
    print("Contém 'Patrimônio:'?", 'Patrimônio:' in edital_conteudo)
    print("Contém ';'?", ';' in edital_conteudo)
    
    print("\n📄 APÓS _limpar_conteudo:")
    content_clean = analyzer._limpar_conteudo(edital_conteudo)
    print("Contém 'Contabilidade Geral:'?", 'Contabilidade Geral:' in content_clean)
    print("Contém 'Patrimônio:'?", 'Patrimônio:' in content_clean)
    print("Contém ';'?", ';' in content_clean)
    
    print("\n📄 COMPARAÇÃO DE TRECHOS IMPORTANTES:")
    
    # Buscar trecho de contabilidade no original
    original_lower = edital_conteudo.lower()
    pos_contab_orig = original_lower.find('contabilidade geral:')
    if pos_contab_orig >= 0:
        trecho_orig = original_lower[pos_contab_orig:pos_contab_orig+200]
        print(f"Original: '{trecho_orig}'")
    
    # Buscar trecho de contabilidade no limpo
    clean_lower = content_clean.lower()
    pos_contab_clean = clean_lower.find('contabilidade geral')
    if pos_contab_clean >= 0:
        trecho_clean = clean_lower[pos_contab_clean:pos_contab_clean+200]
        print(f"Limpo:    '{trecho_clean}'")
    
    print("\n📄 TESTE COM CONTEÚDO ORIGINAL:")
    materias_original = analyzer._detectar_materias(original_lower, 'Contador')
    print(f"Matérias com original: {list(materias_original.keys())}")
    if 'Contabilidade Geral' in materias_original:
        conteudo_orig = materias_original['Contabilidade Geral']['conteudo']
        print(f"Contabilidade (original): {len(conteudo_orig)} tópicos")
        print(f"  Primeiro: {conteudo_orig[0] if conteudo_orig else 'Nenhum'}")
    
    print("\n📄 TESTE COM CONTEÚDO LIMPO:")
    materias_limpo = analyzer._detectar_materias(clean_lower, 'Contador')
    print(f"Matérias com limpo: {list(materias_limpo.keys())}")
    if 'Contabilidade Geral' in materias_limpo:
        conteudo_limpo = materias_limpo['Contabilidade Geral']['conteudo']
        print(f"Contabilidade (limpo): {len(conteudo_limpo)} tópicos")
        print(f"  Primeiro: {conteudo_limpo[0] if conteudo_limpo else 'Nenhum'}")

if __name__ == "__main__":
    debug_limpar_conteudo()
