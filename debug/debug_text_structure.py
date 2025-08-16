#!/usr/bin/env python3
"""
Debug da estrutura do texto para entender o problema
"""

def debug_text_structure():
    """Debug da estrutura do texto"""
    print("🔍 DEBUG DA ESTRUTURA DO TEXTO")
    print("="*50)
    
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
    
    print("📄 ESTRUTURA LINHA POR LINHA:")
    linhas = content_lower.split('\n')
    
    for i, linha in enumerate(linhas):
        linha_limpa = linha.strip()
        if linha_limpa:  # Só mostrar linhas não vazias
            print(f"Linha {i:2d}: '{linha_limpa}'")
            
            # Marcar linhas importantes
            if 'contabilidade geral:' in linha_limpa:
                print("         ^^^ LINHA DA MATÉRIA CONTABILIDADE")
            elif any(palavra in linha_limpa for palavra in ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']):
                print("         ^^^ LINHA COM CONTEÚDO DE CONTABILIDADE")
    
    print(f"\n🔍 BUSCA ESPECÍFICA POR 'contabilidade geral:'")
    
    # Simular o algoritmo linha por linha
    materia_lower = "contabilidade geral"
    encontrou_materia = False
    coletando_conteudo = False
    conteudo_coletado = []
    
    for i, linha in enumerate(linhas):
        linha_limpa = linha.strip()
        
        print(f"Processando linha {i}: '{linha_limpa}'")
        
        # Verificar se encontrou a matéria
        if materia_lower + ':' in linha_limpa:
            print(f"  ✅ ENCONTROU MATÉRIA na linha {i}")
            encontrou_materia = True
            coletando_conteudo = True
            
            # Verificar se há conteúdo na mesma linha após ':'
            pos_dois_pontos = linha_limpa.find(':')
            if pos_dois_pontos > 0 and pos_dois_pontos < len(linha_limpa) - 1:
                conteudo_linha = linha_limpa[pos_dois_pontos + 1:].strip()
                print(f"  📝 Conteúdo na mesma linha: '{conteudo_linha}'")
                
                if len(conteudo_linha) > 10:
                    topicos_linha = [t.strip() for t in conteudo_linha.split(';') if t.strip()]
                    print(f"  📚 Tópicos encontrados: {topicos_linha}")
                    conteudo_coletado.extend(topicos_linha)
            continue
        
        # Se está coletando conteúdo
        if coletando_conteudo:
            print(f"  🔍 Coletando conteúdo...")
            
            # Verificar se chegou em outra matéria
            outras_materias = ['português:', 'matemática:', 'direito:', 'informática:']
            if any(outra in linha_limpa for outra in outras_materias):
                print(f"  ❌ PAROU: encontrou outra matéria")
                break
            
            # Verificar se linha vazia ou nova seção
            if not linha_limpa:
                print(f"  ⚪ Linha vazia, continuando...")
                continue
            
            # Coletar conteúdo da linha
            if len(linha_limpa) > 10:
                print(f"  📝 Coletando: '{linha_limpa}'")
                topicos_linha = [t.strip() for t in linha_limpa.split(';') if t.strip()]
                print(f"  📚 Tópicos: {topicos_linha}")
                conteudo_coletado.extend(topicos_linha)
    
    print(f"\n🎯 RESULTADO FINAL:")
    print(f"Conteúdo coletado: {len(conteudo_coletado)} tópicos")
    for i, topico in enumerate(conteudo_coletado):
        print(f"  {i+1}. {topico}")
    
    # Verificar palavras-chave
    conteudo_texto = ' '.join(conteudo_coletado).lower()
    palavras_contabilidade = ['patrimônio', 'balanço', 'demonstração', 'contas', 'balancete']
    palavras_encontradas = [p for p in palavras_contabilidade if p in conteudo_texto]
    print(f"\nPalavras-chave encontradas: {palavras_encontradas}")

if __name__ == "__main__":
    debug_text_structure()
