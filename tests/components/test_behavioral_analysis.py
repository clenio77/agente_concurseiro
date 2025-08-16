"""
🧪 Testes para Behavioral Analysis - Análise Comportamental
Validação completa do componente de análise comportamental
"""

import pytest
import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from app.components.behavioral_analysis import (
    BehavioralAnalysis,
    BehaviorPattern,
    AttentionLevel,
    FatigueLevel,
    StudyEnvironment
)

class TestBehavioralAnalysis:
    """Testes para o componente Behavioral Analysis"""
    
    def setup_method(self):
        """Setup para cada teste"""
        # Limpar session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        
        self.behavioral_analysis = BehavioralAnalysis()
    
    def test_behavioral_analysis_initialization(self):
        """Testar inicialização da análise comportamental"""
        assert self.behavioral_analysis is not None
        assert 'behavioral_settings' in st.session_state
        assert 'behavioral_data' in st.session_state
        assert 'study_sessions' in st.session_state
        assert 'behavioral_insights' in st.session_state
        assert 'recommendations' in st.session_state
    
    def test_behavioral_settings_default_values(self):
        """Testar valores padrão das configurações"""
        settings = st.session_state.behavioral_settings
        
        assert settings['tracking_enabled'] == True
        assert settings['webcam_analysis'] == False
        assert settings['privacy_mode'] == True
        assert settings['data_retention_days'] == 30
        assert settings['analysis_frequency'] == 'real_time'
        assert settings['notification_threshold'] == 0.7
        assert settings['auto_recommendations'] == True
        assert settings['share_anonymous_data'] == False
    
    def test_behavioral_data_structure(self):
        """Testar estrutura dos dados comportamentais"""
        data = st.session_state.behavioral_data
        
        # Verificar campos obrigatórios
        required_fields = [
            'daily_patterns', 'attention_tracking', 'fatigue_analysis',
            'environment_preferences', 'performance_correlation'
        ]
        
        for field in required_fields:
            assert field in data
            assert isinstance(data[field], list)
        
        # Verificar dados diários (aproximadamente 30 dias)
        assert 30 <= len(data['daily_patterns']) <= 31  # Pode variar por 1 dia devido ao range
        
        # Verificar estrutura dos padrões diários
        daily_pattern = data['daily_patterns'][0]
        required_daily_fields = [
            'date', 'study_hours', 'focus_score', 'break_frequency',
            'peak_performance_hour', 'distraction_count', 'completion_rate'
        ]
        
        for field in required_daily_fields:
            assert field in daily_pattern
        
        # Verificar dados de atenção (18 horas: 6h às 23h)
        assert len(data['attention_tracking']) == 18
        
        # Verificar estrutura de atenção
        attention_entry = data['attention_tracking'][0]
        assert 'hour' in attention_entry
        assert 'attention_level' in attention_entry
        assert 'sample_count' in attention_entry
        assert 'confidence' in attention_entry
    
    def test_study_sessions_generation(self):
        """Testar geração de sessões de estudo"""
        sessions = st.session_state.study_sessions
        
        assert len(sessions) == 50
        
        # Verificar estrutura das sessões
        session = sessions[0]
        required_session_fields = [
            'id', 'start_time', 'duration_minutes', 'subject', 'environment',
            'initial_attention', 'final_attention', 'break_count',
            'distraction_events', 'completion_rate', 'self_reported_focus',
            'fatigue_level', 'performance_score'
        ]
        
        for field in required_session_fields:
            assert field in session
        
        # Verificar tipos de dados
        assert isinstance(session['duration_minutes'], int)
        assert 0.0 <= session['initial_attention'] <= 1.0
        assert 0.0 <= session['final_attention'] <= 1.0
        assert 0.0 <= session['completion_rate'] <= 1.0
        assert 1 <= session['self_reported_focus'] <= 5
        assert session['fatigue_level'] in [level.value for level in FatigueLevel]
        assert session['environment'] in [env.value for env in StudyEnvironment]
        
        # Verificar ordenação por data (mais recente primeiro)
        timestamps = [datetime.fromisoformat(s['start_time']) for s in sessions]
        assert timestamps == sorted(timestamps, reverse=True)
    
    def test_behavioral_insights_structure(self):
        """Testar estrutura dos insights comportamentais"""
        insights = st.session_state.behavioral_insights
        
        # Verificar campos obrigatórios
        required_fields = [
            'dominant_pattern', 'pattern_confidence', 'optimal_study_hours',
            'peak_performance_day', 'average_focus_duration', 'distraction_triggers',
            'learning_efficiency', 'break_optimization', 'environment_ranking',
            'weekly_patterns'
        ]
        
        for field in required_fields:
            assert field in insights
        
        # Verificar tipos específicos
        assert insights['dominant_pattern'] in [pattern.value for pattern in BehaviorPattern]
        assert 0.0 <= insights['pattern_confidence'] <= 1.0
        assert isinstance(insights['optimal_study_hours'], list)
        assert len(insights['optimal_study_hours']) == 3
        assert isinstance(insights['average_focus_duration'], int)
        
        # Verificar triggers de distração
        triggers = insights['distraction_triggers']
        assert len(triggers) == 4
        for trigger in triggers:
            assert 'trigger' in trigger
            assert 'frequency' in trigger
            assert 'impact' in trigger
            assert 0.0 <= trigger['frequency'] <= 1.0
            assert 0.0 <= trigger['impact'] <= 1.0
        
        # Verificar eficiência de aprendizado
        efficiency = insights['learning_efficiency']
        periods = ['morning', 'afternoon', 'evening', 'night']
        for period in periods:
            assert period in efficiency
            assert 0.0 <= efficiency[period] <= 1.0
        
        # Verificar padrões semanais
        weekly = insights['weekly_patterns']
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        for day in days:
            assert day in weekly
            assert 'energy' in weekly[day]
            assert 'focus' in weekly[day]
            assert 'productivity' in weekly[day]
    
    def test_recommendations_generation(self):
        """Testar geração de recomendações"""
        recommendations = st.session_state.recommendations
        
        assert len(recommendations) == 5
        
        # Verificar estrutura das recomendações
        rec = recommendations[0]
        required_rec_fields = [
            'id', 'type', 'priority', 'title', 'description', 'action',
            'expected_improvement', 'confidence', 'implementation_difficulty'
        ]
        
        for field in required_rec_fields:
            assert field in rec
        
        # Verificar valores válidos
        assert rec['priority'] in ['high', 'medium', 'low']
        assert rec['type'] in ['schedule', 'technique', 'environment', 'health']
        assert rec['implementation_difficulty'] in ['easy', 'medium', 'hard']
        assert 0.0 <= rec['confidence'] <= 1.0
        
        # Verificar que há pelo menos uma recomendação de alta prioridade
        high_priority_recs = [r for r in recommendations if r['priority'] == 'high']
        assert len(high_priority_recs) >= 1
    
    def test_attention_calculation_by_hour(self):
        """Testar cálculo de atenção por hora"""
        # Testar diferentes horas do dia
        test_hours = [6, 9, 12, 15, 18, 21]
        
        for hour in test_hours:
            attention = self.behavioral_analysis._calculate_attention_by_hour(hour)
            assert 0.0 <= attention <= 1.0
        
        # Verificar que o pico matinal (9-12h) tem atenção alta
        morning_peak = [
            self.behavioral_analysis._calculate_attention_by_hour(h) 
            for h in [9, 10, 11]
        ]
        assert all(attention >= 0.8 for attention in morning_peak)
        
        # Verificar que a madrugada tem atenção baixa
        late_night = self.behavioral_analysis._calculate_attention_by_hour(23)
        assert late_night <= 0.5
    
    def test_current_session_analysis(self):
        """Testar análise de sessão atual"""
        current_session = self.behavioral_analysis.analyze_current_session()
        
        # Verificar campos obrigatórios
        required_fields = [
            'session_id', 'start_time', 'duration_minutes', 'current_attention',
            'attention_trend', 'distraction_count', 'estimated_fatigue',
            'recommended_action', 'performance_prediction'
        ]
        
        for field in required_fields:
            assert field in current_session
        
        # Verificar tipos e ranges
        assert isinstance(current_session['duration_minutes'], int)
        assert 15 <= current_session['duration_minutes'] <= 120
        assert 0.0 <= current_session['current_attention'] <= 1.0
        assert current_session['attention_trend'] in ['increasing', 'stable', 'decreasing']
        assert current_session['distraction_count'] >= 0
        assert 0.0 <= current_session['estimated_fatigue'] <= 1.0
        assert 0.0 <= current_session['performance_prediction'] <= 1.0
        
        # Verificar timestamp válido
        datetime.fromisoformat(current_session['start_time'])
    
    def test_behavior_pattern_enum(self):
        """Testar enum de padrões comportamentais"""
        assert BehaviorPattern.FOCUSED_LEARNER.value == "focused_learner"
        assert BehaviorPattern.DISTRACTED_STUDENT.value == "distracted_student"
        assert BehaviorPattern.NIGHT_OWL.value == "night_owl"
        assert BehaviorPattern.MORNING_PERSON.value == "morning_person"
        assert BehaviorPattern.PROCRASTINATOR.value == "procrastinator"
        assert BehaviorPattern.CONSISTENT_STUDIER.value == "consistent_studier"
    
    def test_attention_level_enum(self):
        """Testar enum de níveis de atenção"""
        assert AttentionLevel.VERY_LOW.value == "very_low"
        assert AttentionLevel.LOW.value == "low"
        assert AttentionLevel.MEDIUM.value == "medium"
        assert AttentionLevel.HIGH.value == "high"
        assert AttentionLevel.VERY_HIGH.value == "very_high"
    
    def test_fatigue_level_enum(self):
        """Testar enum de níveis de fadiga"""
        assert FatigueLevel.FRESH.value == "fresh"
        assert FatigueLevel.SLIGHTLY_TIRED.value == "slightly_tired"
        assert FatigueLevel.MODERATELY_TIRED.value == "moderately_tired"
        assert FatigueLevel.VERY_TIRED.value == "very_tired"
        assert FatigueLevel.EXHAUSTED.value == "exhausted"
    
    def test_study_environment_enum(self):
        """Testar enum de ambientes de estudo"""
        assert StudyEnvironment.QUIET_ROOM.value == "quiet_room"
        assert StudyEnvironment.LIBRARY.value == "library"
        assert StudyEnvironment.COFFEE_SHOP.value == "coffee_shop"
        assert StudyEnvironment.HOME_OFFICE.value == "home_office"
        assert StudyEnvironment.OUTDOOR.value == "outdoor"
    
    def test_data_consistency(self):
        """Testar consistência dos dados gerados"""
        data = st.session_state.behavioral_data
        insights = st.session_state.behavioral_insights
        
        # Verificar que os dados de atenção cobrem o período correto
        attention_hours = [entry['hour'] for entry in data['attention_tracking']]
        assert min(attention_hours) == 6
        assert max(attention_hours) == 23
        assert len(set(attention_hours)) == 18  # Sem duplicatas
        
        # Verificar que as preferências de ambiente somam aproximadamente 1
        env_prefs = data['environment_preferences']
        total_usage = sum(env['usage_frequency'] for env in env_prefs)
        assert 0.8 <= total_usage <= 1.5  # Permitir variação maior para dados simulados
        
        # Verificar que os padrões semanais têm 7 dias
        weekly_patterns = insights['weekly_patterns']
        assert len(weekly_patterns) == 7
        
        # Verificar que todas as métricas semanais estão no range válido
        for day_data in weekly_patterns.values():
            assert 0.0 <= day_data['energy'] <= 1.0
            assert 0.0 <= day_data['focus'] <= 1.0
            assert 0.0 <= day_data['productivity'] <= 1.0
    
    def test_recommendations_prioritization(self):
        """Testar priorização das recomendações"""
        recommendations = st.session_state.recommendations
        
        # Contar recomendações por prioridade
        priority_counts = {}
        for rec in recommendations:
            priority = rec['priority']
            priority_counts[priority] = priority_counts.get(priority, 0) + 1
        
        # Verificar que há recomendações de diferentes prioridades
        assert 'high' in priority_counts
        assert priority_counts['high'] >= 1
        
        # Verificar que recomendações de alta prioridade têm alta confiança
        high_priority_recs = [r for r in recommendations if r['priority'] == 'high']
        for rec in high_priority_recs:
            assert rec['confidence'] >= 0.7  # Alta confiança para alta prioridade

def test_behavioral_analysis_component():
    """Teste de integração do componente"""
    # Limpar session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Testar inicialização
    behavioral_analysis = BehavioralAnalysis()
    assert behavioral_analysis is not None
    
    # Testar session state
    assert 'behavioral_settings' in st.session_state
    assert 'behavioral_data' in st.session_state
    assert 'study_sessions' in st.session_state
    assert 'behavioral_insights' in st.session_state
    assert 'recommendations' in st.session_state

def test_data_generation_consistency():
    """Testar consistência na geração de dados"""
    # Limpar session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    # Criar múltiplas instâncias e verificar consistência
    ba1 = BehavioralAnalysis()
    data1 = st.session_state.behavioral_data
    
    # Limpar e criar novamente
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    
    ba2 = BehavioralAnalysis()
    data2 = st.session_state.behavioral_data
    
    # Verificar que a estrutura é consistente
    assert len(data1['daily_patterns']) == len(data2['daily_patterns'])
    assert len(data1['attention_tracking']) == len(data2['attention_tracking'])
    assert len(data1['fatigue_analysis']) == len(data2['fatigue_analysis'])

if __name__ == "__main__":
    # Executar testes
    pytest.main([__file__, "-v"])