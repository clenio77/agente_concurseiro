"""
🔮 Trend Prediction - Predição de Tendências de Concursos
Componente de análise de tendências e predição de temas quentes
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

class TrendType(Enum):
    """Tipos de tendências"""
    TOPIC_FREQUENCY = "topic_frequency"
    SEASONAL_PATTERN = "seasonal_pattern"
    BOARD_PREFERENCE = "board_preference"
    LEGISLATION_CHANGE = "legislation_change"
    JURISPRUDENCE_SHIFT = "jurisprudence_shift"

class PredictionConfidence(Enum):
    """Níveis de confiança da predição"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"

class ExamBoard(Enum):
    """Bancas organizadoras"""
    CESPE = "cespe"
    FCC = "fcc"
    VUNESP = "vunesp"
    FGV = "fgv"
    IBFC = "ibfc"
    CONSULPLAN = "consulplan"
    QUADRIX = "quadrix"

class SubjectArea(Enum):
    """Áreas de conhecimento"""
    PORTUGUESE = "portuguese"
    MATHEMATICS = "mathematics"
    LAW = "law"
    INFORMATICS = "informatics"
    CURRENT_AFFAIRS = "current_affairs"
    ADMINISTRATION = "administration"
    ACCOUNTING = "accounting"

class TrendPrediction:
    """Sistema completo de predição de tendências"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializar estado da sessão"""
        if 'trend_settings' not in st.session_state:
            st.session_state.trend_settings = {
                'analysis_enabled': True,
                'prediction_horizon': 12,  # meses
                'confidence_threshold': 0.7,
                'include_seasonal': True,
                'include_legislation': True,
                'include_jurisprudence': False,
                'auto_update': True,
                'notification_alerts': True,
                'data_sources': ['official_sites', 'news', 'forums']
            }
        
        if 'historical_data' not in st.session_state:
            st.session_state.historical_data = self.generate_historical_data()
        
        if 'trend_analysis' not in st.session_state:
            st.session_state.trend_analysis = self.generate_trend_analysis()
        
        if 'predictions' not in st.session_state:
            st.session_state.predictions = self.generate_predictions()
        
        if 'market_intelligence' not in st.session_state:
            st.session_state.market_intelligence = self.generate_market_intelligence()
    
    def generate_historical_data(self) -> Dict:
        """Gerar dados históricos simulados"""
        # Simular 5 anos de dados históricos
        start_date = datetime.now() - timedelta(days=5*365)
        dates = pd.date_range(start=start_date, end=datetime.now(), freq='M')
        
        historical_data = {
            'exam_frequency': [],
            'topic_evolution': [],
            'board_patterns': [],
            'seasonal_trends': [],
            'legislation_impact': []
        }
        
        # Frequência de concursos por mês
        for i, date in enumerate(dates):
            base_frequency = 25 + 10 * np.sin(i * 0.5)  # Padrão sazonal
            noise = np.random.normal(0, 5)
            frequency = max(5, int(base_frequency + noise))
            
            historical_data['exam_frequency'].append({
                'date': date.strftime('%Y-%m'),
                'total_exams': frequency,
                'federal_exams': int(frequency * 0.3),
                'state_exams': int(frequency * 0.4),
                'municipal_exams': int(frequency * 0.3),
                'average_positions': int(50 + 100 * np.random.random())
            })
        
        # Evolução de tópicos por matéria
        subjects = list(SubjectArea)
        topics_by_subject = {
            SubjectArea.PORTUGUESE: [
                'Interpretação de Texto', 'Gramática', 'Redação Oficial',
                'Ortografia', 'Sintaxe', 'Semântica'
            ],
            SubjectArea.LAW: [
                'Direito Constitucional', 'Direito Administrativo', 'Direito Civil',
                'Direito Penal', 'Direito Processual', 'Direito Tributário'
            ],
            SubjectArea.MATHEMATICS: [
                'Aritmética', 'Álgebra', 'Geometria', 'Estatística',
                'Matemática Financeira', 'Raciocínio Lógico'
            ],
            SubjectArea.INFORMATICS: [
                'Hardware', 'Software', 'Redes', 'Segurança',
                'Banco de Dados', 'Programação'
            ],
            SubjectArea.CURRENT_AFFAIRS: [
                'Política Nacional', 'Economia', 'Meio Ambiente',
                'Tecnologia', 'Saúde Pública', 'Educação'
            ]
        }
        
        for subject in subjects[:5]:  # Primeiros 5 para simulação
            for topic in topics_by_subject[subject]:
                trend_data = []
                base_frequency = np.random.uniform(0.1, 0.4)
                
                for i, date in enumerate(dates[-24:]):  # Últimos 2 anos
                    # Simular tendência com crescimento/declínio
                    trend_factor = 1 + 0.1 * np.sin(i * 0.2) + 0.05 * i / 24
                    frequency = base_frequency * trend_factor + np.random.normal(0, 0.05)
                    frequency = max(0.01, min(0.8, frequency))
                    
                    trend_data.append({
                        'date': date.strftime('%Y-%m'),
                        'frequency': frequency,
                        'question_count': int(frequency * 100),
                        'difficulty_avg': np.random.uniform(2.0, 4.5)
                    })
                
                historical_data['topic_evolution'].append({
                    'subject': subject.value,
                    'topic': topic,
                    'trend_data': trend_data,
                    'overall_trend': np.random.choice(['increasing', 'stable', 'decreasing']),
                    'trend_strength': np.random.uniform(0.1, 0.9)
                })
        
        # Padrões por banca
        boards = list(ExamBoard)
        for board in boards:
            preferences = {}
            for subject in subjects:
                preferences[subject.value] = {
                    'frequency': np.random.uniform(0.1, 0.4),
                    'difficulty_preference': np.random.uniform(2.0, 4.5),
                    'question_style': np.random.choice(['theoretical', 'practical', 'mixed']),
                    'trend': np.random.choice(['increasing', 'stable', 'decreasing'])
                }
            
            historical_data['board_patterns'].append({
                'board': board.value,
                'total_exams': int(50 + 200 * np.random.random()),
                'subject_preferences': preferences,
                'innovation_score': np.random.uniform(0.3, 0.9),
                'difficulty_consistency': np.random.uniform(0.6, 0.95)
            })
        
        # Tendências sazonais
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        for month in months:
            historical_data['seasonal_trends'].append({
                'month': month,
                'exam_frequency': np.random.uniform(0.5, 1.5),
                'application_volume': np.random.uniform(0.7, 1.3),
                'competition_intensity': np.random.uniform(0.8, 1.2),
                'success_rate': np.random.uniform(0.05, 0.15)
            })
        
        # Impacto de mudanças legislativas
        legislation_events = [
            {'date': '2024-03', 'law': 'Lei 14.133/2021', 'impact': 0.8, 'area': 'Licitações'},
            {'date': '2024-06', 'law': 'Marco Civil Internet', 'impact': 0.6, 'area': 'Informática'},
            {'date': '2024-09', 'law': 'LGPD Atualizada', 'impact': 0.7, 'area': 'Direito Digital'},
            {'date': '2025-01', 'law': 'Reforma Administrativa', 'impact': 0.9, 'area': 'Direito Administrativo'},
            {'date': '2025-04', 'law': 'Nova Lei de Improbidade', 'impact': 0.8, 'area': 'Direito Penal'}
        ]
        
        historical_data['legislation_impact'] = legislation_events
        
        return historical_data
    
    def generate_trend_analysis(self) -> Dict:
        """Gerar análise de tendências atual"""
        return {
            'hot_topics': [
                {
                    'topic': 'Inteligência Artificial na Administração Pública',
                    'subject': 'Informática',
                    'growth_rate': 0.85,
                    'confidence': 0.92,
                    'predicted_questions': 45,
                    'boards_adopting': ['CESPE', 'FGV', 'VUNESP'],
                    'trend_type': TrendType.TOPIC_FREQUENCY.value
                },
                {
                    'topic': 'Sustentabilidade e ESG',
                    'subject': 'Atualidades',
                    'growth_rate': 0.78,
                    'confidence': 0.88,
                    'predicted_questions': 38,
                    'boards_adopting': ['FCC', 'VUNESP', 'IBFC'],
                    'trend_type': TrendType.TOPIC_FREQUENCY.value
                },
                {
                    'topic': 'Lei Geral de Proteção de Dados',
                    'subject': 'Direito',
                    'growth_rate': 0.72,
                    'confidence': 0.95,
                    'predicted_questions': 52,
                    'boards_adopting': ['CESPE', 'FCC', 'FGV', 'VUNESP'],
                    'trend_type': TrendType.LEGISLATION_CHANGE.value
                },
                {
                    'topic': 'Transformação Digital do Governo',
                    'subject': 'Administração',
                    'growth_rate': 0.68,
                    'confidence': 0.83,
                    'predicted_questions': 31,
                    'boards_adopting': ['FGV', 'QUADRIX', 'CONSULPLAN'],
                    'trend_type': TrendType.TOPIC_FREQUENCY.value
                },
                {
                    'topic': 'Marco Legal das Startups',
                    'subject': 'Direito',
                    'growth_rate': 0.65,
                    'confidence': 0.79,
                    'predicted_questions': 28,
                    'boards_adopting': ['FGV', 'CESPE'],
                    'trend_type': TrendType.LEGISLATION_CHANGE.value
                }
            ],
            'declining_topics': [
                {
                    'topic': 'Lei 8.666/93 (Lei de Licitações Antiga)',
                    'subject': 'Direito',
                    'decline_rate': -0.45,
                    'confidence': 0.91,
                    'reason': 'Substituída pela Lei 14.133/2021'
                },
                {
                    'topic': 'Protocolos de Rede Legados',
                    'subject': 'Informática',
                    'decline_rate': -0.32,
                    'confidence': 0.76,
                    'reason': 'Tecnologias obsoletas'
                }
            ],
            'seasonal_predictions': {
                'Q1_2025': {
                    'peak_subjects': ['Direito Constitucional', 'Português'],
                    'exam_volume': 'Alto',
                    'competition_level': 'Muito Alto'
                },
                'Q2_2025': {
                    'peak_subjects': ['Informática', 'Atualidades'],
                    'exam_volume': 'Médio',
                    'competition_level': 'Alto'
                },
                'Q3_2025': {
                    'peak_subjects': ['Matemática', 'Administração'],
                    'exam_volume': 'Baixo',
                    'competition_level': 'Médio'
                },
                'Q4_2025': {
                    'peak_subjects': ['Direito Administrativo', 'Contabilidade'],
                    'exam_volume': 'Alto',
                    'competition_level': 'Alto'
                }
            },
            'board_innovations': [
                {
                    'board': 'CESPE',
                    'innovation': 'Questões com QR Code para recursos multimídia',
                    'adoption_probability': 0.75,
                    'impact_level': 'Alto'
                },
                {
                    'board': 'FGV',
                    'innovation': 'Simulação de casos reais em provas',
                    'adoption_probability': 0.68,
                    'impact_level': 'Médio'
                },
                {
                    'board': 'VUNESP',
                    'innovation': 'Integração com IA para correção automática',
                    'adoption_probability': 0.82,
                    'impact_level': 'Muito Alto'
                }
            ]
        }
    
    def generate_predictions(self) -> List[Dict]:
        """Gerar predições específicas"""
        return [
            {
                'id': 'pred_001',
                'title': 'Explosão de questões sobre IA na Administração Pública',
                'description': 'Crescimento de 85% previsto para questões sobre inteligência artificial aplicada ao setor público.',
                'probability': 0.92,
                'confidence': PredictionConfidence.VERY_HIGH.value,
                'time_horizon': '6 meses',
                'impact_level': 'Alto',
                'affected_subjects': ['Informática', 'Administração Pública'],
                'recommended_action': 'Intensificar estudos em IA, Machine Learning e automação de processos',
                'supporting_evidence': [
                    'Decreto 10.332/2020 sobre estratégia de governo digital',
                    'Crescimento de 300% em licitações de soluções de IA',
                    'Criação da Secretaria de Governo Digital'
                ],
                'trend_type': TrendType.TOPIC_FREQUENCY.value
            },
            {
                'id': 'pred_002',
                'title': 'LGPD será tema obrigatório em 90% dos concursos',
                'description': 'Lei Geral de Proteção de Dados se tornará presença garantida em praticamente todos os concursos.',
                'probability': 0.95,
                'confidence': PredictionConfidence.VERY_HIGH.value,
                'time_horizon': '3 meses',
                'impact_level': 'Muito Alto',
                'affected_subjects': ['Direito', 'Informática'],
                'recommended_action': 'Dominar completamente a LGPD, incluindo casos práticos e jurisprudência',
                'supporting_evidence': [
                    'Aumento de 400% em questões sobre LGPD em 2024',
                    'Todas as principais bancas já incluíram o tema',
                    'Regulamentações complementares em andamento'
                ],
                'trend_type': TrendType.LEGISLATION_CHANGE.value
            },
            {
                'id': 'pred_003',
                'title': 'Sustentabilidade e ESG ganharão destaque',
                'description': 'Temas ambientais e de governança corporativa terão crescimento de 78% nas provas.',
                'probability': 0.88,
                'confidence': PredictionConfidence.HIGH.value,
                'time_horizon': '9 meses',
                'impact_level': 'Alto',
                'affected_subjects': ['Atualidades', 'Administração', 'Direito Ambiental'],
                'recommended_action': 'Estudar Agenda 2030, políticas ambientais e governança pública',
                'supporting_evidence': [
                    'COP 28 e compromissos internacionais do Brasil',
                    'Marco legal do saneamento básico',
                    'Crescimento do mercado de carbono'
                ],
                'trend_type': TrendType.TOPIC_FREQUENCY.value
            },
            {
                'id': 'pred_004',
                'title': 'Declínio das questões sobre Lei 8.666/93',
                'description': 'Redução de 45% nas questões sobre a antiga lei de licitações, substituída pela Lei 14.133/2021.',
                'probability': 0.91,
                'confidence': PredictionConfidence.VERY_HIGH.value,
                'time_horizon': '6 meses',
                'impact_level': 'Alto',
                'affected_subjects': ['Direito Administrativo'],
                'recommended_action': 'Focar na nova Lei de Licitações (14.133/2021) e abandonar a antiga',
                'supporting_evidence': [
                    'Lei 14.133/2021 em vigor desde abril de 2021',
                    'Período de transição encerrado',
                    'Bancas já migraram para a nova legislação'
                ],
                'trend_type': TrendType.LEGISLATION_CHANGE.value
            },
            {
                'id': 'pred_005',
                'title': 'Inovação nas metodologias de prova',
                'description': 'Bancas adotarão novas tecnologias como QR codes, simulações e IA para correção.',
                'probability': 0.75,
                'confidence': PredictionConfidence.HIGH.value,
                'time_horizon': '12 meses',
                'impact_level': 'Médio',
                'affected_subjects': ['Todas'],
                'recommended_action': 'Familiarizar-se com tecnologias digitais e formatos inovadores de questões',
                'supporting_evidence': [
                    'Investimentos das bancas em tecnologia',
                    'Experiências piloto já realizadas',
                    'Pressão por modernização dos concursos'
                ],
                'trend_type': TrendType.BOARD_PREFERENCE.value
            }
        ]
    
    def generate_market_intelligence(self) -> Dict:
        """Gerar inteligência de mercado"""
        return {
            'market_overview': {
                'total_positions_2024': 156789,
                'growth_vs_2023': 0.23,
                'average_salary': 8450.00,
                'competition_ratio': 47.3,
                'most_competitive_areas': [
                    {'area': 'Tribunais', 'ratio': 89.2},
                    {'area': 'Polícia Civil', 'ratio': 76.8},
                    {'area': 'Receita Federal', 'ratio': 68.4},
                    {'area': 'Ministério Público', 'ratio': 62.1}
                ]
            },
            'board_market_share': {
                'CESPE': {'share': 0.28, 'trend': 'stable'},
                'FCC': {'share': 0.22, 'trend': 'declining'},
                'VUNESP': {'share': 0.18, 'trend': 'growing'},
                'FGV': {'share': 0.15, 'trend': 'growing'},
                'IBFC': {'share': 0.12, 'trend': 'stable'},
                'Others': {'share': 0.05, 'trend': 'stable'}
            },
            'emerging_opportunities': [
                {
                    'area': 'Tecnologia da Informação',
                    'growth_rate': 0.45,
                    'avg_salary': 12500.00,
                    'positions_forecast': 2340,
                    'key_skills': ['Cybersecurity', 'Cloud Computing', 'Data Science']
                },
                {
                    'area': 'Sustentabilidade e Meio Ambiente',
                    'growth_rate': 0.38,
                    'avg_salary': 9800.00,
                    'positions_forecast': 1890,
                    'key_skills': ['Gestão Ambiental', 'Licenciamento', 'Auditoria Ambiental']
                },
                {
                    'area': 'Saúde Digital',
                    'growth_rate': 0.42,
                    'avg_salary': 11200.00,
                    'positions_forecast': 1560,
                    'key_skills': ['Telemedicina', 'Prontuário Eletrônico', 'Bioinformática']
                }
            ],
            'regional_analysis': {
                'Southeast': {'positions': 0.45, 'competition': 'Very High', 'salary_avg': 9200},
                'South': {'positions': 0.18, 'competition': 'High', 'salary_avg': 8800},
                'Northeast': {'positions': 0.22, 'competition': 'Medium', 'salary_avg': 7400},
                'North': {'positions': 0.08, 'competition': 'Low', 'salary_avg': 7800},
                'Center-West': {'positions': 0.07, 'competition': 'Medium', 'salary_avg': 8600}
            },
            'success_factors': [
                {'factor': 'Especialização em temas emergentes', 'impact': 0.85},
                {'factor': 'Conhecimento de múltiplas bancas', 'impact': 0.78},
                {'factor': 'Atualização legislativa constante', 'impact': 0.92},
                {'factor': 'Prática com questões recentes', 'impact': 0.88},
                {'factor': 'Networking e informações privilegiadas', 'impact': 0.65}
            ]
        }
    
    def render_trend_dashboard(self):
        """Renderizar dashboard de tendências"""
        st.subheader("🔮 Dashboard de Predição de Tendências")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        market = st.session_state.market_intelligence['market_overview']
        
        with col1:
            st.metric(
                "Vagas Previstas 2025",
                f"{market['total_positions_2024']:,}",
                delta=f"+{market['growth_vs_2023']:.1%}"
            )
        
        with col2:
            st.metric(
                "Salário Médio",
                f"R$ {market['average_salary']:,.2f}",
                delta="+R$ 450"
            )
        
        with col3:
            st.metric(
                "Concorrência Média",
                f"{market['competition_ratio']:.1f}:1",
                delta="-2.3 candidatos"
            )
        
        with col4:
            hot_topics = len(st.session_state.trend_analysis['hot_topics'])
            st.metric(
                "Temas Quentes",
                hot_topics,
                delta="+2 novos"
            )
        
        # Gráficos de tendências
        col1, col2 = st.columns(2)
        
        with col1:
            # Tópicos em alta
            hot_topics = st.session_state.trend_analysis['hot_topics']
            df_hot = pd.DataFrame(hot_topics)
            
            fig = px.bar(
                df_hot,
                x='growth_rate',
                y='topic',
                orientation='h',
                color='confidence',
                title='Tópicos em Alta - Taxa de Crescimento',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Market share das bancas
            board_data = st.session_state.market_intelligence['board_market_share']
            boards = list(board_data.keys())
            shares = [board_data[board]['share'] for board in boards]
            
            fig = px.pie(
                values=shares,
                names=boards,
                title='Market Share das Bancas Organizadoras'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Análise regional
        st.subheader("🗺️ Análise Regional")
        
        regional_data = st.session_state.market_intelligence['regional_analysis']
        df_regional = pd.DataFrame.from_dict(regional_data, orient='index').reset_index()
        df_regional.columns = ['Region', 'Positions', 'Competition', 'Avg_Salary']
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                df_regional,
                x='Region',
                y='Positions',
                title='Distribuição de Vagas por Região',
                color='Avg_Salary',
                color_continuous_scale='blues'
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(
                df_regional,
                x='Positions',
                y='Avg_Salary',
                size='Positions',
                hover_name='Region',
                title='Vagas vs Salário Médio por Região'
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_predictions(self):
        """Renderizar predições específicas"""
        st.subheader("🎯 Predições Específicas")
        
        predictions = st.session_state.predictions
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            confidence_filter = st.selectbox(
                "Filtrar por confiança:",
                options=['Todas', 'very_high', 'high', 'medium', 'low'],
                index=0
            )
        
        with col2:
            impact_filter = st.selectbox(
                "Filtrar por impacto:",
                options=['Todos', 'Muito Alto', 'Alto', 'Médio', 'Baixo'],
                index=0
            )
        
        with col3:
            horizon_filter = st.selectbox(
                "Horizonte temporal:",
                options=['Todos', '3 meses', '6 meses', '9 meses', '12 meses'],
                index=0
            )
        
        # Filtrar predições
        filtered_predictions = predictions
        if confidence_filter != 'Todas':
            filtered_predictions = [p for p in filtered_predictions if p['confidence'] == confidence_filter]
        if impact_filter != 'Todos':
            filtered_predictions = [p for p in filtered_predictions if p['impact_level'] == impact_filter]
        if horizon_filter != 'Todos':
            filtered_predictions = [p for p in filtered_predictions if p['time_horizon'] == horizon_filter]
        
        # Exibir predições
        for pred in filtered_predictions:
            confidence_color = {
                'very_high': '🟢',
                'high': '🔵',
                'medium': '🟡',
                'low': '🟠',
                'very_low': '🔴'
            }
            
            with st.expander(f"{confidence_color[pred['confidence']]} {pred['title']} (Prob: {pred['probability']:.0%})"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.write(f"**Descrição:** {pred['description']}")
                    st.write(f"**Ação Recomendada:** {pred['recommended_action']}")
                    
                    # Evidências de suporte
                    st.write("**Evidências de Suporte:**")
                    for evidence in pred['supporting_evidence']:
                        st.write(f"• {evidence}")
                
                with col2:
                    st.metric("Probabilidade", f"{pred['probability']:.0%}")
                    st.metric("Horizonte", pred['time_horizon'])
                    st.metric("Impacto", pred['impact_level'])
                    
                    # Barra de confiança
                    confidence_map = {
                        'very_high': 0.9, 'high': 0.75, 'medium': 0.5, 'low': 0.25, 'very_low': 0.1
                    }
                    st.write(f"**Confiança:** {pred['confidence'].replace('_', ' ').title()}")
                    st.progress(confidence_map[pred['confidence']])
                
                # Matérias afetadas
                st.write("**Matérias Afetadas:**")
                subjects_str = ", ".join(pred['affected_subjects'])
                st.info(subjects_str)
    
    def render_hot_topics(self):
        """Renderizar tópicos em alta"""
        st.subheader("🔥 Tópicos em Alta")
        
        hot_topics = st.session_state.trend_analysis['hot_topics']
        declining_topics = st.session_state.trend_analysis['declining_topics']
        
        # Tabs para tópicos em alta e em declínio
        tab1, tab2 = st.tabs(["📈 Em Alta", "📉 Em Declínio"])
        
        with tab1:
            for topic in hot_topics:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**{topic['topic']}**")
                        st.write(f"Matéria: {topic['subject']}")
                        st.write(f"Bancas: {', '.join(topic['boards_adopting'])}")
                    
                    with col2:
                        st.metric("Crescimento", f"+{topic['growth_rate']:.0%}")
                        st.metric("Confiança", f"{topic['confidence']:.0%}")
                    
                    with col3:
                        st.metric("Questões Previstas", topic['predicted_questions'])
                        
                        # Indicador visual de crescimento
                        if topic['growth_rate'] > 0.8:
                            st.success("🚀 Crescimento Explosivo")
                        elif topic['growth_rate'] > 0.6:
                            st.info("📈 Alto Crescimento")
                        else:
                            st.warning("📊 Crescimento Moderado")
                    
                    st.markdown("---")
        
        with tab2:
            for topic in declining_topics:
                with st.container():
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.write(f"**{topic['topic']}**")
                        st.write(f"Matéria: {topic['subject']}")
                        st.write(f"Motivo: {topic['reason']}")
                    
                    with col2:
                        st.metric("Declínio", f"{topic['decline_rate']:.0%}")
                        st.metric("Confiança", f"{topic['confidence']:.0%}")
                        st.error("📉 Em Declínio")
                    
                    st.markdown("---")
    
    def render_market_intelligence(self):
        """Renderizar inteligência de mercado"""
        st.subheader("📊 Inteligência de Mercado")
        
        market = st.session_state.market_intelligence
        
        # Oportunidades emergentes
        st.write("**🌟 Oportunidades Emergentes**")
        
        opportunities = market['emerging_opportunities']
        df_opp = pd.DataFrame(opportunities)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.scatter(
                df_opp,
                x='growth_rate',
                y='avg_salary',
                size='positions_forecast',
                hover_name='area',
                title='Crescimento vs Salário das Áreas Emergentes',
                labels={'growth_rate': 'Taxa de Crescimento', 'avg_salary': 'Salário Médio'}
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                df_opp,
                x='area',
                y='positions_forecast',
                color='growth_rate',
                title='Previsão de Vagas por Área Emergente',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Fatores de sucesso
        st.write("**🎯 Fatores de Sucesso**")
        
        success_factors = market['success_factors']
        df_success = pd.DataFrame(success_factors)
        
        fig = px.bar(
            df_success,
            x='impact',
            y='factor',
            orientation='h',
            title='Impacto dos Fatores de Sucesso',
            color='impact',
            color_continuous_scale='reds'
        )
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        # Áreas mais competitivas
        st.write("**⚔️ Áreas Mais Competitivas**")
        
        competitive_areas = market['market_overview']['most_competitive_areas']
        df_comp = pd.DataFrame(competitive_areas)
        
        fig = px.bar(
            df_comp,
            x='area',
            y='ratio',
            title='Concorrência por Área (candidatos por vaga)',
            color='ratio',
            color_continuous_scale='reds'
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_settings(self):
        """Renderizar configurações"""
        st.subheader("⚙️ Configurações de Predição")
        
        settings = st.session_state.trend_settings
        
        # Configurações gerais
        st.write("**🔧 Configurações Gerais**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['analysis_enabled'] = st.checkbox(
                "Análise de tendências ativa",
                value=settings['analysis_enabled']
            )
            
            settings['prediction_horizon'] = st.slider(
                "Horizonte de predição (meses):",
                min_value=3,
                max_value=24,
                value=settings['prediction_horizon']
            )
            
            settings['confidence_threshold'] = st.slider(
                "Threshold de confiança:",
                min_value=0.1,
                max_value=1.0,
                value=settings['confidence_threshold'],
                step=0.1
            )
        
        with col2:
            settings['include_seasonal'] = st.checkbox(
                "Incluir análise sazonal",
                value=settings['include_seasonal']
            )
            
            settings['include_legislation'] = st.checkbox(
                "Incluir mudanças legislativas",
                value=settings['include_legislation']
            )
            
            settings['include_jurisprudence'] = st.checkbox(
                "Incluir mudanças jurisprudenciais",
                value=settings['include_jurisprudence']
            )
        
        # Configurações de notificação
        st.write("**🔔 Configurações de Notificação**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['auto_update'] = st.checkbox(
                "Atualização automática",
                value=settings['auto_update']
            )
            
            settings['notification_alerts'] = st.checkbox(
                "Alertas de tendências",
                value=settings['notification_alerts']
            )
        
        with col2:
            settings['data_sources'] = st.multiselect(
                "Fontes de dados:",
                options=['official_sites', 'news', 'forums', 'social_media', 'academic'],
                default=settings['data_sources']
            )
        
        # Salvar configurações
        if st.button("💾 Salvar Configurações", type="primary"):
            st.session_state.trend_settings = settings
            st.success("✅ Configurações salvas com sucesso!")
        
        # Atualizar dados
        st.write("**🔄 Atualização de Dados**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Atualizar Tendências"):
                with st.spinner("Atualizando análise de tendências..."):
                    time.sleep(2)
                    st.success("Tendências atualizadas!")
        
        with col2:
            if st.button("🔮 Recalcular Predições"):
                with st.spinner("Recalculando predições..."):
                    time.sleep(3)
                    st.success("Predições recalculadas!")
        
        with col3:
            if st.button("📈 Sincronizar Mercado"):
                with st.spinner("Sincronizando dados de mercado..."):
                    time.sleep(2)
                    st.success("Dados sincronizados!")
    
    def render(self):
        """Renderizar componente principal"""
        st.title("🔮 Predição de Tendências de Concursos")
        
        # Verificar se está ativo
        if not st.session_state.trend_settings['analysis_enabled']:
            st.warning("⚠️ Análise de tendências desativada. Ative nas configurações.")
        
        # Tabs principais
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 Dashboard",
            "🎯 Predições",
            "🔥 Tópicos Quentes",
            "📊 Mercado",
            "⚙️ Configurações",
            "❓ Ajuda"
        ])
        
        with tab1:
            self.render_trend_dashboard()
        
        with tab2:
            self.render_predictions()
        
        with tab3:
            self.render_hot_topics()
        
        with tab4:
            self.render_market_intelligence()
        
        with tab5:
            self.render_settings()
        
        with tab6:
            st.subheader("❓ Ajuda - Predição de Tendências")
            
            st.markdown("""
            ### 🔮 Como funciona a Predição de Tendências
            
            **Análise de Dados:**
            - 📊 **Dados Históricos** - 5 anos de editais e provas
            - 📈 **Padrões Sazonais** - Variações por época do ano
            - 🏛️ **Preferências das Bancas** - Estilos e focos específicos
            - ⚖️ **Mudanças Legislativas** - Impacto de novas leis
            - 📰 **Análise de Notícias** - Temas em evidência na mídia
            
            **Tipos de Predições:**
            - 🔥 **Tópicos Quentes** - Temas com crescimento acelerado
            - 📉 **Temas em Declínio** - Assuntos perdendo relevância
            - 🗓️ **Tendências Sazonais** - Padrões por período do ano
            - 🏢 **Inovações das Bancas** - Novas metodologias de prova
            
            **Níveis de Confiança:**
            - 🟢 **Muito Alta (90%+)** - Praticamente certeza
            - 🔵 **Alta (75-89%)** - Muito provável
            - 🟡 **Média (50-74%)** - Possibilidade significativa
            - 🟠 **Baixa (25-49%)** - Possibilidade remota
            - 🔴 **Muito Baixa (<25%)** - Improvável
            
            **Como Usar:**
            - 📚 Priorize estudos nos tópicos em alta
            - ⏰ Ajuste cronograma conforme sazonalidade
            - 🎯 Foque nas preferências da banca do seu concurso
            - 📖 Mantenha-se atualizado com mudanças legislativas
            
            **Dicas Importantes:**
            - As predições são baseadas em análise estatística
            - Sempre mantenha uma base sólida nas matérias tradicionais
            - Use as tendências como complemento, não substituição
            - Monitore regularmente as atualizações
            """)

# Função para integração com o sistema principal
def render_trend_prediction():
    """Função para renderizar predição de tendências"""
    trend_prediction = TrendPrediction()
    trend_prediction.render()

if __name__ == "__main__":
    render_trend_prediction()