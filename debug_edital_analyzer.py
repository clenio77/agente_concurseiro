#!/usr/bin/env python3
"""
Debug do EditalAnalyzer para entender problemas
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_edital_analyzer():
    """Debug do analisador de edital"""
    print("🔍 DEBUG DO EDITAL ANALYZER")
    print("="*50)
    
    from app.utils.edital_analyzer import EditalAnalyzer
    
    analyzer = EditalAnalyzer()
    
    # Edital de teste simples
    edital_teste = """
    CONCURSO PÚBLICO - PREFEITURA MUNICIPAL
    
    CARGO: Contador
    
    MATÉRIAS:
    Português: 20 questões
    Matemática: 15 questões  
    Contabilidade Geral: 25 questões
    
    CONTEÚDO PROGRAMÁTICO:
    
    Contabilidade Geral: Conceito, objeto e objetivo da contabilidade;
    Patrimônio: componentes, equação fundamental do patrimônio, situação líquida;
    Contas: conceito, contas de débito e crédito e saldos; Plano de contas;
    Fatos contábeis: conceito, fatos permutativos, modificativos e mistos;
    Balancete de verificação; Balanço patrimonial; Demonstração do resultado do exercício;
    Demonstração de lucros ou prejuízos acumulados; Demonstração das mutações;
    Análise das demonstrações financeiras; Contabilidade de custos; Orçamento público.
    """
    
    print("📄 EDITAL DE TESTE:")
    print(edital_teste[:200] + "...")
    
    # Testar análise
    resultado = analyzer.analisar_edital(edital_teste, ['Contador'])
    
    print("\n📊 RESULTADO DA ANÁLISE:")
    print(f"Concurso: {resultado['concurso']}")
    print(f"Cargos analisados: {resultado['cargos_analisados']}")
    print(f"Número de matérias: {len(resultado['materias'])}")
    
    print("\n📚 MATÉRIAS DETECTADAS:")
    for nome, dados in resultado['materias'].items():
        print(f"\n🔸 {nome}:")
        print(f"  Questões: {dados['questoes']}")
        print(f"  Peso: {dados['peso']}")
        print(f"  Conteúdo ({len(dados['conteudo'])} tópicos):")
        for i, topico in enumerate(dados['conteudo'][:5]):
            print(f"    {i+1}. {topico}")
        if len(dados['conteudo']) > 5:
            print(f"    ... e mais {len(dados['conteudo'])-5} tópicos")
    
    # Testar método específico de extração de conteúdo
    print("\n🔍 TESTE ESPECÍFICO DE EXTRAÇÃO DE CONTEÚDO:")
    content_lower = edital_teste.lower()
    
    # Testar extração para Contabilidade Geral
    conteudo_contabilidade = analyzer._extrair_conteudo_materia(content_lower, "Contabilidade Geral")
    print(f"\n📖 Conteúdo extraído para 'Contabilidade Geral': {len(conteudo_contabilidade)} tópicos")
    for i, topico in enumerate(conteudo_contabilidade):
        print(f"  {i+1}. {topico}")
    
    # Verificar se contém palavras-chave esperadas
    conteudo_texto = ' '.join(conteudo_contabilidade).lower()
    palavras_chave = ['patrimônio', 'balanço', 'demonstração', 'contabilidade', 'contas']
    
    print(f"\n🔍 VERIFICAÇÃO DE PALAVRAS-CHAVE:")
    for palavra in palavras_chave:
        presente = palavra in conteudo_texto
        print(f"  '{palavra}': {'✅' if presente else '❌'}")
    
    # Testar busca por cargo específico
    print(f"\n🎯 TESTE DE BUSCA POR CARGO:")
    materias_cargo = analyzer._buscar_materias_por_cargo(content_lower, "Contador")
    print(f"Matérias encontradas para 'Contador': {len(materias_cargo)}")
    for nome, dados in materias_cargo.items():
        print(f"  - {nome}: {dados['questoes']} questões")

if __name__ == "__main__":
    debug_edital_analyzer()
