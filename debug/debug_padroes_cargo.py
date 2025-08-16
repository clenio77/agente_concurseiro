#!/usr/bin/env python3
"""
Debug dos padrões regex para cargo
"""

import sys
import os
from pathlib import Path
import re

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_padroes_cargo():
    """Debug dos padrões regex para cargo"""
    print("🔍 DEBUG PADRÕES REGEX PARA CARGO")
    print("="*50)
    
    # Mesmo edital do teste
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
    
    content_lower = edital_multiplo.lower()
    cargo = 'Técnico Judiciário'
    cargo_lower = cargo.lower()
    
    print(f"📄 TESTANDO PADRÕES PARA CARGO: '{cargo}'")
    print(f"Cargo lower: '{cargo_lower}'")
    
    # Padrões do método atualizado
    padroes_cargo = [
        # Padrão: "CARGO X: Nome do Cargo" seguido de matérias até próximo cargo
        rf'cargo\s*\d*[:\s]*{re.escape(cargo_lower)}[:\-\s]*(.{{0,2000}}?)(?:cargo\s*\d+|conteúdo programático|$)',
        # Padrão: Nome do cargo seguido de matérias até próximo cargo
        rf'{re.escape(cargo_lower)}[:\-\s]*(.{{0,1500}}?)(?:cargo\s*\d+|cargo\s*[a-z]|$)',
        # Padrão: "Matérias para [cargo]:"
        rf'matérias\s+para\s+(?:o\s+cargo\s+(?:de\s+)?)?{re.escape(cargo_lower)}[:\-\s]*(.{{0,1500}}?)(?:cargo|conteúdo|$)',
        # Padrão: "Para o cargo de [cargo]"
        rf'para\s+o\s+cargo\s+de\s+{re.escape(cargo_lower)}[:\-\s]*(.{{0,1500}}?)(?:cargo|função|$)',
        # Padrão: seção específica com nome do cargo
        rf'{re.escape(cargo_lower)}\s*[\-:]\s*(?:matérias?[:\-\s]*)?(.{{0,1000}}?)(?:cargo|função|prova|$)',
    ]
    
    print(f"\n📄 CONTEÚDO DO EDITAL (primeiros 500 chars):")
    print(f"'{content_lower[:500]}'")
    
    for i, padrao in enumerate(padroes_cargo, 1):
        print(f"\n🔍 PADRÃO {i}:")
        print(f"Regex: {padrao}")
        
        match = re.search(padrao, content_lower, re.IGNORECASE | re.DOTALL)
        if match:
            secao_cargo = match.group(1).strip()
            print(f"✅ MATCH ENCONTRADO!")
            print(f"Seção capturada: '{secao_cargo[:200]}{'...' if len(secao_cargo) > 200 else ''}'")
            print(f"Tamanho da seção: {len(secao_cargo)}")
        else:
            print(f"❌ Nenhum match encontrado")
    
    # Testar padrões mais simples
    print(f"\n🔍 TESTES SIMPLES:")
    
    # Teste 1: Buscar "cargo 1: técnico judiciário"
    padrao_simples1 = r'cargo\s*1[:\s]*técnico judiciário'
    match1 = re.search(padrao_simples1, content_lower, re.IGNORECASE)
    print(f"Padrão simples 1: {padrao_simples1}")
    print(f"Match: {'✅' if match1 else '❌'}")
    
    # Teste 2: Buscar qualquer coisa após "técnico judiciário"
    padrao_simples2 = r'técnico judiciário(.{0,200})'
    match2 = re.search(padrao_simples2, content_lower, re.IGNORECASE | re.DOTALL)
    print(f"Padrão simples 2: {padrao_simples2}")
    if match2:
        print(f"✅ Match: '{match2.group(1)}'")
    else:
        print(f"❌ Nenhum match")
    
    # Teste 3: Verificar se o cargo existe no texto
    print(f"\nCargo '{cargo_lower}' existe no texto? {'✅' if cargo_lower in content_lower else '❌'}")
    
    # Mostrar onde o cargo aparece
    pos = content_lower.find(cargo_lower)
    if pos >= 0:
        contexto = content_lower[max(0, pos-50):pos+100]
        print(f"Contexto: '...{contexto}...'")

if __name__ == "__main__":
    debug_padroes_cargo()
