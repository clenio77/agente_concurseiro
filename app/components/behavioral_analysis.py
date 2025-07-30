"""
🧠 Análise Comportamental Avançada
Sistema completo de tracking de padrões de estudo, análise de concentração,
detecção de fadiga e otimização de horários
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta, time
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from enum import Enum
import json
import time as time_module
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class StudyState(Enum):
    """Estados de estudo"""
    FOCUSED = "Focado"
    DISTRACTED = "Distraído"
    TIRED = "Cansado"
    PRODUCTIVE = "Produtivo"
    BREAK_NEEDED = "Precisa de Pausa"

class ConcentrationLevel(Enum):
    """Níveis de concentração"""
    VERY_LOW = "Muito Baixa"
    LOW = "Baixa"
    MEDIUM = "Média"
    HIGH = "Alta"
    VERY_HIGH = "Muito Alta"

class FatigueLevel(Enum):
    """Níveis de fadiga"""
    NONE = "Nenhuma"
    LIGHT = "Leve"
    MODERATE = "Moderada"
    HIGH = "Alta"
    EXTREME = "Extrema"

@dataclass
class StudySession:
    """Dados de uma sessão de estudo"""
    timestamp: datetime
    duration_minutes: int
    subject: str
    activity_type: str  # leitura, exercícios, revisão, simulado
    concentration_score: float  # 0-10
    fatigue_level: int  # 0-10
    productivity_score: float  # 0-10
    interruptions: int
    break_frequency: int  # pausas por hora
    performance_score: float  # 0-100
    mood_before: int  # 1-5
    mood_after: int  # 1-5
    environment_quality: int  # 1-5 (ruído, iluminação, etc.)
    device_used: str  # desktop, mobile, tablet
    location: str  # casa, biblioteca, etc.

@dataclass
class BehavioralPattern:
    """Padrão comportamental identificado"""
    pattern_id: str
    pattern_name: str
    description: str
    frequency: float
    impact_score: float
    recommendations: List[str]
    optimal_conditions: Dict[str, Any]

class BehavioralAnalyzer:
    """Analisador comportamental avançado"""
    
    def __init__(self):
        self.sessions_data = []
        self.patterns = []
        self.user_profile = {}
        
    def add_session(self, session: StudySession):
        """Adiciona uma nova sessão de estudo"""
        self.sessions_data.append(session)
        
    def analyze_concentration_patterns(self, sessions: List[StudySession]) -> Dict[str, Any]:
        """Analisa padrões de concentração"""
        if not sessions:
            return {}
            
        df = pd.DataFrame([asdict(s) for s in sessions])
        
        # Análise por hora do dia
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        concentration_by_hour = df.groupby('hour')['concentration_score'].mean()
        
        # Análise por dia da semana
        df['weekday'] = pd.to_datetime(df['timestamp']).dt.day_name()
        concentration_by_weekday = df.groupby('weekday')['concentration_score'].mean()
        
        # Análise por duração da sessão
        concentration_by_duration = df.groupby(pd.cut(df['duration_minutes'], 
                                                     bins=[0, 30, 60, 120, 300], 
                                                     labels=['0-30min', '30-60min', '1-2h', '2h+']))['concentration_score'].mean()
        
        # Identificar picos de concentração
        peak_hours = concentration_by_hour.nlargest(3).index.tolist()
        best_weekdays = concentration_by_weekday.nlargest(2).index.tolist()
        
        return {
            'concentration_by_hour': concentration_by_hour.to_dict(),
            'concentration_by_weekday': concentration_by_weekday.to_dict(),
            'concentration_by_duration': concentration_by_duration.to_dict(),
            'peak_hours': peak_hours,
            'best_weekdays': best_weekdays,
            'average_concentration': df['concentration_score'].mean(),
            'concentration_trend': self._calculate_trend(df['concentration_score'].tolist())
        }
    
    def analyze_fatigue_patterns(self, sessions: List[StudySession]) -> Dict[str, Any]:
        """Analisa padrões de fadiga"""
        if not sessions:
            return {}
            
        df = pd.DataFrame([asdict(s) for s in sessions])
        
        # Análise de fadiga ao longo do dia
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        fatigue_by_hour = df.groupby('hour')['fatigue_level'].mean()
        
        # Correlação entre duração e fadiga
        fatigue_duration_corr = df['duration_minutes'].corr(df['fatigue_level'])
        
        # Análise de fadiga acumulada
        df_sorted = df.sort_values('timestamp')
        df_sorted['cumulative_study_time'] = df_sorted['duration_minutes'].cumsum()
        
        # Identificar pontos críticos de fadiga
        high_fatigue_sessions = df[df['fatigue_level'] > 7]
        fatigue_triggers = self._identify_fatigue_triggers(df)
        
        return {
            'fatigue_by_hour': fatigue_by_hour.to_dict(),
            'fatigue_duration_correlation': fatigue_duration_corr,
            'high_fatigue_frequency': len(high_fatigue_sessions) / len(df) * 100,
            'fatigue_triggers': fatigue_triggers,
            'optimal_session_length': self._calculate_optimal_session_length(df),
            'recovery_time_needed': self._calculate_recovery_time(df)
        }
    
    def analyze_productivity_patterns(self, sessions: List[StudySession]) -> Dict[str, Any]:
        """Analisa padrões de produtividade"""
        if not sessions:
            return {}
            
        df = pd.DataFrame([asdict(s) for s in sessions])
        
        # Produtividade por matéria
        productivity_by_subject = df.groupby('subject')['productivity_score'].mean()
        
        # Produtividade por tipo de atividade
        productivity_by_activity = df.groupby('activity_type')['productivity_score'].mean()
        
        # Produtividade por ambiente
        productivity_by_environment = df.groupby('environment_quality')['productivity_score'].mean()
        
        # Correlações importantes
        correlations = {
            'concentration_productivity': df['concentration_score'].corr(df['productivity_score']),
            'mood_productivity': df['mood_before'].corr(df['productivity_score']),
            'environment_productivity': df['environment_quality'].corr(df['productivity_score']),
            'fatigue_productivity': df['fatigue_level'].corr(df['productivity_score'])
        }
        
        return {
            'productivity_by_subject': productivity_by_subject.to_dict(),
            'productivity_by_activity': productivity_by_activity.to_dict(),
            'productivity_by_environment': productivity_by_environment.to_dict(),
            'correlations': correlations,
            'average_productivity': df['productivity_score'].mean(),
            'productivity_trend': self._calculate_trend(df['productivity_score'].tolist()),
            'peak_performance_conditions': self._identify_peak_conditions(df)
        }
    
    def detect_behavioral_patterns(self, sessions: List[StudySession]) -> List[BehavioralPattern]:
        """Detecta padrões comportamentais usando ML"""
        if len(sessions) < 10:
            return []
            
        df = pd.DataFrame([asdict(s) for s in sessions])
        
        # Preparar features para clustering
        features = ['concentration_score', 'fatigue_level', 'productivity_score', 
                   'duration_minutes', 'interruptions', 'break_frequency',
                   'mood_before', 'environment_quality']
        
        X = df[features].fillna(df[features].mean())
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Aplicar clustering
        n_clusters = min(5, len(sessions) // 3)
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(X_scaled)
        
        df['cluster'] = clusters
        
        patterns = []
        for cluster_id in range(n_clusters):
            cluster_data = df[df['cluster'] == cluster_id]
            pattern = self._analyze_cluster(cluster_id, cluster_data)
            patterns.append(pattern)
            
        return patterns
    
    def generate_schedule_optimization(self, sessions: List[StudySession]) -> Dict[str, Any]:
        """Gera otimização de cronograma baseada nos padrões"""
        concentration_analysis = self.analyze_concentration_patterns(sessions)
        fatigue_analysis = self.analyze_fatigue_patterns(sessions)
        productivity_analysis = self.analyze_productivity_patterns(sessions)
        
        # Horários ótimos
        optimal_hours = concentration_analysis.get('peak_hours', [9, 14, 19])
        
        # Duração ótima das sessões
        optimal_duration = fatigue_analysis.get('optimal_session_length', 60)
        
        # Frequência de pausas
        optimal_break_frequency = self._calculate_optimal_break_frequency(sessions)
        
        # Cronograma personalizado
        schedule = self._generate_personalized_schedule(
            optimal_hours, optimal_duration, optimal_break_frequency
        )
        
        return {
            'optimal_study_hours': optimal_hours,
            'optimal_session_duration': optimal_duration,
            'optimal_break_frequency': optimal_break_frequency,
            'personalized_schedule': schedule,
            'weekly_distribution': self._generate_weekly_distribution(sessions),
            'subject_prioritization': self._generate_subject_prioritization(sessions)
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calcula tendência dos valores"""
        if len(values) < 2:
            return "Estável"
            
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        if slope > 0.1:
            return "Crescente"
        elif slope < -0.1:
            return "Decrescente"
        else:
            return "Estável"
    
    def _identify_fatigue_triggers(self, df: pd.DataFrame) -> List[str]:
        """Identifica gatilhos de fadiga"""
        triggers = []
        
        # Sessões longas
        if df[df['duration_minutes'] > 120]['fatigue_level'].mean() > 6:
            triggers.append("Sessões muito longas (>2h)")
            
        # Muitas interrupções
        if df[df['interruptions'] > 5]['fatigue_level'].mean() > 6:
            triggers.append("Muitas interrupções")
            
        # Ambiente inadequado
        if df[df['environment_quality'] < 3]['fatigue_level'].mean() > 6:
            triggers.append("Ambiente inadequado")
            
        # Horários inadequados
        late_hours = df[pd.to_datetime(df['timestamp']).dt.hour > 22]
        if not late_hours.empty and late_hours['fatigue_level'].mean() > 6:
            triggers.append("Estudos muito tarde")
            
        return triggers
    
    def _calculate_optimal_session_length(self, df: pd.DataFrame) -> int:
        """Calcula duração ótima das sessões"""
        # Encontrar duração que maximiza produtividade e minimiza fadiga
        duration_bins = pd.cut(df['duration_minutes'], bins=[0, 30, 60, 90, 120, 300])
        
        productivity_by_duration = df.groupby(duration_bins)['productivity_score'].mean()
        fatigue_by_duration = df.groupby(duration_bins)['fatigue_level'].mean()
        
        # Score combinado (produtividade alta, fadiga baixa)
        combined_score = productivity_by_duration - (fatigue_by_duration / 10 * 5)
        
        optimal_bin = combined_score.idxmax()
        
        # Mapear bin para valor médio
        duration_mapping = {
            '(0, 30]': 25,
            '(30, 60]': 45,
            '(60, 90]': 75,
            '(90, 120]': 105,
            '(120, 300]': 150
        }
        
        return duration_mapping.get(str(optimal_bin), 60)
    
    def _calculate_recovery_time(self, df: pd.DataFrame) -> int:
        """Calcula tempo de recuperação necessário"""
        high_fatigue = df[df['fatigue_level'] > 7]
        if high_fatigue.empty:
            return 15
            
        # Analisar tempo entre sessões de alta fadiga
        recovery_times = []
        for idx in high_fatigue.index:
            next_sessions = df[df.index > idx].head(3)
            if not next_sessions.empty:
                recovery_time = (next_sessions['fatigue_level'] < 5).sum() * 15
                recovery_times.append(recovery_time)
                
        return int(np.mean(recovery_times)) if recovery_times else 20
    
    def _identify_peak_conditions(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identifica condições de pico de performance"""
        top_sessions = df.nlargest(int(len(df) * 0.2), 'productivity_score')
        
        return {
            'best_subjects': top_sessions['subject'].mode().tolist(),
            'best_activities': top_sessions['activity_type'].mode().tolist(),
            'best_hours': pd.to_datetime(top_sessions['timestamp']).dt.hour.mode().tolist(),
            'best_duration_range': f"{top_sessions['duration_minutes'].min()}-{top_sessions['duration_minutes'].max()} min",
            'optimal_environment': top_sessions['environment_quality'].mode().tolist()[0] if not top_sessions.empty else 4,
            'optimal_mood': top_sessions['mood_before'].mode().tolist()[0] if not top_sessions.empty else 4
        }
    
    def _analyze_cluster(self, cluster_id: int, cluster_data: pd.DataFrame) -> BehavioralPattern:
        """Analisa um cluster específico"""
        avg_concentration = cluster_data['concentration_score'].mean()
        avg_fatigue = cluster_data['fatigue_level'].mean()
        avg_productivity = cluster_data['productivity_score'].mean()
        
        # Determinar tipo de padrão
        if avg_concentration > 7 and avg_productivity > 7:
            pattern_name = "Padrão de Alta Performance"
            description = "Sessões com alta concentração e produtividade"
        elif avg_fatigue > 7:
            pattern_name = "Padrão de Fadiga"
            description = "Sessões com alta fadiga e baixa performance"
        elif cluster_data['interruptions'].mean() > 5:
            pattern_name = "Padrão de Distração"
            description = "Sessões com muitas interrupções"
        else:
            pattern_name = f"Padrão Misto {cluster_id + 1}"
            description = "Padrão comportamental identificado"
        
        # Gerar recomendações
        recommendations = self._generate_pattern_recommendations(cluster_data)
        
        return BehavioralPattern(
            pattern_id=f"pattern_{cluster_id}",
            pattern_name=pattern_name,
            description=description,
            frequency=len(cluster_data) / len(self.sessions_data) * 100,
            impact_score=avg_productivity,
            recommendations=recommendations,
            optimal_conditions=self._extract_optimal_conditions(cluster_data)
        )
    
    def _generate_pattern_recommendations(self, cluster_data: pd.DataFrame) -> List[str]:
        """Gera recomendações baseadas no padrão"""
        recommendations = []
        
        avg_concentration = cluster_data['concentration_score'].mean()
        avg_fatigue = cluster_data['fatigue_level'].mean()
        avg_duration = cluster_data['duration_minutes'].mean()
        
        if avg_concentration < 5:
            recommendations.append("Implementar técnicas de foco (Pomodoro, meditação)")
            
        if avg_fatigue > 6:
            recommendations.append("Reduzir duração das sessões e aumentar pausas")
            
        if avg_duration > 120:
            recommendations.append("Dividir sessões longas em blocos menores")
            
        if cluster_data['interruptions'].mean() > 3:
            recommendations.append("Criar ambiente livre de distrações")
            
        if cluster_data['environment_quality'].mean() < 3:
            recommendations.append("Melhorar condições do ambiente de estudo")
            
        return recommendations
    
    def _extract_optimal_conditions(self, cluster_data: pd.DataFrame) -> Dict[str, Any]:
        """Extrai condições ótimas do cluster"""
        return {
            'optimal_duration': int(cluster_data['duration_minutes'].median()),
            'optimal_hour': int(pd.to_datetime(cluster_data['timestamp']).dt.hour.mode().iloc[0]),
            'optimal_environment': int(cluster_data['environment_quality'].mode().iloc[0]),
            'max_interruptions': int(cluster_data['interruptions'].quantile(0.25)),
            'break_frequency': int(cluster_data['break_frequency'].median())
        }
    
    def _calculate_optimal_break_frequency(self, sessions: List[StudySession]) -> int:
        """Calcula frequência ótima de pausas"""
        if not sessions:
            return 2
            
        df = pd.DataFrame([asdict(s) for s in sessions])
        
        # Correlação entre pausas e produtividade
        correlation = df['break_frequency'].corr(df['productivity_score'])
        
        if correlation > 0.3:
            return int(df['break_frequency'].quantile(0.75))
        else:
            return int(df['break_frequency'].median())
    
    def _generate_personalized_schedule(self, optimal_hours: List[int], 
                                      optimal_duration: int, 
                                      break_frequency: int) -> Dict[str, List[Dict]]:
        """Gera cronograma personalizado"""
        schedule = {}
        
        weekdays = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        
        for day in weekdays:
            day_schedule = []
            
            for hour in optimal_hours:
                session = {
                    'start_time': f"{hour:02d}:00",
                    'end_time': f"{hour + optimal_duration // 60:02d}:{optimal_duration % 60:02d}",
                    'duration': optimal_duration,
                    'breaks': break_frequency,
                    'type': 'Sessão de Estudo Otimizada'
                }
                day_schedule.append(session)
                
            schedule[day] = day_schedule
            
        return schedule
    
    def _generate_weekly_distribution(self, sessions: List[StudySession]) -> Dict[str, int]:
        """Gera distribuição semanal otimizada"""
        if not sessions:
            return {day: 2 for day in ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']}
            
        df = pd.DataFrame([asdict(s) for s in sessions])
        df['weekday'] = pd.to_datetime(df['timestamp']).dt.day_name()
        
        # Mapear nomes em inglês para português
        day_mapping = {
            'Monday': 'Segunda', 'Tuesday': 'Terça', 'Wednesday': 'Quarta',
            'Thursday': 'Quinta', 'Friday': 'Sexta', 'Saturday': 'Sábado', 'Sunday': 'Domingo'
        }
        
        productivity_by_day = df.groupby('weekday')['productivity_score'].mean()
        
        distribution = {}
        for eng_day, pt_day in day_mapping.items():
            if eng_day in productivity_by_day.index:
                # Mais sessões nos dias mais produtivos
                score = productivity_by_day[eng_day]
                sessions_count = max(1, int(score / 2))
                distribution[pt_day] = min(4, sessions_count)
            else:
                distribution[pt_day] = 2
                
        return distribution
    
    def _generate_subject_prioritization(self, sessions: List[StudySession]) -> Dict[str, float]:
        """Gera priorização de matérias"""
        if not sessions:
            return {}
            
        df = pd.DataFrame([asdict(s) for s in sessions])
        
        # Calcular score de prioridade baseado em performance e tempo gasto
        subject_stats = df.groupby('subject').agg({
            'productivity_score': 'mean',
            'performance_score': 'mean',
            'duration_minutes': 'sum'
        })
        
        # Matérias com baixa performance precisam de mais atenção
        subject_stats['priority_score'] = (
            (100 - subject_stats['performance_score']) * 0.4 +
            (10 - subject_stats['productivity_score']) * 0.3 +
            (subject_stats['duration_minutes'] / subject_stats['duration_minutes'].max()) * 0.3
        )
        
        return subject_stats['priority_score'].to_dict()

def render_behavioral_analysis():
    """Renderiza a interface de análise comportamental"""
    st.title("🧠 Análise Comportamental Avançada")
    st.markdown("---")
    
    # Inicializar analyzer
    if 'behavioral_analyzer' not in st.session_state:
        st.session_state.behavioral_analyzer = BehavioralAnalyzer()
        
        # Gerar dados de exemplo
        example_sessions = generate_example_sessions()
        for session in example_sessions:
            st.session_state.behavioral_analyzer.add_session(session)
    
    analyzer = st.session_state.behavioral_analyzer
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        analysis_period = st.selectbox(
            "Período de Análise",
            ["Última Semana", "Último Mês", "Últimos 3 Meses", "Todos os Dados"]
        )
        
        show_advanced = st.checkbox("Mostrar Análises Avançadas", value=True)
        
        st.markdown("---")
        st.header("📊 Adicionar Sessão")
        
        with st.form("add_session"):
            subject = st.selectbox("Matéria", ["Português", "Matemática", "Direito", "História", "Geografia"])
            activity = st.selectbox("Atividade", ["Leitura", "Exercícios", "Revisão", "Simulado"])
            duration = st.slider("Duração (min)", 15, 300, 60)
            concentration = st.slider("Concentração (0-10)", 0, 10, 7)
            fatigue = st.slider("Fadiga (0-10)", 0, 10, 3)
            productivity = st.slider("Produtividade (0-10)", 0, 10, 7)
            
            if st.form_submit_button("Adicionar Sessão"):
                new_session = StudySession(
                    timestamp=datetime.now(),
                    duration_minutes=duration,
                    subject=subject,
                    activity_type=activity,
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
                analyzer.add_session(new_session)
                st.success("Sessão adicionada com sucesso!")
                st.rerun()
    
    # Filtrar sessões por período
    sessions = filter_sessions_by_period(analyzer.sessions_data, analysis_period)
    
    if not sessions:
        st.warning("Nenhuma sessão encontrada para o período selecionado.")
        return
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Visão Geral", "🎯 Concentração", "😴 Fadiga", 
        "⚡ Produtividade", "🤖 Padrões IA"
    ])
    
    with tab1:
        render_overview_tab(analyzer, sessions)
    
    with tab2:
        render_concentration_tab(analyzer, sessions)
    
    with tab3:
        render_fatigue_tab(analyzer, sessions)
    
    with tab4:
        render_productivity_tab(analyzer, sessions)
    
    with tab5:
        render_patterns_tab(analyzer, sessions)

def generate_example_sessions() -> List[StudySession]:
    """Gera sessões de exemplo para demonstração"""
    sessions = []
    subjects = ["Português", "Matemática", "Direito", "História", "Geografia"]
    activities = ["Leitura", "Exercícios", "Revisão", "Simulado"]
    
    # Gerar 50 sessões dos últimos 30 dias
    for i in range(50):
        timestamp = datetime.now() - timedelta(days=np.random.randint(0, 30))
        
        # Simular padrões realistas
        hour = timestamp.hour
        concentration = np.random.normal(7, 2)
        
        # Concentração varia por hora
        if 9 <= hour <= 11 or 14 <= hour <= 16:
            concentration += 1
        elif hour >= 22 or hour <= 6:
            concentration -= 2
            
        concentration = max(0, min(10, concentration))
        
        # Fadiga correlacionada com duração e hora
        duration = np.random.randint(30, 180)
        fatigue = max(0, min(10, duration / 30 + (hour - 12) / 4 + np.random.normal(0, 1)))
        
        # Produtividade correlacionada com concentração e fadiga
        productivity = max(0, min(10, concentration - fatigue / 2 + np.random.normal(0, 1)))
        
        session = StudySession(
            timestamp=timestamp,
            duration_minutes=duration,
            subject=np.random.choice(subjects),
            activity_type=np.random.choice(activities),
            concentration_score=concentration,
            fatigue_level=fatigue,
            productivity_score=productivity,
            interruptions=np.random.poisson(2),
            break_frequency=np.random.randint(1, 4),
            performance_score=np.random.uniform(50, 95),
            mood_before=np.random.randint(2, 6),
            mood_after=np.random.randint(2, 6),
            environment_quality=np.random.randint(2, 6),
            device_used=np.random.choice(["Desktop", "Mobile", "Tablet"]),
            location=np.random.choice(["Casa", "Biblioteca", "Café"])
        )
        sessions.append(session)
    
    return sessions

def filter_sessions_by_period(sessions: List[StudySession], period: str) -> List[StudySession]:
    """Filtra sessões por período"""
    if not sessions:
        return []
    
    now = datetime.now()
    
    if period == "Última Semana":
        cutoff = now - timedelta(days=7)
    elif period == "Último Mês":
        cutoff = now - timedelta(days=30)
    elif period == "Últimos 3 Meses":
        cutoff = now - timedelta(days=90)
    else:  # Todos os Dados
        return sessions
    
    return [s for s in sessions if s.timestamp >= cutoff]

def render_overview_tab(analyzer: BehavioralAnalyzer, sessions: List[StudySession]):
    """Renderiza tab de visão geral"""
    st.header("📈 Visão Geral do Comportamento de Estudo")
    
    if not sessions:
        st.warning("Nenhuma sessão encontrada.")
        return
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    total_sessions = len(sessions)
    total_hours = sum(s.duration_minutes for s in sessions) / 60
    avg_concentration = np.mean([s.concentration_score for s in sessions])
    avg_productivity = np.mean([s.productivity_score for s in sessions])
    
    with col1:
        st.metric("Total de Sessões", total_sessions)
    
    with col2:
        st.metric("Horas Estudadas", f"{total_hours:.1f}h")
    
    with col3:
        st.metric("Concentração Média", f"{avg_concentration:.1f}/10")
    
    with col4:
        st.metric("Produtividade Média", f"{avg_productivity:.1f}/10")
    
    st.markdown("---")
    
    # Gráficos de tendência
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de concentração ao longo do tempo
        df = pd.DataFrame([asdict(s) for s in sessions])
        df['date'] = pd.to_datetime(df['timestamp']).dt.date
        daily_concentration = df.groupby('date')['concentration_score'].mean().reset_index()
        
        fig = px.line(daily_concentration, x='date', y='concentration_score',
                     title='Concentração ao Longo do Tempo',
                     labels={'concentration_score': 'Concentração', 'date': 'Data'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Gráfico de produtividade por matéria
        productivity_by_subject = df.groupby('subject')['productivity_score'].mean().reset_index()
        
        fig = px.bar(productivity_by_subject, x='subject', y='productivity_score',
                    title='Produtividade por Matéria',
                    labels={'productivity_score': 'Produtividade', 'subject': 'Matéria'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Resumo de insights
    st.markdown("---")
    st.subheader("🎯 Insights Principais")
    
    insights = generate_overview_insights(sessions)
    for insight in insights:
        st.info(f"💡 {insight}")

def render_concentration_tab(analyzer: BehavioralAnalyzer, sessions: List[StudySession]):
    """Renderiza tab de análise de concentração"""
    st.header("🎯 Análise de Concentração")
    
    concentration_analysis = analyzer.analyze_concentration_patterns(sessions)
    
    if not concentration_analysis:
        st.warning("Dados insuficientes para análise de concentração.")
        return
    
    # Métricas de concentração
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_concentration = concentration_analysis['average_concentration']
        st.metric("Concentração Média", f"{avg_concentration:.1f}/10")
    
    with col2:
        trend = concentration_analysis['concentration_trend']
        st.metric("Tendência", trend)
    
    with col3:
        peak_hours = concentration_analysis['peak_hours']
        st.metric("Melhor Horário", f"{peak_hours[0]}h-{peak_hours[0]+2}h")
    
    st.markdown("---")
    
    # Gráficos de concentração
    col1, col2 = st.columns(2)
    
    with col1:
        # Concentração por hora
        conc_by_hour = concentration_analysis['concentration_by_hour']
        hours = list(conc_by_hour.keys())
        values = list(conc_by_hour.values())
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=values, mode='lines+markers',
                               name='Concentração', line=dict(color='blue', width=3)))
        fig.update_layout(title='Concentração por Hora do Dia',
                         xaxis_title='Hora', yaxis_title='Concentração',
                         height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Concentração por dia da semana
        conc_by_weekday = concentration_analysis['concentration_by_weekday']
        
        fig = px.bar(x=list(conc_by_weekday.keys()), y=list(conc_by_weekday.values()),
                    title='Concentração por Dia da Semana',
                    labels={'x': 'Dia da Semana', 'y': 'Concentração'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Recomendações de concentração
    st.markdown("---")
    st.subheader("💡 Recomendações para Melhorar Concentração")
    
    recommendations = generate_concentration_recommendations(concentration_analysis)
    for rec in recommendations:
        st.success(f"✅ {rec}")

def render_fatigue_tab(analyzer: BehavioralAnalyzer, sessions: List[StudySession]):
    """Renderiza tab de análise de fadiga"""
    st.header("😴 Análise de Fadiga")
    
    fatigue_analysis = analyzer.analyze_fatigue_patterns(sessions)
    
    if not fatigue_analysis:
        st.warning("Dados insuficientes para análise de fadiga.")
        return
    
    # Métricas de fadiga
    col1, col2, col3 = st.columns(3)
    
    with col1:
        high_fatigue_freq = fatigue_analysis['high_fatigue_frequency']
        st.metric("Sessões de Alta Fadiga", f"{high_fatigue_freq:.1f}%")
    
    with col2:
        optimal_length = fatigue_analysis['optimal_session_length']
        st.metric("Duração Ótima", f"{optimal_length} min")
    
    with col3:
        recovery_time = fatigue_analysis['recovery_time_needed']
        st.metric("Tempo de Recuperação", f"{recovery_time} min")
    
    st.markdown("---")
    
    # Gráficos de fadiga
    col1, col2 = st.columns(2)
    
    with col1:
        # Fadiga por hora
        fatigue_by_hour = fatigue_analysis['fatigue_by_hour']
        
        fig = px.line(x=list(fatigue_by_hour.keys()), y=list(fatigue_by_hour.values()),
                     title='Fadiga por Hora do Dia',
                     labels={'x': 'Hora', 'y': 'Nível de Fadiga'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Correlação duração vs fadiga
        df = pd.DataFrame([asdict(s) for s in sessions])
        
        fig = px.scatter(df, x='duration_minutes', y='fatigue_level',
                        title='Duração vs Fadiga',
                        labels={'duration_minutes': 'Duração (min)', 'fatigue_level': 'Fadiga'},
                        trendline='ols')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Gatilhos de fadiga
    st.markdown("---")
    st.subheader("⚠️ Gatilhos de Fadiga Identificados")
    
    triggers = fatigue_analysis['fatigue_triggers']
    if triggers:
        for trigger in triggers:
            st.warning(f"🚨 {trigger}")
    else:
        st.success("✅ Nenhum gatilho crítico de fadiga identificado!")
    
    # Recomendações anti-fadiga
    st.subheader("💡 Recomendações Anti-Fadiga")
    
    recommendations = generate_fatigue_recommendations(fatigue_analysis)
    for rec in recommendations:
        st.info(f"💊 {rec}")

def render_productivity_tab(analyzer: BehavioralAnalyzer, sessions: List[StudySession]):
    """Renderiza tab de análise de produtividade"""
    st.header("⚡ Análise de Produtividade")
    
    productivity_analysis = analyzer.analyze_productivity_patterns(sessions)
    
    if not productivity_analysis:
        st.warning("Dados insuficientes para análise de produtividade.")
        return
    
    # Métricas de produtividade
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_productivity = productivity_analysis['average_productivity']
        st.metric("Produtividade Média", f"{avg_productivity:.1f}/10")
    
    with col2:
        trend = productivity_analysis['productivity_trend']
        st.metric("Tendência", trend)
    
    with col3:
        correlations = productivity_analysis['correlations']
        best_correlation = max(correlations.items(), key=lambda x: abs(x[1]))
        st.metric("Maior Correlação", f"{best_correlation[0]}: {best_correlation[1]:.2f}")
    
    st.markdown("---")
    
    # Gráficos de produtividade
    col1, col2 = st.columns(2)
    
    with col1:
        # Produtividade por atividade
        prod_by_activity = productivity_analysis['productivity_by_activity']
        
        fig = px.bar(x=list(prod_by_activity.keys()), y=list(prod_by_activity.values()),
                    title='Produtividade por Tipo de Atividade',
                    labels={'x': 'Atividade', 'y': 'Produtividade'})
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Correlações
        correlations = productivity_analysis['correlations']
        
        fig = go.Figure(data=go.Bar(
            x=list(correlations.keys()),
            y=list(correlations.values()),
            marker_color=['green' if v > 0 else 'red' for v in correlations.values()]
        ))
        fig.update_layout(title='Correlações com Produtividade',
                         xaxis_title='Fatores', yaxis_title='Correlação',
                         height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    # Condições de pico
    st.markdown("---")
    st.subheader("🏆 Condições de Pico de Performance")
    
    peak_conditions = productivity_analysis['peak_performance_conditions']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**Melhores Matérias:**")
        for subject in peak_conditions['best_subjects'][:3]:
            st.write(f"• {subject}")
    
    with col2:
        st.write("**Melhores Atividades:**")
        for activity in peak_conditions['best_activities'][:3]:
            st.write(f"• {activity}")
    
    with col3:
        st.write("**Melhores Horários:**")
        for hour in peak_conditions['best_hours'][:3]:
            st.write(f"• {hour}:00h")
    
    # Recomendações de produtividade
    st.markdown("---")
    st.subheader("🚀 Recomendações para Aumentar Produtividade")
    
    recommendations = generate_productivity_recommendations(productivity_analysis)
    for rec in recommendations:
        st.success(f"⚡ {rec}")

def render_patterns_tab(analyzer: BehavioralAnalyzer, sessions: List[StudySession]):
    """Renderiza tab de padrões identificados por IA"""
    st.header("🤖 Padrões Comportamentais Identificados por IA")
    
    if len(sessions) < 10:
        st.warning("Dados insuficientes para análise de padrões (mínimo 10 sessões).")
        return
    
    # Detectar padrões
    patterns = analyzer.detect_behavioral_patterns(sessions)
    
    if not patterns:
        st.warning("Nenhum padrão comportamental identificado.")
        return
    
    # Mostrar padrões
    for i, pattern in enumerate(patterns):
        with st.expander(f"📊 {pattern.pattern_name} (Frequência: {pattern.frequency:.1f}%)"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Descrição:** {pattern.description}")
                st.write(f"**Impacto na Performance:** {pattern.impact_score:.1f}/10")
                
                st.write("**Condições Ótimas:**")
                conditions = pattern.optimal_conditions
                st.write(f"• Duração: {conditions['optimal_duration']} min")
                st.write(f"• Melhor horário: {conditions['optimal_hour']}:00h")
                st.write(f"• Qualidade ambiente: {conditions['optimal_environment']}/5")
                st.write(f"• Máx. interrupções: {conditions['max_interruptions']}")
            
            with col2:
                st.write("**Recomendações:**")
                for rec in pattern.recommendations:
                    st.write(f"• {rec}")
    
    # Otimização de cronograma
    st.markdown("---")
    st.subheader("📅 Cronograma Otimizado Baseado em IA")
    
    schedule_optimization = analyzer.generate_schedule_optimization(sessions)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Horários Ótimos de Estudo:**")
        for hour in schedule_optimization['optimal_study_hours']:
            st.write(f"• {hour}:00h - {hour+2}:00h")
        
        st.write(f"**Duração Ótima por Sessão:** {schedule_optimization['optimal_session_duration']} min")
        st.write(f"**Frequência de Pausas:** {schedule_optimization['optimal_break_frequency']} por hora")
    
    with col2:
        st.write("**Distribuição Semanal Recomendada:**")
        weekly_dist = schedule_optimization['weekly_distribution']
        for day, sessions_count in weekly_dist.items():
            st.write(f"• {day}: {sessions_count} sessões")
    
    # Priorização de matérias
    st.markdown("---")
    st.subheader("📚 Priorização Inteligente de Matérias")
    
    subject_prioritization = schedule_optimization['subject_prioritization']
    if subject_prioritization:
        # Ordenar por prioridade
        sorted_subjects = sorted(subject_prioritization.items(), key=lambda x: x[1], reverse=True)
        
        for subject, priority in sorted_subjects[:5]:
            priority_level = "🔴 Alta" if priority > 7 else "🟡 Média" if priority > 4 else "🟢 Baixa"
            st.write(f"• **{subject}**: {priority_level} (Score: {priority:.1f})")

def generate_overview_insights(sessions: List[StudySession]) -> List[str]:
    """Gera insights da visão geral"""
    insights = []
    
    df = pd.DataFrame([asdict(s) for s in sessions])
    
    # Insight sobre consistência
    daily_sessions = df.groupby(pd.to_datetime(df['timestamp']).dt.date).size()
    consistency = daily_sessions.std()
    
    if consistency < 1:
        insights.append("Você mantém uma rotina de estudos muito consistente!")
    elif consistency > 2:
        insights.append("Sua rotina de estudos varia bastante. Tente manter mais regularidade.")
    
    # Insight sobre horários
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    most_common_hour = df['hour'].mode().iloc[0]
    
    if 6 <= most_common_hour <= 10:
        insights.append("Você é uma pessoa matutina! Continue aproveitando as manhãs.")
    elif 14 <= most_common_hour <= 18:
        insights.append("Você prefere estudar à tarde. Ótima escolha para manter energia!")
    elif most_common_hour >= 20:
        insights.append("Você estuda mais à noite. Cuidado com a fadiga em horários tardios.")
    
    # Insight sobre duração
    avg_duration = df['duration_minutes'].mean()
    
    if avg_duration > 120:
        insights.append("Suas sessões são longas. Considere pausas mais frequentes.")
    elif avg_duration < 30:
        insights.append("Suas sessões são curtas. Tente aumentar gradualmente a duração.")
    else:
        insights.append("Duração das sessões está no ponto ideal!")
    
    return insights

def generate_concentration_recommendations(analysis: Dict[str, Any]) -> List[str]:
    """Gera recomendações para concentração"""
    recommendations = []
    
    avg_concentration = analysis['average_concentration']
    peak_hours = analysis['peak_hours']
    trend = analysis['concentration_trend']
    
    if avg_concentration < 6:
        recommendations.append("Implemente técnicas de mindfulness antes de estudar")
        recommendations.append("Use a técnica Pomodoro (25min foco + 5min pausa)")
        recommendations.append("Elimine distrações do ambiente (celular, redes sociais)")
    
    if trend == "Decrescente":
        recommendations.append("Sua concentração está diminuindo. Revise sua rotina de sono")
        recommendations.append("Considere fazer exercícios físicos regulares")
    
    recommendations.append(f"Seus melhores horários são: {', '.join(map(str, peak_hours))}h")
    recommendations.append("Mantenha temperatura ambiente entre 20-22°C")
    recommendations.append("Use iluminação adequada (natural de preferência)")
    
    return recommendations

def generate_fatigue_recommendations(analysis: Dict[str, Any]) -> List[str]:
    """Gera recomendações anti-fadiga"""
    recommendations = []
    
    high_fatigue_freq = analysis['high_fatigue_frequency']
    optimal_length = analysis['optimal_session_length']
    recovery_time = analysis['recovery_time_needed']
    triggers = analysis['fatigue_triggers']
    
    if high_fatigue_freq > 30:
        recommendations.append("Reduza a duração das sessões de estudo")
        recommendations.append("Aumente a frequência de pausas ativas")
        recommendations.append("Verifique qualidade do sono (7-9h por noite)")
    
    recommendations.append(f"Mantenha sessões de até {optimal_length} minutos")
    recommendations.append(f"Faça pausas de pelo menos {recovery_time} minutos entre sessões intensas")
    
    for trigger in triggers:
        if "longas" in trigger:
            recommendations.append("Divida sessões longas em blocos menores")
        elif "interrupções" in trigger:
            recommendations.append("Crie um ambiente livre de interrupções")
        elif "ambiente" in trigger:
            recommendations.append("Melhore ergonomia e conforto do local de estudo")
        elif "tarde" in trigger:
            recommendations.append("Evite estudos após 22h")
    
    recommendations.append("Mantenha-se hidratado durante os estudos")
    recommendations.append("Faça pausas ativas (alongamento, caminhada)")
    
    return recommendations

def generate_productivity_recommendations(analysis: Dict[str, Any]) -> List[str]:
    """Gera recomendações para produtividade"""
    recommendations = []
    
    correlations = analysis['correlations']
    peak_conditions = analysis['peak_performance_conditions']
    trend = analysis['productivity_trend']
    
    # Recomendações baseadas em correlações
    if correlations['concentration_productivity'] > 0.5:
        recommendations.append("Foque em melhorar concentração para aumentar produtividade")
    
    if correlations['mood_productivity'] > 0.3:
        recommendations.append("Monitore seu humor antes de estudar")
        recommendations.append("Use técnicas de regulação emocional")
    
    if correlations['environment_productivity'] > 0.4:
        recommendations.append("Invista em melhorar seu ambiente de estudo")
    
    # Recomendações baseadas em condições de pico
    best_subjects = peak_conditions['best_subjects']
    best_activities = peak_conditions['best_activities']
    best_hours = peak_conditions['best_hours']
    
    if best_subjects:
        recommendations.append(f"Você é mais produtivo em: {', '.join(best_subjects[:2])}")
    
    if best_activities:
        recommendations.append(f"Suas atividades mais produtivas: {', '.join(best_activities[:2])}")
    
    if best_hours:
        recommendations.append(f"Agende tarefas importantes nos horários: {', '.join(map(str, best_hours[:2]))}h")
    
    if trend == "Decrescente":
        recommendations.append("Sua produtividade está caindo. Revise estratégias de estudo")
        recommendations.append("Considere variar métodos e técnicas de aprendizagem")
    
    recommendations.append("Use técnicas de gamificação para manter motivação")
    recommendations.append("Estabeleça metas claras e mensuráveis para cada sessão")
    
    return recommendations

def create_behavioral_dashboard():
    """Cria dashboard comportamental completo"""
    st.set_page_config(
        page_title="Análise Comportamental",
        page_icon="🧠",
        layout="wide"
    )

    # CSS customizado
    st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }

    .insight-box {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 0.5rem 0;
    }

    .pattern-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
    }

    .recommendation-item {
        background: #e8f5e8;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.3rem 0;
        border-left: 3px solid #4CAF50;
    }

    .warning-item {
        background: #fff3cd;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.3rem 0;
        border-left: 3px solid #ffc107;
    }

    .danger-item {
        background: #f8d7da;
        padding: 0.8rem;
        border-radius: 6px;
        margin: 0.3rem 0;
        border-left: 3px solid #dc3545;
    }
    </style>
    """, unsafe_allow_html=True)

    render_behavioral_analysis()

