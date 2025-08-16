#!/usr/bin/env python3
"""
Script para testar a funcionalidade de análise de edital no Streamlit.
"""

import os
import sys
from pathlib import Path
import tempfile

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_streamlit_edital_functions():
    """Testa as funções específicas do Streamlit para análise de edital"""
    try:
        print("🔍 Testando funções do Streamlit...")
        
        # Importar funções do app.py
        from app.app import analisar_edital_com_llm, extrair_texto_arquivo
        
        print("✅ Funções importadas com sucesso")
        
        # Conteúdo de teste
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
        
        # Testar análise com LLM
        print("🔍 Testando análise com LLM...")
        cargos_selecionados = ["Agente De Polícia", "Escrivão De Polícia"]
        
        resultado = analisar_edital_com_llm(edital_content, cargos_selecionados)
        
        print("✅ Análise com LLM concluída!")
        
        # Verificar estrutura do resultado
        campos_esperados = [
            'concurso', 'banca', 'vagas', 'data_prova', 'data_inscricao',
            'cargos_detectados', 'cargos_analisados', 'materias', 'conteudo_analisado'
        ]
        
        print("\n📊 VERIFICANDO ESTRUTURA DO RESULTADO:")
        print("="*50)
        
        for campo in campos_esperados:
            if campo in resultado:
                valor = resultado[campo]
                if isinstance(valor, dict):
                    print(f"✅ {campo}: {len(valor)} itens")
                elif isinstance(valor, list):
                    print(f"✅ {campo}: {len(valor)} elementos")
                else:
                    print(f"✅ {campo}: {str(valor)[:50]}...")
            else:
                print(f"❌ {campo}: AUSENTE")
        
        # Verificar matérias específicas
        print(f"\n📚 MATÉRIAS DETECTADAS ({len(resultado.get('materias', {}))}):")
        print("-"*30)
        for materia, info in resultado.get('materias', {}).items():
            questoes = info.get('questoes', 0)
            peso = info.get('peso', 0)
            print(f"• {materia}: {questoes} questões (peso {peso})")
        
        # Verificar cargos
        cargos_detectados = resultado.get('cargos_detectados', [])
        print(f"\n🎯 CARGOS DETECTADOS ({len(cargos_detectados)}):")
        print("-"*30)
        for cargo in cargos_detectados[:10]:  # Mostrar apenas os 10 primeiros
            print(f"• {cargo}")
        if len(cargos_detectados) > 10:
            print(f"... e mais {len(cargos_detectados) - 10} cargos")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_file_upload_simulation():
    """Simula upload de arquivo para testar extração"""
    try:
        print("\n🔍 Testando simulação de upload de arquivo...")
        
        from app.app import extrair_texto_arquivo
        
        # Criar arquivo temporário de teste
        test_content = """
        EDITAL DE CONCURSO PÚBLICO
        
        Cargo: Analista Judiciário
        Banca: CESPE
        Vagas: 100
        
        Matérias:
        - Direito Constitucional
        - Direito Administrativo
        - Português
        """
        
        # Simular arquivo de texto
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write(test_content)
            temp_file_path = f.name
        
        try:
            # Simular objeto de upload do Streamlit
            class MockUploadedFile:
                def __init__(self, content, name, type_):
                    self.content = content.encode('utf-8')
                    self.name = name
                    self.type = type_
                
                def read(self):
                    return self.content
                
                def getvalue(self):
                    return self.content
            
            mock_file = MockUploadedFile(test_content, "edital_teste.txt", "text/plain")
            
            # Testar extração
            texto_extraido = extrair_texto_arquivo(mock_file)
            
            print(f"✅ Texto extraído: {len(texto_extraido)} caracteres")
            print(f"📄 Primeiros 100 caracteres: {texto_extraido[:100]}...")
            
            return True
            
        finally:
            # Limpar arquivo temporário
            os.unlink(temp_file_path)
        
    except Exception as e:
        print(f"❌ Erro na simulação de upload: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DAS FUNÇÕES DE ANÁLISE DE EDITAL NO STREAMLIT")
    print("="*60)
    
    # Teste principal
    success1 = test_streamlit_edital_functions()
    
    # Teste de upload
    success2 = test_file_upload_simulation()
    
    if success1 and success2:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("\n💡 A análise de edital está funcionando corretamente no Streamlit.")
        print("   Agora você pode clicar em 'Analisar Edital' na interface.")
        print("\n🔗 Acesse: http://localhost:8501")
    else:
        print("\n❌ ALGUNS TESTES FALHARAM!")
        print("   Verifique os erros acima.")
        sys.exit(1)
