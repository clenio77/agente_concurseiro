"""
Utilitário de dashboard do sistema.
Fornece funções para renderizar o painel principal do usuário, exibir métricas, conquistas, recomendações e atualizar dados do dashboard.
"""

import json

import altair as alt
import pandas as pd
import streamlit as st

from .gamification import GamificationSystem
from .notifications import NotificationManager, generate_daily_notifications


def load_dashboard_data(user_id: str = None) -> dict:
    """
    Carrega dados do dashboard para um usuário específico.
    
    Args:
        user_id: ID do usuário (opcional)
        
    Returns:
        Dicionário com dados do dashboard
    """
    try:
        # Em produção, isso viria do banco de dados
        # Por enquanto, retornar dados simulados
        return _get_fallback_dashboard_data()
    except Exception as e:
        print(f"Erro ao carregar dados do dashboard: {e}")
        return _get_fallback_dashboard_data()

def _get_fallback_dashboard_data():
    """
    Retorna dados de fallback para o dashboard caso não seja possível carregar do arquivo.
    Utilizado para garantir que o dashboard funcione mesmo sem dados persistidos.
    :return: Dicionário com dados simulados de progresso, atividades, desempenho, etc.
    """
    return {
        "progress_summary": {
            "completed_weeks": 2,
            "total_weeks": 24,
            "completion_percentage": 8.33,
            "current_phase": "Base Teórica",
            "next_milestone": "Início da fase de exercícios",
            "days_until_exam": 180,
            "total_study_hours": 40,
            "weekly_goal_hours": 20,
            "current_week_hours": 8
        },
        "subject_progress": {
            "Português": {"completion": 15, "priority": "Alta", "hours_planned": 48, "hours_completed": 7, "last_score": 70, "trend": "improving"},
            "Matemática": {"completion": 10, "priority": "Média", "hours_planned": 36, "hours_completed": 4, "last_score": 60, "trend": "stable"},
            "Direito": {"completion": 5, "priority": "Alta", "hours_planned": 60, "hours_completed": 3, "last_score": 65, "trend": "needs_attention"}
        },
        "upcoming_activities": [
            {"date": "2024-01-16", "week": 3, "activity": {"type": "Estudo", "description": "Revisão de gramática", "duration": "3 horas", "priority": "Alta"}},
            {"date": "2024-01-17", "week": 3, "activity": {"type": "Exercícios", "description": "Questões de matemática", "duration": "2 horas", "priority": "Média"}},
            {"date": "2024-01-18", "week": 4, "activity": {"type": "Redação", "description": "Prática de redação", "duration": "2 horas", "priority": "Média"}}
        ],
        "performance_metrics": {
            "mock_exam_scores": [
                {"date": "2024-01-01", "score": 65, "subjects": {"Português": 70, "Matemática": 60, "Direito": 65}},
                {"date": "2024-01-08", "score": 72, "subjects": {"Português": 75, "Matemática": 65, "Direito": 75}}
            ],
            "writing_scores": [
                {"date": "2024-01-05", "score": 7.5, "criteria": {"estrutura": 8, "argumentacao": 7, "gramatica": 8}},
                {"date": "2024-01-12", "score": 8.0, "criteria": {"estrutura": 8, "argumentacao": 8, "gramatica": 8}}
            ],
            "questions_accuracy": 68,
            "consistency_score": 75,
            "improvement_rate": 8.5
        },
        "achievements": [],
        "recommendations": [
            {
                "type": "study_focus",
                "priority": "high",
                "title": "Foque em Matemática",
                "description": "Sua pontuação em Matemática precisa melhorar.",
                "action": "Dedique mais 2 horas semanais"
            }
        ],
        "study_streak": {"current_streak": 5, "longest_streak": 8, "total_study_days": 15},
        "goals": {
            "weekly_hours": {"target": 20, "current": 8, "percentage": 40},
            "target_score": {"overall": 80, "current_average": 68, "gap": 12}
        }
    }