def export_behavioral_report(analyzer: BehavioralAnalyzer, sessions: List[StudySession]) -> str:
    """Exporta relatório comportamental completo"""
    report = []

    report.append("# RELATÓRIO DE ANÁLISE COMPORTAMENTAL")
    report.append("=" * 50)
    report.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    report.append(f"Período analisado: {len(sessions)} sessões")
    report.append("")

    # Resumo executivo
    report.append("## RESUMO EXECUTIVO")
    report.append("-" * 20)

    total_hours = sum(s.duration_minutes for s in sessions) / 60
    avg_concentration = np.mean([s.concentration_score for s in sessions])
    avg_productivity = np.mean([s.productivity_score for s in sessions])
    avg_fatigue = np.mean([s.fatigue_level for s in sessions])

    report.append(f"• Total de horas estudadas: {total_hours:.1f}h")
    report.append(f"• Concentração média: {avg_concentration:.1f}/10")
    report.append(f"• Produtividade média: {avg_productivity:.1f}/10")
    report.append(f"• Fadiga média: {avg_fatigue:.1f}/10")
    report.append("")

    # Análise de concentração
    concentration_analysis = analyzer.analyze_concentration_patterns(sessions)
    if concentration_analysis:
        report.append("## ANÁLISE DE CONCENTRAÇÃO")
        report.append("-" * 25)

        peak_hours = concentration_analysis.get('peak_hours', [])
        report.append(f"• Horários de pico: {', '.join(map(str, peak_hours))}h")
        report.append(f"• Tendência: {concentration_analysis.get('concentration_trend', 'N/A')}")

        best_weekdays = concentration_analysis.get('best_weekdays', [])
        report.append(f"• Melhores dias: {', '.join(best_weekdays[:2])}")
        report.append("")

    # Análise de fadiga
    fatigue_analysis = analyzer.analyze_fatigue_patterns(sessions)
    if fatigue_analysis:
        report.append("## ANÁLISE DE FADIGA")
        report.append("-" * 20)

        high_fatigue_freq = fatigue_analysis.get('high_fatigue_frequency', 0)
        optimal_length = fatigue_analysis.get('optimal_session_length', 60)
        recovery_time = fatigue_analysis.get('recovery_time_needed', 15)

        report.append(f"• Frequência de alta fadiga: {high_fatigue_freq:.1f}%")
        report.append(f"• Duração ótima de sessão: {optimal_length} min")
        report.append(f"• Tempo de recuperação: {recovery_time} min")

        triggers = fatigue_analysis.get('fatigue_triggers', [])
        if triggers:
            report.append("• Gatilhos de fadiga:")
            for trigger in triggers:
                report.append(f"  - {trigger}")
        report.append("")

    # Padrões comportamentais
    patterns = analyzer.detect_behavioral_patterns(sessions)
    if patterns:
        report.append("## PADRÕES COMPORTAMENTAIS")
        report.append("-" * 25)

        for pattern in patterns:
            report.append(f"### {pattern.pattern_name}")
            report.append(f"• Frequência: {pattern.frequency:.1f}%")
            report.append(f"• Impacto: {pattern.impact_score:.1f}/10")
            report.append(f"• Descrição: {pattern.description}")

            if pattern.recommendations:
                report.append("• Recomendações:")
                for rec in pattern.recommendations:
                    report.append(f"  - {rec}")
            report.append("")

    # Otimização de cronograma
    schedule_optimization = analyzer.generate_schedule_optimization(sessions)
    if schedule_optimization:
        report.append("## CRONOGRAMA OTIMIZADO")
        report.append("-" * 22)

        optimal_hours = schedule_optimization.get('optimal_study_hours', [])
        optimal_duration = schedule_optimization.get('optimal_session_duration', 60)
        break_frequency = schedule_optimization.get('optimal_break_frequency', 2)

        report.append(f"• Horários ótimos: {', '.join(map(str, optimal_hours))}h")
        report.append(f"• Duração por sessão: {optimal_duration} min")
        report.append(f"• Pausas por hora: {break_frequency}")

        weekly_dist = schedule_optimization.get('weekly_distribution', {})
        if weekly_dist:
            report.append("• Distribuição semanal:")
            for day, sessions_count in weekly_dist.items():
                report.append(f"  - {day}: {sessions_count} sessões")
        report.append("")

    # Recomendações finais
    report.append("## RECOMENDAÇÕES PRIORITÁRIAS")
    report.append("-" * 28)

    # Gerar recomendações baseadas na análise
    priority_recommendations = generate_priority_recommendations(
        concentration_analysis, fatigue_analysis, patterns
    )

    for i, rec in enumerate(priority_recommendations, 1):
        report.append(f"{i}. {rec}")

    report.append("")
    report.append("=" * 50)
    report.append("Relatório gerado pelo Sistema de Análise Comportamental")
    report.append("Agente Concurseiro v2.0")

    return "\n".join(report)

