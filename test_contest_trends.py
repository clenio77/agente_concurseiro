"""
🔮 Teste Completo do Sistema de Predição de Tendências de Concursos
Valida todas as funcionalidades do componente de predição de tendências
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any

from components.contest_trends import (
    ContestTrendsAnalyzer, HistoricalContest, TopicTrend, ContestPrediction,
    TrendType, ContestLevel, ContestArea,
    generate_example_contests
)

class TestContestTrends:
    """Classe de teste para predição de tendências"""
    
    def setup_method(self):
        """Setup para cada teste"""
        self.analyzer = ContestTrendsAnalyzer()
        self.sample_contests = self.create_sample_contests()
        
        # Carregar dados no analyzer
        self.analyzer.load_historical_data(self.sample_contests)
    
    def create_sample_contests(self) -> List[HistoricalContest]:
        """Cria concursos de exemplo para teste"""
        contests = []
        
        # Criar 15 concursos variados
        for i in range(15):
            year = 2020 + (i % 4)  # 2020-2023
            
            contest = HistoricalContest(
                contest_id=f"test_contest_{i+1}",
                name=f"Concurso Teste {i+1}",
                institution=f"Instituição {i % 3 + 1}",
                year=year,
                level=list(ContestLevel)[i % len(ContestLevel)],
                area=list(ContestArea)[i % len(ContestArea)],
                positions=np.random.randint(50, 500),
                candidates=np.random.randint(1000, 10000),
                subjects=["Português", "Matemática", "Direito", "Informática"][:(i % 4) + 1],
                topics=[
                    f"Tópico Comum {j}" for j in range(1, 4)
                ] + [f"Tópico Específico {i}_{j}" for j in range(1, 3)],
                question_distribution={"Português": 20, "Matemática": 15, "Direito": 25},
                difficulty_level=np.random.uniform(3, 9),
                approval_rate=np.random.uniform(5, 30),
                salary_range=(3000, 8000),
                location=f"Cidade {i % 5 + 1}",
                exam_date=datetime(year, np.random.randint(3, 11), 15),
                result_date=datetime(year, np.random.randint(6, 12), 15)
            )
            contests.append(contest)
        
        return contests
    
    def test_data_loading(self):
        """Testa carregamento de dados históricos"""
        print("\n📊 TESTE: Carregamento de Dados")
        
        # Verificar que dados foram carregados
        assert len(self.analyzer.historical_data) == 15
        assert hasattr(self.analyzer, 'df')
        assert not self.analyzer.df.empty
        
        # Verificar estrutura do DataFrame
        expected_columns = ['contest_id', 'name', 'year', 'level', 'area', 'difficulty_level']
        for col in expected_columns:
            assert col in self.analyzer.df.columns
        
        # Verificar features temporais
        assert 'exam_year' in self.analyzer.df.columns
        assert 'exam_month' in self.analyzer.df.columns
        assert 'competition_ratio' in self.analyzer.df.columns
        
        print(f"✅ Concursos carregados: {len(self.analyzer.historical_data)}")
        print(f"✅ DataFrame criado: {self.analyzer.df.shape}")
        print(f"✅ Features temporais: ✓")
        
        return True
    
    def test_model_training(self):
        """Testa treinamento dos modelos de predição"""
        print("\n🤖 TESTE: Treinamento de Modelos")
        
        # Verificar que modelos foram treinados
        assert 'difficulty' in self.analyzer.prediction_models
        assert 'approval' in self.analyzer.prediction_models
        
        # Verificar que modelos são válidos
        difficulty_model = self.analyzer.prediction_models['difficulty']
        approval_model = self.analyzer.prediction_models['approval']
        
        assert hasattr(difficulty_model, 'predict')
        assert hasattr(approval_model, 'predict')
        
        # Testar predição
        test_features = np.array([[100, 2000, 20, 2024]])
        
        difficulty_pred = difficulty_model.predict(test_features)[0]
        approval_pred = approval_model.predict(test_features)[0]
        
        assert 0 <= difficulty_pred <= 10
        assert 0 <= approval_pred <= 100
        
        print(f"✅ Modelo de dificuldade: ✓")
        print(f"✅ Modelo de aprovação: ✓")
        print(f"✅ Predição teste - Dificuldade: {difficulty_pred:.1f}")
        print(f"✅ Predição teste - Aprovação: {approval_pred:.1f}%")
        
        return True
    
    def test_topic_trends_analysis(self):
        """Testa análise de tendências de tópicos"""
        print("\n📈 TESTE: Análise de Tendências de Tópicos")
        
        trends = self.analyzer.analyze_topic_trends()
        
        # Verificar que tendências foram identificadas
        assert isinstance(trends, dict)
        assert len(trends) > 0
        
        # Verificar estrutura das tendências
        for topic, trend in trends.items():
            assert isinstance(trend, TopicTrend)
            assert trend.topic == topic
            assert isinstance(trend.trend_type, TrendType)
            assert 0 <= trend.prediction_score <= 100
            assert 0 <= trend.importance_weight <= 1
            assert trend.frequency >= 0
            assert isinstance(trend.related_topics, list)
        
        # Verificar tipos de tendência
        trend_types = [trend.trend_type for trend in trends.values()]
        assert len(set(trend_types)) > 0  # Pelo menos um tipo de tendência
        
        print(f"✅ Tendências identificadas: {len(trends)}")
        print(f"✅ Tipos de tendência: {len(set(trend_types))}")
        
        # Mostrar algumas tendências
        sorted_trends = sorted(trends.values(), key=lambda x: x.prediction_score, reverse=True)
        for i, trend in enumerate(sorted_trends[:3]):
            print(f"  {i+1}. {trend.topic} - {trend.trend_type.value} (Score: {trend.prediction_score:.1f})")
        
        return True
    
    def test_contest_prediction(self):
        """Testa predição específica de concurso"""
        print("\n🔮 TESTE: Predição de Concurso")
        
        # Analisar tendências primeiro
        self.analyzer.analyze_topic_trends()
        
        # Fazer predição
        prediction = self.analyzer.predict_contest_trends(
            contest_type="Tribunal de Justiça",
            area=ContestArea.JUDICIARIO,
            level=ContestLevel.SUPERIOR,
            positions=100,
            candidates=2000
        )
        
        # Verificar estrutura da predição
        assert isinstance(prediction, ContestPrediction)
        assert prediction.contest_type == "Tribunal de Justiça"
        assert isinstance(prediction.predicted_topics, list)
        assert isinstance(prediction.hot_subjects, list)
        assert 0 <= prediction.difficulty_prediction <= 10
        assert prediction.competition_level in ["Baixa", "Média", "Alta", "Muito Alta"]
        assert isinstance(prediction.strategic_recommendations, list)
        assert isinstance(prediction.study_priority, dict)
        assert 0 <= prediction.confidence_score <= 100
        
        # Verificar tópicos preditos
        assert len(prediction.predicted_topics) > 0
        for topic in prediction.predicted_topics:
            assert isinstance(topic, TopicTrend)
        
        # Verificar recomendações
        assert len(prediction.strategic_recommendations) > 0
        
        print(f"✅ Tópicos preditos: {len(prediction.predicted_topics)}")
        print(f"✅ Matérias quentes: {len(prediction.hot_subjects)}")
        print(f"✅ Dificuldade prevista: {prediction.difficulty_prediction:.1f}/10")
        print(f"✅ Competição: {prediction.competition_level}")
        print(f"✅ Confiança: {prediction.confidence_score:.0f}%")
        print(f"✅ Recomendações: {len(prediction.strategic_recommendations)}")
        
        return True
    
    def test_study_calendar_generation(self):
        """Testa geração de calendário de estudos"""
        print("\n📅 TESTE: Geração de Calendário")
        
        # Analisar tendências e fazer predição
        self.analyzer.analyze_topic_trends()
        prediction = self.analyzer.predict_contest_trends(
            contest_type="Concurso Teste",
            area=ContestArea.JUDICIARIO,
            level=ContestLevel.SUPERIOR,
            positions=100,
            candidates=2000
        )
        
        # Gerar calendário
        calendar = self.analyzer.generate_study_calendar(prediction, study_weeks=8)
        
        # Verificar estrutura do calendário
        assert isinstance(calendar, dict)
        assert len(calendar) == 8  # 8 semanas
        
        # Verificar semanas
        for week in range(1, 9):
            week_key = f"Semana {week}"
            assert week_key in calendar
            assert isinstance(calendar[week_key], list)
        
        # Verificar estrutura dos tópicos
        total_topics = 0
        total_hours = 0
        
        for week_key, topics in calendar.items():
            for topic in topics:
                assert 'topic' in topic
                assert 'subject' in topic
                assert 'hours' in topic
                assert 'priority' in topic
                assert 'trend' in topic
                assert 'activities' in topic
                
                assert topic['hours'] > 0
                assert 0 <= topic['priority'] <= 1
                assert isinstance(topic['activities'], list)
                
                total_topics += 1
                total_hours += topic['hours']
        
        print(f"✅ Semanas geradas: {len(calendar)}")
        print(f"✅ Total de tópicos: {total_topics}")
        print(f"✅ Total de horas: {total_hours}h")
        print(f"✅ Média por semana: {total_hours/len(calendar):.1f}h")
        
        return True
    
    def test_report_generation(self):
        """Testa geração de relatório"""
        print("\n📄 TESTE: Geração de Relatório")
        
        # Analisar tendências primeiro
        self.analyzer.analyze_topic_trends()
        
        # Gerar relatório
        report = self.analyzer.export_trends_report()
        
        # Verificar que relatório foi gerado
        assert isinstance(report, str)
        assert len(report) > 0
        
        # Verificar seções do relatório
        expected_sections = [
            "RELATÓRIO DE TENDÊNCIAS DE CONCURSOS",
            "TENDÊNCIAS POR TIPO",
            "TÓPICOS EMERGENTES",
            "TÓPICOS EM CRESCIMENTO"
        ]
        
        sections_found = 0
        for section in expected_sections:
            if section in report:
                sections_found += 1
        
        assert sections_found >= 2  # Pelo menos 2 seções
        
        print(f"✅ Relatório gerado: {len(report)} caracteres")
        print(f"✅ Seções encontradas: {sections_found}/{len(expected_sections)}")
        
        return True
    
    def test_example_data_generation(self):
        """Testa geração de dados de exemplo"""
        print("\n🎲 TESTE: Dados de Exemplo")
        
        example_contests = generate_example_contests()
        
        # Verificar que dados foram gerados
        assert isinstance(example_contests, list)
        assert len(example_contests) > 0
        
        # Verificar estrutura dos concursos
        for contest in example_contests[:3]:  # Verificar apenas os primeiros 3
            assert isinstance(contest, HistoricalContest)
            assert hasattr(contest, 'contest_id')
            assert hasattr(contest, 'name')
            assert hasattr(contest, 'year')
            assert hasattr(contest, 'level')
            assert hasattr(contest, 'area')
            assert hasattr(contest, 'subjects')
            assert hasattr(contest, 'topics')
            
            # Verificar valores válidos
            assert contest.year >= 2019
            assert isinstance(contest.level, ContestLevel)
            assert isinstance(contest.area, ContestArea)
            assert len(contest.subjects) > 0
            assert len(contest.topics) > 0
            assert contest.positions > 0
            assert contest.candidates > 0
        
        print(f"✅ Concursos de exemplo: {len(example_contests)}")
        print(f"✅ Estrutura validada: ✓")
        
        return True
    
    def test_integration_workflow(self):
        """Testa fluxo completo de integração"""
        print("\n🔄 TESTE: Fluxo de Integração Completo")
        
        # 1. Carregar dados
        analyzer = ContestTrendsAnalyzer()
        contests = generate_example_contests()
        analyzer.load_historical_data(contests)
        
        # 2. Analisar tendências
        trends = analyzer.analyze_topic_trends()
        
        # 3. Fazer predição
        prediction = analyzer.predict_contest_trends(
            contest_type="Teste Integração",
            area=ContestArea.JUDICIARIO,
            level=ContestLevel.SUPERIOR,
            positions=150,
            candidates=3000
        )
        
        # 4. Gerar calendário
        calendar = analyzer.generate_study_calendar(prediction, study_weeks=6)
        
        # 5. Gerar relatório
        report = analyzer.export_trends_report()
        
        # Verificar que tudo funcionou
        assert len(trends) > 0
        assert len(prediction.predicted_topics) > 0
        assert len(calendar) == 6
        assert len(report) > 0
        
        print(f"✅ Dados carregados: {len(contests)} concursos")
        print(f"✅ Tendências analisadas: {len(trends)}")
        print(f"✅ Predição gerada: {len(prediction.predicted_topics)} tópicos")
        print(f"✅ Calendário criado: {len(calendar)} semanas")
        print(f"✅ Relatório exportado: {len(report)} caracteres")
        
        return True

def run_contest_trends_tests():
    """Executa todos os testes de predição de tendências"""
    print("🔮 INICIANDO TESTES DE PREDIÇÃO DE TENDÊNCIAS")
    print("=" * 60)
    
    test_instance = TestContestTrends()
    test_instance.setup_method()
    
    tests = [
        ("Carregamento de Dados", test_instance.test_data_loading),
        ("Treinamento de Modelos", test_instance.test_model_training),
        ("Análise de Tendências", test_instance.test_topic_trends_analysis),
        ("Predição de Concurso", test_instance.test_contest_prediction),
        ("Calendário de Estudos", test_instance.test_study_calendar_generation),
        ("Geração de Relatório", test_instance.test_report_generation),
        ("Dados de Exemplo", test_instance.test_example_data_generation),
        ("Fluxo de Integração", test_instance.test_integration_workflow)
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
        print("\n🎉 TODOS OS TESTES DE PREDIÇÃO DE TENDÊNCIAS PASSARAM!")
        print("✅ Sistema de predição funcionando perfeitamente")
        print("✅ Modelos de Machine Learning operacionais")
        print("✅ Análise de tendências implementada")
        print("✅ Calendário de estudos personalizado")
        print("✅ Relatórios completos sendo gerados")
        print("✅ Integração com interface pronta")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam. Revisar implementação.")
    
    return passed == total

if __name__ == "__main__":
    success = run_contest_trends_tests()
    exit(0 if success else 1)
