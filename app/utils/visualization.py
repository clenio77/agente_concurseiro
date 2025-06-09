import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from typing import Dict, List

def render_progress_charts(progress_data: Dict):
    """Renderiza gráficos de progresso para o dashboard"""
    
    # Gráfico de conclusão por matéria
    if "subject_completion" in progress_data:
        st.subheader("Conclusão por Matéria")
        
        # Preparar dados
        subjects = []
        completion_percentages = []
        latest_scores = []
        
        for subject, data in progress_data["subject_completion"].items():
            subjects.append(subject)
            completion_percentages.append(data["completion_percentage"])
            latest_scores.append(data["latest_score"])
        
        # Criar DataFrame
        df = pd.DataFrame({
            "Matéria": subjects,
            "Conclusão (%)": completion_percentages,
            "Pontuação": latest_scores
        })
        
        # Gráfico de barras para conclusão
        completion_chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Conclusão (%):Q', scale=alt.Scale(domain=[0, 100])),
            y=alt.Y('Matéria:N', sort='-x'),
            color=alt.Color('Conclusão (%):Q', scale=alt.Scale(scheme='blues')),
            tooltip=['Matéria', 'Conclusão (%)', 'Pontuação']
        ).properties(
            height=30 * len(subjects)
        )
        
        st.altair_chart(completion_chart, use_container_width=True)
    
    # Gráfico de curva de aprendizado
    if "learning_curve" in progress_data and progress_data["learning_curve"]:
        st.subheader("Curva de Aprendizado")
        
        # Preparar dados
        weeks = []
        scores = []
        
        for entry in progress_data["learning_curve"]:
            weeks.append(entry["week"])
            scores.append(entry["overall_score"])
        
        # Criar DataFrame
        df = pd.DataFrame({
            "Semana": weeks,
            "Pontuação": scores
        })
        
        # Gráfico de linha para curva de aprendizado
        line_chart = alt.Chart(df).mark_line(point=True).encode(
            x='Semana:Q',
            y=alt.Y('Pontuação:Q', scale=alt.Scale(domain=[0, 100])),
            tooltip=['Semana', 'Pontuação']
        ).properties(
            height=300
        )
        
        # Adicionar linha de tendência
        trend_line = alt.Chart(df).transform_regression(
            'Semana', 'Pontuação'
        ).mark_line(color='red', strokeDash=[5, 5]).encode(
            x='Semana:Q',
            y='Pontuação:Q'
        )
        
        # Combinar gráficos
        chart = line_chart + trend_line
        
        st.altair_chart(chart, use_container_width=True)
    
    # Gráfico de radar para pontuações por matéria
    if "subject_completion" in progress_data and len(progress_data["subject_completion"]) > 2:
        st.subheader("Pontuações por Matéria")
        
        # Preparar dados
        subjects = []
        scores = []
        
        for subject, data in progress_data["subject_completion"].items():
            subjects.append(subject)
            scores.append(data["latest_score"])
        
        # Criar gráfico de radar usando matplotlib
        import matplotlib.pyplot as plt
        from math import pi
        
        # Número de variáveis
        N = len(subjects)
        
        # Ângulos para cada eixo
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]  # Fechar o círculo
        
        # Adicionar pontuações
        scores += scores[:1]  # Fechar o círculo
        
        # Criar figura
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        
        # Desenhar polígono
        ax.plot(angles, scores, linewidth=1, linestyle='solid')
        ax.fill(angles, scores, alpha=0.1)
        
        # Adicionar rótulos
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(subjects)
        
        # Adicionar linhas de grade
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(['20', '40', '60', '80', '100'])
        ax.set_ylim(0, 100)
        
        st.pyplot(fig)
    
    # Gráfico de eficiência de estudo
    if "time_tracking" in progress_data:
        st.subheader("Eficiência de Estudo")
        
        # Preparar dados
        time_data = progress_data["time_tracking"]
        
        # Criar gráfico de medidor
        import plotly.graph_objects as go
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = time_data["efficiency"] * 10,  # Multiplicar por 10 para escala de 0-10
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Eficiência de Estudo"},
            gauge = {
                'axis': {'range': [None, 10]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 3], 'color': "red"},
                    {'range': [3, 7], 'color': "yellow"},
                    {'range': [7, 10], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 7
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)

def render_prediction_charts(prediction_data: Dict):
    """Renderiza gráficos de previsão para o dashboard"""
    
    # Gráfico de previsão de pontuação
    if "predictions" in prediction_data and "expected_timeline" in prediction_data["predictions"]:
        st.subheader("Previsão de Desempenho")
        
        # Preparar dados
        timeline = prediction_data["predictions"]["expected_timeline"]
        dates = []
        scores = []
        labels = []
        
        for date, data in timeline.items():
            dates.append(date)
            scores.append(data["expected_score"])
            labels.append(data["label"])
        
        # Criar DataFrame
        df = pd.DataFrame({
            "Data": dates,
            "Pontuação Prevista": scores,
            "Marco": labels
        })
        
        # Gráfico de linha para previsão
        chart = alt.Chart(df).mark_line(point=True).encode(
            x='Data:T',
            y=alt.Y('Pontuação Prevista:Q', scale=alt.Scale(domain=[0, 100])),
            tooltip=['Data', 'Pontuação Prevista', 'Marco']
        ).properties(
            height=300
        )
        
        st.altair_chart(chart, use_container_width=True)
    
    # Gráfico de probabilidade de sucesso
    if "predictions" in prediction_data and "success_probability" in prediction_data["predictions"]:
        st.subheader("Probabilidade de Sucesso")
        
        # Obter probabilidade
        probability = prediction_data["predictions"]["success_probability"] * 100
        
        # Criar gráfico de medidor
        import plotly.graph_objects as go
        
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = probability,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Probabilidade de Sucesso (%)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 30], 'color': "red"},
                    {'range': [30, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        st.plotly_chart(fig, use_container_width=True)