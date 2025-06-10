"""
Sistema de Notificações para o Agente Concurseiro
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class NotificationType(Enum):
    STUDY_REMINDER = "study_reminder"
    QUIZ_REMINDER = "quiz_reminder"
    GOAL_ACHIEVEMENT = "goal_achievement"
    PERFORMANCE_ALERT = "performance_alert"
    STREAK_MILESTONE = "streak_milestone"
    EXAM_COUNTDOWN = "exam_countdown"
    RECOMMENDATION = "recommendation"

class NotificationPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class Notification:
    """Estrutura de uma notificação"""
    id: str
    type: NotificationType
    priority: NotificationPriority
    title: str
    message: str
    action_text: Optional[str] = None
    action_url: Optional[str] = None
    created_at: str = None
    scheduled_for: Optional[str] = None
    read: bool = False
    dismissed: bool = False
    user_id: str = "demo_user"
    metadata: Dict = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.metadata is None:
            self.metadata = {}

class NotificationManager:
    def __init__(self, user_id: str = "demo_user"):
        self.user_id = user_id
        self.notifications_file = f"data/users/{user_id}/notifications.json"
        self.settings_file = f"data/users/{user_id}/notification_settings.json"
        
        # Criar diretório do usuário se não existir
        os.makedirs(f"data/users/{user_id}", exist_ok=True)
        
        # Carregar notificações e configurações
        self.notifications = self._load_notifications()
        self.settings = self._load_settings()
    
    def _load_notifications(self) -> List[Notification]:
        """Carrega notificações do arquivo"""
        try:
            if os.path.exists(self.notifications_file):
                with open(self.notifications_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    notifications = []
                    for item in data:
                        try:
                            notification = Notification(
                                id=item['id'],
                                type=NotificationType(item['type']),
                                priority=NotificationPriority(item['priority']),
                                title=item['title'],
                                message=item['message'],
                                action_text=item.get('action_text'),
                                action_url=item.get('action_url'),
                                created_at=item['created_at'],
                                scheduled_for=item.get('scheduled_for'),
                                read=item.get('read', False),
                                dismissed=item.get('dismissed', False),
                                user_id=item.get('user_id', self.user_id),
                                metadata=item.get('metadata', {})
                            )
                            notifications.append(notification)
                        except (ValueError, KeyError) as e:
                            print(f"Erro ao carregar notificação: {e}")
                            continue
                    return notifications
        except Exception as e:
            print(f"Erro ao carregar notificações: {e}")
        return []
    
    def _load_settings(self) -> Dict:
        """Carrega configurações de notificação"""
        default_settings = {
            "enabled": True,
            "study_reminders": True,
            "quiz_reminders": True,
            "performance_alerts": True,
            "achievement_notifications": True,
            "exam_countdown": True,
            "quiet_hours": {
                "enabled": False,
                "start": "22:00",
                "end": "07:00"
            },
            "frequency": {
                "study_reminder": "daily",
                "quiz_reminder": "daily",
                "performance_review": "weekly"
            }
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    default_settings.update(data)
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
        
        return default_settings
    
    def save_data(self):
        """Salva notificações e configurações"""
        try:
            # Salvar notificações
            with open(self.notifications_file, 'w', encoding='utf-8') as f:
                json.dump([asdict(n) for n in self.notifications], f, indent=2, ensure_ascii=False, default=str)
            
            # Salvar configurações
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
    
    def create_notification(self, notification_type: NotificationType, title: str, 
                          message: str, priority: NotificationPriority = NotificationPriority.MEDIUM,
                          action_text: str = None, action_url: str = None,
                          scheduled_for: datetime = None, metadata: Dict = None) -> Notification:
        """Cria uma nova notificação"""
        
        # Verificar se notificações estão habilitadas
        if not self.settings.get("enabled", True):
            return None
        
        # Verificar configurações específicas do tipo
        type_enabled = self.settings.get(f"{notification_type.value}s", True)
        if not type_enabled:
            return None
        
        # Gerar ID único
        notification_id = f"{notification_type.value}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        notification = Notification(
            id=notification_id,
            type=notification_type,
            priority=priority,
            title=title,
            message=message,
            action_text=action_text,
            action_url=action_url,
            scheduled_for=scheduled_for.isoformat() if scheduled_for else None,
            user_id=self.user_id,
            metadata=metadata or {}
        )
        
        self.notifications.append(notification)
        self.save_data()
        
        return notification
    
    def get_unread_notifications(self, limit: int = 10) -> List[Notification]:
        """Retorna notificações não lidas"""
        unread = [n for n in self.notifications if not n.read and not n.dismissed]
        unread.sort(key=lambda x: (x.priority.value, x.created_at), reverse=True)
        return unread[:limit]
    
    def get_recent_notifications(self, days: int = 7, limit: int = 20) -> List[Notification]:
        """Retorna notificações recentes"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent = [
            n for n in self.notifications 
            if datetime.fromisoformat(n.created_at) >= cutoff_date
        ]
        recent.sort(key=lambda x: x.created_at, reverse=True)
        return recent[:limit]
    
    def mark_as_read(self, notification_id: str):
        """Marca notificação como lida"""
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.read = True
                self.save_data()
                break
    
    def dismiss_notification(self, notification_id: str):
        """Descarta notificação"""
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.dismissed = True
                self.save_data()
                break
    
    def generate_study_reminders(self, user_data: Dict):
        """Gera lembretes de estudo baseados no padrão do usuário"""
        
        # Verificar última atividade
        last_activity = user_data.get('last_activity')
        if last_activity:
            last_date = datetime.fromisoformat(last_activity)
            hours_since = (datetime.now() - last_date).total_seconds() / 3600
            
            # Lembrete se não estudou há mais de 24 horas
            if hours_since > 24:
                self.create_notification(
                    NotificationType.STUDY_REMINDER,
                    "⏰ Hora de estudar!",
                    f"Você não estuda há {int(hours_since)} horas. Que tal uma sessão rápida?",
                    NotificationPriority.MEDIUM,
                    "Começar estudo",
                    "/plano-estudos"
                )
        
        # Lembrete de quiz diário
        daily_quiz_completed = user_data.get('daily_quiz_completed_today', False)
        if not daily_quiz_completed:
            self.create_notification(
                NotificationType.QUIZ_REMINDER,
                "🎯 Quiz diário disponível",
                "Complete seu quiz diário para manter a sequência!",
                NotificationPriority.LOW,
                "Fazer quiz",
                "/simulados"
            )
    
    def generate_performance_alerts(self, user_data: Dict):
        """Gera alertas baseados no desempenho"""
        
        # Alerta de queda de desempenho
        recent_scores = user_data.get('recent_mock_scores', [])
        if len(recent_scores) >= 3:
            last_three = recent_scores[-3:]
            if all(last_three[i] > last_three[i+1] for i in range(len(last_three)-1)):
                self.create_notification(
                    NotificationType.PERFORMANCE_ALERT,
                    "📉 Atenção: Queda no desempenho",
                    "Suas últimas pontuações estão em declínio. Vamos revisar sua estratégia?",
                    NotificationPriority.HIGH,
                    "Ver análise",
                    "/analytics"
                )
        
        # Alerta de meta próxima
        current_score = user_data.get('average_score', 0)
        target_score = user_data.get('target_score', 80)
        
        if current_score >= target_score * 0.9:  # 90% da meta
            self.create_notification(
                NotificationType.GOAL_ACHIEVEMENT,
                "🎯 Quase lá!",
                f"Você está a apenas {target_score - current_score:.1f} pontos da sua meta!",
                NotificationPriority.MEDIUM,
                "Ver progresso",
                "/dashboard"
            )
    
    def generate_streak_notifications(self, user_data: Dict):
        """Gera notificações de sequência"""
        
        current_streak = user_data.get('current_streak', 0)
        
        # Marcos de sequência
        milestones = [7, 14, 30, 60, 100]
        
        for milestone in milestones:
            if current_streak == milestone:
                self.create_notification(
                    NotificationType.STREAK_MILESTONE,
                    f"🔥 {milestone} dias de sequência!",
                    f"Parabéns! Você manteve uma sequência de {milestone} dias de estudo!",
                    NotificationPriority.HIGH,
                    "Ver conquistas",
                    "/dashboard"
                )
                break
    
    def generate_exam_countdown(self, exam_date: str):
        """Gera notificações de contagem regressiva"""
        
        try:
            exam_datetime = datetime.strptime(exam_date, "%Y-%m-%d")
            days_remaining = (exam_datetime - datetime.now()).days
            
            # Marcos de contagem regressiva
            if days_remaining in [90, 60, 30, 15, 7, 3, 1]:
                urgency = NotificationPriority.HIGH if days_remaining <= 7 else NotificationPriority.MEDIUM
                
                self.create_notification(
                    NotificationType.EXAM_COUNTDOWN,
                    f"📅 {days_remaining} dias para a prova!",
                    f"Faltam apenas {days_remaining} dias. Vamos intensificar os estudos?",
                    urgency,
                    "Revisar plano",
                    "/plano-estudos"
                )
        
        except ValueError:
            pass  # Data inválida
    
    def generate_smart_recommendations(self, user_data: Dict, recommendations: List[Dict]):
        """Gera notificações baseadas em recomendações da IA"""
        
        # Pegar recomendações de alta prioridade
        high_priority_recs = [r for r in recommendations if r.get('priority') == 'high']
        
        for rec in high_priority_recs[:2]:  # Máximo 2 por vez
            self.create_notification(
                NotificationType.RECOMMENDATION,
                f"💡 {rec['title']}",
                rec['description'],
                NotificationPriority.MEDIUM,
                "Ver detalhes",
                "/analytics",
                metadata={"recommendation_id": rec.get('id')}
            )
    
    def process_scheduled_notifications(self):
        """Processa notificações agendadas"""
        now = datetime.now()
        
        for notification in self.notifications:
            if (notification.scheduled_for and 
                not notification.read and 
                not notification.dismissed):
                
                scheduled_time = datetime.fromisoformat(notification.scheduled_for)
                if now >= scheduled_time:
                    # Notificação deve ser exibida agora
                    notification.scheduled_for = None
                    self.save_data()
    
    def cleanup_old_notifications(self, days: int = 30):
        """Remove notificações antigas"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        self.notifications = [
            n for n in self.notifications
            if datetime.fromisoformat(n.created_at) >= cutoff_date
        ]
        
        self.save_data()
    
    def get_notification_summary(self) -> Dict:
        """Retorna resumo das notificações"""
        unread_count = len([n for n in self.notifications if not n.read and not n.dismissed])
        
        # Contar por tipo
        type_counts = {}
        for notification in self.notifications:
            if not notification.read and not notification.dismissed:
                type_name = notification.type.value
                type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        return {
            "total_unread": unread_count,
            "by_type": type_counts,
            "has_urgent": any(
                n.priority == NotificationPriority.URGENT 
                for n in self.notifications 
                if not n.read and not n.dismissed
            )
        }
    
    def update_settings(self, new_settings: Dict):
        """Atualiza configurações de notificação"""
        self.settings.update(new_settings)
        self.save_data()

def generate_daily_notifications(user_id: str, user_data: Dict):
    """Função para gerar notificações diárias (pode ser chamada por um scheduler)"""
    
    manager = NotificationManager(user_id)
    
    # Gerar diferentes tipos de notificação
    manager.generate_study_reminders(user_data)
    manager.generate_performance_alerts(user_data)
    manager.generate_streak_notifications(user_data)
    
    # Verificar data da prova se disponível
    exam_date = user_data.get('exam_date')
    if exam_date:
        manager.generate_exam_countdown(exam_date)
    
    # Processar notificações agendadas
    manager.process_scheduled_notifications()
    
    # Limpeza periódica
    manager.cleanup_old_notifications()
    
    return manager.get_notification_summary()
