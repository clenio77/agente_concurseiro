#!/usr/bin/env python3
"""
Debug comparação entre chamadas com e sem cargo
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_cargo_comparison():
    """Debug comparação entre chamadas"""
    print("🔍 DEBUG COMPARAÇÃO CARGO")
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
    
    content_lower = edital_conteudo.lower()
    
    print("📄 TESTE 1: _detectar_materias SEM cargo")
    materias_sem_cargo = analyzer._detectar_materias(content_lower)
    
    print(f"Matérias encontradas: {list(materias_sem_cargo.keys())}")
    if 'Contabilidade Geral' in materias_sem_cargo:
        conteudo = materias_sem_cargo['Contabilidade Geral']['conteudo']
        print(f"Contabilidade Geral: {len(conteudo)} tópicos")
        print(f"  Primeiro tópico: {conteudo[0] if conteudo else 'Nenhum'}")
    
    print("\n📄 TESTE 2: _detectar_materias COM cargo 'Contador'")
    materias_com_cargo = analyzer._detectar_materias(content_lower, 'Contador')
    
    print(f"Matérias encontradas: {list(materias_com_cargo.keys())}")
    if 'Contabilidade Geral' in materias_com_cargo:
        conteudo = materias_com_cargo['Contabilidade Geral']['conteudo']
        print(f"Contabilidade Geral: {len(conteudo)} tópicos")
        print(f"  Primeiro tópico: {conteudo[0] if conteudo else 'Nenhum'}")
        
        # Verificar palavras-chave
        conteudo_texto = ' '.join(conteudo).lower()
        palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
        palavras_encontradas = [p for p in palavras_contabilidade if p in conteudo_texto]
        print(f"  Palavras-chave: {palavras_encontradas}")
    
    print("\n📄 TESTE 3: analisar_edital COM ['Contador']")
    resultado_completo = analyzer.analisar_edital(edital_conteudo, ['Contador'])
    
    materias_completo = resultado_completo['materias']
    print(f"Matérias encontradas: {list(materias_completo.keys())}")
    
    if 'Contabilidade Geral' in materias_completo:
        conteudo = materias_completo['Contabilidade Geral']['conteudo']
        print(f"Contabilidade Geral: {len(conteudo)} tópicos")
        print(f"  Primeiro tópico: {conteudo[0] if conteudo else 'Nenhum'}")
        
        # Verificar palavras-chave
        conteudo_texto = ' '.join(conteudo).lower()
        palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
        palavras_encontradas = [p for p in palavras_contabilidade if p in conteudo_texto]
        print(f"  Palavras-chave: {palavras_encontradas}")
    
    print("\n🔍 COMPARAÇÃO:")
    print("Teste 1 (sem cargo):", 'Contabilidade Geral' in materias_sem_cargo)
    print("Teste 2 (com cargo):", 'Contabilidade Geral' in materias_com_cargo)
    print("Teste 3 (analisar_edital):", 'Contabilidade Geral' in materias_completo)
    
    if 'Contabilidade Geral' in materias_com_cargo and 'Contabilidade Geral' in materias_completo:
        conteudo_teste2 = len(materias_com_cargo['Contabilidade Geral']['conteudo'])
        conteudo_teste3 = len(materias_completo['Contabilidade Geral']['conteudo'])
        print(f"Conteúdo teste 2: {conteudo_teste2} tópicos")
        print(f"Conteúdo teste 3: {conteudo_teste3} tópicos")
        print(f"Diferença: {conteudo_teste2 != conteudo_teste3}")

if __name__ == "__main__":
    debug_cargo_comparison()
