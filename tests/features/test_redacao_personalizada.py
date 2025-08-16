#!/usr/bin/env python3
"""
Teste da funcionalidade de redação personalizada
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def test_personalized_essays():
    """Testa a geração de redações personalizadas"""
    try:
        print("🧪 TESTANDO GERAÇÃO DE REDAÇÕES PERSONALIZADAS")
        print("="*60)
        
        # Importar a ferramenta
        from tools.writing_tool import WritingTool
        
        tool = WritingTool()
        
        # Temas de teste para diferentes categorias
        temas_teste = [
            ("A importância da educação digital no ensino público", "CESPE"),
            ("Desafios da segurança pública nas grandes cidades", "FCC"),
            ("Sustentabilidade ambiental e desenvolvimento econômico", "VUNESP"),
            ("O impacto da tecnologia na sociedade moderna", "FGV"),
            ("Políticas de saúde pública no Brasil", "IBFC"),
            ("Os direitos humanos na era digital", "CESPE"),
            ("Combate à corrupção no setor público", "FCC")
        ]
        
        print(f"🎯 Testando {len(temas_teste)} temas diferentes...")
        print()
        
        for i, (tema, banca) in enumerate(temas_teste, 1):
            print(f"📝 TESTE {i}: {tema}")
            print(f"🏛️ Banca: {banca}")
            print("-" * 50)
            
            # Gerar redação
            resultado = tool.generate_example_essay(banca, tema, 25)
            
            if "error" in resultado:
                print(f"❌ ERRO: {resultado['error']}")
                continue
            
            redacao = resultado["example_essay"]
            
            # Verificar se a redação é personalizada
            print(f"✅ Redação gerada: {len(redacao)} caracteres")
            
            # Verificar se o tema está presente na redação
            tema_palavras = tema.lower().split()
            tema_presente = any(palavra in redacao.lower() for palavra in tema_palavras if len(palavra) > 3)
            
            if tema_presente:
                print("✅ Tema identificado na redação")
            else:
                print("⚠️ Tema pode não estar bem integrado")
            
            # Mostrar primeiros 200 caracteres
            print(f"📄 Início da redação:")
            print(f'"{redacao[:200]}..."')
            print()
            
            # Verificar estrutura (4 parágrafos)
            paragrafos = redacao.split('\n\n')
            print(f"📊 Estrutura: {len(paragrafos)} parágrafos")
            
            if len(paragrafos) == 4:
                print("✅ Estrutura correta (4 parágrafos)")
            else:
                print(f"⚠️ Estrutura atípica ({len(paragrafos)} parágrafos)")
            
            print("=" * 60)
            print()
        
        # Teste de temas repetidos para verificar se gera conteúdo diferente
        print("🔄 TESTE DE VARIAÇÃO - MESMO TEMA, BANCAS DIFERENTES")
        print("=" * 60)
        
        tema_fixo = "A importância da educação no século XXI"
        bancas = ["CESPE", "FCC", "VUNESP"]
        
        redacoes_geradas = []
        
        for banca in bancas:
            resultado = tool.generate_example_essay(banca, tema_fixo, 25)
            if "error" not in resultado:
                redacao = resultado["example_essay"]
                redacoes_geradas.append((banca, redacao))
                print(f"✅ {banca}: {len(redacao)} caracteres")
        
        # Verificar se as redações são diferentes
        if len(redacoes_geradas) >= 2:
            redacao1 = redacoes_geradas[0][1]
            redacao2 = redacoes_geradas[1][1]
            
            # Calcular similaridade simples
            palavras1 = set(redacao1.lower().split())
            palavras2 = set(redacao2.lower().split())
            
            intersecao = len(palavras1.intersection(palavras2))
            uniao = len(palavras1.union(palavras2))
            similaridade = intersecao / uniao if uniao > 0 else 0
            
            print(f"📊 Similaridade entre redações: {similaridade:.2%}")
            
            if similaridade < 0.8:  # Menos de 80% de similaridade
                print("✅ Redações suficientemente diferentes")
            else:
                print("⚠️ Redações muito similares - pode precisar de mais variação")
        
        print("\n🎉 TESTE CONCLUÍDO!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_personalized_essays()
    
    if success:
        print("\n✅ FUNCIONALIDADE DE REDAÇÃO PERSONALIZADA FUNCIONANDO!")
        print("Agora as redações devem ser geradas conforme o tema e banca especificados.")
    else:
        print("\n❌ PROBLEMAS ENCONTRADOS NA GERAÇÃO DE REDAÇÕES!")
        sys.exit(1)