def render_dashboard():
    """
    Renderiza o dashboard principal do sistema.
    Exibe notificações, métricas de progresso, gamificação, gráficos, próximas atividades, conquistas e recomendações.
    """
    st.title("📊 Dashboard - Acompanhamento de Estudos")

    # Carregar dados do dashboard (em produção, viria do banco de dados)
    try:
        with open("data/dashboard/dashboard_data.json", "r", encoding='utf-8') as f:
            dashboard_data = json.load(f)
    except FileNotFoundError:
        # Tentar carregar do local antigo
        try:
            with open("data/dashboard_data.json", "r", encoding='utf-8') as f:
                dashboard_data = json.load(f)
        except:
            dashboard_data = _get_fallback_dashboard_data()
    except Exception as e:
        print(f"Erro ao carregar dados do dashboard: {e}")
        dashboard_data = _get_fallback_dashboard_data()

    # Sistema de notificações
    notifications_manager = st.session_state.notifications

    # Gerar notificações diárias (simulação)
    if st.button("🔔 Atualizar Notificações", help="Gera notificações baseadas na sua atividade"):
        with st.spinner("Gerando notificações..."):
            summary = generate_daily_notifications(
                st.session_state.get('current_user', 'demo_user'),
                dashboard_data
            )
            st.success(f"✅ {summary['total_unread']} notificações geradas!")

    # Exibir notificações não lidas
    unread_notifications = notifications_manager.get_unread_notifications(5)

    if unread_notifications:
        st.markdown("### 🔔 Notificações")

        for notification in unread_notifications:
            # Emoji baseado na prioridade
            priority_emoji = {
                "urgent": "🚨",
                "high": "🔴",
                "medium": "🟡",
                "low": "🟢"
            }.get(notification.priority.value, "🔵")

            # Emoji baseado no tipo
            type_emoji = {
                "study_reminder": "📚",
                "quiz_reminder": "🎯",
                "goal_achievement": "🏆",
                "performance_alert": "📊",
                "streak_milestone": "🔥",
                "exam_countdown": "📅",
                "recommendation": "💡"
            }.get(notification.type.value, "📢")

            with st.expander(f"{priority_emoji} {type_emoji} {notification.title}", expanded=notification.priority.value in ["urgent", "high"]):
                st.write(notification.message)

                col1, col2, col3 = st.columns(3)

                with col1:
                    if notification.action_text and st.button(f"🚀 {notification.action_text}", key=f"action_{notification.id}"):
                        notifications_manager.mark_as_read(notification.id)
                        st.success("Ação executada!")

                with col2:
                    if st.button("✅ Marcar como lida", key=f"read_{notification.id}"):
                        notifications_manager.mark_as_read(notification.id)
                        st.experimental_rerun()

                with col3:
                    if st.button("❌ Descartar", key=f"dismiss_{notification.id}"):
                        notifications_manager.dismiss_notification(notification.id)
                        st.experimental_rerun()

        st.markdown("---")

    # Inicializar sistemas
    if 'gamification' not in st.session_state:
        st.session_state.gamification = GamificationSystem(
            user_id=st.session_state.get('current_user', 'demo_user')
        )

    if 'notifications' not in st.session_state:
        st.session_state.notifications = NotificationManager(
            user_id=st.session_state.get('current_user', 'demo_user')
        )

    # Header com métricas principais
    st.subheader("📊 Visão Geral")

    # Métricas principais em cards
    col1, col2, col3, col4 = st.columns(4)

    progress_summary = dashboard_data["progress_summary"]

    with col1:
        st.metric(
            "📅 Progresso Geral",
            f"{progress_summary['completion_percentage']:.1f}%",
            delta=f"+{progress_summary.get('weekly_progress', 4.2):.1f}% esta semana"
        )

    with col2:
        st.metric(
            "⏰ Horas Estudadas",
            f"{progress_summary.get('total_study_hours', 0)}h",
            delta=f"+{progress_summary.get('current_week_hours', 0)}h esta semana"
        )

    with col3:
        st.metric(
            "🎯 Dias até Prova",
            f"{progress_summary.get('days_until_exam', 'N/A')}",
            delta=None
        )

    with col4:
        streak = dashboard_data.get('study_streak', {})
        st.metric(
            "🔥 Sequência de Estudos",
            f"{streak.get('current_streak', 0)} dias",
            delta=f"Recorde: {streak.get('longest_streak', 0)}"
        )

    # Seção de Gamificação
    gamification = st.session_state.gamification
    user_summary = gamification.get_user_summary()

    st.markdown("---")
    st.subheader("🎮 Progresso e Conquistas")

    # Métricas de gamificação
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🎯 Nível", user_summary['level'])

    with col2:
        st.metric("⭐ Pontos", f"{user_summary['total_points']:,}")

    with col3:
        achievement_progress = f"{user_summary['achievements_earned']}/{user_summary['total_achievements']}"
        st.metric("🏆 Conquistas", achievement_progress)

    with col4:
        badge_progress = f"{user_summary['badges_earned']}/{user_summary['total_badges']}"
        st.metric("🎖️ Badges", badge_progress)

    with col5:
        st.metric("📚 Melhor Nota", f"{user_summary['best_score']}%")

    # Barra de experiência
    if user_summary['level'] > 1:
        # Calcular XP necessário para próximo nível
        current_level = user_summary['level']
        xp_for_current = sum(100 + (i - 1) * 50 for i in range(1, current_level))
        xp_for_next = 100 + (current_level - 1) * 50
        current_level_xp = user_summary['experience'] - xp_for_current

        progress_pct = current_level_xp / xp_for_next
        st.write(f"**Experiência:** {current_level_xp}/{xp_for_next} XP para nível {current_level + 1}")
        st.progress(progress_pct)

    # Conquistas recentes e em progresso
    col1, col2 = st.columns(2)

    with col1:
        st.write("**🏆 Conquistas Recentes**")
        recent_achievements = gamification.get_recent_achievements(3)

        if recent_achievements:
            for achievement in recent_achievements:
                st.markdown(f"""
                {achievement.icon} **{achievement.title}** (+{achievement.points} pts)
                {achievement.description}
                """)
        else:
            st.info("Complete atividades para ganhar conquistas!")

    with col2:
        st.write("**📈 Progresso de Conquistas**")
        progress_achievements = gamification.get_progress_achievements()

        if progress_achievements:
            for achievement in progress_achievements[:3]:
                progress_pct = achievement.progress / achievement.max_progress
                st.write(f"{achievement.icon} **{achievement.title}**")
                st.progress(progress_pct)
                st.caption(f"{achievement.progress:.0f}/{achievement.max_progress:.0f}")
        else:
            st.info("Continue estudando para desbloquear conquistas!")

    # Barra de progresso principal
    st.subheader("📈 Progresso do Plano de Estudos")
    progress = progress_summary["completion_percentage"]
    st.progress(progress / 100)

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{progress:.1f}%** concluído")
        st.write(f"**Fase atual:** {progress_summary['current_phase']}")
    with col2:
        st.write(f"**Semanas:** {progress_summary['completed_weeks']}/{progress_summary['total_weeks']}")
        if 'next_milestone' in progress_summary:
            st.write(f"**Próximo:** {progress_summary['next_milestone']}")

    # Layout em colunas para conteúdo principal
    col1, col2 = st.columns([2, 1])

    # Coluna 1: Progresso por matéria e gráficos
    with col1:

        # Progresso por matéria com mais detalhes
        st.subheader("📚 Progresso por Matéria")

        # Preparar dados para o gráfico
        subjects = list(dashboard_data["subject_progress"].keys())
        completions = [data["completion"] for data in dashboard_data["subject_progress"].values()]
        priorities = [data["priority"] for data in dashboard_data["subject_progress"].values()]
        last_scores = [data.get("last_score", 0) for data in dashboard_data["subject_progress"].values()]
        trends = [data.get("trend", "stable") for data in dashboard_data["subject_progress"].values()]

        # Criar DataFrame para o Altair
        df = pd.DataFrame({
            'Matéria': subjects,
            'Progresso': completions,
            'Prioridade': priorities,
            'Última Nota': last_scores,
            'Tendência': trends
        })

        # Gráfico de barras com progresso
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Progresso:Q', title='Progresso (%)', scale=alt.Scale(domain=[0, 100])),
            y=alt.Y('Matéria:N', sort='-x', title=''),
            color=alt.Color('Prioridade:N',
                          scale=alt.Scale(
                              domain=['Baixa', 'Média', 'Alta', 'Muito Alta'],
                              range=['#90CAF9', '#4CAF50', '#FFC107', '#F44336']
                          ),
                          legend=alt.Legend(title="Prioridade")),
            tooltip=['Matéria', 'Progresso', 'Prioridade', 'Última Nota', 'Tendência']
        ).properties(height=250, title="Progresso de Estudos por Matéria")

        st.altair_chart(chart, use_container_width=True)

        # Tabela detalhada de matérias
        with st.expander("📋 Detalhes por Matéria"):
            for subject, data in dashboard_data["subject_progress"].items():
                col_a, col_b, col_c, col_d = st.columns(4)

                with col_a:
                    st.write(f"**{subject}**")
                    st.write(f"Progresso: {data['completion']}%")

                with col_b:
                    st.write(f"Prioridade: {data['priority']}")
                    if 'last_score' in data:
                        st.write(f"Última nota: {data['last_score']}%")

                with col_c:
                    st.write(f"Horas: {data.get('hours_completed', 0)}/{data.get('hours_planned', 0)}")
                    if 'trend' in data:
                        trend_emoji = {"improving": "📈", "stable": "➡️", "needs_attention": "📉"}.get(data['trend'], "➡️")
                        st.write(f"Tendência: {trend_emoji}")

                with col_d:
                    if 'next_topic' in data:
                        st.write(f"Próximo: {data['next_topic']}")

                st.divider()

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

    # Coluna 2: Próximas atividades, conquistas e recomendações
    with col2:
        # Próximas atividades
        st.subheader("📅 Próximas Atividades")

        for item in dashboard_data["upcoming_activities"][:3]:  # Mostrar apenas 3
            activity = item["activity"]

            # Emoji baseado no tipo de atividade
            type_emoji = {
                "Estudo": "📖",
                "Exercícios": "✏️",
                "Simulado": "🎯",
                "Redação": "✍️",
                "Revisão": "🔄"
            }.get(activity['type'], "📝")

            # Cor baseada na prioridade
            priority_color = {
                "Muito Alta": "🔴",
                "Alta": "🟠",
                "Média": "🟡",
                "Baixa": "🟢"
            }.get(activity.get('priority', 'Média'), "🟡")

            st.markdown(f"""
            {type_emoji} **{activity['type']}** {priority_color}
            📅 {item.get('date', f"Semana {item.get('week', 'N/A')}")}
            {activity['description']}
            ⏱️ {activity['duration']}
            """)
            st.divider()

        # Conquistas recentes
        if 'achievements' in dashboard_data and dashboard_data['achievements']:
            st.subheader("🏆 Conquistas Recentes")

            for achievement in dashboard_data['achievements'][-2:]:  # Últimas 2 conquistas
                st.markdown(f"""
                {achievement['icon']} **{achievement['title']}**
                {achievement['description']}
                🎁 +{achievement['points']} pontos
                """)
                st.divider()

        # Recomendações
        if 'recommendations' in dashboard_data and dashboard_data['recommendations']:
            st.subheader("💡 Recomendações")

            for rec in dashboard_data['recommendations'][:2]:  # Top 2 recomendações
                priority_emoji = {"high": "🔥", "medium": "⚠️", "low": "💭"}.get(rec.get('priority', 'medium'), "💭")

                st.markdown(f"""
                {priority_emoji} **{rec['title']}**
                {rec['description']}
                ✅ {rec['action']}
                """)

                if 'estimated_impact' in rec:
                    st.caption(f"📊 Impacto estimado: {rec['estimated_impact']}")

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

        # Seção de metas
        if 'goals' in dashboard_data:
            st.subheader("🎯 Metas e Objetivos")
            goals = dashboard_data['goals']

            # Meta de horas semanais
            if 'weekly_hours' in goals:
                weekly = goals['weekly_hours']
                st.write("**📚 Meta Semanal de Estudos**")
                progress_pct = weekly.get('percentage', 0) / 100
                st.progress(progress_pct)
                st.write(f"{weekly.get('current', 0)}h / {weekly.get('target', 0)}h ({weekly.get('percentage', 0):.0f}%)")

            # Meta de pontuação
            if 'target_score' in goals:
                target = goals['target_score']
                st.write("**🎯 Meta de Pontuação**")
                current = target.get('current_average', 0)
                goal = target.get('overall', 80)
                progress_pct = min(current / goal, 1.0)
                st.progress(progress_pct)
                st.write(f"{current:.0f}% / {goal}% (faltam {target.get('gap', 0)} pontos)")

        # Próximos marcos
        if 'next_milestones' in dashboard_data:
            st.subheader("🚀 Próximos Marcos")

            for milestone in dashboard_data['next_milestones'][:2]:
                st.write(f"**{milestone['title']}**")
                st.write(milestone['description'])

                progress = milestone.get('progress', 0)
                st.progress(progress / 100)

                col_a, col_b = st.columns(2)
                col_a.write(f"📅 Meta: {milestone.get('target_date', 'N/A')}")
                col_b.write(f"📈 {progress}% concluído")

                if 'estimated_completion' in milestone:
                    st.caption(f"⏰ Previsão: {milestone['estimated_completion']}")

                st.divider()

