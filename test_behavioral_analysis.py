"""
🧠 Teste Completo do Sistema de Análise Comportamental
Valida todas as funcionalidades do componente de análise comportamental
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any

from components.behavioral_analysis import (
    BehavioralAnalyzer, StudySession, BehavioralPattern,
    StudyState, ConcentrationLevel, FatigueLevel,
    generate_example_sessions, filter_sessions_by_period,
    export_behavioral_report, generate_priority_recommendations
)

class TestBehavioralAnalysis:
    """Classe de teste para análise comportamental"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.analyzer = BehavioralAnalyzer()
        self.sample_sessions = self.create_sample_sessions()
        
        # Adicionar sessões ao analyzer
        for session in self.sample_sessions:
            self.analyzer.add_session(session)
    
    def create_sample_sessions(self) -> List[StudySession]:
        """Cria sessões de exemplo para teste"""
        sessions = []
        
        # Criar 20 sessões variadas
        for i in range(20):
            timestamp = datetime.now() - timedelta(days=i)
            
            # Variar concentração por horário
            hour = 9 + (i % 8)  # Horários de 9h às 16h
            concentration = 8 if 9 <= hour <= 11 else 6 if 14 <= hour <= 16 else 5
            concentration += np.random.normal(0, 1)
            concentration = max(0, min(10, concentration))
            
            # Variar fadiga por duração
            duration = 60 + (i % 3) * 30  # 60, 90, 120 minutos
            fatigue = duration / 30 + np.random.normal(0, 1)
            fatigue = max(0, min(10, fatigue))
            
            # Produtividade correlacionada
            productivity = concentration - fatigue / 2 + np.random.normal(0, 1)
            productivity = max(0, min(10, productivity))
            
            session = StudySession(
                timestamp=timestamp,
                duration_minutes=duration,
                subject=["Português", "Matemática", "Direito"][i % 3],
                activity_type=["Leitura", "Exercícios", "Revisão"][i % 3],
                concentration_score=concentration,
                fatigue_level=fatigue,
                productivity_score=productivity,
                interruptions=np.random.randint(0, 5),
                break_frequency=np.random.randint(1, 4),
                performance_score=np.random.uniform(60, 95),
                mood_before=np.random.randint(3, 6),
                mood_after=np.random.randint(3, 6),
                environment_quality=np.random.randint(3, 6),
                device_used="Desktop",
                location="Casa"
            )
            sessions.append(session)
        
        return sessions
    
    def test_concentration_analysis(self):
        """Testa análise de concentração"""
        print("\n🎯 TESTE: Análise de Concentração")
        
        analysis = self.analyzer.analyze_concentration_patterns(self.sample_sessions)
        
        # Verificar estrutura do resultado
        assert 'concentration_by_hour' in analysis
        assert 'concentration_by_weekday' in analysis
        assert 'peak_hours' in analysis
        assert 'average_concentration' in analysis
        assert 'concentration_trend' in analysis
        
        # Verificar valores
        assert isinstance(analysis['peak_hours'], list)
        assert len(analysis['peak_hours']) > 0
        assert 0 <= analysis['average_concentration'] <= 10
        assert analysis['concentration_trend'] in ['Crescente', 'Decrescente', 'Estável']
        
        print(f"✅ Concentração média: {analysis['average_concentration']:.1f}/10")
        print(f"✅ Horários de pico: {analysis['peak_hours']}")
        print(f"✅ Tendência: {analysis['concentration_trend']}")
        
        return True
    
    def test_fatigue_analysis(self):
        """Testa análise de fadiga"""
        print("\n😴 TESTE: Análise de Fadiga")
        
        analysis = self.analyzer.analyze_fatigue_patterns(self.sample_sessions)
        
        # Verificar estrutura do resultado
        assert 'fatigue_by_hour' in analysis
        assert 'high_fatigue_frequency' in analysis
        assert 'optimal_session_length' in analysis
        assert 'recovery_time_needed' in analysis
        assert 'fatigue_triggers' in analysis
        
        # Verificar valores
        assert 0 <= analysis['high_fatigue_frequency'] <= 100
        assert analysis['optimal_session_length'] > 0
        assert analysis['recovery_time_needed'] > 0
        assert isinstance(analysis['fatigue_triggers'], list)
        
        print(f"✅ Frequência alta fadiga: {analysis['high_fatigue_frequency']:.1f}%")
        print(f"✅ Duração ótima: {analysis['optimal_session_length']} min")
        print(f"✅ Tempo recuperação: {analysis['recovery_time_needed']} min")
        print(f"✅ Gatilhos: {len(analysis['fatigue_triggers'])} identificados")
        
        return True
    
    def test_productivity_analysis(self):
        """Testa análise de produtividade"""
        print("\n⚡ TESTE: Análise de Produtividade")
        
        analysis = self.analyzer.analyze_productivity_patterns(self.sample_sessions)
        
        # Verificar estrutura do resultado
        assert 'productivity_by_subject' in analysis
        assert 'productivity_by_activity' in analysis
        assert 'correlations' in analysis
        assert 'average_productivity' in analysis
        assert 'peak_performance_conditions' in analysis
        
        # Verificar correlações
        correlations = analysis['correlations']
        assert 'concentration_productivity' in correlations
        assert 'mood_productivity' in correlations
        assert 'environment_productivity' in correlations
        assert 'fatigue_productivity' in correlations
        
        # Verificar valores
        assert 0 <= analysis['average_productivity'] <= 10
        
        print(f"✅ Produtividade média: {analysis['average_productivity']:.1f}/10")
        print(f"✅ Correlação concentração: {correlations['concentration_productivity']:.2f}")
        print(f"✅ Correlação fadiga: {correlations['fatigue_productivity']:.2f}")
        
        peak_conditions = analysis['peak_performance_conditions']
        print(f"✅ Melhores matérias: {peak_conditions['best_subjects']}")
        
        return True
    
    def test_pattern_detection(self):
        """Testa detecção de padrões comportamentais"""
        print("\n🤖 TESTE: Detecção de Padrões por IA")
        
        patterns = self.analyzer.detect_behavioral_patterns(self.sample_sessions)
        
        # Verificar que padrões foram detectados
        assert isinstance(patterns, list)
        assert len(patterns) > 0
        
        # Verificar estrutura dos padrões
        for pattern in patterns:
            assert isinstance(pattern, BehavioralPattern)
            assert hasattr(pattern, 'pattern_id')
            assert hasattr(pattern, 'pattern_name')
            assert hasattr(pattern, 'description')
            assert hasattr(pattern, 'frequency')
            assert hasattr(pattern, 'impact_score')
            assert hasattr(pattern, 'recommendations')
            assert hasattr(pattern, 'optimal_conditions')
            
            # Verificar valores
            assert 0 <= pattern.frequency <= 100
            assert 0 <= pattern.impact_score <= 10
            assert isinstance(pattern.recommendations, list)
            assert isinstance(pattern.optimal_conditions, dict)
        
        print(f"✅ Padrões detectados: {len(patterns)}")
        for i, pattern in enumerate(patterns):
            print(f"  {i+1}. {pattern.pattern_name} (Freq: {pattern.frequency:.1f}%, Impacto: {pattern.impact_score:.1f})")
        
        return True
    
    def test_schedule_optimization(self):
        """Testa otimização de cronograma"""
        print("\n📅 TESTE: Otimização de Cronograma")
        
        optimization = self.analyzer.generate_schedule_optimization(self.sample_sessions)
        
        # Verificar estrutura do resultado
        assert 'optimal_study_hours' in optimization
        assert 'optimal_session_duration' in optimization
        assert 'optimal_break_frequency' in optimization
        assert 'personalized_schedule' in optimization
        assert 'weekly_distribution' in optimization
        assert 'subject_prioritization' in optimization
        
        # Verificar valores
        optimal_hours = optimization['optimal_study_hours']
        assert isinstance(optimal_hours, list)
        assert len(optimal_hours) > 0
        assert all(0 <= hour <= 23 for hour in optimal_hours)
        
        optimal_duration = optimization['optimal_session_duration']
        assert optimal_duration > 0
        assert optimal_duration <= 300  # Máximo 5 horas
        
        break_frequency = optimization['optimal_break_frequency']
        assert break_frequency > 0
        
        # Verificar cronograma personalizado
        schedule = optimization['personalized_schedule']
        assert isinstance(schedule, dict)
        weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        for day in weekdays:
            assert day in schedule
            assert isinstance(schedule[day], list)
        
        print(f"✅ Horários ótimos: {optimal_hours}")
        print(f"✅ Duração ótima: {optimal_duration} min")
        print(f"✅ Frequência pausas: {break_frequency}/hora")
        print(f"✅ Cronograma gerado para {len(schedule)} dias")
        
        return True
    
    def test_data_filtering(self):
        """Testa filtragem de dados por período"""
        print("\n📊 TESTE: Filtragem de Dados")
        
        # Testar diferentes períodos
        periods = ["Última Semana", "Último Mês", "Últimos 3 Meses", "Todos os Dados"]
        
        for period in periods:
            filtered_sessions = filter_sessions_by_period(self.sample_sessions, period)
            assert isinstance(filtered_sessions, list)
            
            if period == "Todos os Dados":
                assert len(filtered_sessions) == len(self.sample_sessions)
            else:
                assert len(filtered_sessions) <= len(self.sample_sessions)
            
            print(f"✅ {period}: {len(filtered_sessions)} sessões")
        
        return True
    
    def test_report_generation(self):
        """Testa geração de relatório"""
        print("\n📄 TESTE: Geração de Relatório")
        
        report = export_behavioral_report(self.analyzer, self.sample_sessions)
        
        # Verificar que o relatório foi gerado
        assert isinstance(report, str)
        assert len(report) > 0
        
        # Verificar seções do relatório
        assert "RELATÓRIO DE ANÁLISE COMPORTAMENTAL" in report
        assert "RESUMO EXECUTIVO" in report
        assert "ANÁLISE DE CONCENTRAÇÃO" in report
        assert "ANÁLISE DE FADIGA" in report
        assert "PADRÕES COMPORTAMENTAIS" in report
        assert "CRONOGRAMA OTIMIZADO" in report
        assert "RECOMENDAÇÕES PRIORITÁRIAS" in report
        
        print(f"✅ Relatório gerado: {len(report)} caracteres")
        print(f"✅ Seções incluídas: 7/7")
        
        return True
    
    def test_example_data_generation(self):
        """Testa geração de dados de exemplo"""
        print("\n🎲 TESTE: Geração de Dados de Exemplo")
        
        example_sessions = generate_example_sessions()
        
        # Verificar que dados foram gerados
        assert isinstance(example_sessions, list)
        assert len(example_sessions) > 0
        
        # Verificar estrutura das sessões
        for session in example_sessions[:5]:  # Verificar apenas as primeiras 5
            assert isinstance(session, StudySession)
            assert hasattr(session, 'timestamp')
            assert hasattr(session, 'duration_minutes')
            assert hasattr(session, 'subject')
            assert hasattr(session, 'concentration_score')
            assert hasattr(session, 'productivity_score')
            
            # Verificar valores válidos
            assert 0 <= session.concentration_score <= 10
            assert 0 <= session.fatigue_level <= 10
            assert 0 <= session.productivity_score <= 10
            assert session.duration_minutes > 0
        
        print(f"✅ Sessões de exemplo: {len(example_sessions)}")
        print(f"✅ Estrutura validada: ✓")
        
        return True

