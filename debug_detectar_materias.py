#!/usr/bin/env python3
"""
Debug específico do método _detectar_materias
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_detectar_materias():
    """Debug específico do método _detectar_materias"""
    print("🔍 DEBUG DO MÉTODO _detectar_materias")
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
    cargo_selecionado = 'Contador'
    
    print("📄 CHAMANDO _detectar_materias DIRETAMENTE...")
    materias_resultado = analyzer._detectar_materias(content_lower, cargo_selecionado)
    
    print(f"\n📊 RESULTADO DO _detectar_materias:")
    print(f"Número de matérias: {len(materias_resultado)}")
    
    for nome_materia, dados in materias_resultado.items():
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

if __name__ == "__main__":
    debug_detectar_materias()
