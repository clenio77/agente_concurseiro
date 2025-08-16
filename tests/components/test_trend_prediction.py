"""
🧪 Testes para Trend Prediction - Predição de Tendências
Validação completa do componente de predição de tendências
"""

import pytest
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from app.components.trend_prediction import (
    TrendPrediction,
    TrendType,
    PredictionConfidence,
    ExamBoard,
    SubjectArea
)

class TestTrendPrediction:
    """Testes para o componente Trend Prediction"""
    
    def setup_method(self):
        """Setup para cada teste"""
        # Limpar session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        self.trend_prediction = TrendPrediction()
    
    def test_trend_prediction_initialization(self):
        """Testar inicialização da predição de tendências"""
        assert self.trend_prediction is not None
        assert 'trend_settings' in st.session_state
        assert 'historical_data' in st.session_state
        assert 'trend_analysis' in st.session_state
        assert 'predictions' in st.session_state
        assert 'market_intelligence' in st.session_state
    
    def test_trend_settings_default_values(self):
        """Testar valores padrão das configurações"""
        settings = st.session_state.trend_settings
        
        assert settings['analysis_enabled'] == True
        assert settings['prediction_horizon'] == 12
        assert settings['confidence_threshold'] == 0.7
        assert settings['include_seasonal'] == True
        assert settings['include_legislation'] == True
        assert settings['include_jurisprudence'] == False
        assert settings['auto_update'] == True
        assert settings['notification_alerts'] == True
        assert 'official_sites' in settings['data_sources']
    
    def test_historical_data_structure(self):
        """Testar estrutura dos dados históricos"""
        data = st.session_state.historical_data
        
        # Verificar campos obrigatórios
        required_fields = [
            'exam_frequency', 'topic_evolution', 'board_patterns',
            'seasonal_trends', 'legislation_impact'
        ]
        
        for field in required_fields:
            assert field in data
            assert isinstance(data[field], list)
        
        # Verificar frequência de exames (aproximadamente 5 anos de dados mensais)
        exam_freq = data['exam_frequency']
        assert 55 <= len(exam_freq) <= 65  # ~60 meses ± variação
        
        # Verificar estrutura da frequência de exames
        if exam_freq:
            exam_entry = exam_freq[0]
            required_exam_fields = [
                'date', 'total_exams', 'federal_exams', 'state_exams',
                'municipal_exams', 'average_positions'
            ]
            
            for field in required_exam_fields:
                assert field in exam_entry
        
        # Verificar evolução de tópicos
        topic_evolution = data['topic_evolution']
        assert len(topic_evolution) > 0
        
        if topic_evolution:
            topic_entry = topic_evolution[0]
            assert 'subject' in topic_entry
            assert 'topic' in topic_entry
            assert 'trend_data' in topic_entry
            assert 'overall_trend' in topic_entry
            assert 'trend_strength' in topic_entry
            
            # Verificar dados de tendência
            trend_data = topic_entry['trend_data']
            assert len(trend_data) == 24  # 2 anos de dados mensais
        
        # Verificar padrões das bancas
        board_patterns = data['board_patterns']
        assert len(board_patterns) == len(list(ExamBoard))
        
        # Verificar tendências sazonais (12 meses)
        seasonal_trends = data['seasonal_trends']
        assert len(seasonal_trends) == 12
        
        # Verificar impacto legislativo
        legislation_impact = data['legislation_impact']
        assert len(legislation_impact) >= 3  # Pelo menos algumas mudanças
    
    def test_trend_analysis_structure(self):
        """Testar estrutura da análise de tendências"""
        analysis = st.session_state.trend_analysis
        
        # Verificar campos obrigatórios
        required_fields = [
            'hot_topics', 'declining_topics', 'seasonal_predictions',
            'board_innovations'
        ]
        
        for field in required_fields:
            assert field in analysis
        
        # Verificar tópicos quentes
        hot_topics = analysis['hot_topics']
        assert len(hot_topics) >= 3
        
        for topic in hot_topics:
            required_topic_fields = [
                'topic', 'subject', 'growth_rate', 'confidence',
                'predicted_questions', 'boards_adopting', 'trend_type'
            ]
            
            for field in required_topic_fields:
                assert field in topic
            
            # Verificar ranges válidos
            assert 0.0 <= topic['growth_rate'] <= 2.0
            assert 0.0 <= topic['confidence'] <= 1.0
            assert topic['predicted_questions'] > 0
            assert topic['trend_type'] in [t.value for t in TrendType]
        
        # Verificar tópicos em declínio
        declining_topics = analysis['declining_topics']
        assert len(declining_topics) >= 1
        
        for topic in declining_topics:
            assert 'topic' in topic
            assert 'subject' in topic
            assert 'decline_rate' in topic
            assert 'confidence' in topic
            assert 'reason' in topic
            assert topic['decline_rate'] < 0  # Deve ser negativo
        
        # Verificar predições sazonais
        seasonal_predictions = analysis['seasonal_predictions']
        quarters = ['Q1_2025', 'Q2_2025', 'Q3_2025', 'Q4_2025']
        
        for quarter in quarters:
            assert quarter in seasonal_predictions
            quarter_data = seasonal_predictions[quarter]
            assert 'peak_subjects' in quarter_data
            assert 'exam_volume' in quarter_data
            assert 'competition_level' in quarter_data
        
        # Verificar inovações das bancas
        board_innovations = analysis['board_innovations']
        assert len(board_innovations) >= 2
        
        for innovation in board_innovations:
            assert 'board' in innovation
            assert 'innovation' in innovation
            assert 'adoption_probability' in innovation
            assert 'impact_level' in innovation
            assert 0.0 <= innovation['adoption_probability'] <= 1.0
    
    def test_predictions_structure(self):
        """Testar estrutura das predições"""
        predictions = st.session_state.predictions
        
        assert len(predictions) >= 3
        
        for pred in predictions:
            required_pred_fields = [
                'id', 'title', 'description', 'probability', 'confidence',
                'time_horizon', 'impact_level', 'affected_subjects',
                'recommended_action', 'supporting_evidence', 'trend_type'
            ]
            
            for field in required_pred_fields:
                assert field in pred
            
            # Verificar tipos e ranges
            assert 0.0 <= pred['probability'] <= 1.0
            assert pred['confidence'] in [c.value for c in PredictionConfidence]
            assert pred['impact_level'] in ['Muito Alto', 'Alto', 'Médio', 'Baixo']
            assert pred['trend_type'] in [t.value for t in TrendType]
            assert isinstance(pred['affected_subjects'], list)
            assert isinstance(pred['supporting_evidence'], list)
            assert len(pred['supporting_evidence']) >= 2
    
    def test_market_intelligence_structure(self):
        """Testar estrutura da inteligência de mercado"""
        market = st.session_state.market_intelligence
        
        # Verificar campos obrigatórios
        required_fields = [
            'market_overview', 'board_market_share', 'emerging_opportunities',
            'regional_analysis', 'success_factors'
        ]
        
        for field in required_fields:
            assert field in market
        
        # Verificar overview do mercado
        overview = market['market_overview']
        required_overview_fields = [
            'total_positions_2024', 'growth_vs_2023', 'average_salary',
            'competition_ratio', 'most_competitive_areas'
        ]
        
        for field in required_overview_fields:
            assert field in overview
        
        assert overview['total_positions_2024'] > 0
        assert isinstance(overview['average_salary'], float)
        assert overview['competition_ratio'] > 0
        
        # Verificar market share das bancas
        board_share = market['board_market_share']
        total_share = sum(data['share'] for data in board_share.values())
        assert 0.95 <= total_share <= 1.05  # Deve somar aproximadamente 1
        
        # Verificar oportunidades emergentes
        opportunities = market['emerging_opportunities']
        assert len(opportunities) >= 2
        
        for opp in opportunities:
            assert 'area' in opp
            assert 'growth_rate' in opp
            assert 'avg_salary' in opp
            assert 'positions_forecast' in opp
            assert 'key_skills' in opp
            assert opp['growth_rate'] > 0
            assert opp['avg_salary'] > 0
            assert opp['positions_forecast'] > 0
        
        # Verificar análise regional
        regional = market['regional_analysis']
        regions = ['Southeast', 'South', 'Northeast', 'North', 'Center-West']
        
        for region in regions:
            assert region in regional
            region_data = regional[region]
            assert 'positions' in region_data
            assert 'competition' in region_data
            assert 'salary_avg' in region_data
        
        # Verificar fatores de sucesso
        success_factors = market['success_factors']
        assert len(success_factors) >= 3
        
        for factor in success_factors:
            assert 'factor' in factor
            assert 'impact' in factor
            assert 0.0 <= factor['impact'] <= 1.0
    
    def test_trend_type_enum(self):
        """Testar enum de tipos de tendência"""
        assert TrendType.TOPIC_FREQUENCY.value == "topic_frequency"
        assert TrendType.SEASONAL_PATTERN.value == "seasonal_pattern"
        assert TrendType.BOARD_PREFERENCE.value == "board_preference"
        assert TrendType.LEGISLATION_CHANGE.value == "legislation_change"
        assert TrendType.JURISPRUDENCE_SHIFT.value == "jurisprudence_shift"
    
    def test_prediction_confidence_enum(self):
        """Testar enum de confiança da predição"""
        assert PredictionConfidence.VERY_LOW.value == "very_low"
        assert PredictionConfidence.LOW.value == "low"
        assert PredictionConfidence.MEDIUM.value == "medium"
        assert PredictionConfidence.HIGH.value == "high"
        assert PredictionConfidence.VERY_HIGH.value == "very_high"
    
    def test_exam_board_enum(self):
        """Testar enum de bancas"""
        assert ExamBoard.CESPE.value == "cespe"
        assert ExamBoard.FCC.value == "fcc"
        assert ExamBoard.VUNESP.value == "vunesp"
        assert ExamBoard.FGV.value == "fgv"
        assert ExamBoard.IBFC.value == "ibfc"
        assert ExamBoard.CONSULPLAN.value == "consulplan"
        assert ExamBoard.QUADRIX.value == "quadrix"
    
    def test_subject_area_enum(self):
        """Testar enum de áreas de conhecimento"""
        assert SubjectArea.PORTUGUESE.value == "portuguese"
        assert SubjectArea.MATHEMATICS.value == "mathematics"
        assert SubjectArea.LAW.value == "law"
        assert SubjectArea.INFORMATICS.value == "informatics"
        assert SubjectArea.CURRENT_AFFAIRS.value == "current_affairs"
        assert SubjectArea.ADMINISTRATION.value == "administration"
        assert SubjectArea.ACCOUNTING.value == "accounting"
    
    def test_data_consistency(self):
        """Testar consistência dos dados gerados"""
        data = st.session_state.historical_data
        analysis = st.session_state.trend_analysis
        predictions = st.session_state.predictions
        
        # Verificar que há pelo menos um tópico quente para cada predição de alta confiança
        high_confidence_predictions = [
            p for p in predictions 
            if p['confidence'] in ['high', 'very_high']
        ]
        assert len(high_confidence_predictions) >= 2
        
        # Verificar que tópicos em declínio têm taxa negativa
        declining_topics = analysis['declining_topics']
        for topic in declining_topics:
            assert topic['decline_rate'] < 0
        
        # Verificar que dados históricos têm datas válidas
        exam_freq = data['exam_frequency']
        if exam_freq:
            dates = [datetime.strptime(entry['date'], '%Y-%m') for entry in exam_freq]
            assert dates == sorted(dates)  # Datas em ordem cronológica
        
        # Verificar que market share das bancas é realístico
        market = st.session_state.market_intelligence
        board_shares = market['board_market_share']
        
        # CESPE deve ter uma das maiores participações
        cespe_share = board_shares.get('CESPE', {}).get('share', 0)
        assert cespe_share >= 0.2  # Pelo menos 20%
    
    def test_prediction_quality(self):
        """Testar qualidade das predições"""
        predictions = st.session_state.predictions
        
        # Verificar que predições de alta probabilidade têm alta confiança
        for pred in predictions:
            if pred['probability'] >= 0.9:
                assert pred['confidence'] in ['high', 'very_high']
            
            if pred['probability'] <= 0.3:
                assert pred['confidence'] in ['low', 'very_low']
        
        # Verificar que predições têm evidências suficientes
        for pred in predictions:
            assert len(pred['supporting_evidence']) >= 2
            assert len(pred['affected_subjects']) >= 1
            assert len(pred['recommended_action']) > 20  # Ação detalhada
    
    def test_seasonal_patterns(self):
        """Testar padrões sazonais"""
        data = st.session_state.historical_data
        seasonal_trends = data['seasonal_trends']
        
        # Verificar que há dados para todos os 12 meses
        months = [trend['month'] for trend in seasonal_trends]
        expected_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        for month in expected_months:
            assert month in months
        
        # Verificar que métricas sazonais estão em ranges válidos
        for trend in seasonal_trends:
            assert 0.1 <= trend['exam_frequency'] <= 2.0
            assert 0.1 <= trend['application_volume'] <= 2.0
            assert 0.1 <= trend['competition_intensity'] <= 2.0
            assert 0.01 <= trend['success_rate'] <= 0.5
    
    def test_board_patterns_analysis(self):
        """Testar análise de padrões das bancas"""
        data = st.session_state.historical_data
        board_patterns = data['board_patterns']
        
        # Verificar que há dados para todas as bancas principais
        board_names = [pattern['board'] for pattern in board_patterns]
        main_boards = ['cespe', 'fcc', 'vunesp', 'fgv', 'ibfc']
        
        for board in main_boards:
            assert board in board_names
        
        # Verificar estrutura dos padrões
        for pattern in board_patterns:
            assert 'subject_preferences' in pattern
            assert 'innovation_score' in pattern
            assert 'difficulty_consistency' in pattern
            
            # Verificar ranges
            assert 0.0 <= pattern['innovation_score'] <= 1.0
            assert 0.0 <= pattern['difficulty_consistency'] <= 1.0
            
            # Verificar preferências por matéria
            preferences = pattern['subject_preferences']
            for subject_pref in preferences.values():
                assert 'frequency' in subject_pref
                assert 'difficulty_preference' in subject_pref
                assert 'question_style' in subject_pref
                assert 'trend' in subject_pref

def test_trend_prediction_component():
    """Teste de integração do componente"""
    # Limpar session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Testar inicialização
    trend_prediction = TrendPrediction()
    assert trend_prediction is not None
    
    # Testar session state
    assert 'trend_settings' in st.session_state
    assert 'historical_data' in st.session_state
    assert 'trend_analysis' in st.session_state
    assert 'predictions' in st.session_state
    assert 'market_intelligence' in st.session_state

def test_data_generation_performance():
    """Testar performance da geração de dados"""
    import time
    
    # Limpar session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Medir tempo de inicialização
    start_time = time.time()
    trend_prediction = TrendPrediction()
    end_time = time.time()
    
    # Deve inicializar em menos de 5 segundos
    assert (end_time - start_time) < 5.0
    
    # Verificar que dados foram gerados
    assert len(st.session_state.historical_data['exam_frequency']) > 0
    assert len(st.session_state.trend_analysis['hot_topics']) > 0
    assert len(st.session_state.predictions) > 0

if __name__ == "__main__":
    # Executar testes
    pytest.main([__file__, "-v"])