"""
Sistema de Gamificação para o Agente Concurseiro
Gerencia conquistas, badges, experiência, níveis e estatísticas do usuário.
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict

@dataclass
class Achievement:
    """
    Representa uma conquista do usuário.
    Cada conquista pode ter progresso, ser de diferentes categorias e conceder pontos.
    """
    id: str
    title: str
    description: str
    icon: str
    points: int
    category: str
    earned_date: Optional[str] = None
    progress: float = 0.0
    max_progress: float = 100.0
    is_earned: bool = False

@dataclass
class Badge:
    """
    Representa um badge/medalha do sistema de gamificação.
    Badges têm requisitos, raridade e podem ser conquistados por ações específicas.
    """
    id: str
    name: str
    description: str
    icon: str
    rarity: str  # common, rare, epic, legendary
    requirements: Dict
    earned_date: Optional[str] = None

class GamificationSystem:
    """
    Sistema de gamificação do usuário.
    Gerencia conquistas, badges, experiência, níveis e estatísticas do usuário.
    """
    def __init__(self, user_id: str = "demo_user"):
        """
        Inicializa o sistema de gamificação para um usuário específico.
        Cria diretórios e carrega dados persistidos.
        """
        self.user_id = user_id
        self.user_data_path = f"data/users/{user_id}"
        self.achievements_file = f"{self.user_data_path}/achievements.json"
        self.badges_file = f"{self.user_data_path}/badges.json"
        self.stats_file = f"{self.user_data_path}/stats.json"
        
        # Criar diretório do usuário se não existir
        os.makedirs(self.user_data_path, exist_ok=True)
        
        # Inicializar dados
        self.achievements = self._load_achievements()
        self.badges = self._load_badges()
        self.stats = self._load_stats()
        
        # Definir conquistas disponíveis
        self.available_achievements = self._define_achievements()
        self.available_badges = self._define_badges()
    
    def _define_achievements(self) -> List[Achievement]:
        """Define todas as conquistas disponíveis"""
        return [
            Achievement(
                id="first_login",
                title="Primeiro Acesso",
                description="Bem-vindo ao Agente Concurseiro!",
                icon="🎯",
                points=50,
                category="milestone",
                max_progress=1
            ),
            Achievement(
                id="first_week",
                title="Primeira Semana",
                description="Complete sua primeira semana de estudos",
                icon="📅",
                points=100,
                category="study",
                max_progress=7
            ),
            Achievement(
                id="quiz_streak_3",
                title="Sequência Iniciante",
                description="Complete quiz diário por 3 dias consecutivos",
                icon="🔥",
                points=150,
                category="consistency",
                max_progress=3
            ),
            Achievement(
                id="quiz_streak_7",
                title="Sequência Dedicada",
                description="Complete quiz diário por 7 dias consecutivos",
                icon="🔥",
                points=300,
                category="consistency",
                max_progress=7
            ),
            Achievement(
                id="quiz_streak_30",
                title="Sequência Lendária",
                description="Complete quiz diário por 30 dias consecutivos",
                icon="🏆",
                points=1000,
                category="consistency",
                max_progress=30
            ),
            Achievement(
                id="score_80",
                title="Nota Excelente",
                description="Obtenha 80% ou mais em um simulado",
                icon="⭐",
                points=200,
                category="performance",
                max_progress=1
            ),
            Achievement(
                id="score_90",
                title="Quase Perfeito",
                description="Obtenha 90% ou mais em um simulado",
                icon="🌟",
                points=400,
                category="performance",
                max_progress=1
            ),
            Achievement(
                id="score_95",
                title="Perfeição",
                description="Obtenha 95% ou mais em um simulado",
                icon="💎",
                points=800,
                category="performance",
                max_progress=1
            ),
            Achievement(
                id="study_hours_50",
                title="Estudioso",
                description="Complete 50 horas de estudo",
                icon="📚",
                points=250,
                category="dedication",
                max_progress=50
            ),
            Achievement(
                id="study_hours_100",
                title="Dedicado",
                description="Complete 100 horas de estudo",
                icon="📖",
                points=500,
                category="dedication",
                max_progress=100
            ),
            Achievement(
                id="study_hours_200",
                title="Incansável",
                description="Complete 200 horas de estudo",
                icon="🎓",
                points=1000,
                category="dedication",
                max_progress=200
            ),
            Achievement(
                id="all_subjects",
                title="Conhecimento Amplo",
                description="Estude todas as matérias disponíveis",
                icon="🧠",
                points=300,
                category="knowledge",
                max_progress=8
            ),
            Achievement(
                id="improvement_streak",
                title="Evolução Constante",
                description="Melhore sua pontuação em 3 simulados consecutivos",
                icon="📈",
                points=350,
                category="improvement",
                max_progress=3
            ),
            Achievement(
                id="early_bird",
                title="Madrugador",
                description="Estude antes das 7h da manhã por 5 dias",
                icon="🌅",
                points=200,
                category="schedule",
                max_progress=5
            ),
            Achievement(
                id="night_owl",
                title="Coruja",
                description="Estude depois das 22h por 5 dias",
                icon="🦉",
                points=200,
                category="schedule",
                max_progress=5
            )
        ]
    
    def _define_badges(self) -> List[Badge]:
        """Define todos os badges disponíveis"""
        return [
            Badge(
                id="bronze_student",
                name="Estudante Bronze",
                description="Complete 10 horas de estudo",
                icon="🥉",
                rarity="common",
                requirements={"study_hours": 10}
            ),
            Badge(
                id="silver_student",
                name="Estudante Prata",
                description="Complete 50 horas de estudo",
                icon="🥈",
                rarity="rare",
                requirements={"study_hours": 50}
            ),
            Badge(
                id="gold_student",
                name="Estudante Ouro",
                description="Complete 100 horas de estudo",
                icon="🥇",
                rarity="epic",
                requirements={"study_hours": 100}
            ),
            Badge(
                id="quiz_master",
                name="Mestre dos Quiz",
                description="Complete 100 quiz diários",
                icon="🎯",
                rarity="epic",
                requirements={"daily_quizzes": 100}
            ),
            Badge(
                id="perfectionist",
                name="Perfeccionista",
                description="Obtenha 100% em um simulado",
                icon="💯",
                rarity="legendary",
                requirements={"perfect_score": 1}
            ),
            Badge(
                id="consistency_king",
                name="Rei da Consistência",
                description="Mantenha sequência de 30 dias",
                icon="👑",
                rarity="legendary",
                requirements={"max_streak": 30}
            ),
            Badge(
                id="subject_master_pt",
                name="Mestre do Português",
                description="Obtenha 90%+ em Português por 5 simulados",
                icon="📝",
                rarity="rare",
                requirements={"subject_mastery": {"Português": 5}}
            ),
            Badge(
                id="subject_master_math",
                name="Mestre da Matemática",
                description="Obtenha 90%+ em Matemática por 5 simulados",
                icon="🔢",
                rarity="rare",
                requirements={"subject_mastery": {"Matemática": 5}}
            ),
            Badge(
                id="banca_specialist_cespe",
                name="Especialista CESPE",
                description="Complete 20 simulados da banca CESPE",
                icon="🏛️",
                rarity="epic",
                requirements={"banca_expertise": {"CESPE": 20}}
            )
        ]
    
    def _load_achievements(self) -> List[Achievement]:
        """Carrega conquistas do usuário"""
        try:
            if os.path.exists(self.achievements_file):
                with open(self.achievements_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Achievement(**item) for item in data]
        except Exception as e:
            print(f"Erro ao carregar conquistas: {e}")
        return []
    
    def _load_badges(self) -> List[Badge]:
        """Carrega badges do usuário"""
        try:
            if os.path.exists(self.badges_file):
                with open(self.badges_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return [Badge(**item) for item in data]
        except Exception as e:
            print(f"Erro ao carregar badges: {e}")
        return []
    
    def _load_stats(self) -> Dict:
        """Carrega estatísticas do usuário"""
        default_stats = {
            "total_points": 0,
            "level": 1,
            "experience": 0,
            "study_hours": 0,
            "daily_quizzes_completed": 0,
            "simulados_completed": 0,
            "current_streak": 0,
            "max_streak": 0,
            "best_score": 0,
            "subjects_studied": [],
            "bancas_practiced": [],
            "last_activity": None,
            "achievements_earned": 0,
            "badges_earned": 0
        }
        
        try:
            if os.path.exists(self.stats_file):
                with open(self.stats_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Mesclar com defaults para garantir todas as chaves
                    default_stats.update(data)
        except Exception as e:
            print(f"Erro ao carregar estatísticas: {e}")
        
        return default_stats
    
    def save_data(self):
        """Salva todos os dados do usuário"""
        try:
            # Salvar conquistas
            with open(self.achievements_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(a) for a in self.achievements], f, indent=2, ensure_ascii=False)
            
            # Salvar badges
            with open(self.badges_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(b) for b in self.badges], f, indent=2, ensure_ascii=False)
            
            # Salvar estatísticas
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def add_experience(self, points: int, activity: str = ""):
        """
        Adiciona pontos de experiência ao usuário e verifica se houve level up.
        :param points: Quantidade de experiência a adicionar.
        :param activity: Descrição da atividade que gerou XP.
        """
        old_level = self.stats["level"]
        self.stats["experience"] += points
        self.stats["total_points"] += points
        
        # Calcular novo nível (100 XP por nível, aumentando 50 a cada nível)
        level = 1
        required_xp = 0
        while self.stats["experience"] >= required_xp:
            required_xp += 100 + (level - 1) * 50
            if self.stats["experience"] >= required_xp:
                level += 1
        
        self.stats["level"] = level
        
        # Verificar se subiu de nível
        if level > old_level:
            return self._level_up_reward(level)
        
        return None
    
    def _level_up_reward(self, new_level: int) -> Dict:
        """Recompensa por subir de nível"""
        bonus_points = new_level * 50
        self.stats["total_points"] += bonus_points
        
        return {
            "type": "level_up",
            "new_level": new_level,
            "bonus_points": bonus_points,
            "message": f"🎉 Parabéns! Você subiu para o nível {new_level}!"
        }
    
    def check_achievements(self, activity_data: Dict) -> List[Achievement]:
        """
        Verifica e atualiza conquistas do usuário com base em uma atividade realizada.
        :param activity_data: Dicionário com dados da atividade (ex: tipo, progresso, pontuação).
        :return: Lista de conquistas atualizadas.
        """
        new_achievements = []
        
        for achievement_def in self.available_achievements:
            # Verificar se já foi conquistada
            existing = next((a for a in self.achievements if a.id == achievement_def.id), None)
            if existing and existing.is_earned:
                continue
            
            # Verificar progresso
            progress = self._calculate_achievement_progress(achievement_def, activity_data)
            
            if existing:
                existing.progress = progress
                if progress >= existing.max_progress and not existing.is_earned:
                    existing.is_earned = True
                    existing.earned_date = datetime.now().isoformat()
                    new_achievements.append(existing)
                    self.stats["achievements_earned"] += 1
            else:
                # Criar nova conquista
                new_achievement = Achievement(
                    id=achievement_def.id,
                    title=achievement_def.title,
                    description=achievement_def.description,
                    icon=achievement_def.icon,
                    points=achievement_def.points,
                    category=achievement_def.category,
                    progress=progress,
                    max_progress=achievement_def.max_progress
                )
                
                if progress >= new_achievement.max_progress:
                    new_achievement.is_earned = True
                    new_achievement.earned_date = datetime.now().isoformat()
                    new_achievements.append(new_achievement)
                    self.stats["achievements_earned"] += 1
                
                self.achievements.append(new_achievement)
        
        return new_achievements
    
    def _calculate_achievement_progress(self, achievement: Achievement, activity_data: Dict) -> float:
        """Calcula progresso de uma conquista específica"""
        if achievement.id == "first_login":
            return 1.0
        
        elif achievement.id == "first_week":
            return min(self.stats.get("current_streak", 0), 7)
        
        elif achievement.id.startswith("quiz_streak_"):
            target = int(achievement.id.split("_")[-1])
            return min(self.stats.get("current_streak", 0), target)
        
        elif achievement.id.startswith("score_"):
            target_score = int(achievement.id.split("_")[-1])
            return 1.0 if self.stats.get("best_score", 0) >= target_score else 0.0
        
        elif achievement.id.startswith("study_hours_"):
            target_hours = int(achievement.id.split("_")[-1])
            return min(self.stats.get("study_hours", 0), target_hours)
        
        elif achievement.id == "all_subjects":
            return len(set(self.stats.get("subjects_studied", [])))
        
        elif achievement.id == "improvement_streak":
            return activity_data.get("improvement_streak", 0)
        
        elif achievement.id in ["early_bird", "night_owl"]:
            return activity_data.get(achievement.id, 0)
        
        return 0.0
    
    def update_activity(self, activity_type: str, data: Dict) -> Dict:
        """
        Atualiza estatísticas e progresso do usuário para um tipo de atividade.
        :param activity_type: Tipo da atividade (ex: 'quiz', 'study', 'writing').
        :param data: Dados da atividade.
        :return: Estatísticas atualizadas.
        """
        results = {
            "new_achievements": [],
            "level_up": None,
            "points_earned": 0
        }
        
        # Atualizar estatísticas baseadas no tipo de atividade
        if activity_type == "daily_quiz":
            self.stats["daily_quizzes_completed"] += 1
            self.stats["current_streak"] = data.get("streak", self.stats["current_streak"])
            self.stats["max_streak"] = max(self.stats["max_streak"], self.stats["current_streak"])
            points = 10 + (self.stats["current_streak"] * 2)  # Bonus por sequência
            
        elif activity_type == "simulado":
            self.stats["simulados_completed"] += 1
            score = data.get("score", 0)
            self.stats["best_score"] = max(self.stats["best_score"], score)
            points = int(score / 10)  # 1 ponto por 10% de acerto
            
            # Adicionar matérias estudadas
            subjects = data.get("subjects", [])
            for subject in subjects:
                if subject not in self.stats["subjects_studied"]:
                    self.stats["subjects_studied"].append(subject)
            
            # Adicionar banca praticada
            banca = data.get("banca")
            if banca and banca not in self.stats["bancas_practiced"]:
                self.stats["bancas_practiced"].append(banca)
        
        elif activity_type == "study_session":
            hours = data.get("hours", 0)
            self.stats["study_hours"] += hours
            points = int(hours * 20)  # 20 pontos por hora
        
        else:
            points = data.get("points", 0)
        
        # Adicionar experiência
        level_up = self.add_experience(points, activity_type)
        if level_up:
            results["level_up"] = level_up
        
        results["points_earned"] = points
        
        # Verificar conquistas
        activity_data = {**self.stats, **data}
        new_achievements = self.check_achievements(activity_data)
        results["new_achievements"] = new_achievements
        
        # Adicionar pontos das conquistas
        for achievement in new_achievements:
            self.add_experience(achievement.points, f"achievement_{achievement.id}")
            results["points_earned"] += achievement.points
        
        # Atualizar última atividade
        self.stats["last_activity"] = datetime.now().isoformat()
        
        # Salvar dados
        self.save_data()
        
        return results
    
    def get_user_summary(self) -> Dict:
        """
        Retorna um resumo dos dados de gamificação do usuário para exibição no dashboard.
        Inclui nível, pontos, conquistas, badges, melhor nota, etc.
        :return: Dicionário com resumo dos dados do usuário.
        """
        return {
            "level": self.stats["level"],
            "experience": self.stats["experience"],
            "total_points": self.stats["total_points"],
            "achievements_earned": len([a for a in self.achievements if a.is_earned]),
            "total_achievements": len(self.available_achievements),
            "badges_earned": len([b for b in self.badges if b.earned_date]),
            "total_badges": len(self.available_badges),
            "current_streak": self.stats["current_streak"],
            "max_streak": self.stats["max_streak"],
            "study_hours": self.stats["study_hours"],
            "best_score": self.stats["best_score"]
        }
    
    def get_recent_achievements(self, limit: int = 5) -> List[Achievement]:
        """
        Retorna as conquistas mais recentes do usuário.
        :param limit: Quantidade máxima de conquistas a retornar.
        :return: Lista de conquistas recentes.
        """
        earned_achievements = [a for a in self.achievements if a.is_earned and a.earned_date]
        earned_achievements.sort(key=lambda x: x.earned_date, reverse=True)
        return earned_achievements[:limit]
    
    def get_progress_achievements(self) -> List[Achievement]:
        """
        Retorna conquistas em andamento (ainda não concluídas).
        :return: Lista de conquistas em progresso.
        """
        return [a for a in self.achievements if not a.is_earned and a.progress > 0]