def update_dashboard_data(new_data):
    """
    Atualiza os dados do dashboard no arquivo JSON.
    Mescla os dados existentes com os novos dados fornecidos.
    :param new_data: Dicionário com os dados a serem atualizados.
    :return: True se atualizar com sucesso, False caso contrário.
    """
    """
Utilitário de dashboard do sistema.
Fornece funções para renderizar o painel principal do usuário, exibir métricas, 
conquistas, recomendações e atualizar dados do dashboard.
"""

import json

import altair as alt
import pandas as pd
import streamlit as st

from .gamification import GamificationSystem
from .notifications import NotificationManager, generate_daily_notifications


def load_dashboard_data(user_id: str = None) -> dict:
    """
    Carrega dados do dashboard para um usuário específico.

    Args:
        user_id: ID do usuário (opcional)

    Returns:
        Dicionário com dados do dashboard
    """
    try:
        # Em produção, isso viria do banco de dados
        # Por enquanto, retornar dados simulados
        return _get_fallback_dashboard_data()
    except Exception as e:
        print(f"Erro ao carregar dados do dashboard: {e}")
        return _get_fallback_dashboard_data()

def _get_fallback_dashboard_data():
    """
    Retorna dados de fallback para o dashboard caso não seja possível carregar do arquivo.
    Utilizado para garantir que o dashboard funcione mesmo sem dados persistidos.
    :return: Dicionário com dados simulados de progresso, atividades, desempenho, etc.
    """
    return {
        "progress_summary": {
            "completed_weeks": 2,
            "total_weeks": 24,
            "completion_percentage": 8.33,
            "current_phase": "Base Teórica",
            "next_milestone": "Início da fase de exercícios",
            "days_until_exam": 180,
            "total_study_hours": 40,
            "weekly_goal_hours": 20,
            "current_week_hours": 8
        },
        "subject_progress": {
            "Português": {
                "completion": 15,
                "priority": "Alta",
                "hours_planned": 48,
                "hours_completed": 7,
                "last_score": 70,
                "trend": "improving"
            },
            "Matemática": {
                "completion": 10,
                "priority": "Média",
                "hours_planned": 36,
                "hours_completed": 4,
                "last_score": 60,
                "trend": "stable"
            },
            "Direito": {
                "completion": 5,
                "priority": "Alta",
                "hours_planned": 60,
                "hours_completed": 3,
                "last_score": 65,
                "trend": "needs_attention"
            }
        },
        "upcoming_activities": [
            {
                "date": "2024-01-16",
                "week": 3,
                "activity": {
                    "type": "Estudo",
                    "description": "Revisão de gramática",
                    "duration": "3 horas",
                    "priority": "Alta"
                }
            },
            {
                "date": "2024-01-17",
                "week": 3,
                "activity": {
                    "type": "Exercícios",
                    "description": "Questões de matemática",
                    "duration": "2 horas",
                    "priority": "Média"
                }
            },
            {
                "date": "2024-01-18",
                "week": 4,
                "activity": {
                    "type": "Redação",
                    "description": "Prática de redação",
                    "duration": "2 horas",
                    "priority": "Média"
                }
            }
        ],
        "performance_metrics": {
            "mock_exam_scores": [
                {
                    "date": "2024-01-01",
                    "score": 65,
                    "subjects": {"Português": 70, "Matemática": 60, "Direito": 65}
                },
                {
                    "date": "2024-01-08",
                    "score": 72,
                    "subjects": {"Português": 75, "Matemática": 65, "Direito": 75}
                }
            ],
            "writing_scores": [
                {
                    "date": "2024-01-05",
                    "score": 7.5,
                    "criteria": {"estrutura": 8, "argumentacao": 7, "gramatica": 8}
                },
                {
                    "date": "2024-01-12",
                    "score": 8.0,
                    "criteria": {"estrutura": 8, "argumentacao": 8, "gramatica": 8}
                }
            ],
            "questions_accuracy": 68,
            "consistency_score": 75,
            "improvement_rate": 8.5
        },
        "achievements": [],
        "recommendations": [
            {
                "type": "study_focus",
                "priority": "high",
                "title": "Foque em Matemática",
                "description": "Sua pontuação em Matemática precisa melhorar.",
                "action": "Dedique mais 2 horas semanais"
            }
        ],
        "study_streak": {"current_streak": 5, "longest_streak": 8, "total_study_days": 15},
        "goals": {
            "weekly_hours": {"target": 20, "current": 8, "percentage": 40},
            "target_score": {"overall": 80, "current_average": 68, "gap": 12}
        }
    }

