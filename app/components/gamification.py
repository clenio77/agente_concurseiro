"""
Sistema de Gamificação - Pontos, Badges e Conquistas
Componente para motivar e engajar usuários através de elementos de jogo
"""

import streamlit as st
from datetime import datetime, timedelta
import random
from typing import Dict, List, Any

class GamificationSystem:
    """Sistema completo de gamificação"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializa dados de gamificação na sessão"""
        if 'user_level' not in st.session_state:
            st.session_state.user_level = 1
        
        if 'user_xp' not in st.session_state:
            st.session_state.user_xp = random.randint(150, 800)
        
        if 'user_badges' not in st.session_state:
            st.session_state.user_badges = self.generate_initial_badges()
        
        if 'user_achievements' not in st.session_state:
            st.session_state.user_achievements = self.generate_initial_achievements()
        
        if 'daily_streak' not in st.session_state:
            st.session_state.daily_streak = random.randint(3, 15)
        
        if 'weekly_challenges' not in st.session_state:
            st.session_state.weekly_challenges = self.generate_weekly_challenges()
    
    def get_badges_config(self) -> Dict[str, Dict[str, Any]]:
        """Configuração de todas as badges disponíveis"""
        return {
            'first_steps': {
                'name': '👶 Primeiros Passos',
                'description': 'Complete sua primeira sessão de estudos',
                'icon': '👶',
                'rarity': 'comum',
                'points': 50
            },
            'streak_7': {
                'name': '🔥 Sequência de Fogo',
                'description': 'Estude por 7 dias consecutivos',
                'icon': '🔥',
                'rarity': 'raro',
                'points': 200
            },
            'questions_100': {
                'name': '💯 Centurião',
                'description': 'Resolva 100 questões',
                'icon': '💯',
                'rarity': 'comum',
                'points': 100
            },
            'accuracy_90': {
                'name': '🎯 Atirador de Elite',
                'description': 'Alcance 90% de acerto em um simulado',
                'icon': '🎯',
                'rarity': 'épico',
                'points': 500
            },
            'night_owl': {
                'name': '🦉 Coruja Noturna',
                'description': 'Estude após 22h por 5 dias',
                'icon': '🦉',
                'rarity': 'raro',
                'points': 150
            },
            'early_bird': {
                'name': '🐦 Madrugador',
                'description': 'Estude antes das 6h por 5 dias',
                'icon': '🐦',
                'rarity': 'raro',
                'points': 150
            },
            'marathon': {
                'name': '🏃 Maratonista',
                'description': 'Estude por mais de 8 horas em um dia',
                'icon': '🏃',
                'rarity': 'épico',
                'points': 300
            },
            'perfectionist': {
                'name': '⭐ Perfeccionista',
                'description': 'Acerte 100% das questões em uma matéria',
                'icon': '⭐',
                'rarity': 'lendário',
                'points': 1000
            }
        }
    
    def get_achievements_config(self) -> Dict[str, Dict[str, Any]]:
        """Configuração de conquistas/achievements"""
        return {
            'study_hours_50': {
                'name': '📚 Estudioso Dedicado',
                'description': 'Complete 50 horas de estudo',
                'progress_max': 50,
                'reward_points': 250,
                'icon': '📚'
            },
            'questions_1000': {
                'name': '🎓 Mestre das Questões',
                'description': 'Resolva 1000 questões',
                'progress_max': 1000,
                'reward_points': 500,
                'icon': '🎓'
            },
            'subjects_master': {
                'name': '🧠 Polímata',
                'description': 'Domine todas as matérias (80%+ acerto)',
                'progress_max': 6,
                'reward_points': 750,
                'icon': '🧠'
            },
            'streak_30': {
                'name': '🔥 Chama Eterna',
                'description': 'Mantenha uma sequência de 30 dias',
                'progress_max': 30,
                'reward_points': 1000,
                'icon': '🔥'
            }
        }
    
    def generate_initial_badges(self) -> List[str]:
        """Gera badges iniciais do usuário"""
        badges_config = self.get_badges_config()
        all_badges = list(badges_config.keys())
        # Simular que o usuário já conquistou algumas badges
        earned_badges = random.sample(all_badges, random.randint(2, 5))
        return earned_badges

    def generate_initial_achievements(self) -> Dict[str, int]:
        """Gera progresso inicial das conquistas"""
        achievements_config = self.get_achievements_config()
        achievements = {}
        for achievement_id, config in achievements_config.items():
            # Simular progresso aleatório
            progress = random.randint(0, int(config['progress_max'] * 0.8))
            achievements[achievement_id] = progress
        return achievements
    
    def generate_weekly_challenges(self) -> List[Dict[str, Any]]:
        """Gera desafios semanais"""
        challenges = [
            {
                'id': 'weekly_questions',
                'name': '📝 Maratona de Questões',
                'description': 'Resolva 200 questões esta semana',
                'progress': random.randint(50, 180),
                'target': 200,
                'reward': 300,
                'expires': datetime.now() + timedelta(days=7)
            },
            {
                'id': 'weekly_accuracy',
                'name': '🎯 Precisão Semanal',
                'description': 'Mantenha 85%+ de acerto por 5 dias',
                'progress': random.randint(2, 4),
                'target': 5,
                'reward': 250,
                'expires': datetime.now() + timedelta(days=7)
            },
            {
                'id': 'weekly_subjects',
                'name': '📚 Diversidade de Estudos',
                'description': 'Estude pelo menos 4 matérias diferentes',
                'progress': random.randint(2, 3),
                'target': 4,
                'reward': 200,
                'expires': datetime.now() + timedelta(days=7)
            }
        ]
        return challenges
    
    def calculate_level_from_xp(self, xp: int) -> int:
        """Calcula o nível baseado no XP"""
        # Fórmula: Level = sqrt(XP / 100)
        import math
        return max(1, int(math.sqrt(xp / 100)))
    
    def get_xp_for_next_level(self, current_level: int) -> int:
        """Calcula XP necessário para o próximo nível"""
        return (current_level + 1) ** 2 * 100
    
    def get_badge_rarity_color(self, rarity: str) -> str:
        """Retorna cor baseada na raridade da badge"""
        colors = {
            'comum': '#95a5a6',
            'raro': '#3498db',
            'épico': '#9b59b6',
            'lendário': '#f1c40f'
        }
        return colors.get(rarity, '#95a5a6')
    
    def render_user_profile(self):
        """Renderiza perfil do usuário com nível e XP"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Calcular nível atual
            current_level = self.calculate_level_from_xp(st.session_state.user_xp)
            next_level_xp = self.get_xp_for_next_level(current_level)
            current_level_xp = current_level ** 2 * 100
            progress_to_next = (st.session_state.user_xp - current_level_xp) / (next_level_xp - current_level_xp)
            
            st.markdown(f"""
            <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-bottom: 20px;">
                <h2>🎮 Perfil do Jogador</h2>
                <h1>Nível {current_level}</h1>
                <p style="font-size: 18px;">{st.session_state.user_xp:,} XP</p>
                <p>Próximo nível: {next_level_xp - st.session_state.user_xp:,} XP restantes</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Barra de progresso para próximo nível
            st.progress(progress_to_next)
    
    def render_badges_collection(self):
        """Renderiza coleção de badges do usuário"""
        st.subheader("🏆 Coleção de Badges")
        
        # Badges conquistadas
        st.write("**Badges Conquistadas:**")
        earned_cols = st.columns(4)
        
        for i, badge_id in enumerate(st.session_state.user_badges):
            badges_config = self.get_badges_config()
            badge = badges_config[badge_id]
            col_idx = i % 4
            
            with earned_cols[col_idx]:
                rarity_color = self.get_badge_rarity_color(badge['rarity'])
                st.markdown(f"""
                <div style="text-align: center; padding: 10px; border: 2px solid {rarity_color}; border-radius: 10px; margin: 5px;">
                    <div style="font-size: 30px;">{badge['icon']}</div>
                    <div style="font-size: 12px; font-weight: bold;">{badge['name']}</div>
                    <div style="font-size: 10px; color: {rarity_color};">{badge['rarity'].upper()}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Badges disponíveis (não conquistadas)
        badges_config = self.get_badges_config()
        available_badges = [bid for bid in badges_config.keys() if bid not in st.session_state.user_badges]

        if available_badges:
            st.write("**Badges Disponíveis:**")
            available_cols = st.columns(4)

            for i, badge_id in enumerate(available_badges[:8]):  # Mostrar apenas 8
                badge = badges_config[badge_id]
                col_idx = i % 4
                
                with available_cols[col_idx]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 10px; border: 2px solid #bdc3c7; border-radius: 10px; margin: 5px; opacity: 0.5;">
                        <div style="font-size: 30px;">🔒</div>
                        <div style="font-size: 12px;">???</div>
                        <div style="font-size: 10px; color: #7f8c8d;">{badge['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    def render_achievements_progress(self):
        """Renderiza progresso das conquistas"""
        st.subheader("🎯 Conquistas")

        achievements_config = self.get_achievements_config()
        for achievement_id, config in achievements_config.items():
            progress = st.session_state.user_achievements.get(achievement_id, 0)
            progress_percent = min(progress / config['progress_max'], 1.0)
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{config['icon']} {config['name']}**")
                st.write(config['description'])
                st.progress(progress_percent)
                st.write(f"{progress}/{config['progress_max']} - {config['reward_points']} pontos")
            
            with col2:
                if progress >= config['progress_max']:
                    st.success("✅ Completa!")
                else:
                    remaining = config['progress_max'] - progress
                    st.info(f"Faltam {remaining}")
            
            st.divider()
    
    def render_weekly_challenges(self):
        """Renderiza desafios semanais"""
        st.subheader("⚡ Desafios Semanais")
        
        for challenge in st.session_state.weekly_challenges:
            progress_percent = min(challenge['progress'] / challenge['target'], 1.0)
            days_left = (challenge['expires'] - datetime.now()).days
            
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{challenge['name']}**")
                st.write(challenge['description'])
                st.progress(progress_percent)
                st.write(f"{challenge['progress']}/{challenge['target']} - {challenge['reward']} pontos")
            
            with col2:
                if challenge['progress'] >= challenge['target']:
                    st.success("✅ Completo!")
                else:
                    st.info(f"{days_left} dias restantes")
            
            st.divider()
    
    def render_leaderboard(self):
        """Renderiza ranking/leaderboard"""
        st.subheader("🏆 Ranking Semanal")
        
        # Dados simulados de ranking
        leaderboard_data = [
            {"pos": 1, "nome": "Você", "pontos": st.session_state.user_xp, "badge": "🥇"},
            {"pos": 2, "nome": "ConcurseiroTop", "pontos": st.session_state.user_xp - 50, "badge": "🥈"},
            {"pos": 3, "nome": "EstudanteX", "pontos": st.session_state.user_xp - 120, "badge": "🥉"},
            {"pos": 4, "nome": "FuturoServidor", "pontos": st.session_state.user_xp - 200, "badge": "4️⃣"},
            {"pos": 5, "nome": "Determinado123", "pontos": st.session_state.user_xp - 350, "badge": "5️⃣"},
        ]
        
        for player in leaderboard_data:
            col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
            
            with col1:
                st.write(player["badge"])
            with col2:
                if player["nome"] == "Você":
                    st.write(f"**{player['nome']}** 👈")
                else:
                    st.write(player["nome"])
            with col3:
                st.write(f"{player['pontos']:,} XP")
            with col4:
                st.write(f"#{player['pos']}")
    
    def render_gamification_page(self):
        """Renderiza página completa de gamificação"""
        st.title("🎮 Sistema de Gamificação")
        
        # Perfil do usuário
        self.render_user_profile()
        
        # Tabs para organizar conteúdo
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏆 Badges", "🎯 Conquistas", "⚡ Desafios", "🏆 Ranking", "📊 Estatísticas"
        ])
        
        with tab1:
            self.render_badges_collection()
        
        with tab2:
            self.render_achievements_progress()
        
        with tab3:
            self.render_weekly_challenges()
        
        with tab4:
            self.render_leaderboard()
        
        with tab5:
            self.render_statistics()
    
    def render_statistics(self):
        """Renderiza estatísticas detalhadas"""
        st.subheader("📊 Suas Estatísticas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("🔥 Sequência Atual", f"{st.session_state.daily_streak} dias")
            st.metric("🏆 Badges Conquistadas", f"{len(st.session_state.user_badges)}")
            st.metric("⭐ Pontos Totais", f"{st.session_state.user_xp:,}")
        
        with col2:
            achievements_config = self.get_achievements_config()
            completed_achievements = sum(1 for aid, progress in st.session_state.user_achievements.items()
                                       if progress >= achievements_config[aid]['progress_max'])
            st.metric("🎯 Conquistas Completas", f"{completed_achievements}")
            st.metric("📈 Nível Atual", f"{self.calculate_level_from_xp(st.session_state.user_xp)}")
            st.metric("⚡ Desafios Ativos", f"{len(st.session_state.weekly_challenges)}")
