"""
IA Preditiva para Desempenho - Fase 2
Sistema de Machine Learning para predição de aprovação e análise de desempenho
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
from typing import Dict, List, Tuple, Any
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

class AIPredictor:
    """Sistema de IA Preditiva para análise de desempenho"""
    
    def __init__(self):
        self.initialize_session_state()
        self.model_approval = None
        self.model_performance = None
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def initialize_session_state(self):
        """Inicializa estado da sessão"""
        if 'ai_predictions' not in st.session_state:
            st.session_state.ai_predictions = {}
        
        if 'user_performance_history' not in st.session_state:
            st.session_state.user_performance_history = self.generate_performance_history()
        
        if 'prediction_confidence' not in st.session_state:
            st.session_state.prediction_confidence = 0.0
        
        if 'weak_points' not in st.session_state:
            st.session_state.weak_points = []
        
        if 'recommendations' not in st.session_state:
            st.session_state.recommendations = []
    
    def generate_performance_history(self) -> List[Dict[str, Any]]:
        """Gera histórico de performance simulado"""
        materias = [
            'Português', 'Matemática', 'Direito Constitucional', 
            'Direito Administrativo', 'Informática', 'Atualidades',
            'Raciocínio Lógico', 'Legislação Específica'
        ]
        
        history = []
        base_date = datetime.now() - timedelta(days=90)
        
        for i in range(90):  # 90 dias de histórico
            date = base_date + timedelta(days=i)
            
            # Simular evolução do desempenho ao longo do tempo
            progress_factor = min(1.0, i / 60)  # Melhora gradual
            
            for materia in materias:
                # Performance base por matéria (algumas são mais difíceis)
                base_performance = {
                    'Português': 0.75,
                    'Matemática': 0.60,
                    'Direito Constitucional': 0.70,
                    'Direito Administrativo': 0.65,
                    'Informática': 0.80,
                    'Atualidades': 0.55,
                    'Raciocínio Lógico': 0.58,
                    'Legislação Específica': 0.62
                }[materia]
                
                # Adicionar variação e progresso
                performance = base_performance + (progress_factor * 0.2) + random.uniform(-0.1, 0.1)
                performance = max(0.3, min(0.95, performance))  # Limitar entre 30% e 95%
                
                questoes_resolvidas = random.randint(5, 25)
                acertos = int(questoes_resolvidas * performance)
                tempo_medio = random.uniform(1.2, 3.5)  # minutos por questão
                
                history.append({
                    'data': date,
                    'materia': materia,
                    'questoes_resolvidas': questoes_resolvidas,
                    'acertos': acertos,
                    'taxa_acerto': performance,
                    'tempo_medio_questao': tempo_medio,
                    'dificuldade_media': random.uniform(2.0, 4.5),
                    'horas_estudo': random.uniform(0.5, 4.0)
                })
        
        return history
    
    def prepare_training_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Prepara dados para treinamento dos modelos"""
        df = pd.DataFrame(st.session_state.user_performance_history)
        
        # Agregar dados por matéria e semana
        df['semana'] = df['data'].dt.isocalendar().week
        df['mes'] = df['data'].dt.month
        
        # Features para o modelo
        features_list = []
        targets_approval = []
        targets_performance = []
        
        materias = df['materia'].unique()
        
        for semana in df['semana'].unique():
            week_data = df[df['semana'] == semana]
            
            if len(week_data) < 5:  # Pular semanas com poucos dados
                continue
            
            # Calcular features agregadas
            features = []
            
            # Features gerais
            features.extend([
                week_data['questoes_resolvidas'].sum(),
                week_data['taxa_acerto'].mean(),
                week_data['tempo_medio_questao'].mean(),
                week_data['dificuldade_media'].mean(),
                week_data['horas_estudo'].sum(),
                len(week_data['materia'].unique()),  # Diversidade de matérias
                week_data['taxa_acerto'].std() or 0,  # Consistência
            ])
            
            # Features por matéria (top 5 matérias)
            for materia in materias[:5]:
                materia_data = week_data[week_data['materia'] == materia]
                if len(materia_data) > 0:
                    features.extend([
                        materia_data['taxa_acerto'].mean(),
                        materia_data['questoes_resolvidas'].sum(),
                        materia_data['tempo_medio_questao'].mean()
                    ])
                else:
                    features.extend([0, 0, 0])
            
            features_list.append(features)
            
            # Target para aprovação (baseado em performance geral)
            overall_performance = week_data['taxa_acerto'].mean()
            consistency = 1 - (week_data['taxa_acerto'].std() or 0)
            volume = min(1.0, week_data['questoes_resolvidas'].sum() / 100)
            
            approval_score = (overall_performance * 0.5 + consistency * 0.3 + volume * 0.2)
            targets_approval.append(1 if approval_score > 0.7 else 0)
            targets_performance.append(overall_performance)
        
        X = np.array(features_list)
        y_approval = np.array(targets_approval)
        y_performance = np.array(targets_performance)
        
        return train_test_split(X, y_approval, y_performance, test_size=0.2, random_state=42)
    
    def train_models(self):
        """Treina os modelos de IA"""
        try:
            X_train, X_test, y_approval_train, y_approval_test, y_perf_train, y_perf_test = self.prepare_training_data()
            
            if len(X_train) < 10:  # Dados insuficientes
                st.warning("⚠️ Dados insuficientes para treinamento. Usando modelo pré-treinado.")
                self.is_trained = False
                return
            
            # Normalizar features
            X_train_scaled = self.scaler.fit_transform(X_train)
            X_test_scaled = self.scaler.transform(X_test)
            
            # Modelo de aprovação (classificação)
            self.model_approval = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.model_approval.fit(X_train_scaled, y_approval_train)
            
            # Modelo de performance (regressão)
            self.model_performance = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                random_state=42
            )
            self.model_performance.fit(X_train_scaled, y_perf_train)
            
            # Avaliar modelos
            approval_pred = self.model_approval.predict(X_test_scaled)
            approval_accuracy = accuracy_score(y_approval_test, approval_pred)
            
            performance_pred = self.model_performance.predict(X_test_scaled)
            performance_mse = np.mean((y_perf_test - performance_pred) ** 2)
            
            st.session_state.prediction_confidence = (approval_accuracy + (1 - performance_mse)) / 2
            self.is_trained = True
            
            st.success(f"✅ Modelos treinados! Acurácia: {approval_accuracy:.2%}")
            
        except Exception as e:
            st.error(f"❌ Erro no treinamento: {str(e)}")
            self.is_trained = False
    
    def predict_approval_probability(self) -> float:
        """Prediz probabilidade de aprovação"""
        if not self.is_trained or self.model_approval is None:
            # Usar heurística simples se modelo não estiver treinado
            df = pd.DataFrame(st.session_state.user_performance_history)
            recent_data = df[df['data'] >= datetime.now() - timedelta(days=14)]
            
            if len(recent_data) == 0:
                return 0.5
            
            avg_performance = recent_data['taxa_acerto'].mean()
            consistency = 1 - (recent_data['taxa_acerto'].std() or 0)
            volume_factor = min(1.0, len(recent_data) / 50)
            
            probability = (avg_performance * 0.6 + consistency * 0.3 + volume_factor * 0.1)
            return max(0.1, min(0.9, probability))
        
        # Usar modelo treinado
        try:
            # Preparar features atuais
            df = pd.DataFrame(st.session_state.user_performance_history)
            recent_data = df[df['data'] >= datetime.now() - timedelta(days=7)]
            
            if len(recent_data) == 0:
                return 0.5
            
            # Calcular features (mesmo formato do treinamento)
            features = [
                recent_data['questoes_resolvidas'].sum(),
                recent_data['taxa_acerto'].mean(),
                recent_data['tempo_medio_questao'].mean(),
                recent_data['dificuldade_media'].mean(),
                recent_data['horas_estudo'].sum(),
                len(recent_data['materia'].unique()),
                recent_data['taxa_acerto'].std() or 0,
            ]
            
            # Adicionar features por matéria
            materias = recent_data['materia'].unique()
            for i in range(5):
                if i < len(materias):
                    materia_data = recent_data[recent_data['materia'] == materias[i]]
                    features.extend([
                        materia_data['taxa_acerto'].mean(),
                        materia_data['questoes_resolvidas'].sum(),
                        materia_data['tempo_medio_questao'].mean()
                    ])
                else:
                    features.extend([0, 0, 0])
            
            X = np.array([features])
            X_scaled = self.scaler.transform(X)
            
            probability = self.model_approval.predict_proba(X_scaled)[0][1]
            return max(0.1, min(0.9, probability))
            
        except Exception as e:
            st.error(f"Erro na predição: {str(e)}")
            return 0.5
    
    def analyze_weak_points(self) -> List[Dict[str, Any]]:
        """Analisa pontos fracos do usuário"""
        df = pd.DataFrame(st.session_state.user_performance_history)
        recent_data = df[df['data'] >= datetime.now() - timedelta(days=30)]
        
        weak_points = []
        
        # Análise por matéria
        for materia in recent_data['materia'].unique():
            materia_data = recent_data[recent_data['materia'] == materia]
            
            avg_performance = materia_data['taxa_acerto'].mean()
            consistency = 1 - (materia_data['taxa_acerto'].std() or 0)
            volume = len(materia_data)
            avg_time = materia_data['tempo_medio_questao'].mean()
            
            # Identificar problemas
            issues = []
            severity = 0
            
            if avg_performance < 0.6:
                issues.append("Taxa de acerto baixa")
                severity += 3
            
            if consistency < 0.7:
                issues.append("Performance inconsistente")
                severity += 2
            
            if volume < 10:
                issues.append("Pouco volume de questões")
                severity += 1
            
            if avg_time > 3.0:
                issues.append("Tempo por questão elevado")
                severity += 2
            
            if issues:
                weak_points.append({
                    'materia': materia,
                    'performance': avg_performance,
                    'consistency': consistency,
                    'volume': volume,
                    'avg_time': avg_time,
                    'issues': issues,
                    'severity': severity,
                    'priority': 'Alta' if severity >= 5 else 'Média' if severity >= 3 else 'Baixa'
                })
        
        # Ordenar por severidade
        weak_points.sort(key=lambda x: x['severity'], reverse=True)
        
        return weak_points[:5]  # Top 5 pontos fracos
    
    def generate_recommendations(self, weak_points: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Gera recomendações personalizadas"""
        recommendations = []
        
        for weak_point in weak_points:
            materia = weak_point['materia']
            issues = weak_point['issues']
            
            for issue in issues:
                if issue == "Taxa de acerto baixa":
                    recommendations.append({
                        'type': 'study_focus',
                        'title': f'Foque em {materia}',
                        'description': f'Dedique mais tempo estudando {materia}. Sua taxa de acerto atual é {weak_point["performance"]:.1%}.',
                        'action': f'Resolver pelo menos 20 questões de {materia} por dia',
                        'priority': weak_point['priority'],
                        'estimated_impact': 'Alto',
                        'timeframe': '2-3 semanas'
                    })
                
                elif issue == "Performance inconsistente":
                    recommendations.append({
                        'type': 'consistency',
                        'title': f'Melhore consistência em {materia}',
                        'description': f'Sua performance em {materia} varia muito. Foque em técnicas de resolução.',
                        'action': f'Revisar teoria básica de {materia} e praticar questões similares',
                        'priority': weak_point['priority'],
                        'estimated_impact': 'Médio',
                        'timeframe': '1-2 semanas'
                    })
                
                elif issue == "Tempo por questão elevado":
                    recommendations.append({
                        'type': 'speed',
                        'title': f'Acelere resolução em {materia}',
                        'description': f'Você está gastando {weak_point["avg_time"]:.1f} min por questão em {materia}.',
                        'action': f'Praticar questões cronometradas de {materia}',
                        'priority': weak_point['priority'],
                        'estimated_impact': 'Médio',
                        'timeframe': '1 semana'
                    })
                
                elif issue == "Pouco volume de questões":
                    recommendations.append({
                        'type': 'volume',
                        'title': f'Aumente volume em {materia}',
                        'description': f'Você resolveu apenas {weak_point["volume"]} questões de {materia} no último mês.',
                        'action': f'Resolver pelo menos 10 questões de {materia} por dia',
                        'priority': weak_point['priority'],
                        'estimated_impact': 'Alto',
                        'timeframe': '1 semana'
                    })
        
        # Adicionar recomendações gerais
        df = pd.DataFrame(st.session_state.user_performance_history)
        recent_data = df[df['data'] >= datetime.now() - timedelta(days=7)]
        
        if len(recent_data) < 20:
            recommendations.append({
                'type': 'general',
                'title': 'Aumente frequência de estudos',
                'description': 'Você resolveu poucas questões na última semana.',
                'action': 'Estabelecer meta de pelo menos 30 questões por dia',
                'priority': 'Alta',
                'estimated_impact': 'Alto',
                'timeframe': 'Imediato'
            })
        
        return recommendations[:8]  # Top 8 recomendações

    def render_prediction_dashboard(self):
        """Renderiza dashboard de predições"""
        st.title("🧠 IA Preditiva - Análise de Desempenho")
        st.markdown("Sistema inteligente de predição de aprovação e análise personalizada")

        # Treinar modelos se necessário
        if not self.is_trained:
            with st.spinner("🤖 Treinando modelos de IA..."):
                self.train_models()

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)

        approval_prob = self.predict_approval_probability()
        confidence = st.session_state.prediction_confidence

        with col1:
            st.metric(
                "🎯 Probabilidade de Aprovação",
                f"{approval_prob:.1%}",
                delta=f"Confiança: {confidence:.1%}" if confidence > 0 else None
            )

        with col2:
            weak_points = self.analyze_weak_points()
            st.metric(
                "⚠️ Pontos Fracos Identificados",
                len(weak_points),
                delta="Prioridade Alta" if any(wp['priority'] == 'Alta' for wp in weak_points) else "Sob Controle"
            )

        with col3:
            recommendations = self.generate_recommendations(weak_points)
            high_impact = len([r for r in recommendations if r['estimated_impact'] == 'Alto'])
            st.metric(
                "💡 Recomendações Ativas",
                len(recommendations),
                delta=f"{high_impact} Alto Impacto"
            )

        with col4:
            df = pd.DataFrame(st.session_state.user_performance_history)
            recent_performance = df[df['data'] >= datetime.now() - timedelta(days=7)]['taxa_acerto'].mean()
            st.metric(
                "📈 Performance Recente",
                f"{recent_performance:.1%}",
                delta="Última semana"
            )

        st.divider()

        # Tabs para diferentes análises
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Predição de Aprovação",
            "⚠️ Análise de Pontos Fracos",
            "💡 Recomendações Personalizadas",
            "📊 Análise Temporal"
        ])

        with tab1:
            self.render_approval_prediction(approval_prob, confidence)

        with tab2:
            self.render_weak_points_analysis(weak_points)

        with tab3:
            self.render_recommendations(recommendations)

        with tab4:
            self.render_temporal_analysis()

    def render_approval_prediction(self, probability: float, confidence: float):
        """Renderiza análise de predição de aprovação"""
        st.subheader("🎯 Análise Preditiva de Aprovação")

        # Gauge de probabilidade
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = probability * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Probabilidade de Aprovação (%)"},
            delta = {'reference': 70, 'increasing': {'color': "green"}, 'decreasing': {'color': "red"}},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))

        fig_gauge.update_layout(height=400)
        st.plotly_chart(fig_gauge, use_container_width=True)

        # Interpretação da probabilidade
        col1, col2 = st.columns(2)

        with col1:
            if probability >= 0.8:
                st.success("🎉 **Excelente!** Você está no caminho certo para a aprovação!")
                interpretation = "Sua performance indica alta probabilidade de sucesso. Continue mantendo o ritmo!"
            elif probability >= 0.6:
                st.warning("⚡ **Bom progresso!** Você está bem encaminhado, mas há espaço para melhorias.")
                interpretation = "Você está numa boa posição. Foque nos pontos fracos para aumentar suas chances."
            elif probability >= 0.4:
                st.warning("⚠️ **Atenção necessária!** Sua performance precisa de ajustes importantes.")
                interpretation = "É hora de revisar sua estratégia de estudos e focar nas áreas mais críticas."
            else:
                st.error("🚨 **Ação urgente!** Mudanças significativas são necessárias na sua preparação.")
                interpretation = "Sua preparação atual não está no nível necessário. Considere revisar completamente seu plano."

            st.write(interpretation)

        with col2:
            st.info("**Como interpretamos sua probabilidade:**")
            st.write("""
            - **80-100%**: Preparação excelente
            - **60-79%**: Boa preparação, pequenos ajustes
            - **40-59%**: Preparação média, melhorias necessárias
            - **0-39%**: Preparação insuficiente, mudanças urgentes
            """)

            if confidence > 0:
                st.write(f"**Confiança do modelo**: {confidence:.1%}")
                if confidence > 0.8:
                    st.write("✅ Alta confiabilidade")
                elif confidence > 0.6:
                    st.write("⚡ Confiabilidade moderada")
                else:
                    st.write("⚠️ Baixa confiabilidade - mais dados necessários")

    def render_weak_points_analysis(self, weak_points: List[Dict[str, Any]]):
        """Renderiza análise de pontos fracos"""
        st.subheader("⚠️ Análise de Pontos Fracos")

        if not weak_points:
            st.success("🎉 Parabéns! Não identificamos pontos fracos significativos em sua preparação.")
            st.balloons()
            return

        # Gráfico de radar dos pontos fracos
        materias = [wp['materia'] for wp in weak_points]
        performances = [wp['performance'] * 100 for wp in weak_points]
        consistencies = [wp['consistency'] * 100 for wp in weak_points]

        fig_radar = go.Figure()

        fig_radar.add_trace(go.Scatterpolar(
            r=performances,
            theta=materias,
            fill='toself',
            name='Performance (%)',
            line_color='red'
        ))

        fig_radar.add_trace(go.Scatterpolar(
            r=consistencies,
            theta=materias,
            fill='toself',
            name='Consistência (%)',
            line_color='blue'
        ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Radar de Pontos Fracos",
            height=500
        )

        st.plotly_chart(fig_radar, use_container_width=True)

        # Lista detalhada de pontos fracos
        st.write("### 📋 Detalhamento dos Pontos Fracos")

        for i, wp in enumerate(weak_points, 1):
            with st.expander(f"{i}. {wp['materia']} - Prioridade {wp['priority']}", expanded=i<=2):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Performance", f"{wp['performance']:.1%}")
                    st.metric("Consistência", f"{wp['consistency']:.1%}")

                with col2:
                    st.metric("Volume (questões)", wp['volume'])
                    st.metric("Tempo médio", f"{wp['avg_time']:.1f} min")

                with col3:
                    st.write("**Problemas identificados:**")
                    for issue in wp['issues']:
                        if "baixa" in issue.lower():
                            st.write(f"🔴 {issue}")
                        elif "inconsistente" in issue.lower():
                            st.write(f"🟡 {issue}")
                        else:
                            st.write(f"🟠 {issue}")

                # Barra de progresso da severidade
                severity_pct = min(100, (wp['severity'] / 8) * 100)
                st.progress(severity_pct / 100)
                st.caption(f"Nível de severidade: {wp['severity']}/8")

    def render_recommendations(self, recommendations: List[Dict[str, Any]]):
        """Renderiza recomendações personalizadas"""
        st.subheader("💡 Recomendações Personalizadas")

        if not recommendations:
            st.info("🎯 Sua performance está equilibrada! Continue mantendo o bom trabalho.")
            return

        # Filtros
        col1, col2, col3 = st.columns(3)

        with col1:
            priority_filter = st.selectbox(
                "Filtrar por prioridade:",
                ["Todas", "Alta", "Média", "Baixa"]
            )

        with col2:
            impact_filter = st.selectbox(
                "Filtrar por impacto:",
                ["Todos", "Alto", "Médio", "Baixo"]
            )

        with col3:
            type_filter = st.selectbox(
                "Filtrar por tipo:",
                ["Todos", "study_focus", "consistency", "speed", "volume", "general"]
            )

        # Aplicar filtros
        filtered_recs = recommendations

        if priority_filter != "Todas":
            filtered_recs = [r for r in filtered_recs if r['priority'] == priority_filter]

        if impact_filter != "Todos":
            filtered_recs = [r for r in filtered_recs if r['estimated_impact'] == impact_filter]

        if type_filter != "Todos":
            filtered_recs = [r for r in filtered_recs if r['type'] == type_filter]

        # Exibir recomendações
        for i, rec in enumerate(filtered_recs, 1):
            # Definir cor baseada na prioridade
            if rec['priority'] == 'Alta':
                border_color = "red"
                icon = "🚨"
            elif rec['priority'] == 'Média':
                border_color = "orange"
                icon = "⚡"
            else:
                border_color = "green"
                icon = "💡"

            with st.container():
                st.markdown(f"""
                <div style="border-left: 4px solid {border_color}; padding-left: 15px; margin: 10px 0;">
                    <h4>{icon} {rec['title']}</h4>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(rec['description'])
                    st.write(f"**Ação recomendada:** {rec['action']}")

                with col2:
                    st.write(f"**Prioridade:** {rec['priority']}")
                    st.write(f"**Impacto:** {rec['estimated_impact']}")

                with col3:
                    st.write(f"**Prazo:** {rec['timeframe']}")
                    if st.button(f"✅ Marcar como feito", key=f"rec_{i}"):
                        st.success("Recomendação marcada como concluída!")

                st.divider()

    def render_temporal_analysis(self):
        """Renderiza análise temporal do desempenho"""
        st.subheader("📊 Análise Temporal de Performance")

        df = pd.DataFrame(st.session_state.user_performance_history)
        df['data'] = pd.to_datetime(df['data'])

        # Gráfico de evolução temporal
        daily_performance = df.groupby('data').agg({
            'taxa_acerto': 'mean',
            'questoes_resolvidas': 'sum',
            'horas_estudo': 'sum'
        }).reset_index()

        # Suavizar com média móvel
        daily_performance['taxa_acerto_smooth'] = daily_performance['taxa_acerto'].rolling(window=7, center=True).mean()

        fig_temporal = make_subplots(
            rows=3, cols=1,
            subplot_titles=('Taxa de Acerto (%)', 'Questões Resolvidas', 'Horas de Estudo'),
            vertical_spacing=0.08
        )

        # Taxa de acerto
        fig_temporal.add_trace(
            go.Scatter(
                x=daily_performance['data'],
                y=daily_performance['taxa_acerto'] * 100,
                mode='markers',
                name='Taxa Diária',
                opacity=0.6,
                marker=dict(color='lightblue')
            ),
            row=1, col=1
        )

        fig_temporal.add_trace(
            go.Scatter(
                x=daily_performance['data'],
                y=daily_performance['taxa_acerto_smooth'] * 100,
                mode='lines',
                name='Tendência (7 dias)',
                line=dict(color='blue', width=3)
            ),
            row=1, col=1
        )

        # Questões resolvidas
        fig_temporal.add_trace(
            go.Bar(
                x=daily_performance['data'],
                y=daily_performance['questoes_resolvidas'],
                name='Questões/Dia',
                marker_color='green',
                opacity=0.7
            ),
            row=2, col=1
        )

        # Horas de estudo
        fig_temporal.add_trace(
            go.Scatter(
                x=daily_performance['data'],
                y=daily_performance['horas_estudo'],
                mode='lines+markers',
                name='Horas/Dia',
                line=dict(color='orange', width=2),
                marker=dict(size=6)
            ),
            row=3, col=1
        )

        fig_temporal.update_layout(
            height=800,
            title_text="Evolução Temporal do Desempenho",
            showlegend=True
        )

        fig_temporal.update_xaxes(title_text="Data")
        fig_temporal.update_yaxes(title_text="Taxa (%)", row=1, col=1)
        fig_temporal.update_yaxes(title_text="Questões", row=2, col=1)
        fig_temporal.update_yaxes(title_text="Horas", row=3, col=1)

        st.plotly_chart(fig_temporal, use_container_width=True)

        # Estatísticas de tendência
        col1, col2, col3 = st.columns(3)

        recent_7_days = daily_performance.tail(7)
        previous_7_days = daily_performance.tail(14).head(7)

        with col1:
            recent_avg = recent_7_days['taxa_acerto'].mean()
            previous_avg = previous_7_days['taxa_acerto'].mean()
            delta = recent_avg - previous_avg

            st.metric(
                "Performance (7 dias)",
                f"{recent_avg:.1%}",
                delta=f"{delta:+.1%}"
            )

        with col2:
            recent_volume = recent_7_days['questoes_resolvidas'].sum()
            previous_volume = previous_7_days['questoes_resolvidas'].sum()
            delta_volume = recent_volume - previous_volume

            st.metric(
                "Volume (7 dias)",
                f"{recent_volume:.0f} questões",
                delta=f"{delta_volume:+.0f}"
            )

        with col3:
            recent_hours = recent_7_days['horas_estudo'].sum()
            previous_hours = previous_7_days['horas_estudo'].sum()
            delta_hours = recent_hours - previous_hours

            st.metric(
                "Dedicação (7 dias)",
                f"{recent_hours:.1f} horas",
                delta=f"{delta_hours:+.1f}h"
            )
