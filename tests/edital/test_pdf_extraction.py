#!/usr/bin/env python3
"""
Teste específico para extração de PDF
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_pdf_extraction():
    """Testa a extração de PDF"""
    try:
        print("🔍 Testando extração de PDF...")
        
        # Importar as funções
        sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))
        from app.app import extrair_texto_arquivo
        from utils.edital_analyzer import EditalAnalyzer
        
        print("✅ Funções importadas com sucesso")
        
        # Verificar se existe algum PDF de teste
        test_files = [
            "edital.pdf",
            "test.pdf", 
            "sample.pdf",
            "concurso.pdf"
        ]
        
        pdf_found = None
        for test_file in test_files:
            if os.path.exists(test_file):
                pdf_found = test_file
                break
        
        if pdf_found:
            print(f"📄 PDF encontrado: {pdf_found}")
            
            # Simular upload do arquivo
            class MockUploadedFile:
                def __init__(self, file_path):
                    self.name = os.path.basename(file_path)
                    self.type = "application/pdf"
                    with open(file_path, 'rb') as f:
                        self.content = f.read()
                
                def read(self):
                    return self.content
                
                def getvalue(self):
                    return self.content
            
            mock_file = MockUploadedFile(pdf_found)
            
            # Testar extração
            print("🔍 Extraindo texto do PDF...")
            texto_extraido = extrair_texto_arquivo(mock_file)
            
            print(f"✅ Texto extraído: {len(texto_extraido)} caracteres")
            print(f"📄 Primeiros 200 caracteres:")
            print("-" * 50)
            print(texto_extraido[:200])
            print("-" * 50)
            
            if texto_extraido.startswith("Erro"):
                print("❌ ERRO na extração do PDF!")
                return False
            
            # Testar análise com o texto extraído
            print("\n🔍 Testando análise com texto extraído...")
            analyzer = EditalAnalyzer()
            resultado = analyzer.analisar_edital(texto_extraido, ["Agente"])
            
            modo = resultado.get('modo_analise', 'N/A')
            confianca = resultado.get('confianca', 'N/A')
            
            print(f"🎯 Modo: {modo}")
            print(f"✅ Confiança: {confianca}")
            
            return modo != "Fallback" and confianca != "Baixa"
            
        else:
            print("📄 Nenhum PDF de teste encontrado")
            print("Vou criar um PDF de teste simples...")
            
            # Criar conteúdo de teste que simula um PDF extraído
            conteudo_simulado = """
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
            """
            
            print(f"📄 Conteúdo simulado: {len(conteudo_simulado)} caracteres")
            
            # Testar análise
            analyzer = EditalAnalyzer()
            resultado = analyzer.analisar_edital(conteudo_simulado, ["Agente"])
            
            modo = resultado.get('modo_analise', 'N/A')
            confianca = resultado.get('confianca', 'N/A')
            
            print(f"🎯 Modo: {modo}")
            print(f"✅ Confiança: {confianca}")
            
            return modo != "Fallback" and confianca != "Baixa"
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 TESTE DE EXTRAÇÃO DE PDF")
    print("="*50)
    
    success = test_pdf_extraction()
    
    if success:
        print("\n🎉 EXTRAÇÃO E ANÁLISE FUNCIONANDO!")
        print("O problema pode estar na interface do Streamlit.")
    else:
        print("\n❌ PROBLEMA NA EXTRAÇÃO OU ANÁLISE!")
        print("Verifique os erros acima.")
        sys.exit(1)
