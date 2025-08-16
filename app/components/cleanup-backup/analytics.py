"""
Página de Analytics e Predições de Desempenho
"""

import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render_analytics_page():
    """
    Renderiza a página de análise de desempenho e predição.
    As importações são feitas aqui dentro para evitar importações circulares.
    """
    from app.utils.performance_predictor import PerformancePredictor
    from tools.recommendation_tool import RecommendationTool

    st.title("📊 Analytics e Predições de Desempenho")
    st.markdown("Análise avançada do seu progresso e predições baseadas em IA")

    # Carregar dados do usuário
    user_data = _load_user_data()

    # Inicializar ferramentas
    predictor = PerformancePredictor()
    recommender = RecommendationTool()

    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "🎯 Predição de Desempenho",
        "💡 Recomendações IA",
        "📈 Análise Detalhada",
        "🔮 Simulação de Cenários"
    ])

    with tab1:
        render_performance_prediction(predictor, user_data)

    with tab2:
        render_ai_recommendations(recommender, user_data)

    with tab3:
        render_detailed_analysis(predictor, user_data)

    with tab4:
        render_scenario_simulation(predictor, user_data)

def render_performance_prediction(predictor, user_data):
    """Renderiza predições de desempenho"""

    st.subheader("🎯 Predição de Desempenho na Prova")

    # Configurações da predição
    col1, col2, col3 = st.columns(3)

    with col1:
        target_banca = st.selectbox(
            "Banca do Concurso",
            ["CESPE", "FCC", "VUNESP", "FGV", "IBFC"],
            index=0
        )

    with col2:
        days_until_exam = st.number_input(
            "Dias até a Prova",
            min_value=1,
            max_value=365,
            value=90
        )

    with col3:
        if st.button("🔮 Gerar Predição", use_container_width=True):
            st.session_state.prediction_generated = True

    if st.session_state.get('prediction_generated', False):
        with st.spinner("🤖 Analisando dados e gerando predição..."):
            # Gerar predição
            prediction = predictor.predict_exam_performance(
                user_data, target_banca, days_until_exam
            )

            # Exibir resultado principal
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📊 Pontuação Prevista",
                    f"{prediction.predicted_score:.1f}%",
                    delta=f"Confiança: {prediction.confidence:.0f}%"
                )

            with col2:
                improvement = prediction.improvement_potential
                st.metric(
                    "📈 Potencial de Melhoria",
                    f"{improvement:.1f}%",
                    delta="Com estudo focado"
                )

            with col3:
                # Determinar status baseado na pontuação
                if prediction.predicted_score >= 80:
                    status = "🌟 Excelente"
                elif prediction.predicted_score >= 70:
                    status = "✅ Aprovável"
                elif prediction.predicted_score >= 60:
                    status = "⚠️ Limítrofe"
                else:
                    status = "🚨 Risco"

                st.metric("🎯 Status", status)

            # Gráfico de distribuição de probabilidades
            st.subheader("📊 Distribuição de Probabilidades")

            prob_data = prediction.probability_ranges
            ranges = list(prob_data.keys())
            probabilities = [prob_data[r] * 100 for r in ranges]

            fig = px.bar(
                x=ranges,
                y=probabilities,
                title="Probabilidade por Faixa de Pontuação",
                labels={'x': 'Faixa de Pontuação (%)', 'y': 'Probabilidade (%)'},
                color=probabilities,
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            # Recomendações da predição
            if prediction.recommendations:
                st.subheader("💡 Recomendações Baseadas na Predição")
                for i, rec in enumerate(prediction.recommendations, 1):
                    st.markdown(f"**{i}.** {rec}")

            # Fatores de risco
            if prediction.risk_factors:
                st.subheader("⚠️ Fatores de Risco Identificados")
                for risk in prediction.risk_factors:
                    st.warning(risk)

def render_ai_recommendations(recommender, user_data):
    """Renderiza recomendações da IA"""

    st.subheader("💡 Recomendações Personalizadas por IA")

    # Gerar recomendações
    with st.spinner("🤖 Analisando seu perfil e gerando recomendações..."):
        try:
            recommendations_json = recommender._run(
                "generate_recommendations",
                json.dumps({"user_data": user_data})
            )
            recommendations = json.loads(recommendations_json)

            if "error" in recommendations:
                st.error(f"Erro ao gerar recomendações: {recommendations['error']}")
                return

            # Filtrar por categoria
            categories = {
                "🎯 Foco de Estudo": [
                    r for r in recommendations if r['type'] == 'study_focus'
                ],
                "⏰ Cronograma": [r for r in recommendations if r['type'] == 'schedule'],
                "🧠 Técnicas": [r for r in recommendations if r['type'] == 'technique'],
                "💪 Motivação": [r for r in recommendations if r['type'] == 'motivation'],
                "📚 Materiais": [r for r in recommendations if r['type'] == 'material']
            }

            # Exibir por categoria
            for category, recs in categories.items():
                if recs:
                    st.markdown(f"### {category}")

                    for rec in recs:
                        # Cor baseada na prioridade
                        if rec['priority'] == 'high':
                            priority_color = "🔴"
                        elif rec['priority'] == 'medium':
                            priority_color = "🟡"
                        else:
                            priority_color = "🟢"

                        with st.expander(
                            f"{priority_color} {rec['title']} "
                            f"(Confiança: {rec['confidence']:.0%})"
                        ):
                            st.write(f"**Descrição:** {rec['description']}")
                            st.write(f"**Ação:** {rec['action']}")
                            st.write(f"**Impacto Estimado:** {rec['estimated_impact']}")

                            # Tags
                            if rec['tags']:
                                st.write(
                                    "**Tags:** "
                                    + " • ".join([f"`{tag}`" for tag in rec['tags']])
                                )

            # Dicas rápidas
            st.markdown("### ⚡ Dicas Rápidas")

            user_level = _determine_user_level(user_data)
            tips_json = recommender._run(
                "get_quick_tips", json.dumps({"user_level": user_level})
            )
            tips = json.loads(tips_json)

            for tip in tips:
                st.info(tip['tip'])

        except Exception as e:
            st.error(f"Erro ao carregar recomendações: {str(e)}")

def render_detailed_analysis(predictor, user_data):
    """Renderiza análise detalhada"""

    st.subheader("📈 Análise Detalhada de Desempenho")

    # Analisar métricas atuais
    metrics = predictor.analyze_performance(user_data)

    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📊 Pontuação Geral", f"{metrics.overall_score:.1f}%")

    with col2:
        st.metric("🎯 Consistência", f"{metrics.consistency_score:.1f}%")

    with col3:
        trend_emoji = "📈" if metrics.improvement_rate > 0 else "📉" if metrics.improvement_rate < 0 else "➡️"
        st.metric(
            "📈 Taxa de Melhoria", f"{metrics.improvement_rate:.1f}", delta=trend_emoji
        )

    with col4:
        st.metric("⚡ Eficiência", f"{metrics.study_efficiency:.1f}")

    # Análise por matéria
    st.subheader("📚 Desempenho por Matéria")

    if metrics.subject_scores:
        # Criar DataFrame para visualização
        subject_df = pd.DataFrame([
            {
                'Matéria': subject,
                'Pontuação': score,
                'Status': 'Forte' if score >= 80 else 'Médio' if score >= 60 else 'Fraco'
            }
            for subject, score in metrics.subject_scores.items()
        ])

        # Gráfico de barras
        fig = px.bar(
            subject_df,
            x='Matéria',
            y='Pontuação',
            color='Status',
            color_discrete_map={'Forte': 'green', 'Médio': 'orange', 'Fraco': 'red'},
            title="Pontuação por Matéria"
        )
        fig.add_hline(
            y=60, line_dash="dash", line_color="red", annotation_text="Linha de Aprovação"
        )
        fig.add_hline(y=80, line_dash="dash", line_color="green", annotation_text="Excelência")
        st.plotly_chart(fig, use_container_width=True)

    # Áreas de atenção
    col1, col2 = st.columns(2)

    with col1:
        if metrics.weak_areas:
            st.subheader("⚠️ Áreas que Precisam de Atenção")
            for area in metrics.weak_areas:
                st.error(f"📉 {area}")
        else:
            st.success("✅ Nenhuma área crítica identificada!")

    with col2:
        if metrics.strong_areas:
            st.subheader("🌟 Suas Áreas Fortes")
            for area in metrics.strong_areas:
                st.success(f"💪 {area}")
        else:
            st.info("Continue estudando para desenvolver áreas fortes!")

def render_scenario_simulation(predictor, user_data):
    """Renderiza simulação de cenários"""

    st.subheader("🔮 Simulação de Cenários")
    st.markdown("Veja como diferentes estratégias podem afetar seu desempenho")

    # Configurações do cenário
    st.markdown("### ⚙️ Configurar Cenário")

    col1, col2 = st.columns(2)

    with col1:
        extra_hours = st.slider(
            "Horas extras de estudo por semana",
            min_value=0,
            max_value=20,
            value=0,
            step=2
        )

        focus_subject = st.selectbox(
            "Matéria de foco extra",
            ["Nenhuma"] + list(user_data.get('subject_progress', {}).keys())
        )

    with col2:
        study_intensity = st.selectbox(
            "Intensidade de estudo",
            ["Normal", "Intensiva", "Máxima"]
        )

        technique_improvement = st.slider(
            "Melhoria nas técnicas de estudo (%)",
            min_value=0,
            max_value=50,
            value=0,
            step=5
        )

    if st.button("🚀 Simular Cenário", use_container_width=True):
        with st.spinner("🔄 Simulando cenário..."):
            # Simular modificações nos dados
            modified_data = user_data.copy()

            # Aplicar modificações
            current_hours = modified_data.get('total_study_hours', 40)
            modified_data['total_study_hours'] = current_hours + (extra_hours * 4)  # 4 semanas

            # Simular melhoria na matéria de foco
            if focus_subject != "Nenhuma" and 'subject_progress' in modified_data:
                if focus_subject in modified_data['subject_progress']:
                    current_score = modified_data['subject_progress'][focus_subject].get(
                        'last_score', 60
                    )
                    improvement = min(15, extra_hours * 2)  # Máximo 15 pontos de melhoria
                    modified_data['subject_progress'][focus_subject]['last_score'] = min(
                        100, current_score + improvement
                    )

            # Aplicar melhoria geral baseada na intensidade
            intensity_multiplier = {'Normal': 1.0, 'Intensiva': 1.2, 'Máxima': 1.5}
            multiplier = intensity_multiplier[study_intensity]

            # Simular melhoria geral
            if 'mock_exam_scores' in modified_data:
                for exam in modified_data['mock_exam_scores']:
                    base_improvement = technique_improvement / 100
                    exam['score'] = min(
                        100, exam['score'] * (1 + base_improvement * multiplier)
                    )

            # Gerar predições para cenário original e modificado
            original_prediction = predictor.predict_exam_performance(
                user_data, "CESPE", 90
            )
            scenario_prediction = predictor.predict_exam_performance(
                modified_data, "CESPE", 90
            )

            # Comparar resultados
            st.markdown("### 📊 Comparação de Resultados")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "📊 Cenário Atual",
                    f"{original_prediction.predicted_score:.1f}%"
                )

            with col2:
                improvement = (
                    scenario_prediction.predicted_score
                    - original_prediction.predicted_score
                )
                st.metric(
                    "🚀 Cenário Simulado",
                    f"{scenario_prediction.predicted_score:.1f}%",
                    delta=f"+{improvement:.1f}%"
                )

            with col3:
                confidence_change = (
                    scenario_prediction.confidence - original_prediction.confidence
                )
                st.metric(
                    "🎯 Mudança na Confiança",
                    f"{scenario_prediction.confidence:.0f}%",
                    delta=f"{confidence_change:+.0f}%"
                )

            # Gráfico de comparação
            comparison_data = {
                'Cenário': ['Atual', 'Simulado'],
                'Pontuação': [
                    original_prediction.predicted_score,
                    scenario_prediction.predicted_score,
                ],
                'Confiança': [
                    original_prediction.confidence,
                    scenario_prediction.confidence,
                ]
            }

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name='Pontuação Prevista',
                x=comparison_data['Cenário'],
                y=comparison_data['Pontuação'],
                yaxis='y',
                offsetgroup=1
            ))
            fig.add_trace(go.Bar(
                name='Confiança',
                x=comparison_data['Cenário'],
                y=comparison_data['Confiança'],
                yaxis='y2',
                offsetgroup=2
            ))

            fig.update_layout(
                title='Comparação: Atual vs Cenário Simulado',
                xaxis_title='Cenário',
                yaxis=dict(title='Pontuação (%)', side='left'),
                yaxis2=dict(title='Confiança (%)', side='right', overlaying='y'),
                barmode='group'
            )

            st.plotly_chart(fig, use_container_width=True)

            # Insights do cenário
            if improvement > 5:
                st.success(
                    f"🎉 Excelente! Este cenário pode melhorar sua pontuação em "
                    f"{improvement:.1f} pontos!"
                )
            elif improvement > 0:
                st.info(
                    f"📈 Melhoria moderada de {improvement:.1f} pontos com esta "
                    "estratégia."
                )
            else:
                st.warning(
                    "⚠️ Este cenário não mostra melhoria significativa. Considere "
                    "outras estratégias."
                )

def _load_user_data():
    """Carrega dados do usuário para análise"""
    try:
        with open("data/dashboard/dashboard_data.json", "r", encoding='utf-8') as f:
            return json.load(f)
    except:
        # Dados de fallback
        return {
            "total_study_hours": 80,
            "simulados_completed": 3,
            "average_score": 72,
            "consistency_score": 75,
            "current_streak": 12,
            "subject_progress": {
                "Português": {"last_score": 78},
                "Matemática": {"last_score": 65},
                "Direito": {"last_score": 82},
                "Informática": {"last_score": 85}
            },
            "mock_exam_scores": [
                {"date": "2024-01-01", "score": 65},
                {"date": "2024-01-08", "score": 70},
                {"date": "2024-01-15", "score": 75}
            ]
        }

def _determine_user_level(user_data):
    """Determina o nível do usuário baseado nos dados"""
    study_hours = user_data.get('total_study_hours', 0)
    average_score = user_data.get('average_score', 0)

    if study_hours < 20 or average_score < 50:
        return 'beginner'
    elif study_hours < 100 or average_score < 75:
        return 'intermediate'
    else:
        return 'advanced'