def generate_priority_recommendations(concentration_analysis: Dict,
                                    fatigue_analysis: Dict,
                                    patterns: List[BehavioralPattern]) -> List[str]:
    """Gera recomendações prioritárias baseadas em todas as análises"""
    recommendations = []

    # Recomendações de concentração
    if concentration_analysis:
        avg_concentration = concentration_analysis.get('average_concentration', 5)
        if avg_concentration < 6:
            recommendations.append("PRIORIDADE ALTA: Implementar técnicas de melhoria de concentração (mindfulness, Pomodoro)")

        trend = concentration_analysis.get('concentration_trend', '')
        if trend == 'Decrescente':
            recommendations.append("ATENÇÃO: Concentração em declínio - revisar rotina de sono e exercícios")

    # Recomendações de fadiga
    if fatigue_analysis:
        high_fatigue_freq = fatigue_analysis.get('high_fatigue_frequency', 0)
        if high_fatigue_freq > 30:
            recommendations.append("CRÍTICO: Alta frequência de fadiga - reduzir duração das sessões")

        triggers = fatigue_analysis.get('fatigue_triggers', [])
        if triggers:
            recommendations.append(f"Eliminar gatilhos de fadiga: {', '.join(triggers[:2])}")

    # Recomendações dos padrões
    for pattern in patterns:
        if pattern.impact_score < 5 and pattern.frequency > 20:
            recommendations.append(f"Otimizar padrão '{pattern.pattern_name}' (baixo impacto, alta frequência)")

    # Recomendações gerais
    recommendations.append("Manter registro consistente de sessões para análises mais precisas")
    recommendations.append("Revisar e ajustar estratégias mensalmente baseado nos dados")

    return recommendations[:8]  # Limitar a 8 recomendações prioritárias

