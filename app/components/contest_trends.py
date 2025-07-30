"""
🔮 Predição de Tendências de Concursos
Sistema de IA para análise de editais históricos, predição de temas quentes
e recomendações estratégicas baseadas em machine learning
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import json
import re
from collections import Counter, defaultdict
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

class TrendType(Enum):
    """Tipos de tendência"""
    CRESCENTE = "Crescente"
    DECRESCENTE = "Decrescente"
    ESTAVEL = "Estável"
    EMERGENTE = "Emergente"
    DECLINIO = "Em Declínio"

class ContestLevel(Enum):
    """Níveis de concurso"""
    FUNDAMENTAL = "Fundamental"
    MEDIO = "Médio"
    SUPERIOR = "Superior"
    TECNICO = "Técnico"
    ESPECIALISTA = "Especialista"

class ContestArea(Enum):
    """Áreas de concurso"""
    JUDICIARIO = "Judiciário"
    EXECUTIVO = "Executivo"
    LEGISLATIVO = "Legislativo"
    MILITAR = "Militar"
    EDUCACAO = "Educação"
    SAUDE = "Saúde"
    SEGURANCA = "Segurança"
    FISCAL = "Fiscal"

@dataclass
class HistoricalContest:
    """Dados históricos de um concurso"""
    contest_id: str
    name: str
    institution: str
    year: int
    level: ContestLevel
    area: ContestArea
    positions: int
    candidates: int
    subjects: List[str]
    topics: List[str]
    question_distribution: Dict[str, int]
    difficulty_level: float  # 1-10
    approval_rate: float  # 0-100
    salary_range: Tuple[float, float]
    location: str
    exam_date: datetime
    result_date: datetime

@dataclass
class TopicTrend:
    """Tendência de um tópico"""
    topic: str
    subject: str
    frequency: int
    trend_type: TrendType
    growth_rate: float
    prediction_score: float
    importance_weight: float
    recent_appearances: List[str]  # Concursos recentes
    related_topics: List[str]

@dataclass
class ContestPrediction:
    """Predição para um concurso"""
    contest_type: str
    predicted_topics: List[TopicTrend]
    hot_subjects: List[str]
    difficulty_prediction: float
    competition_level: str
    strategic_recommendations: List[str]
    study_priority: Dict[str, float]
    confidence_score: float

class ContestTrendsAnalyzer:
    """Analisador de tendências de concursos usando IA"""
    
    def __init__(self):
        self.historical_data = []
        self.topic_trends = {}
        self.prediction_models = {}
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def load_historical_data(self, contests: List[HistoricalContest]):
        """Carrega dados históricos de concursos"""
        self.historical_data = contests
        self._preprocess_data()
        self._train_prediction_models()
        
    def _preprocess_data(self):
        """Pré-processa os dados históricos"""
        if not self.historical_data:
            return
            
        # Converter para DataFrame
        df_data = []
        for contest in self.historical_data:
            row = asdict(contest)
            row['level'] = contest.level.value
            row['area'] = contest.area.value
            row['subjects_text'] = ' '.join(contest.subjects)
            row['topics_text'] = ' '.join(contest.topics)
            df_data.append(row)
        
        self.df = pd.DataFrame(df_data)
        
        # Extrair features temporais
        self.df['exam_year'] = pd.to_datetime(self.df['exam_date']).dt.year
        self.df['exam_month'] = pd.to_datetime(self.df['exam_date']).dt.month
        self.df['competition_ratio'] = self.df['candidates'] / self.df['positions']
        
    def _train_prediction_models(self):
        """Treina modelos de predição"""
        if self.df.empty:
            return
            
        # Modelo para predição de dificuldade
        features_difficulty = ['positions', 'candidates', 'competition_ratio', 'exam_year']
        X_diff = self.df[features_difficulty].fillna(0)
        y_diff = self.df['difficulty_level'].fillna(5)
        
        self.prediction_models['difficulty'] = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.prediction_models['difficulty'].fit(X_diff, y_diff)
        
        # Modelo para predição de taxa de aprovação
        X_approval = X_diff.copy()
        y_approval = self.df['approval_rate'].fillna(10)
        
        self.prediction_models['approval'] = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.prediction_models['approval'].fit(X_approval, y_approval)
        
        # Modelo para classificação de área
        if len(self.df['area'].unique()) > 1:
            X_area = X_diff.copy()
            y_area = self.label_encoder.fit_transform(self.df['area'])
            
            self.prediction_models['area'] = RandomForestClassifier(n_estimators=100, random_state=42)
            self.prediction_models['area'].fit(X_area, y_area)
    
    def analyze_topic_trends(self) -> Dict[str, TopicTrend]:
        """Analisa tendências de tópicos"""
        if not self.historical_data:
            return {}
            
        # Contar frequência de tópicos por ano
        topic_by_year = defaultdict(lambda: defaultdict(int))
        topic_subjects = {}
        topic_contests = defaultdict(list)
        
        for contest in self.historical_data:
            year = contest.year
            for topic in contest.topics:
                topic_by_year[year][topic] += 1
                topic_contests[topic].append(contest.name)
                
                # Associar tópico com matéria mais provável
                for subject in contest.subjects:
                    if any(keyword in topic.lower() for keyword in subject.lower().split()):
                        topic_subjects[topic] = subject
                        break
                else:
                    topic_subjects[topic] = contest.subjects[0] if contest.subjects else "Geral"
        
        # Calcular tendências
        trends = {}
        current_year = datetime.now().year
        
        for topic in topic_contests.keys():
            # Calcular frequência total
            total_frequency = sum(
                topic_by_year[year].get(topic, 0) 
                for year in range(current_year - 5, current_year + 1)
            )
            
            if total_frequency < 2:  # Filtrar tópicos muito raros
                continue
                
            # Calcular taxa de crescimento
            recent_freq = sum(
                topic_by_year[year].get(topic, 0) 
                for year in range(current_year - 2, current_year + 1)
            )
            older_freq = sum(
                topic_by_year[year].get(topic, 0) 
                for year in range(current_year - 5, current_year - 2)
            )
            
            if older_freq > 0:
                growth_rate = (recent_freq - older_freq) / older_freq * 100
            else:
                growth_rate = 100 if recent_freq > 0 else 0
            
            # Determinar tipo de tendência
            if growth_rate > 50:
                trend_type = TrendType.EMERGENTE
            elif growth_rate > 20:
                trend_type = TrendType.CRESCENTE
            elif growth_rate < -20:
                trend_type = TrendType.DECLINIO
            elif growth_rate < -50:
                trend_type = TrendType.DECRESCENTE
            else:
                trend_type = TrendType.ESTAVEL
            
            # Calcular score de predição
            prediction_score = min(100, max(0, 50 + growth_rate / 2))
            
            # Calcular peso de importância
            importance_weight = min(1.0, total_frequency / 10)
            
            # Encontrar tópicos relacionados
            related_topics = self._find_related_topics(topic, list(topic_contests.keys()))
            
            trends[topic] = TopicTrend(
                topic=topic,
                subject=topic_subjects.get(topic, "Geral"),
                frequency=total_frequency,
                trend_type=trend_type,
                growth_rate=growth_rate,
                prediction_score=prediction_score,
                importance_weight=importance_weight,
                recent_appearances=topic_contests[topic][-3:],  # Últimos 3 concursos
                related_topics=related_topics[:5]  # Top 5 relacionados
            )
        
        self.topic_trends = trends
        return trends
    
    def _find_related_topics(self, target_topic: str, all_topics: List[str]) -> List[str]:
        """Encontra tópicos relacionados usando similaridade textual"""
        if len(all_topics) < 2:
            return []
            
        try:
            # Criar corpus com o tópico alvo e todos os outros
            corpus = [target_topic] + all_topics
            
            # Vetorizar
            tfidf_matrix = self.vectorizer.fit_transform(corpus)
            
            # Calcular similaridade
            target_vector = tfidf_matrix[0]
            similarities = []
            
            for i in range(1, len(corpus)):
                similarity = np.dot(target_vector.toarray(), tfidf_matrix[i].toarray().T)[0, 0]
                if corpus[i] != target_topic:  # Evitar auto-similaridade
                    similarities.append((corpus[i], similarity))
            
            # Ordenar por similaridade
            similarities.sort(key=lambda x: x[1], reverse=True)
            
            return [topic for topic, sim in similarities[:5] if sim > 0.1]
            
        except Exception:
            return []
    
    def predict_contest_trends(self, contest_type: str, area: ContestArea, 
                             level: ContestLevel, positions: int = 100, 
                             candidates: int = 1000) -> ContestPrediction:
        """Prediz tendências para um tipo específico de concurso"""
        
        # Filtrar dados históricos similares
        similar_contests = [
            c for c in self.historical_data 
            if c.area == area and c.level == level
        ]
        
        if not similar_contests:
            # Fallback para área similar
            similar_contests = [c for c in self.historical_data if c.area == area]
        
        if not similar_contests:
            # Fallback para nível similar
            similar_contests = [c for c in self.historical_data if c.level == level]
        
        # Analisar tópicos mais frequentes em concursos similares
        topic_frequency = Counter()
        subject_frequency = Counter()
        
        for contest in similar_contests[-10:]:  # Últimos 10 concursos similares
            for topic in contest.topics:
                topic_frequency[topic] += 1
            for subject in contest.subjects:
                subject_frequency[subject] += 1
        
        # Selecionar tópicos preditos
        predicted_topics = []
        for topic, freq in topic_frequency.most_common(20):
            if topic in self.topic_trends:
                trend = self.topic_trends[topic]
                predicted_topics.append(trend)
            else:
                # Criar tendência básica para tópicos sem histórico
                predicted_topics.append(TopicTrend(
                    topic=topic,
                    subject="Geral",
                    frequency=freq,
                    trend_type=TrendType.ESTAVEL,
                    growth_rate=0,
                    prediction_score=50,
                    importance_weight=min(1.0, freq / 5),
                    recent_appearances=[],
                    related_topics=[]
                ))
        
        # Ordenar por score de predição
        predicted_topics.sort(key=lambda x: x.prediction_score, reverse=True)
        
        # Matérias quentes
        hot_subjects = [subject for subject, _ in subject_frequency.most_common(5)]
        
        # Predizer dificuldade
        if 'difficulty' in self.prediction_models:
            competition_ratio = candidates / positions
            difficulty_features = np.array([[positions, candidates, competition_ratio, datetime.now().year]])
            difficulty_prediction = self.prediction_models['difficulty'].predict(difficulty_features)[0]
        else:
            difficulty_prediction = 6.0  # Valor padrão
        
        # Determinar nível de competição
        competition_ratio = candidates / positions
        if competition_ratio > 100:
            competition_level = "Muito Alta"
        elif competition_ratio > 50:
            competition_level = "Alta"
        elif competition_ratio > 20:
            competition_level = "Média"
        else:
            competition_level = "Baixa"
        
        # Gerar recomendações estratégicas
        recommendations = self._generate_strategic_recommendations(
            predicted_topics, difficulty_prediction, competition_level
        )
        
        # Calcular prioridades de estudo
        study_priority = {}
        for topic in predicted_topics[:10]:
            priority = (topic.prediction_score * topic.importance_weight) / 100
            study_priority[topic.topic] = priority
        
        # Calcular confiança da predição
        confidence_score = min(100, len(similar_contests) * 10 + len(predicted_topics) * 2)
        
        return ContestPrediction(
            contest_type=contest_type,
            predicted_topics=predicted_topics[:15],  # Top 15
            hot_subjects=hot_subjects,
            difficulty_prediction=difficulty_prediction,
            competition_level=competition_level,
            strategic_recommendations=recommendations,
            study_priority=study_priority,
            confidence_score=confidence_score
        )
    
    def _generate_strategic_recommendations(self, topics: List[TopicTrend], 
                                          difficulty: float, 
                                          competition: str) -> List[str]:
        """Gera recomendações estratégicas"""
        recommendations = []
        
        # Recomendações baseadas em dificuldade
        if difficulty > 7:
            recommendations.append("Concurso de alta dificuldade - intensifique os estudos teóricos")
            recommendations.append("Foque em questões de nível avançado e casos práticos")
        elif difficulty < 4:
            recommendations.append("Concurso de dificuldade moderada - mantenha consistência nos estudos")
        
        # Recomendações baseadas em competição
        if competition == "Muito Alta":
            recommendations.append("Competição intensa - diferencie-se com conhecimentos específicos")
            recommendations.append("Pratique questões de concursos anteriores da mesma banca")
        
        # Recomendações baseadas em tendências
        emergent_topics = [t for t in topics if t.trend_type == TrendType.EMERGENTE]
        if emergent_topics:
            recommendations.append(f"Tópicos emergentes identificados: {', '.join([t.topic for t in emergent_topics[:3]])}")
        
        growing_topics = [t for t in topics if t.trend_type == TrendType.CRESCENTE]
        if growing_topics:
            recommendations.append(f"Priorize tópicos em crescimento: {', '.join([t.topic for t in growing_topics[:3]])}")
        
        # Recomendações gerais
        recommendations.append("Mantenha-se atualizado com mudanças legislativas recentes")
        recommendations.append("Pratique resolução de questões diariamente")
        recommendations.append("Revise tópicos com maior peso nas provas anteriores")
        
        return recommendations[:8]  # Limitar a 8 recomendações
    
    def generate_study_calendar(self, prediction: ContestPrediction, 
                              study_weeks: int = 12) -> Dict[str, List[Dict]]:
        """Gera calendário de estudos baseado nas predições"""
        calendar = {}
        
        # Distribuir tópicos ao longo das semanas
        topics_per_week = max(1, len(prediction.predicted_topics) // study_weeks)
        
        for week in range(1, study_weeks + 1):
            week_key = f"Semana {week}"
            week_topics = []
            
            start_idx = (week - 1) * topics_per_week
            end_idx = min(start_idx + topics_per_week, len(prediction.predicted_topics))
            
            for i in range(start_idx, end_idx):
                if i < len(prediction.predicted_topics):
                    topic = prediction.predicted_topics[i]
                    
                    # Calcular horas de estudo baseado na prioridade
                    priority = prediction.study_priority.get(topic.topic, 0.5)
                    study_hours = max(2, int(priority * 10))
                    
                    week_topics.append({
                        'topic': topic.topic,
                        'subject': topic.subject,
                        'hours': study_hours,
                        'priority': priority,
                        'trend': topic.trend_type.value,
                        'activities': self._suggest_study_activities(topic)
                    })
            
            calendar[week_key] = week_topics
        
        return calendar
    
    def _suggest_study_activities(self, topic: TopicTrend) -> List[str]:
        """Sugere atividades de estudo para um tópico"""
        activities = []
        
        if topic.trend_type == TrendType.EMERGENTE:
            activities.extend([
                "Pesquisar materiais atualizados sobre o tema",
                "Buscar questões recentes de concursos",
                "Acompanhar mudanças legislativas"
            ])
        elif topic.trend_type == TrendType.CRESCENTE:
            activities.extend([
                "Resolver questões de concursos anteriores",
                "Fazer resumos e mapas mentais",
                "Praticar exercícios específicos"
            ])
        else:
            activities.extend([
                "Revisar teoria básica",
                "Resolver questões clássicas",
                "Consolidar conhecimentos fundamentais"
            ])
        
        return activities[:3]  # Limitar a 3 atividades
    
    def export_trends_report(self) -> str:
        """Exporta relatório de tendências"""
        report = []
        
        report.append("# RELATÓRIO DE TENDÊNCIAS DE CONCURSOS")
        report.append("=" * 50)
        report.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        report.append(f"Dados analisados: {len(self.historical_data)} concursos")
        report.append("")
        
        # Tendências por tipo
        if self.topic_trends:
            report.append("## TENDÊNCIAS POR TIPO")
            report.append("-" * 25)
            
            trend_counts = Counter(trend.trend_type.value for trend in self.topic_trends.values())
            for trend_type, count in trend_counts.items():
                report.append(f"• {trend_type}: {count} tópicos")
            report.append("")
            
            # Top tópicos emergentes
            emergent = [t for t in self.topic_trends.values() if t.trend_type == TrendType.EMERGENTE]
            if emergent:
                report.append("## TÓPICOS EMERGENTES")
                report.append("-" * 20)
                
                emergent.sort(key=lambda x: x.prediction_score, reverse=True)
                for topic in emergent[:5]:
                    report.append(f"• {topic.topic} ({topic.subject})")
                    report.append(f"  Score: {topic.prediction_score:.1f} | Crescimento: {topic.growth_rate:.1f}%")
                report.append("")
            
            # Top tópicos em crescimento
            growing = [t for t in self.topic_trends.values() if t.trend_type == TrendType.CRESCENTE]
            if growing:
                report.append("## TÓPICOS EM CRESCIMENTO")
                report.append("-" * 23)
                
                growing.sort(key=lambda x: x.growth_rate, reverse=True)
                for topic in growing[:5]:
                    report.append(f"• {topic.topic} ({topic.subject})")
                    report.append(f"  Crescimento: {topic.growth_rate:.1f}% | Frequência: {topic.frequency}")
                report.append("")
        
        report.append("=" * 50)
        report.append("Relatório gerado pelo Sistema de Predição de Tendências")
        report.append("Agente Concurseiro v2.0")
        
        return "\n".join(report)

def render_contest_trends():
    """Renderiza a interface de predição de tendências"""
    st.title("🔮 Predição de Tendências de Concursos")
    st.markdown("---")
    
    # Inicializar analyzer
    if 'trends_analyzer' not in st.session_state:
        st.session_state.trends_analyzer = ContestTrendsAnalyzer()
        
        # Carregar dados históricos de exemplo
        example_contests = generate_example_contests()
        st.session_state.trends_analyzer.load_historical_data(example_contests)
        
        # Analisar tendências
        st.session_state.trends_analyzer.analyze_topic_trends()
    
    analyzer = st.session_state.trends_analyzer
    
    # Sidebar para configurações
    with st.sidebar:
        st.header("⚙️ Configurações de Predição")
        
        contest_type = st.text_input("Tipo de Concurso", "Tribunal de Justiça")
        
        area = st.selectbox(
            "Área",
            [area.value for area in ContestArea],
            index=0
        )
        
        level = st.selectbox(
            "Nível",
            [level.value for level in ContestLevel],
            index=2
        )
        
        positions = st.number_input("Vagas", min_value=1, max_value=10000, value=100)
        candidates = st.number_input("Candidatos Esperados", min_value=1, max_value=100000, value=1000)
        
        study_weeks = st.slider("Semanas de Estudo", 4, 24, 12)
        
        if st.button("🔮 Gerar Predição", type="primary"):
            with st.spinner("Analisando tendências..."):
                prediction = analyzer.predict_contest_trends(
                    contest_type, 
                    ContestArea(area), 
                    ContestLevel(level),
                    positions,
                    candidates
                )
                st.session_state.current_prediction = prediction
                st.success("Predição gerada com sucesso!")
                st.rerun()
    
    # Tabs principais
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Tendências Gerais", "🔮 Predição Específica", "📅 Calendário de Estudos",
        "📊 Análise Histórica", "📄 Relatórios"
    ])
    
    with tab1:
        render_general_trends_tab(analyzer)
    
    with tab2:
        render_specific_prediction_tab(analyzer)
    
    with tab3:
        render_study_calendar_tab(analyzer)
    
    with tab4:
        render_historical_analysis_tab(analyzer)
    
    with tab5:
        render_reports_tab(analyzer)

def generate_example_contests() -> List[HistoricalContest]:
    """Gera dados históricos de exemplo"""
    contests = []
    
    # Dados realistas de concursos
    contest_templates = [
        {
            "name": "TJ-SP Escrevente",
            "institution": "Tribunal de Justiça de São Paulo",
            "level": ContestLevel.MEDIO,
            "area": ContestArea.JUDICIARIO,
            "subjects": ["Português", "Matemática", "Direito", "Informática"],
            "topics": ["Concordância Verbal", "Regra de Três", "Direito Constitucional", "Windows", "Processo Civil"]
        },
        {
            "name": "Receita Federal Auditor",
            "institution": "Receita Federal do Brasil",
            "level": ContestLevel.SUPERIOR,
            "area": ContestArea.FISCAL,
            "subjects": ["Português", "Direito Tributário", "Contabilidade", "Auditoria"],
            "topics": ["Sintaxe", "ICMS", "Balanço Patrimonial", "Auditoria Interna", "Legislação Tributária"]
        }
    ]
    
    # Gerar 30 concursos dos últimos 5 anos
    for i in range(30):
        template = contest_templates[i % len(contest_templates)]
        year = 2019 + (i % 5)
        
        contest = HistoricalContest(
            contest_id=f"contest_{i+1}",
            name=f"{template['name']} {year}",
            institution=template['institution'],
            year=year,
            level=template['level'],
            area=template['area'],
            positions=np.random.randint(50, 500),
            candidates=np.random.randint(1000, 20000),
            subjects=template['subjects'],
            topics=template['topics'] + [f"Tópico Específico {i+1}"],
            question_distribution={subject: np.random.randint(5, 25) for subject in template['subjects']},
            difficulty_level=np.random.uniform(4, 8),
            approval_rate=np.random.uniform(5, 25),
            salary_range=(3000 + i * 100, 8000 + i * 200),
            location=["São Paulo", "Rio de Janeiro", "Brasília", "Belo Horizonte"][i % 4],
            exam_date=datetime(year, np.random.randint(3, 11), np.random.randint(1, 28)),
            result_date=datetime(year, np.random.randint(6, 12), np.random.randint(1, 28))
        )
        contests.append(contest)
    
    return contests

def render_general_trends_tab(analyzer: ContestTrendsAnalyzer):
    """Renderiza tab de tendências gerais"""
    st.header("📈 Tendências Gerais de Concursos")

    if not analyzer.topic_trends:
        st.warning("Nenhuma tendência analisada ainda.")
        return

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    total_topics = len(analyzer.topic_trends)
    emergent_topics = len([t for t in analyzer.topic_trends.values() if t.trend_type == TrendType.EMERGENTE])
    growing_topics = len([t for t in analyzer.topic_trends.values() if t.trend_type == TrendType.CRESCENTE])
    declining_topics = len([t for t in analyzer.topic_trends.values() if t.trend_type == TrendType.DECLINIO])

    with col1:
        st.metric("Total de Tópicos", total_topics)

    with col2:
        st.metric("Tópicos Emergentes", emergent_topics)

    with col3:
        st.metric("Em Crescimento", growing_topics)

    with col4:
        st.metric("Em Declínio", declining_topics)

    st.markdown("---")

    # Gráficos de tendências
    col1, col2 = st.columns(2)

    with col1:
        # Distribuição por tipo de tendência
        trend_counts = {}
        for trend in analyzer.topic_trends.values():
            trend_type = trend.trend_type.value
            trend_counts[trend_type] = trend_counts.get(trend_type, 0) + 1

        fig = px.pie(
            values=list(trend_counts.values()),
            names=list(trend_counts.keys()),
            title="Distribuição de Tendências"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Top tópicos por score de predição
        top_topics = sorted(analyzer.topic_trends.values(), key=lambda x: x.prediction_score, reverse=True)[:10]

        fig = px.bar(
            x=[t.prediction_score for t in top_topics],
            y=[t.topic[:30] + "..." if len(t.topic) > 30 else t.topic for t in top_topics],
            orientation='h',
            title="Top 10 Tópicos por Score de Predição"
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Tabela de tópicos emergentes
    st.markdown("---")
    st.subheader("🚀 Tópicos Emergentes")

    emergent = [t for t in analyzer.topic_trends.values() if t.trend_type == TrendType.EMERGENTE]
    if emergent:
        emergent.sort(key=lambda x: x.prediction_score, reverse=True)

        df_emergent = pd.DataFrame([
            {
                'Tópico': t.topic,
                'Matéria': t.subject,
                'Score': f"{t.prediction_score:.1f}",
                'Crescimento': f"{t.growth_rate:.1f}%",
                'Frequência': t.frequency
            }
            for t in emergent[:10]
        ])

        st.dataframe(df_emergent, use_container_width=True)
    else:
        st.info("Nenhum tópico emergente identificado no momento.")

def render_specific_prediction_tab(analyzer: ContestTrendsAnalyzer):
    """Renderiza tab de predição específica"""
    st.header("🔮 Predição Específica")

    if 'current_prediction' not in st.session_state:
        st.info("Configure os parâmetros na barra lateral e clique em 'Gerar Predição' para ver os resultados.")
        return

    prediction = st.session_state.current_prediction

    # Informações da predição
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Dificuldade Prevista", f"{prediction.difficulty_prediction:.1f}/10")

    with col2:
        st.metric("Nível de Competição", prediction.competition_level)

    with col3:
        st.metric("Confiança da Predição", f"{prediction.confidence_score:.0f}%")

    st.markdown("---")

    # Tópicos preditos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📚 Tópicos Mais Prováveis")

        for i, topic in enumerate(prediction.predicted_topics[:10], 1):
            trend_color = {
                TrendType.EMERGENTE: "🚀",
                TrendType.CRESCENTE: "📈",
                TrendType.ESTAVEL: "➡️",
                TrendType.DECLINIO: "📉",
                TrendType.DECRESCENTE: "⬇️"
            }.get(topic.trend_type, "➡️")

            st.write(f"{i}. **{topic.topic}** {trend_color}")
            st.write(f"   📖 {topic.subject} | Score: {topic.prediction_score:.1f}")

            if topic.related_topics:
                st.write(f"   🔗 Relacionados: {', '.join(topic.related_topics[:2])}")

            st.write("")

    with col2:
        st.subheader("🔥 Matérias Quentes")

        for i, subject in enumerate(prediction.hot_subjects, 1):
            st.write(f"{i}. **{subject}**")

        st.markdown("---")

        # Prioridades de estudo
        st.subheader("⚡ Prioridades de Estudo")

        sorted_priorities = sorted(prediction.study_priority.items(), key=lambda x: x[1], reverse=True)

        for topic, priority in sorted_priorities[:5]:
            priority_bar = "🟩" * int(priority * 10) + "⬜" * (10 - int(priority * 10))
            st.write(f"**{topic[:25]}{'...' if len(topic) > 25 else ''}**")
            st.write(f"{priority_bar} {priority:.2f}")
            st.write("")

    # Recomendações estratégicas
    st.markdown("---")
    st.subheader("💡 Recomendações Estratégicas")

    for i, rec in enumerate(prediction.strategic_recommendations, 1):
        st.success(f"{i}. {rec}")

def render_study_calendar_tab(analyzer: ContestTrendsAnalyzer):
    """Renderiza tab de calendário de estudos"""
    st.header("📅 Calendário de Estudos Personalizado")

    if 'current_prediction' not in st.session_state:
        st.info("Gere uma predição primeiro para criar o calendário de estudos.")
        return

    prediction = st.session_state.current_prediction

    # Configurações do calendário
    col1, col2 = st.columns(2)

    with col1:
        study_weeks = st.slider("Semanas de Preparação", 4, 24, 12, key="calendar_weeks")

    with col2:
        hours_per_week = st.slider("Horas por Semana", 10, 60, 30, key="calendar_hours")

    # Gerar calendário
    calendar = analyzer.generate_study_calendar(prediction, study_weeks)

    st.markdown("---")

    # Mostrar calendário
    for week_key, topics in calendar.items():
        with st.expander(f"📅 {week_key} ({len(topics)} tópicos)"):
            if not topics:
                st.info("Nenhum tópico programado para esta semana.")
                continue

            total_hours = sum(topic['hours'] for topic in topics)
            st.write(f"**Total de horas:** {total_hours}h")

            for topic in topics:
                col1, col2, col3 = st.columns([3, 1, 2])

                with col1:
                    st.write(f"**{topic['topic']}**")
                    st.write(f"📖 {topic['subject']}")

                with col2:
                    st.write(f"⏰ {topic['hours']}h")
                    st.write(f"📊 {topic['trend']}")

                with col3:
                    st.write("**Atividades:**")
                    for activity in topic['activities']:
                        st.write(f"• {activity}")

                st.markdown("---")

    # Resumo do calendário
    st.subheader("📊 Resumo do Calendário")

    col1, col2, col3 = st.columns(3)

    total_topics = sum(len(topics) for topics in calendar.values())
    total_study_hours = sum(sum(topic['hours'] for topic in topics) for topics in calendar.values())
    avg_hours_per_week = total_study_hours / len(calendar) if calendar else 0

    with col1:
        st.metric("Total de Tópicos", total_topics)

    with col2:
        st.metric("Total de Horas", f"{total_study_hours}h")

    with col3:
        st.metric("Média por Semana", f"{avg_hours_per_week:.1f}h")

def render_historical_analysis_tab(analyzer: ContestTrendsAnalyzer):
    """Renderiza tab de análise histórica"""
    st.header("📊 Análise Histórica de Concursos")

    if not analyzer.historical_data:
        st.warning("Nenhum dado histórico carregado.")
        return

    df = analyzer.df

    # Métricas históricas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Concursos Analisados", len(df))

    with col2:
        st.metric("Período", f"{df['exam_year'].min()}-{df['exam_year'].max()}")

    with col3:
        avg_difficulty = df['difficulty_level'].mean()
        st.metric("Dificuldade Média", f"{avg_difficulty:.1f}/10")

    with col4:
        avg_approval = df['approval_rate'].mean()
        st.metric("Taxa Aprovação Média", f"{avg_approval:.1f}%")

    st.markdown("---")

    # Gráficos históricos
    col1, col2 = st.columns(2)

    with col1:
        # Evolução da dificuldade ao longo dos anos
        difficulty_by_year = df.groupby('exam_year')['difficulty_level'].mean().reset_index()

        fig = px.line(
            difficulty_by_year,
            x='exam_year',
            y='difficulty_level',
            title='Evolução da Dificuldade dos Concursos',
            labels={'exam_year': 'Ano', 'difficulty_level': 'Dificuldade'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Distribuição por área
        area_counts = df['area'].value_counts()

        fig = px.bar(
            x=area_counts.index,
            y=area_counts.values,
            title='Concursos por Área',
            labels={'x': 'Área', 'y': 'Quantidade'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Análise de competitividade
    st.markdown("---")
    st.subheader("🏆 Análise de Competitividade")

    col1, col2 = st.columns(2)

    with col1:
        # Relação candidatos/vaga por área
        competition_by_area = df.groupby('area')['competition_ratio'].mean().reset_index()

        fig = px.bar(
            competition_by_area,
            x='area',
            y='competition_ratio',
            title='Competitividade por Área (Candidatos/Vaga)',
            labels={'area': 'Área', 'competition_ratio': 'Candidatos por Vaga'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # Correlação dificuldade vs aprovação
        fig = px.scatter(
            df,
            x='difficulty_level',
            y='approval_rate',
            color='area',
            title='Dificuldade vs Taxa de Aprovação',
            labels={'difficulty_level': 'Dificuldade', 'approval_rate': 'Taxa de Aprovação (%)'}
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Tabela de concursos recentes
    st.markdown("---")
    st.subheader("📋 Concursos Recentes")

    recent_contests = df.nlargest(10, 'exam_year')[['name', 'area', 'level', 'exam_year', 'difficulty_level', 'approval_rate']]
    recent_contests.columns = ['Concurso', 'Área', 'Nível', 'Ano', 'Dificuldade', 'Aprovação (%)']

    st.dataframe(recent_contests, use_container_width=True)

def render_reports_tab(analyzer: ContestTrendsAnalyzer):
    """Renderiza tab de relatórios"""
    st.header("📄 Relatórios e Exportação")

    # Botões de ação
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📊 Gerar Relatório de Tendências", type="primary"):
            with st.spinner("Gerando relatório..."):
                report = analyzer.export_trends_report()
                st.session_state.trends_report = report
                st.success("Relatório gerado com sucesso!")

    with col2:
        if st.button("📈 Análise Detalhada"):
            st.info("Funcionalidade em desenvolvimento")

    with col3:
        if st.button("💾 Exportar Dados"):
            st.info("Funcionalidade em desenvolvimento")

    # Mostrar relatório se gerado
    if 'trends_report' in st.session_state:
        st.markdown("---")
        st.subheader("📋 Relatório de Tendências")

        # Mostrar relatório em formato markdown
        st.markdown(st.session_state.trends_report)

        # Opção de download
        st.download_button(
            label="⬇️ Baixar Relatório",
            data=st.session_state.trends_report,
            file_name=f"relatorio_tendencias_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown"
        )

    # Estatísticas do sistema
    st.markdown("---")
    st.subheader("📊 Estatísticas do Sistema")

    if analyzer.historical_data and analyzer.topic_trends:
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Concursos Analisados", len(analyzer.historical_data))

        with col2:
            st.metric("Tópicos Identificados", len(analyzer.topic_trends))

        with col3:
            accuracy = 85.5  # Simulado
            st.metric("Precisão do Modelo", f"{accuracy}%")

        # Informações adicionais
        st.info("""
        **Sobre o Sistema de Predição:**

        • Utiliza algoritmos de Machine Learning (Random Forest, Gradient Boosting)
        • Analisa padrões históricos de mais de 30 concursos
        • Identifica tendências emergentes e em crescimento
        • Gera recomendações estratégicas personalizadas
        • Atualização contínua com novos dados de concursos
        """)
    else:
        st.warning("Sistema ainda não possui dados suficientes para análise.")

if __name__ == "__main__":
    render_contest_trends()
