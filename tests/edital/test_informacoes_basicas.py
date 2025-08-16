#!/usr/bin/env python3
"""
Teste específico para verificar a extração de informações básicas do edital
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.edital_analyzer import EditalAnalyzer

def test_informacoes_basicas():
    """Testa a extração de informações básicas"""
    
    # Texto de exemplo com informações básicas
    texto_exemplo = """
    EDITAL DE CONCURSO PÚBLICO
    
    CONCURSO PÚBLICO PARA PROVIMENTO DE CARGOS DA POLÍCIA CIVIL DO ESTADO DE MINAS GERAIS
    
    BANCA ORGANIZADORA: FUNDAÇÃO GETÚLIO VARGAS - FGV
    
    TOTAL DE VAGAS: 100 vagas
    
    DATA DA PROVA: 15/12/2024
    
    PERÍODO DE INSCRIÇÕES: 01/10/2024 a 30/11/2024
    
    CARGOS:
    - Agente de Polícia Civil
    - Escrivão de Polícia Civil
    - Delegado de Polícia Civil
    
    MATÉRIAS PARA AGENTE:
    • Língua Portuguesa: 20 questões
    • Direito Penal: 15 questões
    • Direito Processual Penal: 15 questões
    • Direito Constitucional: 10 questões
    • Legislação Específica: 10 questões
    • Raciocínio Lógico: 10 questões
    • Conhecimentos Gerais: 10 questões
    """
    
    print("🔍 TESTE DE EXTRAÇÃO DE INFORMAÇÕES BÁSICAS")
    print("=" * 60)
    
    # Inicializar analisador
    analyzer = EditalAnalyzer()
    
    # Testar extração de informações básicas
    print("\n📋 Testando extração de informações básicas...")
    content_lower = texto_exemplo.lower()
    info_extraida = analyzer._extrair_informacoes_basicas(content_lower)
    
    print("\n✅ INFORMAÇÕES EXTRAÍDAS:")
    print("-" * 40)
    for campo, valor in info_extraida.items():
        print(f"• {campo.upper()}: {valor}")
    
    # Testar análise completa
    print("\n🔬 Testando análise completa...")
    resultado = analyzer.analisar_edital(texto_exemplo, ['Agente de Polícia Civil'])
    
    print("\n📊 RESULTADO DA ANÁLISE COMPLETA:")
    print("-" * 40)
    print(f"• CONCURSO: {resultado['concurso']}")
    print(f"• BANCA: {resultado['banca']}")
    print(f"• VAGAS: {resultado['vagas']}")
    print(f"• DATA DA PROVA: {resultado['data_prova']}")
    print(f"• PERÍODO DE INSCRIÇÕES: {resultado['data_inscricao']}")
    print(f"• CARGOS DETECTADOS: {resultado['cargos_detectados']}")
    print(f"• CONFIANÇA: {resultado['confianca']}")
    
    print("\n📚 MATÉRIAS DETECTADAS:")
    print("-" * 40)
    for materia, info in resultado['materias'].items():
        questoes = info.get('questoes', 'N/A')
        print(f"• {materia}: {questoes} questões")
    
    print("\n📈 ESTATÍSTICAS:")
    print("-" * 40)
    stats = resultado.get('estatisticas', {})
    for key, value in stats.items():
        print(f"• {key}: {value}")

if __name__ == "__main__":
    test_informacoes_basicas()
