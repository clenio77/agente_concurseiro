#!/usr/bin/env python3
"""
Script para debugar a análise de edital.
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_edital_analysis():
    """Debug da análise de edital"""
    try:
        print("🔍 Debugando análise de edital...")
        
        # Importar as funções
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        from utils.edital_analyzer import EditalAnalyzer
        
        # Conteúdo de teste similar ao que está sendo usado
        edital_content = """
        EDITAL DE CONCURSO PÚBLICO Nº 001/2024
        
        PREFEITURA MUNICIPAL DE SÃO PAULO
        
        CONCURSO PÚBLICO PARA PROVIMENTO DE CARGOS DE:
        - AGENTE
        - ESCRIVÃO
        - DELEGADO
        - PERITO
        - PAPILOSCOPISTA
        - ANALISTA
        - TÉCNICO
        
        BANCA EXAMINADORA: CESPE/CEBRASPE
        
        TOTAL DE VAGAS: 500 vagas
        
        DATA DA PROVA: 15/12/2024
        
        PERÍODO DE INSCRIÇÕES: 01/10/2024 a 30/10/2024
        
        CONTEÚDO PROGRAMÁTICO:
        
        1. PORTUGUÊS (Peso: 1.0, Questões: 20)
        - Interpretação de textos
        - Gramática
        - Redação oficial
        
        2. RACIOCÍNIO LÓGICO (Peso: 1.0, Questões: 15)
        - Lógica proposicional
        - Problemas aritméticos
        - Sequências
        
        3. DIREITO CONSTITUCIONAL (20 questões)
        - Princípios fundamentais
        - Direitos e garantias fundamentais
        - Organização do Estado
        
        4. DIREITO ADMINISTRATIVO (15 questões)
        - Princípios da administração pública
        - Atos administrativos
        - Licitações e contratos
        
        5. DIREITO PENAL (25 questões)
        - Teoria geral do crime
        - Crimes contra a pessoa
        - Crimes contra o patrimônio
        """
        
        print("📄 Conteúdo preparado")
        
        # Criar analisador
        analyzer = EditalAnalyzer()
        print("✅ EditalAnalyzer criado")
        
        # Testar análise
        cargos_selecionados = ["Agente"]
        
        print("🔍 Executando análise...")
        resultado = analyzer.analisar_edital(edital_content, cargos_selecionados)
        
        print("✅ Análise concluída!")
        
        # Mostrar resultados detalhados
        print("\n📊 RESULTADO COMPLETO:")
        print("="*50)
        
        for chave, valor in resultado.items():
            print(f"\n🔹 {chave.upper()}:")
            if isinstance(valor, dict):
                for sub_chave, sub_valor in valor.items():
                    print(f"  • {sub_chave}: {sub_valor}")
            elif isinstance(valor, list):
                for item in valor[:5]:  # Mostrar apenas os 5 primeiros
                    print(f"  • {item}")
                if len(valor) > 5:
                    print(f"  ... e mais {len(valor) - 5} itens")
            else:
                print(f"  {valor}")
        
        # Verificar se está em modo fallback
        modo_analise = resultado.get('modo_analise', 'Desconhecido')
        confianca = resultado.get('confianca', 'Desconhecida')
        
        print(f"\n🎯 DIAGNÓSTICO:")
        print(f"• Modo de Análise: {modo_analise}")
        print(f"• Confiança: {confianca}")
        
        if modo_analise == "Fallback" or confianca == "Baixa":
            print("❌ PROBLEMA DETECTADO: Análise em modo fallback")
            
            # Verificar erros
            if 'erro' in resultado:
                print(f"❌ Erro: {resultado['erro']}")
            
            # Verificar estatísticas
            if 'estatisticas' in resultado:
                stats = resultado['estatisticas']
                print(f"📊 Estatísticas:")
                for stat_key, stat_value in stats.items():
                    print(f"  • {stat_key}: {stat_value}")
        else:
            print("✅ ANÁLISE FUNCIONANDO CORRETAMENTE")
        
        return resultado
        
    except Exception as e:
        print(f"❌ Erro no debug: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("🐛 DEBUG DA ANÁLISE DE EDITAL")
    print("="*50)
    
    resultado = debug_edital_analysis()
    
    if resultado:
        print("\n✅ Debug concluído com sucesso!")
    else:
        print("\n❌ Debug falhou!")
        sys.exit(1)