def render_dashboard():
    """
    Renderiza o dashboard principal do sistema.
    Exibe notificações, métricas de progresso, gamificação, gráficos, 
    próximas atividades, conquistas e recomendações.
    """
    st.title("📊 Dashboard - Acompanhamento de Estudos")

    # Carregar dados do dashboard (em produção, viria do banco de dados)
    try:
        with open("data/dashboard/dashboard_data.json", "r", encoding='utf-8') as f:
            dashboard_data = json.load(f)
    except FileNotFoundError:
        # Tentar carregar do local antigo
        try:
            with open("data/dashboard_data.json", "r", encoding='utf-8') as f:
                dashboard_data = json.load(f)
        except FileNotFoundError:
            dashboard_data = _get_fallback_dashboard_data()
    except Exception as e:
        print(f"Erro ao carregar dados do dashboard: {e}")
        dashboard_data = _get_fallback_dashboard_data()

    # Sistema de notificações
    notifications_manager = st.session_state.notifications

    # Gerar notificações diárias (simulação)
    if st.button(
        "🔔 Atualizar Notificações", help="Gera notificações baseadas na sua atividade"
    ):
        with st.spinner("Gerando notificações..."):
            summary = generate_daily_notifications(
                st.session_state.get('current_user', 'demo_user'),
                dashboard_data
            )
            st.success(f"✅ {summary['total_unread']} notificações geradas!")

    # Exibir notificações não lidas
    unread_notifications = notifications_manager.get_unread_notifications(5)

    if unread_notifications:
        st.markdown("### 🔔 Notificações")

        for notification in unread_notifications:
            # Emoji baseado na prioridade
            priority_emoji = {
                "urgent": "🚨",
                "high": "🔴",
                "medium": "🟡",
                "low": "🟢"
            }.get(notification.priority.value, "🔵")

            # Emoji baseado no tipo
            type_emoji = {
                "study_reminder": "📚",
                "quiz_reminder": "🎯",
                "goal_achievement": "🏆",
                "performance_alert": "📊",
                "streak_milestone": "🔥",
                "exam_countdown": "📅",
                "recommendation": "💡"
            }.get(notification.type.value, "📢")

            with st.expander(
                f"{priority_emoji} {type_emoji} {notification.title}",
                expanded=notification.priority.value in ["urgent", "high"]
            ):
                st.write(notification.message)

                col1, col2, col3 = st.columns(3)

                with col1:
                    if notification.action_text and st.button(
                        f"🚀 {notification.action_text}", key=f"action_{notification.id}"
                    ):
                        notifications_manager.mark_as_read(notification.id)
                        st.success("Ação executada!")

                with col2:
                    if st.button("✅ Marcar como lida", key=f"read_{notification.id}"):
                        notifications_manager.mark_as_read(notification.id)
                        st.experimental_rerun()

                with col3:
                    if st.button("❌ Descartar", key=f"dismiss_{notification.id}"):
                        notifications_manager.dismiss_notification(notification.id)
                        st.experimental_rerun()

        st.markdown("---")

    # Inicializar sistemas
    if 'gamification' not in st.session_state:
        st.session_state.gamification = GamificationSystem(
            user_id=st.session_state.get('current_user', 'demo_user')
        )

    if 'notifications' not in st.session_state:
        st.session_state.notifications = NotificationManager(
            user_id=st.session_state.get('current_user', 'demo_user')
        )

    # Header com métricas principais
    st.subheader("📊 Visão Geral")

    # Métricas principais em cards
    col1, col2, col3, col4 = st.columns(4)

    progress_summary = dashboard_data["progress_summary"]

    with col1:
        st.metric(
            "📅 Progresso Geral",
            f"{progress_summary['completion_percentage']:.1f}%",
            delta=f"+{progress_summary.get('weekly_progress', 4.2):.1f}% esta semana"
        )

    with col2:
        st.metric(
            "⏰ Horas Estudadas",
            f"{progress_summary.get('total_study_hours', 0)}h",
            delta=f"+{progress_summary.get('current_week_hours', 0)}h esta semana"
        )

    with col3:
        st.metric(
            "🎯 Dias até Prova",
            f"{progress_summary.get('days_until_exam', 'N/A')}",
            delta=None
        )

    with col4:
        streak = dashboard_data.get('study_streak', {})
        st.metric(
            "🔥 Sequência de Estudos",
            f"{streak.get('current_streak', 0)} dias",
            delta=f"Recorde: {streak.get('longest_streak', 0)}"
        )

    # Seção de Gamificação
    gamification = st.session_state.gamification
    user_summary = gamification.get_user_summary()

    st.markdown("---")
    st.subheader("🎮 Progresso e Conquistas")

    # Métricas de gamificação
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("🎯 Nível", user_summary['level'])

    with col2:
        st.metric("⭐ Pontos", f"{user_summary['total_points']:,}")

    with col3:
        achievement_progress = (
            f"{user_summary['achievements_earned']}/"
            f"{user_summary['total_achievements']}"
        )
        st.metric("🏆 Conquistas", achievement_progress)

    with col4:
        badge_progress = (
            f"{user_summary['badges_earned']}/{user_summary['total_badges']}"
        )
        st.metric("🎖️ Badges", badge_progress)

    with col5:
        st.metric("📚 Melhor Nota", f"{user_summary['best_score']}%")

    # Barra de experiência
    if user_summary['level'] > 1:
        # Calcular XP necessário para próximo nível
        current_level = user_summary['level']
        xp_for_current = sum(100 + (i - 1) * 50 for i in range(1, current_level))
        xp_for_next = 100 + (current_level - 1) * 50
        current_level_xp = user_summary['experience'] - xp_for_current

        progress_pct = current_level_xp / xp_for_next
        st.write(
            f"**Experiência:** {current_level_xp}/{xp_for_next} XP para nível "
            f"{current_level + 1}"
        )
        st.progress(progress_pct)

    # Conquistas recentes e em progresso
    col1, col2 = st.columns(2)

    with col1:
        st.write("**🏆 Conquistas Recentes**")
        recent_achievements = gamification.get_recent_achievements(3)

        if recent_achievements:
            for achievement in recent_achievements:
                st.markdown(f"""
                {achievement.icon} **{achievement.title}** (+{achievement.points} pts)
                {achievement.description}
                """)
        else:
            st.info("Complete atividades para ganhar conquistas!")

    with col2:
        st.write("**📈 Progresso de Conquistas**")
        progress_achievements = gamification.get_progress_achievements()

        if progress_achievements:
            for achievement in progress_achievements[:3]:
                progress_pct = achievement.progress / achievement.max_progress
                st.write(f"{achievement.icon} **{achievement.title}**")
                st.progress(progress_pct)
                st.caption(f"{achievement.progress:.0f}/{achievement.max_progress:.0f}")
        else:
            st.info("Continue estudando para desbloquear conquistas!")

    # Barra de progresso principal
    st.subheader("📈 Progresso do Plano de Estudos")
    progress = progress_summary["completion_percentage"]
    st.progress(progress / 100)

    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**{progress:.1f}%** concluído")
        st.write(f"**Fase atual:** {progress_summary['current_phase']}")
    with col2:
        st.write(
            f"**Semanas:** {progress_summary['completed_weeks']}/"
            f"{progress_summary['total_weeks']}"
        )
        if 'next_milestone' in progress_summary:
            st.write(f"**Próximo:** {progress_summary['next_milestone']}")

    # Layout em colunas para conteúdo principal
    col1, col2 = st.columns([2, 1])

    # Coluna 1: Progresso por matéria e gráficos
    with col1:

        # Progresso por matéria com mais detalhes
        st.subheader("📚 Progresso por Matéria")

        # Preparar dados para o gráfico
        subjects = list(dashboard_data["subject_progress"].keys())
        completions = [
            data["completion"] for data in dashboard_data["subject_progress"].values()
        ]
        priorities = [
            data["priority"] for data in dashboard_data["subject_progress"].values()
        ]
        last_scores = [
            data.get("last_score", 0)
            for data in dashboard_data["subject_progress"].values()
        ]
        trends = [
            data.get("trend", "stable")
            for data in dashboard_data["subject_progress"].values()
        ]

        # Criar DataFrame para o Altair
        df = pd.DataFrame({
            'Matéria': subjects,
            'Progresso': completions,
            'Prioridade': priorities,
            'Última Nota': last_scores,
            'Tendência': trends
        })

        # Gráfico de barras com progresso
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('Progresso:Q', title='Progresso (%)', scale=alt.Scale(domain=[0, 100])),
            y=alt.Y('Matéria:N', sort='-x', title=''),
            color=alt.Color('Prioridade:N',
                          scale=alt.Scale(
                              domain=['Baixa', 'Média', 'Alta', 'Muito Alta'],
                              range=['#90CAF9', '#4CAF50', '#FFC107', '#F44336']
                          ),
                          legend=alt.Legend(title="Prioridade")),
            tooltip=['Matéria', 'Progresso', 'Prioridade', 'Última Nota', 'Tendência']
        ).properties(height=250, title="Progresso de Estudos por Matéria")

        st.altair_chart(chart, use_container_width=True)

        # Tabela detalhada de matérias
        with st.expander("📋 Detalhes por Matéria"):
            for subject, data in dashboard_data["subject_progress"].items():
                col_a, col_b, col_c, col_d = st.columns(4)

                with col_a:
                    st.write(f"**{subject}**")
                    st.write(f"Progresso: {data['completion']}%")

                with col_b:
                    st.write(f"Prioridade: {data['priority']}")
                    if 'last_score' in data:
                        st.write(f"Última nota: {data['last_score']}%")

                with col_c:
                    st.write(
                        f"Horas: {data.get('hours_completed', 0)}/"
                        f"{data.get('hours_planned', 0)}"
                    )
                    if 'trend' in data:
                        trend_emoji = {
                            "improving": "📈",
                            "stable": "➡️",
                            "needs_attention": "📉",
                        }.get(data['trend'], "➡️")
                        st.write(f"Tendência: {trend_emoji}")

                with col_d:
                    if 'next_topic' in data:
                        st.write(f"Próximo: {data['next_topic']}")

                st.divider()

        # Gráfico de desempenho
        st.subheader("Evolução de Desempenho")

        # Preparar dados para o gráfico de linha
        if dashboard_data["performance_metrics"]["mock_exam_scores"]:
            mock_dates = [
                item["date"]
                for item in dashboard_data["performance_metrics"]["mock_exam_scores"]
            ]
            mock_scores = [
                item["score"]
                for item in dashboard_data["performance_metrics"]["mock_exam_scores"]
            ]

            df_mock = pd.DataFrame({
                'Data': pd.to_datetime(mock_dates),
                'Pontuação': mock_scores,
                'Tipo': ['Simulado'] * len(mock_dates)
            })

            if dashboard_data["performance_metrics"]["writing_scores"]:
                writing_dates = [
                    item["date"]
                    for item in dashboard_data["performance_metrics"]["writing_scores"]
                ]
                writing_scores = [
                    item["score"] * 10
                    for item in dashboard_data["performance_metrics"]["writing_scores"]
                ]  # Converter para escala 0-100

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

    # Coluna 2: Próximas atividades, conquistas e recomendações
    with col2:
        # Próximas atividades
        st.subheader("📅 Próximas Atividades")

        for item in dashboard_data["upcoming_activities"][:3]:  # Mostrar apenas 3
            activity = item["activity"]

            # Emoji baseado no tipo de atividade
            type_emoji = {
                "Estudo": "📖",
                "Exercícios": "✏️",
                "Simulado": "🎯",
                "Redação": "✍️",
                "Revisão": "🔄"
            }.get(activity['type'], "📝")

            # Cor baseada na prioridade
            priority_color = {
                "Muito Alta": "🔴",
                "Alta": "🟠",
                "Média": "🟡",
                "Baixa": "🟢"
            }.get(activity.get('priority', 'Média'), "🟡")

            st.markdown(f"""
            {type_emoji} **{activity['type']}** {priority_color}
            📅 {item.get('date', f"Semana {item.get('week', 'N/A')}")}
            {activity['description']}
            ⏱️ {activity['duration']}
            """)
            st.divider()

        # Conquistas recentes
        if 'achievements' in dashboard_data and dashboard_data['achievements']:
            st.subheader("🏆 Conquistas Recentes")

            for achievement in dashboard_data['achievements'][-2:]:  # Últimas 2 conquistas
                st.markdown(f"""
                {achievement['icon']} **{achievement['title']}**
                {achievement['description']}
                🎁 +{achievement['points']} pontos
                """)
                st.divider()

        # Recomendações
        if 'recommendations' in dashboard_data and dashboard_data['recommendations']:
            st.subheader("💡 Recomendações")

            for rec in dashboard_data['recommendations'][:2]:  # Top 2 recomendações
                priority_emoji = {"high": "🔥", "medium": "⚠️", "low": "💭"}.get(
                    rec.get('priority', 'medium'), "💭"
                )

                st.markdown(f"""
                {priority_emoji} **{rec['title']}**
                {rec['description']}
                ✅ {rec['action']}
                """)

                if 'estimated_impact' in rec:
                    st.caption(f"📊 Impacto estimado: {rec['estimated_impact']}")

                st.divider()

        # Métricas de desempenho
        st.subheader("Métricas")

        # Calcular média de simulados
        mock_scores = [
            item["score"]
            for item in dashboard_data["performance_metrics"]["mock_exam_scores"]
        ]
        mock_avg = sum(mock_scores) / len(mock_scores) if mock_scores else 0

        # Calcular média de redações
        writing_scores = [
            item["score"]
            for item in dashboard_data["performance_metrics"]["writing_scores"]
        ]
        writing_avg = sum(writing_scores) / len(writing_scores) if writing_scores else 0

        # Exibir métricas
        col_a, col_b = st.columns(2)
        col_a.metric("Média Simulados", f"{mock_avg:.1f}%")
        col_b.metric("Média Redações", f"{writing_avg:.1f}")

        col_c, col_d = st.columns(2)
        col_c.metric(
            "Acertos Questões",
            f"{dashboard_data['performance_metrics']['questions_accuracy']}%
        )
        col_d.metric(
            "Semanas Concluídas",
            f"{dashboard_data['progress_summary']['completed_weeks']}"
        )

        # Seção de metas
        if 'goals' in dashboard_data:
            st.subheader("🎯 Metas e Objetivos")
            goals = dashboard_data['goals']

            # Meta de horas semanais
            if 'weekly_hours' in goals:
                weekly = goals['weekly_hours']
                st.write("**📚 Meta Semanal de Estudos**")
                progress_pct = weekly.get('percentage', 0) / 100
                st.progress(progress_pct)
                st.write(
                    f"{weekly.get('current', 0)}h / {weekly.get('target', 0)}h "
                    f"({weekly.get('percentage', 0):.0f}%)"
                )

            # Meta de pontuação
            if 'target_score' in goals:
                target = goals['target_score']
                st.write("**🎯 Meta de Pontuação**")
                current = target.get('current_average', 0)
                goal = target.get('overall', 80)
                progress_pct = min(current / goal, 1.0)
                st.progress(progress_pct)
                st.write(
                    f"{current:.0f}% / {goal}% (faltam {target.get('gap', 0)} pontos)"
                )

        # Próximos marcos
        if 'next_milestones' in dashboard_data:
            st.subheader("🚀 Próximos Marcos")

            for milestone in dashboard_data['next_milestones'][:2]:
                st.write(f"**{milestone['title']}**")
                st.write(milestone['description'])

                progress = milestone.get('progress', 0)
                st.progress(progress / 100)

                col_a, col_b = st.columns(2)
                col_a.write(f"📅 Meta: {milestone.get('target_date', 'N/A')}")
                col_b.write(f"📈 {progress}% concluído")

                if 'estimated_completion' in milestone:
                    st.caption(f"⏰ Previsão: {milestone['estimated_completion']}")

                st.divider()

def update_dashboard_data(new_data):
    """
    Atualiza os dados do dashboard no arquivo JSON.
    Mescla os dados existentes com os novos dados fornecidos.
    :param new_data: Dicionário com os dados a serem atualizados.
    :return: True se atualizar com sucesso, False caso contrário.
    """
    try:
        # Carregar dados existentes
        try:
            with open("data/dashboard/dashboard_data.json", "r") as f:
                current_data = json.load(f)
        except FileNotFoundError:
            current_data = {}

        # Atualizar com novos dados
        if isinstance(current_data, dict) and isinstance(new_data, dict):
            for key, value in new_data.items():
                if (
                    key in current_data
                    and isinstance(current_data[key], dict)
                    and isinstance(value, dict)
                ):
                    current_data[key].update(value)
                else:
                    current_data[key] = value
        else:
            current_data = new_data

        # Salvar dados atualizados
        with open("data/dashboard/dashboard_data.json", "w") as f:
            json.dump(current_data, f, indent=2)

        return True
    except Exception as e:
        print(f"Erro ao atualizar dashboard: {str(e)}")
        return False
