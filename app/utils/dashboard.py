import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt
from datetime import datetime, timedelta

def render_dashboard():
    """Renderiza o dashboard principal"""
    st.title("Dashboard de Preparação para Concursos")
    
    # Carregar dados do dashboard (em produção, viria do banco de dados)
    try:
        with open("data/dashboard_data.json", "r") as f:
            dashboard_data = json.load(f)
    except:
        # Dados de exemplo se o arquivo não existir
        dashboard_data = {
            "progress_summary": {
                "completed_weeks": 2,
                "total_weeks": 24,
                "completion_percentage": 8.33,
                "current_phase": "Base Teórica"
            },
            "subject_progress": {
                "Português": {"completion": 15, "priority": "Alta", "hours_planned": 48, "hours_completed": 7},
                "Matemática": {"completion": 10, "priority": "Média", "hours_planned": 36, "hours_completed": 4},
                "Direito": {"completion": 5, "priority": "Alta", "hours_planned": 60, "hours_completed": 3}
            },
            "upcoming_activities": [
                {"week": 3, "activity": {"type": "Estudo", "description": "Revisão de gramática", "duration": "3 horas"}},
                {"week": 3, "activity": {"type": "Exercícios", "description": "Questões de matemática", "duration": "2 horas"}},
                {"week": 4, "activity": {"type": "Redação", "description": "Prática de redação", "duration": "2 horas"}}
            ],
            "performance_metrics": {
                "mock_exam_scores": [
                    {"date": "2023-06-01", "score": 65},
                    {"date": "2023-06-15", "score": 72}
                ],
                "writing_scores": [
                    {"date": "2023-06-05", "score": 7.5},
                    {"date": "2023-06-19", "score": 8.0}
                ],
                "questions_accuracy": 68
            }
        }
    
    # Layout em colunas
    col1, col2 = st.columns([2, 1])
    
    # Coluna 1: Progresso geral e gráficos
    with col1:
        # Progresso geral
        st.subheader("Progresso Geral")
        progress = dashboard_data["progress_summary"]["completion_percentage"]
        st.progress(progress / 100)
        st.write(f"**{progress}%** concluído - Fase atual: **{dashboard_data['progress_summary']['current_phase']}**")
        
        # Gráfico de progresso por matéria
        st.subheader("Progresso por Matéria")
        
        # Preparar dados para o gráfico
        subjects = list(dashboard_data["subject_progress"].keys())
        completions = [data["completion"] for data in dashboard_data["subject_progress"].values()]
        priorities = [data["priority"] for data in dashboard_data["subject_progress"].values()]
        
        # Criar DataFrame para o Altair
        df = pd.DataFrame({
            'Matéria': subjects,
            'Progresso': completions,
            'Prioridade': priorities
        })
        
        # Criar gráfico com Altair
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Progresso:Q', title='Progresso (%)'),
            y=alt.Y('Matéria:N', sort='-x', title=''),
            color=alt.Color('Prioridade:N', scale=alt.Scale(
                domain=['Baixa', 'Média', 'Alta', 'Muito Alta'],
                range=['#90CAF9', '#4CAF50', '#FFC107', '#F44336']
            )),
            tooltip=['Matéria', 'Progresso', 'Prioridade']
        ).properties(height=200)
        
        st.altair_chart(chart, use_container_width=True)
        
        # Gráfico de desempenho
        st.subheader("Evolução de Desempenho")
        
        # Preparar dados para o gráfico de linha
        if dashboard_data["performance_metrics"]["mock_exam_scores"]:
            mock_dates = [item["date"] for item in dashboard_data["performance_metrics"]["mock_exam_scores"]]
            mock_scores = [item["score"] for item in dashboard_data["performance_metrics"]["mock_exam_scores"]]
            
            df_mock = pd.DataFrame({
                'Data': pd.to_datetime(mock_dates),
                'Pontuação': mock_scores,
                'Tipo': ['Simulado'] * len(mock_dates)
            })
            
            if dashboard_data["performance_metrics"]["writing_scores"]:
                writing_dates = [item["date"] for item in dashboard_data["performance_metrics"]["writing_scores"]]
                writing_scores = [item["score"] * 10 for item in dashboard_data["performance_metrics"]["writing_scores"]]  # Converter para escala 0-100
                
                df_writing = pd.DataFrame({
                    'Data': pd.to_datetime(writing_dates),
                    'Pontuação': writing_scores,
                    'Tipo': ['Redação'] * len(writing_dates)
                })
                
                # Combinar DataFrames
                df_performance = pd.concat([df_mock, df_writing])
            else:
                df_performance = df_mock
            
            # Criar gráfico de linha
            line_chart = alt.Chart(df_performance).mark_line(point=True).encode(
                x='Data:T',
                y=alt.Y('Pontuação:Q', scale=alt.Scale(domain=[0, 100])),
                color='Tipo:N',
                tooltip=['Data', 'Pontuação', 'Tipo']
            ).properties(height=250)
            
            st.altair_chart(line_chart, use_container_width=True)
        else:
            st.info("Ainda não há dados de desempenho disponíveis.")
    
    # Coluna 2: Próximas atividades e métricas
    with col2:
        # Próximas atividades
        st.subheader("Próximas Atividades")
        for item in dashboard_data["upcoming_activities"]:
            activity = item["activity"]
            st.markdown(f"""
            **Semana {item['week']}**: {activity['type']}  
            {activity['description']}  
            Duração: {activity['duration']}
            """)
            st.divider()
        
        # Métricas de desempenho
        st.subheader("Métricas")
        
        # Calcular média de simulados
        mock_scores = [item["score"] for item in dashboard_data["performance_metrics"]["mock_exam_scores"]]
        mock_avg = sum(mock_scores) / len(mock_scores) if mock_scores else 0
        
        # Calcular média de redações
        writing_scores = [item["score"] for item in dashboard_data["performance_metrics"]["writing_scores"]]
        writing_avg = sum(writing_scores) / len(writing_scores) if writing_scores else 0
        
        # Exibir métricas
        col_a, col_b = st.columns(2)
        col_a.metric("Média Simulados", f"{mock_avg:.1f}%")
        col_b.metric("Média Redações", f"{writing_avg:.1f}")
        
        col_c, col_d = st.columns(2)
        col_c.metric("Acertos Questões", f"{dashboard_data['performance_metrics']['questions_accuracy']}%")
        col_d.metric("Semanas Concluídas", f"{dashboard_data['progress_summary']['completed_weeks']}")

def update_dashboard_data(new_data):
    """Atualiza os dados do dashboard"""
    try:
        # Carregar dados existentes
        try:
            with open("data/dashboard_data.json", "r") as f:
                current_data = json.load(f)
        except:
            current_data = {}
        
        # Atualizar com novos dados
        if isinstance(current_data, dict) and isinstance(new_data, dict):
            for key, value in new_data.items():
                if key in current_data and isinstance(current_data[key], dict) and isinstance(value, dict):
                    current_data[key].update(value)
                else:
                    current_data[key] = value
        else:
            current_data = new_data
        
        # Salvar dados atualizados
        with open("data/dashboard_data.json", "w") as f:
            json.dump(current_data, f, indent=2)
        
        return True
    except Exception as e:
        print(f"Erro ao atualizar dashboard: {str(e)}")
        return False