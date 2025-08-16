#!/usr/bin/env python3
"""
Script para testar a análise de edital do Agente Concurseiro.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_edital_analyzer():
    """Testa o analisador de edital"""
    try:
        print("🔍 Testando analisador de edital...")
        
        # Importar o analisador
        from app.utils.edital_analyzer import EditalAnalyzer
        
        # Criar instância
        analyzer = EditalAnalyzer()
        print("✅ EditalAnalyzer criado com sucesso")
        
        # Conteúdo de teste (simulando um edital)
        edital_content = """
        EDITAL DE CONCURSO PÚBLICO Nº 001/2024
        
        POLÍCIA CIVIL DO ESTADO DE SÃO PAULO
        
        CONCURSO PÚBLICO PARA PROVIMENTO DE CARGOS DE:
        - AGENTE DE POLÍCIA
        - ESCRIVÃO DE POLÍCIA  
        - DELEGADO DE POLÍCIA
        - PERITO CRIMINAL
        - PAPILOSCOPISTA
        
        BANCA EXAMINADORA: CESPE/CEBRASPE
        
        TOTAL DE VAGAS: 500 vagas
        
        DATA DA PROVA: 15/12/2024
        
        PERÍODO DE INSCRIÇÕES: 01/10/2024 a 30/10/2024
        
        CONTEÚDO PROGRAMÁTICO:
        
        1. DIREITO CONSTITUCIONAL (20 questões)
        - Princípios fundamentais
        - Direitos e garantias fundamentais
        - Organização do Estado
        
        2. DIREITO ADMINISTRATIVO (15 questões)
        - Princípios da administração pública
        - Atos administrativos
        - Licitações e contratos
        
        3. DIREITO PENAL (25 questões)
        - Teoria geral do crime
        - Crimes contra a pessoa
        - Crimes contra o patrimônio
        
        4. LÍNGUA PORTUGUESA (20 questões)
        - Interpretação de textos
        - Gramática
        - Redação oficial
        
        5. RACIOCÍNIO LÓGICO (10 questões)
        - Lógica proposicional
        - Problemas aritméticos
        - Sequências
        """
        
        print("📄 Conteúdo de teste preparado")
        
        # Testar análise
        print("🔍 Executando análise...")
        cargos_selecionados = ["Agente", "Escrivão"]
        
        resultado = analyzer.analisar_edital(edital_content, cargos_selecionados)
        
        print("✅ Análise concluída com sucesso!")
        
        # Mostrar resultados
        print("\n📊 RESULTADOS DA ANÁLISE:")
        print("="*50)
        
        print(f"🏛️  Concurso: {resultado['concurso']}")
        print(f"🏢 Banca: {resultado['banca']}")
        print(f"👥 Vagas: {resultado['vagas']}")
        print(f"📅 Data da Prova: {resultado['data_prova']}")
        print(f"📝 Período de Inscrição: {resultado['data_inscricao']}")
        print(f"🎯 Cargos Detectados: {', '.join(resultado['cargos_detectados'])}")
        print(f"📋 Cargos Analisados: {', '.join(resultado['cargos_analisados'])}")
        print(f"🔍 Modo de Análise: {resultado['modo_analise']}")
        print(f"✅ Confiança: {resultado['confianca']}")
        
        print(f"\n📚 MATÉRIAS DETECTADAS ({len(resultado['materias'])}):")
        print("-"*30)
        for materia, info in resultado['materias'].items():
            peso = info.get('peso', 1.0)
            questoes = info.get('questoes', 10)
            print(f"• {materia}: {questoes} questões (peso {peso})")
            
            conteudos = info.get('conteudo', [])
            if conteudos:
                for conteudo in conteudos[:3]:  # Mostrar apenas os 3 primeiros
                    print(f"  - {conteudo}")
                if len(conteudos) > 3:
                    print(f"  ... e mais {len(conteudos) - 3} tópicos")
        
        print(f"\n📊 ESTATÍSTICAS:")
        print("-"*20)
        stats = resultado['estatisticas']
        print(f"• Tamanho do conteúdo: {stats['tamanho_conteudo']:,} caracteres")
        print(f"• Padrões encontrados: {stats['padroes_encontrados']}")
        print(f"• Cargos detectados: {stats['cargos_detectados']}")
        print(f"• Matérias detectadas: {stats['materias_detectadas']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_file_extraction():
    """Testa extração de texto de arquivo"""
    try:
        print("\n🔍 Testando extração de texto...")
        
        from app.utils.edital_analyzer import EditalAnalyzer
        
        analyzer = EditalAnalyzer()
        
        # Simular um arquivo de texto
        test_content = "Este é um teste de extração de texto."
        
        # Testar método de limpeza
        content_clean = analyzer._limpar_conteudo(test_content)
        print(f"✅ Limpeza de conteúdo: '{content_clean}'")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na extração: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DO ANALISADOR DE EDITAL")
    print("="*50)
    
    # Teste principal
    success1 = test_edital_analyzer()
    
    # Teste de extração
    success2 = test_file_extraction()
    
    if success1 and success2:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\n💡 O analisador de edital está funcionando corretamente.")
        print("   Agora você pode usar a funcionalidade no Streamlit.")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        print("   Verifique os erros acima.")
        sys.exit(1)