def create_behavioral_analytics_api():
    """Cria API para análise comportamental"""
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel
    from typing import List, Dict, Any

    app = FastAPI(title="Behavioral Analytics API")

    class SessionData(BaseModel):
        timestamp: str
        duration_minutes: int
        subject: str
        activity_type: str
        concentration_score: float
        fatigue_level: int
        productivity_score: float
        interruptions: int
        break_frequency: int
        performance_score: float
        mood_before: int
        mood_after: int
        environment_quality: int
        device_used: str
        location: str

    class AnalysisRequest(BaseModel):
        sessions: List[SessionData]
        analysis_type: str  # 'concentration', 'fatigue', 'productivity', 'patterns', 'all'

    @app.post("/analyze")
    async def analyze_behavior(request: AnalysisRequest):
        """Endpoint para análise comportamental"""
        try:
            # Converter dados para objetos StudySession
            sessions = []
            for session_data in request.sessions:
                session = StudySession(
                    timestamp=datetime.fromisoformat(session_data.timestamp),
                    duration_minutes=session_data.duration_minutes,
                    subject=session_data.subject,
                    activity_type=session_data.activity_type,
                    concentration_score=session_data.concentration_score,
                    fatigue_level=session_data.fatigue_level,
                    productivity_score=session_data.productivity_score,
                    interruptions=session_data.interruptions,
                    break_frequency=session_data.break_frequency,
                    performance_score=session_data.performance_score,
                    mood_before=session_data.mood_before,
                    mood_after=session_data.mood_after,
                    environment_quality=session_data.environment_quality,
                    device_used=session_data.device_used,
                    location=session_data.location
                )
                sessions.append(session)

            # Criar analyzer e executar análise
            analyzer = BehavioralAnalyzer()
            for session in sessions:
                analyzer.add_session(session)

            result = {}

            if request.analysis_type in ['concentration', 'all']:
                result['concentration'] = analyzer.analyze_concentration_patterns(sessions)

            if request.analysis_type in ['fatigue', 'all']:
                result['fatigue'] = analyzer.analyze_fatigue_patterns(sessions)

            if request.analysis_type in ['productivity', 'all']:
                result['productivity'] = analyzer.analyze_productivity_patterns(sessions)

            if request.analysis_type in ['patterns', 'all']:
                patterns = analyzer.detect_behavioral_patterns(sessions)
                result['patterns'] = [asdict(pattern) for pattern in patterns]

            if request.analysis_type == 'all':
                result['schedule_optimization'] = analyzer.generate_schedule_optimization(sessions)

            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/report")
    async def generate_report(request: AnalysisRequest):
        """Endpoint para gerar relatório completo"""
        try:
            # Converter dados para objetos StudySession
            sessions = []
            for session_data in request.sessions:
                session = StudySession(
                    timestamp=datetime.fromisoformat(session_data.timestamp),
                    duration_minutes=session_data.duration_minutes,
                    subject=session_data.subject,
                    activity_type=session_data.activity_type,
                    concentration_score=session_data.concentration_score,
                    fatigue_level=session_data.fatigue_level,
                    productivity_score=session_data.productivity_score,
                    interruptions=session_data.interruptions,
                    break_frequency=session_data.break_frequency,
                    performance_score=session_data.performance_score,
                    mood_before=session_data.mood_before,
                    mood_after=session_data.mood_after,
                    environment_quality=session_data.environment_quality,
                    device_used=session_data.device_used,
                    location=session_data.location
                )
                sessions.append(session)

            # Gerar relatório
            analyzer = BehavioralAnalyzer()
            for session in sessions:
                analyzer.add_session(session)

            report = export_behavioral_report(analyzer, sessions)

            return {"report": report}

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app

if __name__ == "__main__":
    create_behavioral_dashboard()
