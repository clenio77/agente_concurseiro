#!/usr/bin/env python3
"""
Debug passo a passo do EditalAnalyzer
"""

import sys
import os
from pathlib import Path
import re

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_step_by_step():
    """Debug passo a passo"""
    print("🔍 DEBUG PASSO A PASSO")
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
    
    print("📄 SIMULANDO O MÉTODO _detectar_materias...")
    
    # Simular o início do método
    materias_detectadas = {}
    
    # 1. Buscar matérias específicas do cargo
    print("\n🔍 PASSO 1: Buscar matérias por cargo")
    materias_por_cargo = analyzer._buscar_materias_por_cargo(content_lower, cargo_selecionado)
    print(f"Matérias encontradas por cargo: {list(materias_por_cargo.keys())}")
    
    for nome, dados in materias_por_cargo.items():
        print(f"  {nome}: {len(dados['conteudo'])} tópicos - {dados['conteudo'][:1]}")
    
    materias_detectadas.update(materias_por_cargo)
    print(f"Estado atual de materias_detectadas: {list(materias_detectadas.keys())}")
    
    # 2. Padrões de matérias
    print("\n🔍 PASSO 2: Buscar com padrões regex")
    padroes_materias = [
        r'([a-záéíóúâêôãõç\s]+):\s*(\d+)\s*questões?',
        r'(\d+)\s*questões?\s*(?:de\s+)?([a-záéíóúâêôãõç\s]+)',
        r'([a-záéíóúâêôãõç\s]+)\s*[-–]\s*(\d+)\s*questões?',
        r'matéria[:\s]*([a-záéíóúâêôãõç\s]+)[:\s]*(\d+)',
    ]
    
    from app.utils.edital_analyzer import is_valid_materia, safe_questoes_conversion
    
    for i, padrao in enumerate(padroes_materias):
        print(f"\n  Testando padrão {i+1}: {padrao}")
        matches = re.findall(padrao, content_lower)
        print(f"  Matches encontrados: {matches}")
        
        for match in matches:
            if len(match) >= 2:
                if match[0].isdigit():
                    questoes_str, materia = match[0], match[1].strip().title()
                else:
                    materia, questoes_str = match[0].strip().title(), match[1]

                questoes = safe_questoes_conversion(questoes_str)
                
                print(f"    Processando: {materia} ({questoes} questões)")
                
                # Validar se é uma matéria válida
                if materia and is_valid_materia(materia, cargo_selecionado):
                    print(f"    ✅ Matéria válida: {materia}")
                    
                    # Extrair conteúdo detalhado da matéria
                    conteudo_detalhado = analyzer._extrair_conteudo_materia(content_lower, materia)
                    print(f"    📚 Conteúdo extraído: {len(conteudo_detalhado)} tópicos")
                    if conteudo_detalhado:
                        print(f"        Primeiro tópico: {conteudo_detalhado[0]}")
                    
                    # Verificar se deve sobrescrever
                    deve_sobrescrever = (materia not in materias_detectadas or 
                                       len(conteudo_detalhado) > len(materias_detectadas[materia].get('conteudo', [])))
                    
                    print(f"    🔄 Deve sobrescrever? {deve_sobrescrever}")
                    if materia in materias_detectadas:
                        conteudo_atual = materias_detectadas[materia].get('conteudo', [])
                        print(f"        Conteúdo atual: {len(conteudo_atual)} tópicos")
                        print(f"        Novo conteúdo: {len(conteudo_detalhado)} tópicos")
                    
                    if deve_sobrescrever:
                        materias_detectadas[materia] = {
                            'questoes': questoes,
                            'peso': analyzer._extrair_peso_materia(content_lower, materia),
                            'conteudo': conteudo_detalhado if conteudo_detalhado else [f"Conteúdo de {materia}"]
                        }
                        print(f"    ✅ Matéria atualizada!")
                    else:
                        print(f"    ⏭️ Matéria não atualizada")
                else:
                    print(f"    ❌ Matéria inválida: {materia}")
    
    print(f"\n🎯 RESULTADO FINAL:")
    print(f"Matérias detectadas: {len(materias_detectadas)}")
    
    for nome, dados in materias_detectadas.items():
        print(f"\n🔸 {nome}:")
        print(f"  Questões: {dados['questoes']}")
        print(f"  Conteúdo ({len(dados['conteudo'])} tópicos):")
        for i, topico in enumerate(dados['conteudo'][:3]):
            print(f"    {i+1}. {topico}")
        
        # Verificar palavras-chave para contabilidade
        if 'contabilidade' in nome.lower():
            conteudo_texto = ' '.join(dados['conteudo']).lower()
            palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
            palavras_encontradas = [p for p in palavras_contabilidade if p in conteudo_texto]
            print(f"  Palavras-chave: {palavras_encontradas}")

if __name__ == "__main__":
    debug_step_by_step()