def run_behavioral_analysis_tests():
    """Executa todos os testes de análise comportamental"""
    print("🧠 INICIANDO TESTES DE ANÁLISE COMPORTAMENTAL")
    print("=" * 60)
    
    test_instance = TestBehavioralAnalysis()
    test_instance.setup_method()
    
    tests = [
        ("Análise de Concentração", test_instance.test_concentration_analysis),
        ("Análise de Fadiga", test_instance.test_fatigue_analysis),
        ("Análise de Produtividade", test_instance.test_productivity_analysis),
        ("Detecção de Padrões", test_instance.test_pattern_detection),
        ("Otimização de Cronograma", test_instance.test_schedule_optimization),
        ("Filtragem de Dados", test_instance.test_data_filtering),
        ("Geração de Relatório", test_instance.test_report_generation),
        ("Dados de Exemplo", test_instance.test_example_data_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, "✅ PASSOU" if result else "❌ FALHOU"))
        except Exception as e:
            results.append((test_name, f"❌ ERRO: {str(e)}"))
    
    # Mostrar resultados
    print("\n" + "=" * 60)
    print("RESULTADOS DOS TESTES")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, status in results:
        print(f"{test_name:<25} | {status}")
        if "PASSOU" in status:
            passed += 1
    
    print("-" * 60)
    print(f"TOTAL: {passed}/{total} testes passaram ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 TODOS OS TESTES DE ANÁLISE COMPORTAMENTAL PASSARAM!")
        print("✅ Sistema de análise comportamental funcionando perfeitamente")
        print("✅ Detecção de padrões por IA operacional")
        print("✅ Otimização de cronograma implementada")
        print("✅ Relatórios completos sendo gerados")
        print("✅ Integração com interface pronta")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Revisar implementação.")
    
    return passed == total

if __name__ == "__main__":
    success = run_behavioral_analysis_tests()
    exit(0 if success else 1)
