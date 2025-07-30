#!/usr/bin/env python3
"""
Teste exato da funcionalidade do Streamlit
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_exact_streamlit_flow():
    """Testa o fluxo exato do Streamlit"""
    try:
        print("🔍 Testando fluxo exato do Streamlit...")
        
        # Importar exatamente como no Streamlit
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        from app.app import analisar_edital_com_llm, extrair_texto_arquivo
        
        print("✅ Funções importadas com sucesso")
        
        # Simular conteúdo de arquivo PDF real
        pdf_content = """
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
        
        # Simular cargos selecionados exatamente como no Streamlit
        cargos_selecionados = ["Agente"]
        
        print(f"📄 Conteúdo preparado: {len(pdf_content)} caracteres")
        print(f"🎯 Cargos selecionados: {cargos_selecionados}")
        
        # Chamar a função exatamente como no Streamlit
        print("\n🔍 Chamando analisar_edital_com_llm...")
        resultado = analisar_edital_com_llm(pdf_content, cargos_selecionados)
        
        print("\n📊 RESULTADO RECEBIDO:")
        print("="*50)
        
        # Verificar campos essenciais
        campos_essenciais = [
            'concurso', 'banca', 'vagas', 'data_prova', 'data_inscricao',
            'cargos_detectados', 'cargos_analisados', 'materias', 
            'modo_analise', 'confianca'
        ]
        
        for campo in campos_essenciais:
            if campo in resultado:
                valor = resultado[campo]
                if isinstance(valor, dict):
                    print(f"✅ {campo}: {len(valor)} itens")
                elif isinstance(valor, list):
                    print(f"✅ {campo}: {len(valor)} elementos - {valor[:3]}...")
                else:
                    print(f"✅ {campo}: {valor}")
            else:
                print(f"❌ {campo}: AUSENTE")
        
        # Verificar modo e confiança
        modo_analise = resultado.get('modo_analise', 'N/A')
        confianca = resultado.get('confianca', 'N/A')
        
        print(f"\n🎯 DIAGNÓSTICO FINAL:")
        print(f"• Modo de Análise: {modo_analise}")
        print(f"• Confiança: {confianca}")
        
        if modo_analise == "Fallback" or confianca == "Baixa":
            print("❌ PROBLEMA: Análise em modo fallback!")
            if 'erro' in resultado:
                print(f"❌ Erro capturado: {resultado['erro']}")
            return False
        else:
            print("✅ ANÁLISE FUNCIONANDO CORRETAMENTE!")
            return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 TESTE EXATO DO FLUXO STREAMLIT")
    print("="*50)
    
    success = test_exact_streamlit_flow()
    
    if success:
        print("\n🎉 TESTE PASSOU!")
        print("A análise deve funcionar corretamente no Streamlit.")
    else:
        print("\n❌ TESTE FALHOU!")
        print("Há um problema na análise que precisa ser corrigido.")
        sys.exit(1)
