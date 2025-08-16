"""
🧠 Behavioral Analysis - Análise Comportamental Avançada
Componente de análise de padrões comportamentais e otimização de estudos
"""

import streamlit as st
import json
import time
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class BehaviorPattern(Enum):
    """Padrões comportamentais identificados"""
    FOCUSED_LEARNER = "focused_learner"
    DISTRACTED_STUDENT = "distracted_student"
    NIGHT_OWL = "night_owl"
    MORNING_PERSON = "morning_person"
    PROCRASTINATOR = "procrastinator"
    CONSISTENT_STUDIER = "consistent_studier"

class AttentionLevel(Enum):
    """Níveis de atenção"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class FatigueLevel(Enum):
    """Níveis de fadiga"""
    FRESH = "fresh"
    SLIGHTLY_TIRED = "slightly_tired"
    MODERATELY_TIRED = "moderately_tired"
    VERY_TIRED = "very_tired"
    EXHAUSTED = "exhausted"

class StudyEnvironment(Enum):
    """Ambientes de estudo"""
    QUIET_ROOM = "quiet_room"
    LIBRARY = "library"
    COFFEE_SHOP = "coffee_shop"
    HOME_OFFICE = "home_office"
    OUTDOOR = "outdoor"

class BehavioralAnalysis:
    """Sistema completo de análise comportamental"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializar estado da sessão"""
        if 'behavioral_settings' not in st.session_state:
            st.session_state.behavioral_settings = {
                'tracking_enabled': True,
                'webcam_analysis': False,
                'privacy_mode': True,
                'data_retention_days': 30,
                'analysis_frequency': 'real_time',
                'notification_threshold': 0.7,
                'auto_recommendations': True,
                'share_anonymous_data': False
            }
        
        if 'behavioral_data' not in st.session_state:
            st.session_state.behavioral_data = self.generate_behavioral_data()
        
        if 'study_sessions' not in st.session_state:
            st.session_state.study_sessions = self.generate_study_sessions()
        
        if 'behavioral_insights' not in st.session_state:
            st.session_state.behavioral_insights = self.generate_behavioral_insights()
        
        if 'recommendations' not in st.session_state:
            st.session_state.recommendations = self.generate_recommendations()
    
    def generate_behavioral_data(self) -> Dict:
        """Gerar dados comportamentais simulados"""
        # Simular dados de 30 dias
        dates = pd.date_range(start='2025-07-05', end='2025-08-04', freq='D')
        
        behavioral_data = {
            'daily_patterns': [],
            'attention_tracking': [],
            'fatigue_analysis': [],
            'environment_preferences': [],
            'performance_correlation': []
        }
        
        # Gerar padrões diários
        for i, date in enumerate(dates):
            # Simular diferentes padrões ao longo do mês
            base_focus = 0.7 + 0.2 * np.sin(i * 0.2)  # Variação sazonal
            daily_noise = np.random.normal(0, 0.1)
            
            daily_pattern = {
                'date': date.strftime('%Y-%m-%d'),
                'study_hours': max(1, 8 + 2 * np.sin(i * 0.3) + np.random.normal(0, 1)),
                'focus_score': max(0.1, min(1.0, base_focus + daily_noise)),
                'break_frequency': max(1, int(6 + 3 * np.random.random())),
                'peak_performance_hour': int(9 + 6 * np.random.random()),
                'distraction_count': max(0, int(15 + 10 * np.random.random())),
                'completion_rate': max(0.3, min(1.0, base_focus + 0.1 + daily_noise))
            }
            behavioral_data['daily_patterns'].append(daily_pattern)
        
        # Gerar dados de atenção por hora
        for hour in range(6, 24):  # 6h às 23h
            attention_score = self._calculate_attention_by_hour(hour)
            behavioral_data['attention_tracking'].append({
                'hour': hour,
                'attention_level': attention_score,
                'sample_count': int(50 + 30 * np.random.random()),
                'confidence': 0.8 + 0.15 * np.random.random()
            })
        
        # Gerar análise de fadiga
        fatigue_periods = ['morning', 'afternoon', 'evening', 'night']
        for period in fatigue_periods:
            behavioral_data['fatigue_analysis'].append({
                'period': period,
                'average_fatigue': np.random.uniform(0.2, 0.8),
                'performance_impact': np.random.uniform(-0.3, 0.2),
                'recovery_time': int(15 + 30 * np.random.random())
            })
        
        # Preferências de ambiente
        environments = list(StudyEnvironment)
        for env in environments:
            behavioral_data['environment_preferences'].append({
                'environment': env.value,
                'usage_frequency': np.random.uniform(0.1, 0.4),
                'performance_score': np.random.uniform(0.6, 0.95),
                'satisfaction_rating': np.random.uniform(3.5, 5.0)
            })
        
        # Correlação performance
        subjects = ['Português', 'Matemática', 'Direito', 'Informática', 'Atualidades']
        for subject in subjects:
            behavioral_data['performance_correlation'].append({
                'subject': subject,
                'focus_correlation': np.random.uniform(0.4, 0.9),
                'time_correlation': np.random.uniform(0.2, 0.7),
                'environment_impact': np.random.uniform(0.1, 0.5),
                'optimal_duration': int(30 + 60 * np.random.random())
            })
        
        return behavioral_data
    
    def _calculate_attention_by_hour(self, hour: int) -> float:
        """Calcular nível de atenção por hora (curva realística)"""
        # Curva baseada em pesquisas de cronobiologia
        if 6 <= hour <= 9:  # Manhã - crescente
            return 0.6 + 0.3 * (hour - 6) / 3
        elif 9 <= hour <= 12:  # Pico matinal
            return 0.85 + 0.1 * np.sin((hour - 9) * np.pi / 3)
        elif 12 <= hour <= 14:  # Queda pós-almoço
            return 0.7 - 0.2 * (hour - 12) / 2
        elif 14 <= hour <= 17:  # Recuperação tarde
            return 0.5 + 0.25 * (hour - 14) / 3
        elif 17 <= hour <= 20:  # Pico vespertino
            return 0.75 + 0.15 * np.sin((hour - 17) * np.pi / 3)
        else:  # Noite - declínio
            return max(0.3, 0.8 - 0.5 * (hour - 20) / 3)
    
    def generate_study_sessions(self) -> List[Dict]:
        """Gerar sessões de estudo simuladas"""
        sessions = []
        
        for i in range(50):  # 50 sessões simuladas
            start_time = datetime.now() - timedelta(days=np.random.randint(1, 30))
            duration = int(30 + 90 * np.random.random())  # 30-120 minutos
            
            session = {
                'id': f'session_{i+1}',
                'start_time': start_time.isoformat(),
                'duration_minutes': duration,
                'subject': np.random.choice(['Português', 'Matemática', 'Direito', 'Informática']),
                'environment': np.random.choice(list(StudyEnvironment)).value,
                'initial_attention': np.random.uniform(0.4, 0.9),
                'final_attention': np.random.uniform(0.3, 0.8),
                'break_count': int(duration / 45 + np.random.randint(-1, 2)),
                'distraction_events': int(duration / 20 * np.random.uniform(0.5, 2.0)),
                'completion_rate': np.random.uniform(0.6, 1.0),
                'self_reported_focus': int(1 + 4 * np.random.random()),
                'fatigue_level': np.random.choice(list(FatigueLevel)).value,
                'performance_score': np.random.uniform(0.5, 0.95)
            }
            sessions.append(session)
        
        return sorted(sessions, key=lambda x: x['start_time'], reverse=True)
    
    def generate_behavioral_insights(self) -> Dict:
        """Gerar insights comportamentais"""
        return {
            'dominant_pattern': BehaviorPattern.FOCUSED_LEARNER.value,
            'pattern_confidence': 0.82,
            'optimal_study_hours': ['09:00-11:00', '15:00-17:00', '19:00-21:00'],
            'peak_performance_day': 'Tuesday',
            'average_focus_duration': 47,  # minutos
            'distraction_triggers': [
                {'trigger': 'Notificações do celular', 'frequency': 0.35, 'impact': 0.7},
                {'trigger': 'Ruído externo', 'frequency': 0.28, 'impact': 0.5},
                {'trigger': 'Fadiga mental', 'frequency': 0.22, 'impact': 0.8},
                {'trigger': 'Fome/sede', 'frequency': 0.15, 'impact': 0.4}
            ],
            'learning_efficiency': {
                'morning': 0.85,
                'afternoon': 0.72,
                'evening': 0.78,
                'night': 0.45
            },
            'break_optimization': {
                'recommended_frequency': 45,  # minutos
                'optimal_duration': 12,  # minutos
                'activity_suggestions': ['Caminhada', 'Hidratação', 'Respiração', 'Alongamento']
            },
            'environment_ranking': [
                {'environment': 'Biblioteca', 'score': 0.92, 'usage': 0.35},
                {'environment': 'Home Office', 'score': 0.87, 'usage': 0.45},
                {'environment': 'Sala Silenciosa', 'score': 0.89, 'usage': 0.20}
            ],
            'weekly_patterns': {
                'Monday': {'energy': 0.75, 'focus': 0.70, 'productivity': 0.72},
                'Tuesday': {'energy': 0.85, 'focus': 0.88, 'productivity': 0.90},
                'Wednesday': {'energy': 0.80, 'focus': 0.82, 'productivity': 0.85},
                'Thursday': {'energy': 0.78, 'focus': 0.80, 'productivity': 0.83},
                'Friday': {'energy': 0.70, 'focus': 0.65, 'productivity': 0.68},
                'Saturday': {'energy': 0.65, 'focus': 0.60, 'productivity': 0.62},
                'Sunday': {'energy': 0.68, 'focus': 0.63, 'productivity': 0.65}
            }
        }
    
    def generate_recommendations(self) -> List[Dict]:
        """Gerar recomendações personalizadas"""
        return [
            {
                'id': 'schedule_optimization',
                'type': 'schedule',
                'priority': 'high',
                'title': 'Otimize seu horário de estudos',
                'description': 'Seus dados mostram maior produtividade entre 9h-11h e 15h-17h.',
                'action': 'Concentre 70% dos estudos nestes períodos',
                'expected_improvement': '25%',
                'confidence': 0.87,
                'implementation_difficulty': 'medium'
            },
            {
                'id': 'break_frequency',
                'type': 'technique',
                'priority': 'high',
                'title': 'Ajuste a frequência de pausas',
                'description': 'Você mantém foco por 47 minutos em média. Pausas de 12 minutos são ideais.',
                'action': 'Use a técnica Pomodoro modificada: 45min estudo + 12min pausa',
                'expected_improvement': '18%',
                'confidence': 0.92,
                'implementation_difficulty': 'easy'
            },
            {
                'id': 'distraction_management',
                'type': 'environment',
                'priority': 'medium',
                'title': 'Gerencie distrações digitais',
                'description': 'Notificações do celular causam 35% das suas distrações.',
                'action': 'Use modo "Não Perturbe" durante estudos',
                'expected_improvement': '15%',
                'confidence': 0.78,
                'implementation_difficulty': 'easy'
            },
            {
                'id': 'environment_change',
                'type': 'environment',
                'priority': 'medium',
                'title': 'Varie o ambiente de estudo',
                'description': 'Biblioteca mostra 92% de eficiência vs 87% em casa.',
                'action': 'Estude na biblioteca 2-3x por semana',
                'expected_improvement': '12%',
                'confidence': 0.85,
                'implementation_difficulty': 'medium'
            },
            {
                'id': 'fatigue_monitoring',
                'type': 'health',
                'priority': 'low',
                'title': 'Monitore sinais de fadiga',
                'description': 'Fadiga mental reduz sua performance em 30% após 2h contínuas.',
                'action': 'Limite sessões intensas a 90 minutos',
                'expected_improvement': '20%',
                'confidence': 0.73,
                'implementation_difficulty': 'easy'
            }
        ]
    
    def analyze_current_session(self) -> Dict:
        """Analisar sessão atual (simulado)"""
        # Simular análise em tempo real
        current_time = datetime.now()
        session_duration = np.random.randint(15, 120)  # minutos
        
        return {
            'session_id': f'current_{int(current_time.timestamp())}',
            'start_time': (current_time - timedelta(minutes=session_duration)).isoformat(),
            'duration_minutes': session_duration,
            'current_attention': np.random.uniform(0.4, 0.9),
            'attention_trend': np.random.choice(['increasing', 'stable', 'decreasing']),
            'distraction_count': int(session_duration / 20 * np.random.uniform(0.5, 2.0)),
            'estimated_fatigue': np.random.uniform(0.2, 0.8),
            'recommended_action': np.random.choice([
                'Continue studying - good focus',
                'Take a 10-minute break',
                'Switch to lighter material',
                'End session - high fatigue detected'
            ]),
            'performance_prediction': np.random.uniform(0.6, 0.95)
        }
    
    def render_behavioral_dashboard(self):
        """Renderizar dashboard comportamental"""
        st.subheader("🧠 Dashboard de Análise Comportamental")
        
        insights = st.session_state.behavioral_insights
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Padrão Dominante",
                insights['dominant_pattern'].replace('_', ' ').title(),
                delta=f"{insights['pattern_confidence']:.0%} confiança"
            )
        
        with col2:
            st.metric(
                "Foco Médio",
                f"{insights['average_focus_duration']} min",
                delta="+5 min esta semana"
            )
        
        with col3:
            peak_hour = insights['optimal_study_hours'][0]
            st.metric(
                "Melhor Horário",
                peak_hour,
                delta="Pico de performance"
            )
        
        with col4:
            best_day = insights['peak_performance_day']
            st.metric(
                "Melhor Dia",
                best_day,
                delta="90% produtividade"
            )
        
        # Gráficos de análise
        col1, col2 = st.columns(2)
        
        with col1:
            # Atenção por hora do dia
            attention_data = st.session_state.behavioral_data['attention_tracking']
            df_attention = pd.DataFrame(attention_data)
            
            fig = px.line(
                df_attention,
                x='hour',
                y='attention_level',
                title='Nível de Atenção por Hora do Dia',
                markers=True
            )
            fig.update_layout(
                xaxis_title='Hora do Dia',
                yaxis_title='Nível de Atenção',
                height=350
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Performance semanal
            weekly_data = insights['weekly_patterns']
            days = list(weekly_data.keys())
            productivity = [weekly_data[day]['productivity'] for day in days]
            
            fig = px.bar(
                x=days,
                y=productivity,
                title='Produtividade por Dia da Semana',
                color=productivity,
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        # Análise de distrações
        st.subheader("🎯 Análise de Distrações")
        
        distractions = insights['distraction_triggers']
        df_distractions = pd.DataFrame(distractions)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                df_distractions,
                x='frequency',
                y='trigger',
                orientation='h',
                title='Frequência de Distrações',
                color='impact',
                color_continuous_scale='reds'
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                df_distractions,
                x='frequency',
                y='impact',
                size='frequency',
                hover_name='trigger',
                title='Impacto vs Frequência das Distrações'
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_session_analysis(self):
        """Renderizar análise de sessões"""
        st.subheader("📊 Análise de Sessões de Estudo")
        
        sessions = st.session_state.study_sessions
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            subjects = list(set([s['subject'] for s in sessions]))
            selected_subject = st.selectbox(
                "Filtrar por matéria:",
                options=['Todas'] + subjects,
                index=0
            )
        
        with col2:
            environments = list(set([s['environment'] for s in sessions]))
            selected_env = st.selectbox(
                "Filtrar por ambiente:",
                options=['Todos'] + environments,
                index=0
            )
        
        with col3:
            time_range = st.selectbox(
                "Período:",
                options=['Última semana', 'Último mês', 'Todos'],
                index=1
            )
        
        # Filtrar dados
        filtered_sessions = sessions
        if selected_subject != 'Todas':
            filtered_sessions = [s for s in filtered_sessions if s['subject'] == selected_subject]
        if selected_env != 'Todos':
            filtered_sessions = [s for s in filtered_sessions if s['environment'] == selected_env]
        
        # Estatísticas das sessões
        if filtered_sessions:
            df_sessions = pd.DataFrame(filtered_sessions)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_duration = df_sessions['duration_minutes'].mean()
                st.metric("Duração Média", f"{avg_duration:.0f} min")
            
            with col2:
                avg_attention = df_sessions['initial_attention'].mean()
                st.metric("Atenção Inicial", f"{avg_attention:.1%}")
            
            with col3:
                avg_completion = df_sessions['completion_rate'].mean()
                st.metric("Taxa de Conclusão", f"{avg_completion:.1%}")
            
            with col4:
                avg_performance = df_sessions['performance_score'].mean()
                st.metric("Performance Média", f"{avg_performance:.1%}")
            
            # Gráficos de sessões
            col1, col2 = st.columns(2)
            
            with col1:
                # Duração vs Performance
                fig = px.scatter(
                    df_sessions,
                    x='duration_minutes',
                    y='performance_score',
                    color='subject',
                    size='completion_rate',
                    title='Duração vs Performance das Sessões',
                    hover_data=['environment', 'break_count']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Atenção inicial vs final
                fig = px.scatter(
                    df_sessions,
                    x='initial_attention',
                    y='final_attention',
                    color='fatigue_level',
                    title='Atenção: Inicial vs Final',
                    hover_data=['duration_minutes', 'subject']
                )
                fig.add_shape(
                    type="line",
                    x0=0, y0=0, x1=1, y1=1,
                    line=dict(dash="dash", color="gray")
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
            
            # Tabela de sessões recentes
            st.subheader("📋 Sessões Recentes")
            
            # Preparar dados para exibição
            display_sessions = df_sessions.head(10).copy()
            display_sessions['start_time'] = pd.to_datetime(display_sessions['start_time']).dt.strftime('%d/%m %H:%M')
            display_sessions['duration'] = display_sessions['duration_minutes'].astype(str) + ' min'
            display_sessions['attention'] = (display_sessions['initial_attention'] * 100).round(0).astype(str) + '%'
            display_sessions['performance'] = (display_sessions['performance_score'] * 100).round(0).astype(str) + '%'
            
            st.dataframe(
                display_sessions[['start_time', 'subject', 'duration', 'attention', 'performance', 'environment']],
                column_config={
                    'start_time': 'Início',
                    'subject': 'Matéria',
                    'duration': 'Duração',
                    'attention': 'Atenção',
                    'performance': 'Performance',
                    'environment': 'Ambiente'
                },
                use_container_width=True
            )
        else:
            st.info("Nenhuma sessão encontrada com os filtros selecionados.")
    
    def render_recommendations(self):
        """Renderizar recomendações personalizadas"""
        st.subheader("💡 Recomendações Personalizadas")
        
        recommendations = st.session_state.recommendations
        
        # Filtrar por prioridade
        priority_filter = st.selectbox(
            "Filtrar por prioridade:",
            options=['Todas', 'high', 'medium', 'low'],
            index=0
        )
        
        if priority_filter != 'Todas':
            recommendations = [r for r in recommendations if r['priority'] == priority_filter]
        
        # Exibir recomendações
        for i, rec in enumerate(recommendations):
            priority_color = {
                'high': '🔴',
                'medium': '🟡', 
                'low': '🟢'
            }
            
            with st.expander(f"{priority_color[rec['priority']]} {rec['title']} (Melhoria: +{rec['expected_improvement']})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Descrição:** {rec['description']}")
                    st.write(f"**Ação recomendada:** {rec['action']}")
                    
                    # Barra de progresso para confiança
                    st.write(f"**Confiança:** {rec['confidence']:.0%}")
                    st.progress(rec['confidence'])
                
                with col2:
                    st.metric("Melhoria Esperada", rec['expected_improvement'])
                    st.metric("Dificuldade", rec['implementation_difficulty'].title())
                    st.metric("Tipo", rec['type'].title())
                
                # Botões de ação
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button(f"✅ Implementar", key=f"implement_{i}"):
                        st.success("Recomendação marcada para implementação!")
                
                with col2:
                    if st.button(f"⏰ Lembrar depois", key=f"remind_{i}"):
                        st.info("Lembrete configurado para amanhã.")
                
                with col3:
                    if st.button(f"❌ Dispensar", key=f"dismiss_{i}"):
                        st.warning("Recomendação dispensada.")
    
    def render_real_time_monitoring(self):
        """Renderizar monitoramento em tempo real"""
        st.subheader("⏱️ Monitoramento em Tempo Real")
        
        # Simular sessão atual
        current_session = self.analyze_current_session()
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Sessão Atual:**")
            
            # Métricas da sessão atual
            col1a, col2a, col3a = st.columns(3)
            
            with col1a:
                st.metric(
                    "Duração",
                    f"{current_session['duration_minutes']} min"
                )
            
            with col2a:
                attention = current_session['current_attention']
                st.metric(
                    "Atenção Atual",
                    f"{attention:.0%}",
                    delta=f"Tendência: {current_session['attention_trend']}"
                )
            
            with col3a:
                st.metric(
                    "Distrações",
                    current_session['distraction_count']
                )
            
            # Gráfico de atenção em tempo real (simulado)
            time_points = list(range(0, current_session['duration_minutes'], 5))
            attention_values = [
                max(0.2, min(1.0, current_session['current_attention'] + 0.2 * np.sin(t * 0.1) + np.random.normal(0, 0.05)))
                for t in time_points
            ]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=time_points,
                y=attention_values,
                mode='lines+markers',
                name='Nível de Atenção',
                line=dict(color='blue', width=2)
            ))
            
            # Linha de threshold
            fig.add_hline(
                y=0.7,
                line_dash="dash",
                line_color="red",
                annotation_text="Threshold de Alerta"
            )
            
            fig.update_layout(
                title='Atenção Durante a Sessão Atual',
                xaxis_title='Tempo (minutos)',
                yaxis_title='Nível de Atenção',
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Status Atual:**")
            
            # Indicadores visuais
            attention_level = current_session['current_attention']
            if attention_level > 0.8:
                st.success("🟢 Atenção Excelente")
            elif attention_level > 0.6:
                st.info("🟡 Atenção Boa")
            else:
                st.warning("🔴 Atenção Baixa")
            
            # Recomendação atual
            st.write("**Recomendação:**")
            st.info(current_session['recommended_action'])
            
            # Predição de performance
            pred_performance = current_session['performance_prediction']
            st.write("**Performance Prevista:**")
            st.metric("", f"{pred_performance:.0%}")
            
            # Botões de controle
            st.write("**Controles:**")
            
            if st.button("⏸️ Pausar Sessão", type="primary"):
                st.success("Sessão pausada. Faça uma pausa de 10-15 minutos.")
            
            if st.button("🔄 Resetar Métricas"):
                st.info("Métricas da sessão resetadas.")
            
            if st.button("📊 Salvar Dados"):
                st.success("Dados da sessão salvos para análise.")
    
    def render_settings(self):
        """Renderizar configurações"""
        st.subheader("⚙️ Configurações de Análise Comportamental")
        
        settings = st.session_state.behavioral_settings
        
        # Configurações de tracking
        st.write("**🔍 Configurações de Rastreamento**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['tracking_enabled'] = st.checkbox(
                "Análise comportamental ativa",
                value=settings['tracking_enabled']
            )
            
            settings['webcam_analysis'] = st.checkbox(
                "Análise por webcam (experimental)",
                value=settings['webcam_analysis'],
                help="Requer permissão de câmera"
            )
            
            settings['auto_recommendations'] = st.checkbox(
                "Recomendações automáticas",
                value=settings['auto_recommendations']
            )
        
        with col2:
            settings['privacy_mode'] = st.checkbox(
                "Modo privacidade (dados locais)",
                value=settings['privacy_mode']
            )
            
            settings['share_anonymous_data'] = st.checkbox(
                "Compartilhar dados anônimos para pesquisa",
                value=settings['share_anonymous_data']
            )
            
            settings['data_retention_days'] = st.slider(
                "Retenção de dados (dias):",
                min_value=7,
                max_value=90,
                value=settings['data_retention_days']
            )
        
        # Configurações de análise
        st.write("**📊 Configurações de Análise**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['analysis_frequency'] = st.selectbox(
                "Frequência de análise:",
                options=['real_time', 'hourly', 'daily'],
                index=0
            )
            
            settings['notification_threshold'] = st.slider(
                "Threshold para notificações:",
                min_value=0.1,
                max_value=1.0,
                value=settings['notification_threshold'],
                step=0.1
            )
        
        with col2:
            st.write("**Calibração de Sensores:**")
            if st.button("🎯 Calibrar Atenção"):
                st.success("Calibração de atenção iniciada. Siga as instruções na tela.")
            
            if st.button("😴 Calibrar Fadiga"):
                st.success("Calibração de fadiga iniciada.")
        
        # Salvar configurações
        if st.button("💾 Salvar Configurações", type="primary"):
            st.session_state.behavioral_settings = settings
            st.success("✅ Configurações salvas com sucesso!")
        
        # Exportar dados
        st.write("**📤 Exportar Dados**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Exportar CSV"):
                st.success("Dados exportados para CSV.")
        
        with col2:
            if st.button("📈 Relatório PDF"):
                st.success("Relatório PDF gerado.")
        
        with col3:
            if st.button("🗑️ Limpar Dados"):
                if st.checkbox("Confirmar exclusão"):
                    st.warning("Todos os dados foram removidos.")
    
    def render(self):
        """Renderizar componente principal"""
        st.title("🧠 Análise Comportamental Avançada")
        
        # Verificar se está ativo
        if not st.session_state.behavioral_settings['tracking_enabled']:
            st.warning("⚠️ Análise comportamental desativada. Ative nas configurações.")
        
        # Tabs principais
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 Dashboard",
            "📊 Sessões",
            "💡 Recomendações",
            "⏱️ Tempo Real",
            "⚙️ Configurações",
            "❓ Ajuda"
        ])
        
        with tab1:
            self.render_behavioral_dashboard()
        
        with tab2:
            self.render_session_analysis()
        
        with tab3:
            self.render_recommendations()
        
        with tab4:
            self.render_real_time_monitoring()
        
        with tab5:
            self.render_settings()
        
        with tab6:
            st.subheader("❓ Ajuda - Análise Comportamental")
            
            st.markdown("""
            ### 🧠 Como funciona a Análise Comportamental
            
            **Dados Coletados:**
            - ⏱️ **Tempo de foco** - Duração das sessões de estudo
            - 👁️ **Padrões de atenção** - Variações durante o estudo
            - 😴 **Níveis de fadiga** - Sinais de cansaço mental
            - 🏠 **Preferências ambientais** - Locais mais produtivos
            - 📱 **Distrações** - Frequência e impacto das interrupções
            
            **Insights Gerados:**
            - 📈 **Horários ótimos** para cada tipo de atividade
            - 🎯 **Padrões comportamentais** dominantes
            - 💡 **Recomendações personalizadas** de melhoria
            - 📊 **Correlações** entre ambiente e performance
            
            **Privacidade:**
            - 🔒 Todos os dados são processados localmente
            - 🚫 Nenhuma informação pessoal é compartilhada
            - 🗑️ Dados podem ser excluídos a qualquer momento
            - ⚙️ Controle total sobre coleta e uso dos dados
            
            **Dicas de Uso:**
            - Mantenha o tracking ativo por pelo menos 2 semanas
            - Seja consistente nos horários de estudo
            - Experimente diferentes ambientes
            - Implemente as recomendações gradualmente
            """)

# Função para integração com o sistema principal
def render_behavioral_analysis():
    """Função para renderizar análise comportamental"""
    behavioral_analysis = BehavioralAnalysis()
    behavioral_analysis.render()

if __name__ == "__main__":
    render_behavioral_analysis()