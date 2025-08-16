#!/usr/bin/env python3
"""
Debug do fluxo completo do EditalAnalyzer
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_full_flow():
    """Debug do fluxo completo"""
    print("🔍 DEBUG DO FLUXO COMPLETO")
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
    
    print("📄 EXECUTANDO ANÁLISE COMPLETA...")
    resultado = analyzer.analisar_edital(edital_conteudo, ['Contador'])
    
    print(f"\n📊 RESULTADO DA ANÁLISE:")
    print(f"Concurso: {resultado['concurso']}")
    print(f"Cargos analisados: {resultado['cargos_analisados']}")
    print(f"Número de matérias: {len(resultado['materias'])}")
    
    print(f"\n📚 MATÉRIAS DETECTADAS:")
    for nome_materia, dados in resultado['materias'].items():
        print(f"\n🔸 {nome_materia}:")
        print(f"  Questões: {dados['questoes']}")
        print(f"  Peso: {dados['peso']}")
        print(f"  Conteúdo ({len(dados['conteudo'])} tópicos):")
        
        conteudo_texto = ' '.join(dados['conteudo']).lower()
        
        for i, topico in enumerate(dados['conteudo'][:5]):
            print(f"    {i+1}. {topico}")
        if len(dados['conteudo']) > 5:
            print(f"    ... e mais {len(dados['conteudo'])-5} tópicos")
        
        # Verificar palavras-chave para contabilidade
        if 'contabilidade' in nome_materia.lower():
            print(f"\n  🔍 ANÁLISE ESPECÍFICA DE CONTABILIDADE:")
            palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
            palavras_encontradas = [p for p in palavras_contabilidade if p in conteudo_texto]
            
            print(f"  Palavras-chave encontradas: {palavras_encontradas}")
            
            for palavra in palavras_contabilidade:
                presente = palavra in conteudo_texto
                print(f"    '{palavra}': {'✅' if presente else '❌'}")
    
    # Testar métodos individuais
    print(f"\n🧪 TESTE DOS MÉTODOS INDIVIDUAIS:")
    content_lower = edital_conteudo.lower()
    
    # 1. Detectar cargos
    cargos = analyzer._detectar_cargos(content_lower)
    print(f"1. Cargos detectados: {cargos}")
    
    # 2. Detectar matérias (sem cargo específico)
    materias_sem_cargo = analyzer._detectar_materias(content_lower)
    print(f"2. Matérias sem cargo: {list(materias_sem_cargo.keys())}")
    
    # 3. Detectar matérias (com cargo específico)
    materias_com_cargo = analyzer._detectar_materias(content_lower, 'Contador')
    print(f"3. Matérias com cargo 'Contador': {list(materias_com_cargo.keys())}")
    
    # 4. Buscar matérias por cargo
    materias_por_cargo = analyzer._buscar_materias_por_cargo(content_lower, 'Contador')
    print(f"4. Matérias por cargo: {list(materias_por_cargo.keys())}")
    
    # 5. Extrair conteúdo específico
    conteudo_contabilidade = analyzer._extrair_conteudo_materia(content_lower, "Contabilidade Geral")
    print(f"5. Conteúdo de Contabilidade Geral: {len(conteudo_contabilidade)} tópicos")
    for i, topico in enumerate(conteudo_contabilidade[:3]):
        print(f"   {i+1}. {topico}")

if __name__ == "__main__":
    debug_full_flow()
