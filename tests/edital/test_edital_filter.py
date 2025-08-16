"""
🔍 Teste do Filtro de Matérias do Edital
Verifica se o sistema está filtrando corretamente as matérias relevantes para o cargo
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from utils.edital_analyzer import EditalAnalyzer

def test_materia_filter():
    """Testa o filtro de matérias"""
    print("🔍 TESTANDO FILTRO DE MATÉRIAS PARA ANALISTA EM CONTROLE INTERNO")
    print("=" * 70)
    
    analyzer = EditalAnalyzer()
    cargo = "Analista Em Controle Interno"
    
    # Teste 1: Matérias válidas
    print("\n✅ TESTE 1: Matérias que DEVEM ser aceitas")
    materias_validas = [
        "Português", "Língua Portuguesa", "Matemática", "Raciocínio Lógico",
        "Direito Constitucional", "Direito Administrativo", "Contabilidade",
        "Auditoria", "Controle Interno", "Administração Pública", "Informática"
    ]
    
    for materia in materias_validas:
        resultado = analyzer._is_materia_valida(materia, cargo)
        status = "✅ ACEITA" if resultado else "❌ REJEITADA"
        print(f"  {materia:<25} | {status}")
    
    # Teste 2: Matérias inválidas
    print("\n❌ TESTE 2: Matérias que DEVEM ser rejeitadas")
    materias_invalidas = [
        "Pontuação Máxima", "Dia De Aplicação", "N", "Orientador", "Cid", "Art",
        "Lei Geral De Proteção De Dados Pessoais", "Código Brasileiro",
        "Estabelece Normas", "Data", "Horário", "Local", "Inscrição", "Taxa"
    ]
    
    for materia in materias_invalidas:
        resultado = analyzer._is_materia_valida(materia, cargo)
        status = "❌ REJEITADA" if not resultado else "✅ ACEITA (ERRO!)"
        print(f"  {materia:<35} | {status}")
    
    # Teste 3: Teste com seção simulada
    print("\n🧪 TESTE 3: Extração de seção simulada")
    secao_simulada = """
    Para o cargo de Analista Em Controle Interno:
    • Português (Peso: 1,0, Questões: 20)
    • Matemática (15)
    • Direito Administrativo: 25 questões
    • Contabilidade Geral (30)
    • Auditoria Interna: 20
    • Pontuação Máxima (100)
    • Data de Aplicação: 15/08/2024
    • Orientador: João Silva
    • Art. 5º da Constituição
    """
    
    materias_extraidas = analyzer._extrair_materias_de_secao(secao_simulada, secao_simulada.lower())
    
    print(f"\nMatérias extraídas: {len(materias_extraidas)}")
    for materia, info in materias_extraidas.items():
        print(f"  ✅ {materia}: {info['questoes']} questões")
    
    # Verificar se rejeitou as inválidas
    materias_rejeitadas = ["Pontuação Máxima", "Data De Aplicação", "Orientador", "Art"]
    rejeitadas_corretamente = 0
    
    for materia_rejeitada in materias_rejeitadas:
        if materia_rejeitada not in materias_extraidas:
            rejeitadas_corretamente += 1
            print(f"  ❌ {materia_rejeitada}: CORRETAMENTE REJEITADA")
        else:
            print(f"  ⚠️  {materia_rejeitada}: ERRO - NÃO FOI REJEITADA!")
    
    print(f"\nResumo do teste:")
    print(f"  Matérias válidas extraídas: {len(materias_extraidas)}")
    print(f"  Matérias inválidas rejeitadas: {rejeitadas_corretamente}/{len(materias_rejeitadas)}")
    
    # Resultado final
    if len(materias_extraidas) >= 3 and rejeitadas_corretamente == len(materias_rejeitadas):
        print("\n🎉 TESTE PASSOU! Filtro funcionando corretamente.")
        return True
    else:
        print("\n❌ TESTE FALHOU! Filtro precisa de ajustes.")
        return False

if __name__ == "__main__":
    success = test_materia_filter()
    exit(0 if success else 1)
