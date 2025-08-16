#!/usr/bin/env python3
"""
Debug específico para detecção por cargo
"""

import sys
import os
from pathlib import Path

# Adicionar o diretório raiz ao path
root_dir = Path(__file__).parent
sys.path.insert(0, str(root_dir))

def debug_cargo_especifico():
    """Debug específico para detecção por cargo"""
    print("🔍 DEBUG DETECÇÃO POR CARGO ESPECÍFICO")
    print("="*50)
    
    from app.utils.edital_analyzer import EditalAnalyzer
    
    analyzer = EditalAnalyzer()
    
    # Mesmo edital do teste que está falhando
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
    
    print("📄 TESTE 1: _buscar_materias_por_cargo para 'Técnico Judiciário'")
    materias_tecnico_direto = analyzer._buscar_materias_por_cargo(content_lower, 'Técnico Judiciário')
    print(f"Matérias encontradas: {list(materias_tecnico_direto.keys())}")
    print(f"Número de matérias: {len(materias_tecnico_direto)}")
    
    print("\n📄 TESTE 2: _buscar_materias_por_cargo para 'Analista Judiciário - Área Administrativa'")
    materias_admin_direto = analyzer._buscar_materias_por_cargo(content_lower, 'Analista Judiciário - Área Administrativa')
    print(f"Matérias encontradas: {list(materias_admin_direto.keys())}")
    print(f"Número de matérias: {len(materias_admin_direto)}")
    
    print("\n📄 TESTE 3: _detectar_materias para 'Técnico Judiciário'")
    materias_tecnico_completo = analyzer._detectar_materias(content_lower, 'Técnico Judiciário')
    print(f"Matérias encontradas: {list(materias_tecnico_completo.keys())}")
    print(f"Número de matérias: {len(materias_tecnico_completo)}")
    
    print("\n📄 TESTE 4: _detectar_materias para 'Analista Judiciário - Área Administrativa'")
    materias_admin_completo = analyzer._detectar_materias(content_lower, 'Analista Judiciário - Área Administrativa')
    print(f"Matérias encontradas: {list(materias_admin_completo.keys())}")
    print(f"Número de matérias: {len(materias_admin_completo)}")
    
    print("\n📄 TESTE 5: analisar_edital completo para 'Técnico Judiciário'")
    resultado_tecnico = analyzer.analisar_edital(edital_multiplo, ['Técnico Judiciário'])
    materias_tecnico_final = set(resultado_tecnico['materias'].keys())
    print(f"Matérias encontradas: {list(materias_tecnico_final)}")
    print(f"Número de matérias: {len(materias_tecnico_final)}")
    
    print("\n📄 TESTE 6: analisar_edital completo para 'Analista Judiciário - Área Administrativa'")
    resultado_admin = analyzer.analisar_edital(edital_multiplo, ['Analista Judiciário - Área Administrativa'])
    materias_admin_final = set(resultado_admin['materias'].keys())
    print(f"Matérias encontradas: {list(materias_admin_final)}")
    print(f"Número de matérias: {len(materias_admin_final)}")
    
    print("\n🔍 COMPARAÇÃO FINAL:")
    sobreposicao = len(materias_tecnico_final.intersection(materias_admin_final)) / max(len(materias_tecnico_final), len(materias_admin_final))
    print(f"Sobreposição entre Técnico e Admin: {sobreposicao:.1%}")
    print(f"Teste passaria? {sobreposicao < 0.9}")
    
    print(f"\nMatérias Técnico: {materias_tecnico_final}")
    print(f"Matérias Admin: {materias_admin_final}")
    print(f"Interseção: {materias_tecnico_final.intersection(materias_admin_final)}")

if __name__ == "__main__":
    debug_cargo_especifico()
