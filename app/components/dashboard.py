"""
Dashboard Principal - Métricas e Analytics
Componente para exibir estatísticas de progresso do usuário
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import pandas as pd
import random

class Dashboard:
    """Classe para gerenciar o dashboard principal"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializa dados de sessão para o dashboard"""
        if 'user_stats' not in st.session_state:
            st.session_state.user_stats = self.generate_mock_data()
        
        if 'study_streak' not in st.session_state:
            st.session_state.study_streak = random.randint(3, 15)
        
        if 'total_points' not in st.session_state:
            st.session_state.total_points = random.randint(1250, 5000)
    
    def generate_mock_data(self):
        """Gera dados simulados para demonstração"""
        # Dados de progresso por matéria
        materias = ['Português', 'Matemática', 'Direito Constitucional', 
                   'Direito Administrativo', 'Raciocínio Lógico', 'Informática']
        
        progress_data = {}
        for materia in materias:
            progress_data[materia] = {
                'questoes_resolvidas': random.randint(50, 200),
                'acertos': random.randint(60, 95),
                'tempo_estudo': random.randint(10, 40),  # horas
                'ultima_atividade': datetime.now() - timedelta(days=random.randint(0, 7))
            }
        
        # Dados de atividade semanal
        dates = [(datetime.now() - timedelta(days=i)) for i in range(30, 0, -1)]
        activity_data = []
        
        for date in dates:
            activity_data.append({
                'data': date,
                'horas_estudo': random.uniform(0, 8),
                'questoes': random.randint(0, 50),
                'acertos': random.randint(60, 95)
            })
        
        return {
            'materias': progress_data,
            'atividade_diaria': activity_data
        }
    
    def render_metrics_cards(self):
        """Renderiza cards de métricas principais"""
        col1, col2, col3, col4 = st.columns(4)
        
        # Total de questões resolvidas
        total_questoes = sum([data['questoes_resolvidas'] 
                             for data in st.session_state.user_stats['materias'].values()])
        
        with col1:
            st.metric(
                label="📊 Questões Resolvidas",
                value=f"{total_questoes:,}",
                delta=f"+{random.randint(10, 50)} hoje"
            )
        
        # Média de acertos
        acertos_list = [data['acertos'] 
                       for data in st.session_state.user_stats['materias'].values()]
        media_acertos = sum(acertos_list) / len(acertos_list)
        
        with col2:
            st.metric(
                label="🎯 Taxa de Acerto",
                value=f"{media_acertos:.1f}%",
                delta=f"+{random.uniform(0.5, 2.5):.1f}% esta semana"
            )
        
        # Streak de dias
        with col3:
            st.metric(
                label="🔥 Sequência de Dias",
                value=f"{st.session_state.study_streak} dias",
                delta="Mantendo o ritmo!" if st.session_state.study_streak > 7 else "Continue assim!"
            )
        
        # Total de pontos
        with col4:
            st.metric(
                label="⭐ Pontos Totais",
                value=f"{st.session_state.total_points:,}",
                delta=f"+{random.randint(50, 200)} hoje"
            )
    
    def render_progress_chart(self):
        """Renderiza gráfico de progresso por matéria"""
        st.subheader("📈 Progresso por Matéria")
        
        # Preparar dados
        materias = list(st.session_state.user_stats['materias'].keys())
        acertos = [st.session_state.user_stats['materias'][m]['acertos'] for m in materias]
        questoes = [st.session_state.user_stats['materias'][m]['questoes_resolvidas'] for m in materias]
        
        # Criar DataFrame
        df = pd.DataFrame({
            'Matéria': materias,
            'Taxa de Acerto (%)': acertos,
            'Questões Resolvidas': questoes
        })
        
        # Gráfico de barras
        fig = px.bar(
            df, 
            x='Matéria', 
            y='Taxa de Acerto (%)',
            color='Taxa de Acerto (%)',
            color_continuous_scale='RdYlGn',
            title="Taxa de Acerto por Matéria"
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_activity_heatmap(self):
        """Renderiza heatmap de atividade diária"""
        st.subheader("🗓️ Atividade de Estudos")
        
        # Preparar dados para heatmap
        activity_data = st.session_state.user_stats['atividade_diaria']
        
        df_activity = pd.DataFrame(activity_data)
        df_activity['dia_semana'] = df_activity['data'].dt.day_name()
        df_activity['semana'] = df_activity['data'].dt.isocalendar().week
        
        # Criar heatmap
        fig = px.density_heatmap(
            df_activity,
            x='data',
            y='horas_estudo',
            title="Horas de Estudo por Dia",
            color_continuous_scale='Blues'
        )
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_performance_radar(self):
        """Renderiza gráfico radar de performance"""
        st.subheader("🎯 Radar de Performance")
        
        materias = list(st.session_state.user_stats['materias'].keys())
        acertos = [st.session_state.user_stats['materias'][m]['acertos'] for m in materias]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=acertos,
            theta=materias,
            fill='toself',
            name='Taxa de Acerto',
            line_color='rgb(0, 123, 255)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_recent_activity(self):
        """Renderiza atividade recente"""
        st.subheader("📋 Atividade Recente")
        
        # Simular atividades recentes
        activities = [
            {"acao": "Resolveu 25 questões", "materia": "Português", "tempo": "2 horas atrás"},
            {"acao": "Completou simulado", "materia": "Direito Constitucional", "tempo": "5 horas atrás"},
            {"acao": "Estudou por 3h", "materia": "Matemática", "tempo": "1 dia atrás"},
            {"acao": "Ganhou badge", "materia": "Sequência de 7 dias", "tempo": "2 dias atrás"},
            {"acao": "Revisou conteúdo", "materia": "Raciocínio Lógico", "tempo": "3 dias atrás"}
        ]
        
        for activity in activities:
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1:
                    st.write(f"**{activity['acao']}**")
                with col2:
                    st.write(activity['materia'])
                with col3:
                    st.write(f"*{activity['tempo']}*")
                st.divider()
    
    def render_goals_progress(self):
        """Renderiza progresso das metas"""
        st.subheader("🎯 Progresso das Metas")
        
        goals = [
            {"meta": "Resolver 1000 questões", "atual": 750, "total": 1000},
            {"meta": "Estudar 100 horas", "atual": 65, "total": 100},
            {"meta": "80% de acerto geral", "atual": 75, "total": 80},
            {"meta": "Completar todas as matérias", "atual": 4, "total": 6}
        ]
        
        for goal in goals:
            progress = goal['atual'] / goal['total']
            st.write(f"**{goal['meta']}**")
            st.progress(progress)
            st.write(f"{goal['atual']}/{goal['total']} ({progress*100:.1f}%)")
            st.write("")
    
    def render_dashboard(self):
        """Renderiza o dashboard completo"""
        st.title("📊 Dashboard de Progresso")
        
        # Métricas principais
        self.render_metrics_cards()
        
        st.divider()
        
        # Layout em colunas para gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_progress_chart()
            self.render_recent_activity()
        
        with col2:
            self.render_performance_radar()
            self.render_goals_progress()
        
        # Heatmap de atividade (largura completa)
        self.render_activity_heatmap()
        
        # Botão para atualizar dados
        if st.button("🔄 Atualizar Dados", type="secondary"):
            st.session_state.user_stats = self.generate_mock_data()
            st.rerun()
