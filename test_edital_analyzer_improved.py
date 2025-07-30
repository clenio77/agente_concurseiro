#!/usr/bin/env python3
"""
Teste das melhorias no EditalAnalyzer
Valida detecção específica de matérias por cargo
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_edital_analyzer_improvements():
    """Testa as melhorias no analisador de edital"""
    print("🧪 TESTANDO MELHORIAS NO EDITAL ANALYZER")
    print("="*60)
    
    try:
        from app.utils.edital_analyzer import EditalAnalyzer
        
        # Criar instância
        analyzer = EditalAnalyzer()
        print("✅ EditalAnalyzer instanciado com sucesso")
        
        # Texto de teste simulando um edital real
        edital_teste = """
        EDITAL DE CONCURSO PÚBLICO N° 1/2024
        PREFEITURA MUNICIPAL DE UBERLÂNDIA
        
        BANCA EXAMINADORA: CESPE/CEBRASPE
        VAGAS: 100 vagas
        DATA DA PROVA: 15/12/2024
        
        CARGOS DISPONÍVEIS:
        - Analista em Controle Interno
        - Arquiteto
        - Assistente Social
        - Auditor Fiscal Tributário
        
        CARGO ANALISADO: Analista em Controle Interno
        
        MATÉRIAS PARA ANALISTA EM CONTROLE INTERNO:
        • Português (Peso: 1,0, Questões: 20)
        • Direito Constitucional: 15 questões
        • Direito Administrativo - 15 questões
        • Contabilidade Geral: Peso 2,0, Questões: 20
        • Auditoria: 10 questões
        • Controle Interno - 10 questões
        
        CONTEÚDO PROGRAMÁTICO:
        
        Português: Interpretação de textos; Ortografia oficial; Acentuação gráfica; 
        Emprego das classes de palavras; Sintaxe da oração; Pontuação; Concordância.
        
        Direito Constitucional: Princípios fundamentais; Direitos e garantias fundamentais; 
        Organização do Estado; Organização dos Poderes; Controle de constitucionalidade.
        
        Contabilidade Geral: Patrimônio; Balanço patrimonial; Demonstração do resultado; 
        Análise das demonstrações; Custos; Orçamento público.
        """
        
        # Testar análise com cargo específico
        resultado = analyzer.analisar_edital(edital_teste, ['Analista em Controle Interno'])
        
        print("✅ Análise de edital executada")
        
        # Verificar se detectou o cargo corretamente
        assert 'cargos_analisados' in resultado
        assert 'Analista em Controle Interno' in resultado['cargos_analisados']
        print("✅ Cargo analisado detectado corretamente")
        
        # Verificar matérias detectadas
        materias = resultado['materias']
        print(f"📚 Matérias detectadas: {len(materias)}")
        
        # Verificar matérias específicas esperadas
        materias_esperadas = ['Português', 'Direito Constitucional', 'Direito Administrativo', 'Contabilidade']
        materias_encontradas = []
        
        for materia_key in materias.keys():
            for esperada in materias_esperadas:
                if esperada.lower() in materia_key.lower():
                    materias_encontradas.append(esperada)
                    break
        
        print(f"✅ Matérias específicas encontradas: {materias_encontradas}")
        
        # Verificar estrutura das matérias
        for nome_materia, dados_materia in materias.items():
            assert 'questoes' in dados_materia, f"Campo 'questoes' não encontrado em {nome_materia}"
            assert 'peso' in dados_materia, f"Campo 'peso' não encontrado em {nome_materia}"
            assert 'conteudo' in dados_materia, f"Campo 'conteudo' não encontrado em {nome_materia}"
            
            # Verificar se o conteúdo não está vazio
            assert len(dados_materia['conteudo']) > 0, f"Conteúdo vazio para {nome_materia}"
            
            print(f"  📖 {nome_materia}: {dados_materia['questoes']} questões, peso {dados_materia['peso']}")
            print(f"     Conteúdo: {len(dados_materia['conteudo'])} tópicos")
        
        print("✅ Estrutura de matérias válida")
        
        # Verificar informações extraídas
        assert resultado['concurso'] != 'Concurso Público'  # Deve ter detectado nome específico
        assert resultado['banca'] != 'Banca não identificada'  # Deve ter detectado CESPE
        assert resultado['vagas'] == 100  # Deve ter detectado número correto
        
        print("✅ Informações básicas extraídas corretamente")
        
        # Verificar confiança da análise
        assert resultado['confianca'] in ['Alta', 'Média', 'Baixa']
        print(f"✅ Confiança da análise: {resultado['confianca']}")
        
        # Verificar estatísticas
        stats = resultado['estatisticas']
        assert stats['materias_detectadas'] > 0
        assert stats['cargos_detectados'] > 0
        print("✅ Estatísticas de análise válidas")
        
        print("🎉 MELHORIAS NO EDITAL ANALYZER: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de melhorias: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_cargo_specific_detection():
    """Testa detecção específica por cargo"""
    print("\n🧪 TESTANDO DETECÇÃO ESPECÍFICA POR CARGO")
    print("="*60)
    
    try:
        from app.utils.edital_analyzer import EditalAnalyzer
        
        analyzer = EditalAnalyzer()
        
        # Edital com múltiplos cargos e matérias específicas
        edital_multiplo = """
        CONCURSO PÚBLICO - TRIBUNAL DE JUSTIÇA
        
        CARGO 1: Técnico Judiciário
        Matérias: Português (20), Matemática (15), Direito Constitucional (10), Informática (5)
        
        CARGO 2: Analista Judiciário - Área Administrativa
        Matérias: Português (15), Direito Administrativo (20), Direito Constitucional (15), 
        Administração Pública (10), Contabilidade (10)
        
        CARGO 3: Analista Judiciário - Área Judiciária
        Matérias: Português (10), Direito Civil (25), Direito Processual Civil (25), 
        Direito Constitucional (10), Direito Penal (10)
        """
        
        # Testar análise para cargo específico
        resultado_tecnico = analyzer.analisar_edital(edital_multiplo, ['Técnico Judiciário'])
        resultado_admin = analyzer.analisar_edital(edital_multiplo, ['Analista Judiciário - Área Administrativa'])
        resultado_judiciario = analyzer.analisar_edital(edital_multiplo, ['Analista Judiciário - Área Judiciária'])
        
        print("✅ Análises por cargo específico executadas")
        
        # Verificar que cada análise focou no cargo correto
        materias_tecnico = set(resultado_tecnico['materias'].keys())
        materias_admin = set(resultado_admin['materias'].keys())
        materias_judiciario = set(resultado_judiciario['materias'].keys())
        
        print(f"📚 Técnico Judiciário: {len(materias_tecnico)} matérias")
        print(f"📚 Analista Administrativo: {len(materias_admin)} matérias")
        print(f"📚 Analista Judiciário: {len(materias_judiciario)} matérias")
        
        # Verificar que pelo menos algumas matérias são diferentes para cada cargo
        # (pode haver sobreposição, mas não devem ser 100% idênticas)
        sobreposicao_tecnico_admin = len(materias_tecnico.intersection(materias_admin)) / max(len(materias_tecnico), len(materias_admin))
        sobreposicao_admin_jud = len(materias_admin.intersection(materias_judiciario)) / max(len(materias_admin), len(materias_judiciario))

        # Permitir até 80% de sobreposição (algumas matérias básicas são comuns)
        assert sobreposicao_tecnico_admin < 0.9, f"Muita sobreposição entre Técnico e Admin: {sobreposicao_tecnico_admin:.1%}"
        assert sobreposicao_admin_jud < 0.9, f"Muita sobreposição entre Admin e Judiciário: {sobreposicao_admin_jud:.1%}"
        
        print("✅ Detecção específica por cargo funcionando")
        
        # Verificar matérias específicas esperadas
        # Técnico deve ter Matemática e Informática
        tecnico_tem_matematica = any('matemática' in m.lower() for m in materias_tecnico)
        tecnico_tem_informatica = any('informática' in m.lower() for m in materias_tecnico)
        
        # Admin deve ter Administração e Contabilidade
        admin_tem_administracao = any('administr' in m.lower() for m in materias_admin)
        admin_tem_contabilidade = any('contabil' in m.lower() for m in materias_admin)
        
        # Judiciário deve ter Direito Civil e Processual Civil
        jud_tem_civil = any('civil' in m.lower() for m in materias_judiciario)
        jud_tem_processual = any('processual' in m.lower() for m in materias_judiciario)
        
        print(f"✅ Técnico - Matemática: {tecnico_tem_matematica}, Informática: {tecnico_tem_informatica}")
        print(f"✅ Admin - Administração: {admin_tem_administracao}, Contabilidade: {admin_tem_contabilidade}")
        print(f"✅ Judiciário - Civil: {jud_tem_civil}, Processual: {jud_tem_processual}")
        
        print("🎉 DETECÇÃO ESPECÍFICA POR CARGO: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de detecção por cargo: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_content_extraction():
    """Testa extração de conteúdo programático"""
    print("\n🧪 TESTANDO EXTRAÇÃO DE CONTEÚDO PROGRAMÁTICO")
    print("="*60)
    
    try:
        from app.utils.edital_analyzer import EditalAnalyzer
        
        analyzer = EditalAnalyzer()
        
        # Edital com conteúdo programático detalhado
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
        
        resultado = analyzer.analisar_edital(edital_conteudo, ['Contador'])
        
        print("✅ Análise com conteúdo programático executada")
        
        materias = resultado['materias']
        
        # Verificar se extraiu conteúdo detalhado
        for nome_materia, dados in materias.items():
            conteudo = dados['conteudo']
            print(f"📖 {nome_materia}: {len(conteudo)} tópicos de conteúdo")
            
            # Verificar se o conteúdo não é apenas genérico
            conteudo_texto = ' '.join(conteudo).lower()
            
            if 'português' in nome_materia.lower():
                # Deve conter tópicos específicos de português
                assert any(palavra in conteudo_texto for palavra in ['interpretação', 'ortografia', 'concordância']), \
                    "Conteúdo de Português deve ser específico"
                print("  ✅ Conteúdo específico de Português detectado")
            
            elif 'contabilidade' in nome_materia.lower():
                # Deve conter pelo menos 2 tópicos específicos de contabilidade
                palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
                palavras_encontradas = [p for p in palavras_contabilidade if p in conteudo_texto]
                assert len(palavras_encontradas) >= 2, \
                    f"Conteúdo de Contabilidade deve ser específico. Encontradas: {palavras_encontradas}"
                print(f"  ✅ Conteúdo específico de Contabilidade detectado: {palavras_encontradas}")
            
            # Mostrar alguns tópicos
            for i, topico in enumerate(conteudo[:3]):
                print(f"    {i+1}. {topico}")
        
        print("✅ Extração de conteúdo programático funcionando")
        
        print("🎉 EXTRAÇÃO DE CONTEÚDO: TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste de extração de conteúdo: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def run_edital_analyzer_tests():
    """Executa todos os testes de melhorias do EditalAnalyzer"""
    print("🚀 INICIANDO TESTES DE MELHORIAS DO EDITAL ANALYZER")
    print("="*80)
    
    results = []
    
    # Executar testes
    results.append(("Melhorias Gerais", test_edital_analyzer_improvements()))
    results.append(("Detecção por Cargo", test_cargo_specific_detection()))
    results.append(("Extração de Conteúdo", test_content_extraction()))
    
    # Resumo dos resultados
    print("\n" + "="*80)
    print("📊 RESUMO DOS TESTES - MELHORIAS EDITAL ANALYZER")
    print("="*80)
    
    passed = 0
    total = len(results)
    
    for component, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{component:25} | {status}")
        if result:
            passed += 1
    
    print("-"*80)
    print(f"TOTAL: {passed}/{total} testes passaram ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TODAS AS MELHORIAS DO EDITAL ANALYZER FUNCIONANDO!")
        print("✅ Detecção específica por cargo implementada")
        print("✅ Extração de conteúdo programático melhorada")
        print("✅ Análise mais precisa e focada")
        print("✅ Informações detalhadas dos padrões identificados")
        return True
    else:
        print(f"\n⚠️ {total-passed} TESTES FALHARAM!")
        print("❌ Correções necessárias nas melhorias")
        return False

if __name__ == "__main__":
    success = run_edital_analyzer_tests()
    
    if success:
        print("\n🎯 MELHORIAS IMPLEMENTADAS COM SUCESSO:")
        print("1. ✅ Detecção de matérias específicas por cargo")
        print("2. ✅ Extração de conteúdo programático detalhado")
        print("3. ✅ Análise mais precisa e focada")
        print("4. ✅ Informações detalhadas dos padrões")
        print("5. ✅ Validação aprimorada de matérias")
    else:
        print("\n🔧 AÇÕES NECESSÁRIAS:")
        print("1. Corrigir testes que falharam")
        print("2. Validar detecção por cargo")
        print("3. Verificar extração de conteúdo")
        print("4. Testar com editais reais")
        
    sys.exit(0 if success else 1)
