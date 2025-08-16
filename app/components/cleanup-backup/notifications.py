"""
Sistema de Notificações para o Agente Concurseiro
Gerencia notificações, lembretes, alertas e recomendações para o usuário.
"""

import logging
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any, Dict, List

import requests

# Configurar logger local
logger = logging.getLogger(__name__)

# Exceções locais
class ExternalServiceError(Exception):
    def __init__(self, service: str, message: str, details: Dict = None):
        self.service = service
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

class ConfigurationError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

# Configurações locais (simuladas)
class Settings:
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "seu-email@gmail.com"
    SMTP_PASSWORD = "sua-senha"

settings = Settings()

# Classes simuladas para User e Notification
class User:
    def __init__(self, id: str, email: str):
        self.id = id
        self.email = email
        self.push_token = None

class Notification:
    def __init__(self, id: str, user_id: str, title: str, message: str):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.message = message

def log_user_activity(logger, user_id: str, action: str, details: str):
    """Função local para logging de atividade do usuário"""
    logger.info(f"User {user_id} performed {action}: {details}")

class NotificationType:
    """Tipos de notificação disponíveis"""
    STUDY_REMINDER = "study_reminder"
    EXAM_REMINDER = "exam_reminder"
    ACHIEVEMENT = "achievement"
    PERFORMANCE_UPDATE = "performance_update"
    SYSTEM_ALERT = "system_alert"
    STUDY_PLAN_READY = "study_plan_ready"
    DAILY_SUMMARY = "daily_summary"
    WEEKLY_REPORT = "weekly_report"

