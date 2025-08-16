#!/usr/bin/env python3
"""
🧪 Script para executar todos os testes do Agente Concurseiro v2.0
Organizado por categorias e com relatórios detalhados
"""

import subprocess
import sys
import os
from pathlib import Path
import time
from datetime import datetime

def run_command(command, description):
    """Executar comando e capturar resultado"""
    print(f"\n🔄 {description}")
    print(f"Comando: {command}")
    print("-" * 60)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(
            command.split(),
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ Sucesso ({duration:.2f}s)")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ Falha ({duration:.2f}s)")
            if result.stderr:
                print("STDERR:", result.stderr)
            if result.stdout:
                print("STDOUT:", result.stdout)
        
        return result.returncode == 0, result.stdout, result.stderr
        
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
        return False, "", str(e)

def main():
    """Executar todos os testes organizados"""
    print("🧪 AGENTE CONCURSEIRO v2.0 - SUITE DE TESTES")
    print("=" * 60)
    print(f"📅 Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📁 Diretório: {Path.cwd()}")
    
    # Verificar se pytest está instalado
    try:
        import pytest
        print(f"✅ Pytest instalado: {pytest.__version__}")
    except ImportError:
        print("❌ Pytest não encontrado. Instalando...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest"])
    
    results = {}
    total_tests = 0
    passed_tests = 0
    
    # 1. Testes dos Componentes Principais
    print("\n" + "=" * 60)
    print("🧩 TESTES DOS COMPONENTES PRINCIPAIS")
    print("=" * 60)
    
    component_tests = [
        ("pytest tests/components/test_voice_assistant.py -v", "Assistente de Voz"),
        ("pytest tests/components/test_behavioral_analysis.py -v", "Análise Comportamental"),
        ("pytest tests/components/test_trend_prediction.py -v", "Predição de Tendências"),
        ("pytest tests/components/test_ai_predictor.py -v", "IA Preditiva"),
        ("pytest tests/components/test_augmented_reality.py -v", "Realidade Aumentada"),
        ("pytest tests/components/test_collaborative_features.py -v", "Recursos Colaborativos"),
        ("pytest tests/components/test_mobile_companion.py -v", "Mobile Companion"),
        ("pytest tests/components/test_spaced_repetition.py -v", "Revisão Espaçada"),
    ]
    
    for command, description in component_tests:
        success, stdout, stderr = run_command(command, f"Testando {description}")
        results[description] = success
        
        # Contar testes
        if "passed" in stdout:
            try:
                passed = int(stdout.split("passed")[0].split()[-1])
                total_tests += passed
                if success:
                    passed_tests += passed
            except:
                pass
    
    # 2. Testes de Análise de Editais
    print("\n" + "=" * 60)
    print("📋 TESTES DE ANÁLISE DE EDITAIS")
    print("=" * 60)
    
    success, stdout, stderr = run_command(
        "pytest tests/edital/ -v", 
        "Testando Análise de Editais"
    )
    results["Análise de Editais"] = success
    
    # 3. Testes dos Agentes IA
    print("\n" + "=" * 60)
    print("🤖 TESTES DOS AGENTES IA")
    print("=" * 60)
    
    success, stdout, stderr = run_command(
        "pytest tests/agents/ -v", 
        "Testando Agentes CrewAI"
    )
    results["Agentes IA"] = success
    
    # 4. Testes da API
    print("\n" + "=" * 60)
    print("🌐 TESTES DA API")
    print("=" * 60)
    
    success, stdout, stderr = run_command(
        "pytest tests/api/ -v", 
        "Testando API FastAPI"
    )
    results["API FastAPI"] = success
    
    # 5. Testes de Funcionalidades
    print("\n" + "=" * 60)
    print("⭐ TESTES DE FUNCIONALIDADES")
    print("=" * 60)
    
    success, stdout, stderr = run_command(
        "pytest tests/features/ -v", 
        "Testando Funcionalidades Específicas"
    )
    results["Funcionalidades"] = success
    
    # 6. Todos os Testes (Resumo)
    print("\n" + "=" * 60)
    print("📊 RESUMO GERAL - TODOS OS TESTES")
    print("=" * 60)
    
    success, stdout, stderr = run_command(
        "pytest tests/ --tb=short", 
        "Executando Todos os Testes"
    )
    results["Todos os Testes"] = success
    
    # Relatório Final
    print("\n" + "=" * 60)
    print("📊 RELATÓRIO FINAL")
    print("=" * 60)
    
    successful = sum(1 for result in results.values() if result)
    total_categories = len(results)
    
    print(f"📈 Categorias testadas: {total_categories}")
    print(f"✅ Categorias com sucesso: {successful}")
    print(f"❌ Categorias com falha: {total_categories - successful}")
    print(f"📊 Taxa de sucesso: {(successful/total_categories)*100:.1f}%")
    
    print("\n📋 Detalhes por Categoria:")
    for category, success in results.items():
        status = "✅ PASSOU" if success else "❌ FALHOU"
        print(f"  {status} - {category}")
    
    # Status final
    if successful == total_categories:
        print("\n🎉 TODOS OS TESTES PASSARAM! Sistema pronto para produção.")
        return 0
    else:
        print(f"\n⚠️  {total_categories - successful} categoria(s) com falha. Verificar logs acima.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)