class NotificationPriority:
    """Prioridades de notificação"""
    LOW = "low"
    NORMAL = "normal"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class NotificationManager:
    """Gerenciador centralizado de notificações"""

    def __init__(self, user_id: str = None):
        self.user_id = user_id
        self.notification_types = {
            "study_reminder": {
                "title": "Lembrete de Estudo",
                "template": "study_reminder.html",
                "channels": ["email", "push", "in_app"]
            },
            "exam_reminder": {
                "title": "Lembrete de Prova",
                "template": "exam_reminder.html",
                "channels": ["email", "push", "in_app"]
            },
            "achievement": {
                "title": "Nova Conquista!",
                "template": "achievement.html",
                "channels": ["email", "push", "in_app"]
            },
            "performance_update": {
                "title": "Atualização de Desempenho",
                "template": "performance_update.html",
                "channels": ["email", "in_app"]
            },
            "system_alert": {
                "title": "Alerta do Sistema",
                "template": "system_alert.html",
                "channels": ["email", "in_app"]
            },
            "study_plan_ready": {
                "title": "Plano de Estudo Pronto",
                "template": "study_plan_ready.html",
                "channels": ["email", "push", "in_app"]
            }
        }

        # Configurações de canais
        self.channels = {
            "email": self._send_email_notification,
            "push": self._send_push_notification,
            "in_app": self._save_in_app_notification
        }

    async def send_notification(
        self,
        user: User,
        notification_type: str,
        data: Dict[str, Any],
        channels: List[str] = None,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Envia notificação para o usuário"""

        if notification_type not in self.notification_types:
            raise ValueError(f"Tipo de notificação '{notification_type}' não suportado")

        # Usar canais padrão se não especificados
        if channels is None:
            channels = self.notification_types[notification_type]["channels"]

        # Verificar preferências do usuário
        user_preferences = self._get_user_notification_preferences(user)
        channels = [
            ch
            for ch in channels
            if ch in user_preferences.get("enabled_channels", channels)
        ]

        results = {}

        for channel in channels:
            try:
                if channel == "email":
                    result = await self._send_email_notification(
                        user, notification_type, data, priority
                    )
                elif channel == "push":
                    result = await self._send_push_notification(
                        user, notification_type, data, priority
                    )
                elif channel == "in_app":
                    result = await self._save_in_app_notification(
                        user, notification_type, data, priority
                    )
                else:
                    result = {"success": False, "error": f"Canal '{channel}' não suportado"}

                results[channel] = result

            except Exception as e:
                logger.error(f"Erro ao enviar notificação via {channel}: {e}")
                results[channel] = {"success": False, "error": str(e)}

        # Log da atividade
        log_user_activity(
            logger,
            user.id,
            "notification_sent",
            f"Tipo: {notification_type}, Canais: {list(results.keys())}"
        )

        return results

    async def _send_email_notification(
        self,
        user: User,
        notification_type: str,
        data: Dict[str, Any],
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Envia notificação por email"""

        try:
            # Verificar configurações de email
            if not all(
                [
                    settings.SMTP_SERVER,
                    settings.SMTP_PORT,
                    settings.SMTP_USER,
                    settings.SMTP_PASSWORD,
                ]
            ):
                raise ConfigurationError("Configurações de email incompletas")

            # Preparar conteúdo
            notification_config = self.notification_types[notification_type]
            subject = notification_config["title"]

            # Gerar conteúdo HTML
            html_content = self._generate_email_content(notification_type, data, user)

            # Criar mensagem
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.SMTP_USER
            msg['To'] = user.email
            msg['Priority'] = 'high' if priority == 'high' else 'normal'

            # Adicionar conteúdo HTML
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)

            # Enviar email
            with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)

            logger.info(f"Email enviado para {user.email}: {subject}")

            return {"success": True, "message": "Email enviado com sucesso"}

        except Exception as e:
            logger.error(f"Erro ao enviar email para {user.email}: {e}")
            raise ExternalServiceError("email", f"Erro ao enviar email: {str(e)}")

    async def _send_push_notification(
        self,
        user: User,
        notification_type: str,
        data: Dict[str, Any],
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Envia notificação push"""

        try:
            # Verificar se usuário tem token de push
            push_token = getattr(user, 'push_token', None)
            if not push_token:
                return {
                    "success": False,
                    "error": "Usuário não tem token de push configurado"
                }

            # Configurações de push (exemplo com Firebase)
            notification_config = self.notification_types[notification_type]

            push_data = {
                "to": push_token,
                "notification": {
                    "title": notification_config["title"],
                    "body": self._generate_push_content(notification_type, data),
                    "priority": priority
                },
                "data": {
                    "type": notification_type,
                    "user_id": str(user.id),
                    "timestamp": datetime.utcnow().isoformat()
                }
            }

            # Enviar via Firebase (exemplo)
            if settings.FIREBASE_SERVER_KEY:
                headers = {
                    "Authorization": f"key={settings.FIREBASE_SERVER_KEY}",
                    "Content-Type": "application/json"
                }

                response = requests.post(
                    "https://fcm.googleapis.com/fcm/send",
                    headers=headers,
                    json=push_data,
                    timeout=10
                )

                if response.status_code == 200:
                    logger.info(f"Push notification enviado para {user.username}")
                    return {"success": True, "message": "Push notification enviado"}
                else:
                    raise ExternalServiceError(
                        "firebase", f"HTTP {response.status_code}"
                    )
            else:
                # Simular envio para desenvolvimento
                logger.info(
                    f"Push notification simulado para {user.username}: {push_data}"
                )
                return {"success": True, "message": "Push notification simulado"}

        except Exception as e:
            logger.error(f"Erro ao enviar push notification: {e}")
            raise ExternalServiceError("push", f"Erro ao enviar push: {str(e)}")

    async def _save_in_app_notification(
        self,
        user: User,
        notification_type: str,
        data: Dict[str, Any],
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """Salva notificação in-app no banco de dados"""

        try:
            notification_config = self.notification_types[notification_type]

            # Criar notificação no banco
            Notification(
                user_id=user.id,
                type=notification_type,
                title=notification_config["title"],
                message=self._generate_in_app_content(notification_type, data),
                data=data,
                priority=priority,
                read=False,
                created_at=datetime.utcnow()
            )

            # Salvar no banco (requer sessão)
            # Nota: Em uma implementação real, você precisaria passar a sessão do banco
            logger.info(
                f"Notificação in-app salva para {user.username}: {notification_type}"
            )

            return {"success": True, "message": "Notificação in-app salva"}

        except Exception as e:
            logger.error(f"Erro ao salvar notificação in-app: {e}")
            raise ExternalServiceError(
                "database", f"Erro ao salvar notificação: {str(e)}"
            )

    def _generate_email_content(
        self, notification_type: str, data: Dict[str, Any], user: User
    ) -> str:
        """Gera conteúdo HTML para email"""

        base_template = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: #2c3e50; color: white; padding: 20px; text-align: center; }
                .content { padding: 20px; background: #f9f9f9; }
                .footer { text-align: center; padding: 20px; color: #666; font-size: 12px; }
                .button { display: inline-block; padding: 10px 20px; background: #3498db; color: white; text-decoration: none; border-radius: 5px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Agente Concurseiro</h1>
                </div>
                <div class="content">
                    {content}
                </div>
                <div class="footer">
                    <p>Esta é uma notificação automática do Agente Concurseiro.</p>
                    <p>Para desativar notificações, acesse suas configurações.</p>
                </div>
            </div>
        </body>
        </html>
        """

        if notification_type == "study_reminder":
            content = f"""
            <h2>Olá, {user.full_name}!</h2>
            <p>É hora de estudar! Seu plano de estudo indica que você deve revisar:</p>
            <ul>
                <li><strong>Disciplina:</strong> {data.get('subject', 'Não especificado')}</li>
                <li><strong>Tópico:</strong> {data.get('topic', 'Não especificado')}</li>
                <li><strong>Tempo estimado:</strong> {data.get('duration', '30')} minutos</li>
            </ul>
            <p><a href="{settings.FRONTEND_URL}/study" class="button">Começar a Estudar</a></p>
            """

        elif notification_type == "achievement":
            content = f"""
            <h2>Parabéns, {user.full_name}!</h2>
            <p>Você conquistou uma nova medalha:</p>
            <div style="text-align: center; margin: 20px 0;">
                <h3>🏆 {data.get('achievement_name', 'Nova Conquista')}</h3>
                <p>{data.get('description', '')}</p>
            </div>
            <p><a href="{settings.FRONTEND_URL}/achievements" class="button">Ver Conquistas</a></p>
            """

        elif notification_type == "study_plan_ready":
            content = f"""
            <h2>Seu plano de estudo está pronto!</h2>
            <p>Olá, {user.full_name}! Seu plano personalizado para o concurso {data.get('concurso', '')} foi criado.</p>
            <ul>
                <li><strong>Concurso:</strong> {data.get('concurso', '')}</li>
                <li><strong>Cargo:</strong> {data.get('cargo', '')}</li>
                <li><strong>Duração:</strong> {data.get('duration_months', '')} meses</li>
            </ul>
            <p><a href="{settings.FRONTEND_URL}/study-plan" class="button">Ver Plano de Estudo</a></p>
            """

        else:
            content = f"""
            <h2>{self.notification_types[notification_type]['title']}</h2>
            <p>{data.get('message', 'Nova notificação disponível.')}</p>
            """

        return base_template.format(content=content)

    def _generate_push_content(
        self, notification_type: str, data: Dict[str, Any]
    ) -> str:
        """Gera conteúdo para push notification"""

        if notification_type == "study_reminder":
            return f"Lembrete: Estudar {data.get('subject', '')} - {data.get('topic', '')}"
        elif notification_type == "achievement":
            return f"🏆 Nova conquista: {data.get('achievement_name', '')}"
        elif notification_type == "study_plan_ready":
            return f"Seu plano de estudo para {data.get('concurso', '')} está pronto!"
        else:
            return data.get('message', 'Nova notificação')

    def _generate_in_app_content(
        self, notification_type: str, data: Dict[str, Any]
    ) -> str:
        """Gera conteúdo para notificação in-app"""

        if notification_type == "study_reminder":
            return f"Lembrete de estudo: {data.get('subject', '')} - {data.get('topic', '')}"
        elif notification_type == "achievement":
            return f"Conquista desbloqueada: {data.get('achievement_name', '')}"
        elif notification_type == "study_plan_ready":
            return f"Plano de estudo criado para {data.get('concurso', '')}"
        else:
            return data.get('message', 'Nova notificação')

    def _get_user_notification_preferences(self, user: User) -> Dict[str, Any]:
        """Obtém preferências de notificação do usuário"""

        # Em uma implementação real, isso viria do banco de dados
        # Por enquanto, retornar configurações padrão
        return {
            "enabled_channels": ["email", "in_app"],
            "email_frequency": "daily",
            "push_enabled": False,
            "quiet_hours": {
                "start": "22:00",
                "end": "08:00"
            }
        }

    async def send_bulk_notification(
        self,
        users: List[User],
        notification_type: str,
        data: Dict[str, Any],
        channels: List[str] = None
    ) -> Dict[str, Any]:
        """Envia notificação para múltiplos usuários"""

        results = {
            "total_users": len(users),
            "successful": 0,
            "failed": 0,
            "errors": []
        }

        for user in users:
            try:
                result = await self.send_notification(
                    user, notification_type, data, channels
                )

                # Verificar se pelo menos um canal funcionou
                if any(r.get("success", False) for r in result.values()):
                    results["successful"] += 1
                else:
                    results["failed"] += 1
                    results["errors"].append({
                        "user_id": user.id,
                        "username": user.username,
                        "errors": result
                    })

            except Exception as e:
                results["failed"] += 1
                results["errors"].append({
                    "user_id": user.id,
                    "username": user.username,
                    "error": str(e)
                })

        logger.info(
            f"Bulk notification sent: {results['successful']} successful, "
            f"{results['failed']} failed"
        )
        return results

    async def schedule_notification(
        self,
        user: User,
        notification_type: str,
        data: Dict[str, Any],
        scheduled_time: datetime,
        channels: List[str] = None
    ) -> Dict[str, Any]:
        """Agenda notificação para envio futuro"""

        # Em uma implementação real, isso seria salvo no banco de dados
        # e processado por um worker/background task

        {
            "user_id": user.id,
            "notification_type": notification_type,
            "data": data,
            "channels": channels
            or self.notification_types[notification_type]["channels"],
            "scheduled_time": scheduled_time,
            "created_at": datetime.utcnow()
        }

        logger.info(f"Notification scheduled for {user.username} at {scheduled_time}")

        return {
            "success": True,
            "scheduled_time": scheduled_time.isoformat(),
            "notification_id": f"scheduled_{int(scheduled_time.timestamp())}"
        }

    def create_notification(
        self, notification_type: str, title: str, message: str,
        priority: str = "normal", data: dict = None
    ) -> dict:
        """Cria uma nova notificação"""

        try:
            notification_data = {
                "type": notification_type,
                "title": title,
                "message": message,
                "priority": priority,
                "data": data or {},
                "created_at": datetime.utcnow().isoformat()
            }

            logger.info(f"Notificação criada: {title}")

            return {
                "success": True,
                "notification": notification_data,
                "notification_id": f"notif_{int(datetime.utcnow().timestamp())}"
            }

        except Exception as e:
            logger.error(f"Erro ao criar notificação: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    def get_unread_notifications(self, limit: int = 10) -> list:
        """Obtém notificações não lidas (simulado)"""
        # Em produção, isso viria do banco de dados
        return []

    def mark_as_read(self, notification_id: str) -> bool:
        """Marca notificação como lida"""
        # Em produção, isso seria salvo no banco de dados
        return True

    def dismiss_notification(self, notification_id: str) -> bool:
        """Descartar notificação"""
        # Em produção, isso seria salvo no banco de dados
        return True

# Instância global
notification_manager = NotificationManager()

# Funções utilitárias
async def send_study_reminder(
    user: User, subject: str, topic: str, duration: int = 30
):
    """Envia lembrete de estudo"""
    data = {
        "subject": subject,
        "topic": topic,
        "duration": duration
    }

    return await notification_manager.send_notification(
        user, "study_reminder", data, priority="normal"
    )

async def send_achievement_notification(
    user: User, achievement_name: str, description: str
):
    """Envia notificação de conquista"""
    data = {
        "achievement_name": achievement_name,
        "description": description
    }

    return await notification_manager.send_notification(
        user, "achievement", data, priority="high"
    )

async def send_study_plan_notification(
    user: User, concurso: str, cargo: str, duration_months: int
):
    """Envia notificação de plano de estudo pronto"""
    data = {
        "concurso": concurso,
        "cargo": cargo,
        "duration_months": duration_months
    }

    return await notification_manager.send_notification(
        user, "study_plan_ready", data, priority="high"
    )

async def generate_daily_notifications():
    """Gera notificações diárias para todos os usuários ativos"""
    NotificationManager()

    try:
        # Aqui você implementaria a lógica para buscar usuários ativos
        # e gerar notificações personalizadas baseadas em seus dados

        # Exemplo de notificação diária
        {
            "date": datetime.now().strftime("%d/%m/%Y"),
            "message": "Bom dia! Que tal revisar o que estudou ontem?",
            "suggested_activities": [
                "Revisar flashcards",
                "Fazer quiz diário",
                "Continuar plano de estudos"
            ]
        }

        logger.info("Notificações diárias geradas com sucesso")
        return {"success": True, "notifications_sent": 0}

    except Exception as e:
        logger.error(f"Erro ao gerar notificações diárias: {e}")
        return {"success": False, "error": str(e)}
