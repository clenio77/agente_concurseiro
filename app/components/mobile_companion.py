#!/usr/bin/env python3
"""
Mobile Companion - Fase 2
Versão responsiva com notificações push e sincronização em tempo real
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import uuid
from typing import Dict, List, Any, Optional
from enum import Enum
import json

class DeviceType(Enum):
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"

class NotificationType(Enum):
    STUDY_REMINDER = "study_reminder"
    GROUP_MESSAGE = "group_message"
    DEADLINE_ALERT = "deadline_alert"
    ACHIEVEMENT = "achievement"
    MENTOR_MESSAGE = "mentor_message"
    MATERIAL_SHARED = "material_shared"

class SyncStatus(Enum):
    SYNCED = "synced"
    SYNCING = "syncing"
    OFFLINE = "offline"
    ERROR = "error"

class MobileCompanion:
    def __init__(self):
        self.initialize_session_state()
        self.detect_device_type()
    
    def initialize_session_state(self):
        """Inicializa o estado da sessão para o companion móvel"""
        if 'mobile_settings' not in st.session_state:
            st.session_state.mobile_settings = {
                'notifications_enabled': True,
                'offline_mode': False,
                'sync_frequency': 'real_time',
                'data_saver': False,
                'dark_mode': False,
                'quick_actions': ['study_timer', 'flashcards', 'notes', 'progress']
            }
        
        if 'push_notifications' not in st.session_state:
            st.session_state.push_notifications = self.generate_sample_notifications()
        
        if 'offline_data' not in st.session_state:
            st.session_state.offline_data = self.generate_offline_data()
        
        if 'sync_status' not in st.session_state:
            st.session_state.sync_status = SyncStatus.SYNCED
        
        if 'device_info' not in st.session_state:
            st.session_state.device_info = {
                'type': DeviceType.DESKTOP,
                'screen_width': 1920,
                'screen_height': 1080,
                'is_touch': False,
                'connection': 'wifi'
            }
    
    def detect_device_type(self):
        """Detecta o tipo de dispositivo (simulado)"""
        # Em uma implementação real, isso seria feito via JavaScript
        # Por enquanto, vamos simular baseado em configurações
        screen_width = st.session_state.device_info['screen_width']
        
        if screen_width < 768:
            st.session_state.device_info['type'] = DeviceType.MOBILE
        elif screen_width < 1024:
            st.session_state.device_info['type'] = DeviceType.TABLET
        else:
            st.session_state.device_info['type'] = DeviceType.DESKTOP
    
    def generate_sample_notifications(self) -> List[Dict[str, Any]]:
        """Gera notificações de exemplo"""
        notifications = []
        
        notification_templates = [
            {
                'type': NotificationType.STUDY_REMINDER,
                'title': '⏰ Hora de Estudar!',
                'message': 'Sua sessão de Direito Constitucional está agendada para agora.',
                'priority': 'high'
            },
            {
                'type': NotificationType.GROUP_MESSAGE,
                'title': '💬 Nova Mensagem no Grupo',
                'message': 'João compartilhou um material sobre Português.',
                'priority': 'medium'
            },
            {
                'type': NotificationType.DEADLINE_ALERT,
                'title': '🚨 Prazo se Aproximando',
                'message': 'Inscrições para o concurso terminam em 3 dias!',
                'priority': 'high'
            },
            {
                'type': NotificationType.ACHIEVEMENT,
                'title': '🏆 Conquista Desbloqueada!',
                'message': 'Você completou 7 dias consecutivos de estudo!',
                'priority': 'low'
            },
            {
                'type': NotificationType.MENTOR_MESSAGE,
                'title': '🎓 Mensagem do Mentor',
                'message': 'Prof. Silva respondeu sua dúvida sobre Matemática.',
                'priority': 'medium'
            },
            {
                'type': NotificationType.MATERIAL_SHARED,
                'title': '📚 Novo Material Disponível',
                'message': 'Resumo de História do Brasil foi adicionado ao grupo.',
                'priority': 'low'
            }
        ]
        
        for i, template in enumerate(notification_templates):
            notification = template.copy()
            notification.update({
                'id': str(uuid.uuid4()),
                'timestamp': datetime.now() - timedelta(minutes=random.randint(1, 120)),
                'read': random.choice([True, False]),
                'action_url': f'/action/{i}',
                'icon': self.get_notification_icon(template['type'])
            })
            notifications.append(notification)
        
        return sorted(notifications, key=lambda x: x['timestamp'], reverse=True)
    
    def get_notification_icon(self, notification_type: NotificationType) -> str:
        """Retorna ícone para tipo de notificação"""
        icons = {
            NotificationType.STUDY_REMINDER: '⏰',
            NotificationType.GROUP_MESSAGE: '💬',
            NotificationType.DEADLINE_ALERT: '🚨',
            NotificationType.ACHIEVEMENT: '🏆',
            NotificationType.MENTOR_MESSAGE: '🎓',
            NotificationType.MATERIAL_SHARED: '📚'
        }
        return icons.get(notification_type, '📱')
    
    def generate_offline_data(self) -> Dict[str, Any]:
        """Gera dados para modo offline"""
        return {
            'flashcards': [
                {
                    'id': str(uuid.uuid4()),
                    'front': 'O que é a Constituição Federal?',
                    'back': 'Lei fundamental e suprema do Estado brasileiro, estabelecendo direitos, deveres e organização do poder.',
                    'subject': 'Direito Constitucional',
                    'difficulty': 'medium',
                    'last_reviewed': datetime.now() - timedelta(days=2)
                },
                {
                    'id': str(uuid.uuid4()),
                    'front': 'Qual a fórmula da área do círculo?',
                    'back': 'A = π × r²',
                    'subject': 'Matemática',
                    'difficulty': 'easy',
                    'last_reviewed': datetime.now() - timedelta(days=1)
                },
                {
                    'id': str(uuid.uuid4()),
                    'front': 'Quando foi proclamada a República no Brasil?',
                    'back': '15 de novembro de 1889',
                    'subject': 'História',
                    'difficulty': 'easy',
                    'last_reviewed': datetime.now() - timedelta(days=3)
                }
            ],
            'notes': [
                {
                    'id': str(uuid.uuid4()),
                    'title': 'Resumo - Direitos Fundamentais',
                    'content': 'Os direitos fundamentais são classificados em: 1) Direitos individuais, 2) Direitos coletivos, 3) Direitos sociais...',
                    'subject': 'Direito Constitucional',
                    'created_at': datetime.now() - timedelta(days=1),
                    'tags': ['direitos', 'constituição', 'fundamentais']
                },
                {
                    'id': str(uuid.uuid4()),
                    'title': 'Fórmulas de Matemática',
                    'content': 'Área do triângulo: A = (b×h)/2\nÁrea do retângulo: A = b×h\nVolume do cubo: V = a³',
                    'subject': 'Matemática',
                    'created_at': datetime.now() - timedelta(hours=6),
                    'tags': ['fórmulas', 'geometria', 'área']
                }
            ],
            'progress_data': {
                'daily_goals': {
                    'study_hours': 4,
                    'completed_hours': 2.5,
                    'questions_answered': 50,
                    'completed_questions': 32,
                    'flashcards_reviewed': 20,
                    'completed_flashcards': 15
                },
                'weekly_stats': {
                    'total_hours': 18.5,
                    'goal_hours': 28,
                    'subjects_studied': 5,
                    'avg_performance': 78.5
                }
            },
            'cached_materials': [
                {
                    'id': str(uuid.uuid4()),
                    'title': 'Resumo Direito Administrativo',
                    'type': 'PDF',
                    'size': '2.3 MB',
                    'downloaded_at': datetime.now() - timedelta(hours=2),
                    'expires_at': datetime.now() + timedelta(days=7)
                }
            ]
        }
    
    def render_mobile_dashboard(self):
        """Renderiza dashboard otimizado para mobile"""
        st.markdown("### 📱 Dashboard Mobile")
        
        # Detectar tipo de dispositivo
        device_type = st.session_state.device_info['type']
        
        if device_type == DeviceType.MOBILE:
            # Layout para mobile (1 coluna)
            self.render_mobile_layout()
        elif device_type == DeviceType.TABLET:
            # Layout para tablet (2 colunas)
            self.render_tablet_layout()
        else:
            # Layout para desktop (3 colunas)
            self.render_desktop_layout()
    
    def render_mobile_layout(self):
        """Layout otimizado para mobile"""
        st.markdown("""
        <style>
        .mobile-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            color: white;
            text-align: center;
        }
        .quick-action {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            margin: 5px;
            text-align: center;
            border: 1px solid #dee2e6;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Status de sincronização
        sync_status = st.session_state.sync_status
        sync_color = {
            SyncStatus.SYNCED: "🟢",
            SyncStatus.SYNCING: "🟡", 
            SyncStatus.OFFLINE: "🔴",
            SyncStatus.ERROR: "🟠"
        }
        
        st.markdown(f"""
        <div class="mobile-card">
            <h3>{sync_color[sync_status]} Status: {sync_status.value.title()}</h3>
            <p>Última sincronização: {datetime.now().strftime('%H:%M')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Progresso do dia
        progress = st.session_state.offline_data['progress_data']['daily_goals']
        
        st.markdown("#### 📊 Progresso de Hoje")
        
        # Horas de estudo
        hours_progress = progress['completed_hours'] / progress['study_hours']
        st.progress(hours_progress)
        st.write(f"⏱️ Estudo: {progress['completed_hours']:.1f}h / {progress['study_hours']}h")
        
        # Questões respondidas
        questions_progress = progress['completed_questions'] / progress['questions_answered']
        st.progress(questions_progress)
        st.write(f"❓ Questões: {progress['completed_questions']} / {progress['questions_answered']}")
        
        # Flashcards revisados
        flashcards_progress = progress['completed_flashcards'] / progress['flashcards_reviewed']
        st.progress(flashcards_progress)
        st.write(f"🃏 Flashcards: {progress['completed_flashcards']} / {progress['flashcards_reviewed']}")
        
        # Ações rápidas
        st.markdown("#### ⚡ Ações Rápidas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⏱️ Timer de Estudo", use_container_width=True):
                self.show_study_timer()
            
            if st.button("🃏 Flashcards", use_container_width=True):
                self.show_flashcards()
        
        with col2:
            if st.button("📝 Notas Rápidas", use_container_width=True):
                self.show_quick_notes()
            
            if st.button("📊 Progresso", use_container_width=True):
                self.show_progress_summary()
    
    def render_tablet_layout(self):
        """Layout otimizado para tablet"""
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_sync_status()
            self.render_daily_progress()
        
        with col2:
            self.render_quick_actions()
            self.render_recent_notifications()
    
    def render_desktop_layout(self):
        """Layout para desktop"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            self.render_sync_status()
            self.render_quick_actions()
        
        with col2:
            self.render_daily_progress()
            self.render_offline_content()
        
        with col3:
            self.render_recent_notifications()
            self.render_device_info()

    def render_sync_status(self):
        """Renderiza status de sincronização"""
        st.markdown("#### 🔄 Sincronização")

        sync_status = st.session_state.sync_status

        status_colors = {
            SyncStatus.SYNCED: "success",
            SyncStatus.SYNCING: "warning",
            SyncStatus.OFFLINE: "error",
            SyncStatus.ERROR: "error"
        }

        status_messages = {
            SyncStatus.SYNCED: "✅ Dados sincronizados",
            SyncStatus.SYNCING: "🔄 Sincronizando...",
            SyncStatus.OFFLINE: "📴 Modo offline",
            SyncStatus.ERROR: "❌ Erro na sincronização"
        }

        st.success(status_messages[sync_status])

        # Botões de controle
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔄 Sincronizar", use_container_width=True):
                self.force_sync()

        with col2:
            if st.button("📴 Modo Offline", use_container_width=True):
                self.toggle_offline_mode()

    def render_daily_progress(self):
        """Renderiza progresso diário"""
        st.markdown("#### 📊 Progresso de Hoje")

        progress = st.session_state.offline_data['progress_data']['daily_goals']

        # Criar gráfico de progresso
        categories = ['Horas de Estudo', 'Questões', 'Flashcards']
        completed = [
            progress['completed_hours'],
            progress['completed_questions'],
            progress['completed_flashcards']
        ]
        goals = [
            progress['study_hours'],
            progress['questions_answered'],
            progress['flashcards_reviewed']
        ]

        fig = go.Figure()

        fig.add_trace(go.Bar(
            name='Concluído',
            x=categories,
            y=completed,
            marker_color='#28a745'
        ))

        fig.add_trace(go.Bar(
            name='Meta',
            x=categories,
            y=goals,
            marker_color='#6c757d',
            opacity=0.3
        ))

        fig.update_layout(
            title="Progresso vs Metas",
            barmode='overlay',
            height=300,
            showlegend=True
        )

        st.plotly_chart(fig, use_container_width=True)

    def render_quick_actions(self):
        """Renderiza ações rápidas"""
        st.markdown("#### ⚡ Ações Rápidas")

        actions = [
            ("⏱️", "Timer", "study_timer"),
            ("🃏", "Flashcards", "flashcards"),
            ("📝", "Notas", "notes"),
            ("📊", "Progresso", "progress"),
            ("🎯", "Simulado", "mock_exam"),
            ("📚", "Materiais", "materials")
        ]

        cols = st.columns(2)

        for i, (icon, label, action) in enumerate(actions):
            with cols[i % 2]:
                if st.button(f"{icon} {label}", key=f"action_{action}", use_container_width=True):
                    self.execute_quick_action(action)

    def render_recent_notifications(self):
        """Renderiza notificações recentes"""
        st.markdown("#### 🔔 Notificações")

        notifications = st.session_state.push_notifications[:5]  # Últimas 5

        for notification in notifications:
            with st.container():
                # Estilo baseado na prioridade
                priority_colors = {
                    'high': '#dc3545',
                    'medium': '#ffc107',
                    'low': '#28a745'
                }

                color = priority_colors.get(notification['priority'], '#6c757d')
                read_style = "opacity: 0.6;" if notification['read'] else ""

                st.markdown(f"""
                <div style="border-left: 4px solid {color}; padding: 10px; margin: 5px 0; {read_style}">
                    <strong>{notification['icon']} {notification['title']}</strong><br>
                    <small>{notification['message']}</small><br>
                    <small style="color: #6c757d;">{notification['timestamp'].strftime('%H:%M')}</small>
                </div>
                """, unsafe_allow_html=True)

                if not notification['read']:
                    if st.button("✓ Marcar como lida", key=f"read_{notification['id']}"):
                        self.mark_notification_read(notification['id'])

    def render_offline_content(self):
        """Renderiza conteúdo offline"""
        st.markdown("#### 📴 Conteúdo Offline")

        offline_data = st.session_state.offline_data

        # Estatísticas de conteúdo offline
        st.metric("🃏 Flashcards", len(offline_data['flashcards']))
        st.metric("📝 Notas", len(offline_data['notes']))
        st.metric("📚 Materiais", len(offline_data['cached_materials']))

        # Espaço usado
        total_size = sum([2.3, 1.8, 0.5])  # MB simulado
        st.metric("💾 Espaço Usado", f"{total_size:.1f} MB")

        if st.button("🗑️ Limpar Cache", use_container_width=True):
            self.clear_offline_cache()

    def render_device_info(self):
        """Renderiza informações do dispositivo"""
        st.markdown("#### 📱 Dispositivo")

        device_info = st.session_state.device_info

        st.write(f"**Tipo:** {device_info['type'].value.title()}")
        st.write(f"**Tela:** {device_info['screen_width']}x{device_info['screen_height']}")
        st.write(f"**Conexão:** {device_info['connection'].upper()}")
        st.write(f"**Touch:** {'Sim' if device_info['is_touch'] else 'Não'}")

    def render_push_notifications(self):
        """Renderiza sistema de notificações push"""
        st.markdown("### 🔔 Notificações Push")

        # Configurações de notificação
        st.markdown("#### ⚙️ Configurações")

        settings = st.session_state.mobile_settings

        col1, col2 = st.columns(2)

        with col1:
            notifications_enabled = st.checkbox(
                "📱 Notificações Habilitadas",
                value=settings['notifications_enabled'],
                key="notifications_toggle"
            )

            if notifications_enabled != settings['notifications_enabled']:
                st.session_state.mobile_settings['notifications_enabled'] = notifications_enabled
                st.rerun()

        with col2:
            if notifications_enabled:
                st.success("✅ Notificações Ativas")
            else:
                st.warning("⚠️ Notificações Desabilitadas")

        # Tipos de notificação
        st.markdown("#### 📋 Tipos de Notificação")

        notification_types = [
            ("⏰", "Lembretes de Estudo", "study_reminders"),
            ("💬", "Mensagens de Grupo", "group_messages"),
            ("🚨", "Alertas de Prazo", "deadline_alerts"),
            ("🏆", "Conquistas", "achievements"),
            ("🎓", "Mensagens de Mentor", "mentor_messages"),
            ("📚", "Novos Materiais", "new_materials")
        ]

        for icon, label, key in notification_types:
            enabled = st.checkbox(f"{icon} {label}", value=True, key=f"notif_{key}")

        # Histórico de notificações
        st.markdown("#### 📜 Histórico")

        # Filtros
        col1, col2, col3 = st.columns(3)

        with col1:
            filter_type = st.selectbox(
                "Tipo",
                ["Todas", "Lembretes", "Mensagens", "Alertas", "Conquistas"]
            )

        with col2:
            filter_status = st.selectbox(
                "Status",
                ["Todas", "Não Lidas", "Lidas"]
            )

        with col3:
            filter_date = st.selectbox(
                "Período",
                ["Hoje", "Esta Semana", "Este Mês", "Todas"]
            )

        # Lista de notificações filtradas
        filtered_notifications = self.filter_notifications(filter_type, filter_status, filter_date)

        for notification in filtered_notifications:
            with st.expander(f"{notification['icon']} {notification['title']} - {notification['timestamp'].strftime('%d/%m %H:%M')}"):
                st.write(notification['message'])

                col1, col2, col3 = st.columns(3)

                with col1:
                    if not notification['read']:
                        if st.button("✓ Marcar como lida", key=f"mark_read_{notification['id']}"):
                            self.mark_notification_read(notification['id'])

                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_{notification['id']}"):
                        self.delete_notification(notification['id'])

                with col3:
                    if notification.get('action_url'):
                        if st.button("🔗 Abrir", key=f"open_{notification['id']}"):
                            st.info(f"Redirecionando para: {notification['action_url']}")

    def render_offline_mode(self):
        """Renderiza modo offline"""
        st.markdown("### 📴 Modo Offline")

        offline_enabled = st.session_state.mobile_settings['offline_mode']

        if offline_enabled:
            st.success("✅ Modo Offline Ativo")
            st.info("📱 Você pode continuar estudando mesmo sem conexão!")
        else:
            st.info("🌐 Modo Online - Dados sincronizados em tempo real")

        # Toggle modo offline
        if st.button("🔄 Alternar Modo", use_container_width=True):
            st.session_state.mobile_settings['offline_mode'] = not offline_enabled
            st.session_state.sync_status = SyncStatus.OFFLINE if not offline_enabled else SyncStatus.SYNCED
            st.rerun()

        if offline_enabled:
            self.render_offline_content_detailed()

    def render_offline_content_detailed(self):
        """Renderiza conteúdo offline detalhado"""
        st.markdown("#### 📚 Conteúdo Disponível Offline")

        tabs = st.tabs(["🃏 Flashcards", "📝 Notas", "📊 Progresso", "📚 Materiais"])

        with tabs[0]:
            self.render_offline_flashcards()

        with tabs[1]:
            self.render_offline_notes()

        with tabs[2]:
            self.render_offline_progress()

        with tabs[3]:
            self.render_offline_materials()

    def render_offline_flashcards(self):
        """Renderiza flashcards offline"""
        flashcards = st.session_state.offline_data['flashcards']

        st.write(f"📊 **{len(flashcards)} flashcards** disponíveis offline")

        for card in flashcards:
            with st.expander(f"🃏 {card['subject']} - {card['difficulty'].title()}"):
                st.write(f"**Pergunta:** {card['front']}")

                if st.button("👁️ Ver Resposta", key=f"show_answer_{card['id']}"):
                    st.write(f"**Resposta:** {card['back']}")

                    # Botões de avaliação
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if st.button("😰 Difícil", key=f"hard_{card['id']}"):
                            self.rate_flashcard(card['id'], 'hard')

                    with col2:
                        if st.button("😐 Médio", key=f"medium_{card['id']}"):
                            self.rate_flashcard(card['id'], 'medium')

                    with col3:
                        if st.button("😊 Fácil", key=f"easy_{card['id']}"):
                            self.rate_flashcard(card['id'], 'easy')

    def render_offline_notes(self):
        """Renderiza notas offline"""
        notes = st.session_state.offline_data['notes']

        st.write(f"📝 **{len(notes)} notas** disponíveis offline")

        # Botão para criar nova nota
        if st.button("➕ Nova Nota", use_container_width=True):
            self.show_new_note_modal()

        for note in notes:
            with st.expander(f"📝 {note['title']} - {note['subject']}"):
                st.write(note['content'])
                st.write(f"**Tags:** {', '.join(note['tags'])}")
                st.write(f"**Criado:** {note['created_at'].strftime('%d/%m/%Y %H:%M')}")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button("✏️ Editar", key=f"edit_note_{note['id']}"):
                        self.edit_note(note['id'])

                with col2:
                    if st.button("🗑️ Excluir", key=f"delete_note_{note['id']}"):
                        self.delete_note(note['id'])

    def render_offline_progress(self):
        """Renderiza progresso offline"""
        progress_data = st.session_state.offline_data['progress_data']

        # Progresso diário
        st.markdown("##### 📊 Progresso de Hoje")
        daily = progress_data['daily_goals']

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "⏱️ Horas de Estudo",
                f"{daily['completed_hours']:.1f}h",
                f"Meta: {daily['study_hours']}h"
            )

        with col2:
            st.metric(
                "❓ Questões",
                daily['completed_questions'],
                f"Meta: {daily['questions_answered']}"
            )

        with col3:
            st.metric(
                "🃏 Flashcards",
                daily['completed_flashcards'],
                f"Meta: {daily['flashcards_reviewed']}"
            )

        # Progresso semanal
        st.markdown("##### 📈 Progresso da Semana")
        weekly = progress_data['weekly_stats']

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "📚 Total de Horas",
                f"{weekly['total_hours']:.1f}h",
                f"Meta: {weekly['goal_hours']}h"
            )

        with col2:
            st.metric(
                "🎯 Performance Média",
                f"{weekly['avg_performance']:.1f}%",
                f"{weekly['subjects_studied']} matérias"
            )

    def render_offline_materials(self):
        """Renderiza materiais offline"""
        materials = st.session_state.offline_data['cached_materials']

        st.write(f"📚 **{len(materials)} materiais** em cache")

        for material in materials:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.write(f"📄 **{material['title']}**")
                    st.write(f"Tipo: {material['type']} | Tamanho: {material['size']}")

                with col2:
                    if st.button("📖 Abrir", key=f"open_material_{material['id']}"):
                        st.info("Material aberto offline")

                with col3:
                    if st.button("🗑️ Remover", key=f"remove_material_{material['id']}"):
                        self.remove_cached_material(material['id'])

                # Informações de cache
                expires_in = material['expires_at'] - datetime.now()
                if expires_in.days > 0:
                    st.write(f"⏰ Expira em {expires_in.days} dias")
                else:
                    st.warning("⚠️ Cache expirado")

                st.divider()

    # Métodos de ação e funcionalidades auxiliares

    def execute_quick_action(self, action: str):
        """Executa ação rápida"""
        actions = {
            'study_timer': self.show_study_timer,
            'flashcards': self.show_flashcards,
            'notes': self.show_quick_notes,
            'progress': self.show_progress_summary,
            'mock_exam': self.show_mock_exam,
            'materials': self.show_materials
        }

        if action in actions:
            actions[action]()
        else:
            st.error(f"Ação '{action}' não encontrada")

    def show_study_timer(self):
        """Mostra timer de estudo"""
        st.markdown("#### ⏱️ Timer de Estudo")

        # Configurações do timer
        col1, col2 = st.columns(2)

        with col1:
            study_minutes = st.number_input("Minutos de Estudo", min_value=1, max_value=120, value=25)

        with col2:
            break_minutes = st.number_input("Minutos de Pausa", min_value=1, max_value=30, value=5)

        # Técnica Pomodoro
        st.info("🍅 **Técnica Pomodoro:** 25min estudo + 5min pausa")

        # Controles do timer
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("▶️ Iniciar", use_container_width=True):
                st.success(f"⏱️ Timer iniciado: {study_minutes} minutos")
                self.start_study_session(study_minutes)

        with col2:
            if st.button("⏸️ Pausar", use_container_width=True):
                st.warning("⏸️ Timer pausado")

        with col3:
            if st.button("⏹️ Parar", use_container_width=True):
                st.info("⏹️ Timer parado")

        # Histórico de sessões
        st.markdown("##### 📊 Sessões de Hoje")
        sessions = [
            {"subject": "Direito Constitucional", "duration": 25, "completed": True},
            {"subject": "Matemática", "duration": 30, "completed": True},
            {"subject": "Português", "duration": 20, "completed": False}
        ]

        for i, session in enumerate(sessions):
            status = "✅" if session['completed'] else "⏸️"
            st.write(f"{status} {session['subject']} - {session['duration']}min")

    def show_flashcards(self):
        """Mostra sistema de flashcards"""
        st.markdown("#### 🃏 Flashcards")

        flashcards = st.session_state.offline_data['flashcards']

        if not flashcards:
            st.info("📚 Nenhum flashcard disponível")
            return

        # Seletor de matéria
        subjects = list(set([card['subject'] for card in flashcards]))
        selected_subject = st.selectbox("Matéria", ["Todas"] + subjects)

        # Filtrar flashcards
        if selected_subject != "Todas":
            filtered_cards = [card for card in flashcards if card['subject'] == selected_subject]
        else:
            filtered_cards = flashcards

        if not filtered_cards:
            st.info(f"📚 Nenhum flashcard encontrado para {selected_subject}")
            return

        # Modo de estudo
        study_mode = st.radio(
            "Modo de Estudo",
            ["🎯 Sessão Focada", "🔄 Revisão Aleatória", "📈 Por Dificuldade"]
        )

        # Iniciar sessão
        if st.button("🚀 Iniciar Sessão", use_container_width=True):
            st.session_state.flashcard_session = {
                'cards': filtered_cards,
                'current_index': 0,
                'mode': study_mode,
                'started': True
            }
            st.rerun()

        # Sessão ativa
        if st.session_state.get('flashcard_session', {}).get('started'):
            self.render_flashcard_session()

    def render_flashcard_session(self):
        """Renderiza sessão de flashcards"""
        session = st.session_state.flashcard_session
        cards = session['cards']
        current_index = session['current_index']

        if current_index >= len(cards):
            st.success("🎉 Sessão concluída!")
            st.balloons()
            del st.session_state.flashcard_session
            return

        current_card = cards[current_index]

        # Progresso
        progress = (current_index + 1) / len(cards)
        st.progress(progress)
        st.write(f"Cartão {current_index + 1} de {len(cards)}")

        # Cartão atual
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    padding: 30px; border-radius: 15px; text-align: center; color: white; margin: 20px 0;">
            <h3>🃏 {current_card['subject']}</h3>
            <h2>{current_card['front']}</h2>
        </div>
        """, unsafe_allow_html=True)

        # Mostrar resposta
        if st.button("👁️ Ver Resposta", use_container_width=True):
            st.markdown(f"""
            <div style="background: #28a745; padding: 20px; border-radius: 10px;
                        text-align: center; color: white; margin: 10px 0;">
                <h3>{current_card['back']}</h3>
            </div>
            """, unsafe_allow_html=True)

            # Avaliação
            st.markdown("##### Como foi sua performance?")

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("😰 Difícil", use_container_width=True):
                    self.next_flashcard('hard')

            with col2:
                if st.button("😐 Médio", use_container_width=True):
                    self.next_flashcard('medium')

            with col3:
                if st.button("😊 Fácil", use_container_width=True):
                    self.next_flashcard('easy')

    def next_flashcard(self, difficulty: str):
        """Avança para próximo flashcard"""
        session = st.session_state.flashcard_session
        session['current_index'] += 1

        # Registrar performance (simulado)
        st.success(f"✅ Avaliado como: {difficulty}")
        st.rerun()

    def show_quick_notes(self):
        """Mostra sistema de notas rápidas"""
        st.markdown("#### 📝 Notas Rápidas")

        # Nova nota
        with st.form("quick_note_form"):
            title = st.text_input("Título da Nota")
            subject = st.selectbox("Matéria", [
                "Direito Constitucional", "Direito Administrativo", "Português",
                "Matemática", "História", "Geografia", "Atualidades"
            ])
            content = st.text_area("Conteúdo", height=150)
            tags = st.text_input("Tags (separadas por vírgula)")

            if st.form_submit_button("💾 Salvar Nota", use_container_width=True):
                if title and content:
                    new_note = {
                        'id': str(uuid.uuid4()),
                        'title': title,
                        'subject': subject,
                        'content': content,
                        'tags': [tag.strip() for tag in tags.split(',') if tag.strip()],
                        'created_at': datetime.now()
                    }

                    st.session_state.offline_data['notes'].append(new_note)
                    st.success("✅ Nota salva com sucesso!")
                    st.rerun()
                else:
                    st.error("❌ Título e conteúdo são obrigatórios")

        # Notas existentes
        st.markdown("##### 📚 Suas Notas")
        notes = st.session_state.offline_data['notes']

        if not notes:
            st.info("📝 Nenhuma nota encontrada")
            return

        # Filtros
        col1, col2 = st.columns(2)

        with col1:
            filter_subject = st.selectbox("Filtrar por Matéria",
                ["Todas"] + list(set([note['subject'] for note in notes])))

        with col2:
            search_term = st.text_input("🔍 Buscar nas notas")

        # Filtrar notas
        filtered_notes = notes

        if filter_subject != "Todas":
            filtered_notes = [note for note in filtered_notes if note['subject'] == filter_subject]

        if search_term:
            filtered_notes = [note for note in filtered_notes
                            if search_term.lower() in note['title'].lower()
                            or search_term.lower() in note['content'].lower()]

        # Mostrar notas
        for note in filtered_notes:
            with st.expander(f"📝 {note['title']} - {note['subject']}"):
                st.write(note['content'])
                if note['tags']:
                    st.write(f"**Tags:** {', '.join(note['tags'])}")
                st.write(f"**Criado:** {note['created_at'].strftime('%d/%m/%Y %H:%M')}")

    def show_progress_summary(self):
        """Mostra resumo de progresso"""
        st.markdown("#### 📊 Resumo de Progresso")

        progress_data = st.session_state.offline_data['progress_data']

        # Métricas principais
        col1, col2, col3 = st.columns(3)

        daily = progress_data['daily_goals']
        weekly = progress_data['weekly_stats']

        with col1:
            st.metric(
                "⏱️ Horas Hoje",
                f"{daily['completed_hours']:.1f}h",
                f"{daily['completed_hours'] - daily['study_hours']:.1f}h"
            )

        with col2:
            st.metric(
                "❓ Questões Hoje",
                daily['completed_questions'],
                daily['completed_questions'] - daily['questions_answered']
            )

        with col3:
            st.metric(
                "🎯 Performance",
                f"{weekly['avg_performance']:.1f}%",
                "2.5%"
            )

        # Gráfico de progresso semanal
        st.markdown("##### 📈 Progresso da Semana")

        days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        hours = [3.2, 4.1, 2.8, 3.5, 4.2, 2.1, 0.6]

        fig = px.bar(
            x=days,
            y=hours,
            title="Horas de Estudo por Dia",
            labels={'x': 'Dia da Semana', 'y': 'Horas'}
        )

        fig.update_traces(marker_color='#667eea')
        st.plotly_chart(fig, use_container_width=True)

        # Distribuição por matéria
        st.markdown("##### 📚 Distribuição por Matéria")

        subjects = ['Direito Constitucional', 'Português', 'Matemática', 'História', 'Atualidades']
        hours_by_subject = [4.2, 3.8, 3.1, 2.9, 2.5]

        fig = px.pie(
            values=hours_by_subject,
            names=subjects,
            title="Horas por Matéria (Esta Semana)"
        )

        st.plotly_chart(fig, use_container_width=True)

    def show_mock_exam(self):
        """Mostra simulados rápidos"""
        st.markdown("#### 🎯 Simulado Rápido")

        st.info("🚀 **Simulado Express:** 10 questões em 15 minutos")

        # Configurações do simulado
        col1, col2 = st.columns(2)

        with col1:
            subject = st.selectbox("Matéria", [
                "Mista", "Direito Constitucional", "Português",
                "Matemática", "Atualidades"
            ])

        with col2:
            difficulty = st.selectbox("Dificuldade", ["Mista", "Fácil", "Médio", "Difícil"])

        # Estatísticas de simulados
        st.markdown("##### 📊 Suas Estatísticas")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🎯 Simulados Feitos", "23")

        with col2:
            st.metric("📈 Média Geral", "78.5%")

        with col3:
            st.metric("🏆 Melhor Resultado", "95%")

        # Iniciar simulado
        if st.button("🚀 Iniciar Simulado", use_container_width=True):
            st.success("🎯 Simulado iniciado! Boa sorte!")
            st.info("⏱️ Tempo: 15:00")

            # Simulação de questão
            st.markdown("##### Questão 1 de 10")
            st.write("**Direito Constitucional**")
            st.write("Sobre os direitos fundamentais na Constituição Federal de 1988, é correto afirmar que:")

            options = [
                "A) São absolutos e não podem sofrer limitações",
                "B) Aplicam-se apenas aos brasileiros natos",
                "C) Podem ser limitados em situações específicas previstas na Constituição",
                "D) Não se aplicam às pessoas jurídicas"
            ]

            selected = st.radio("Escolha sua resposta:", options)

            col1, col2 = st.columns(2)

            with col1:
                if st.button("⏭️ Próxima", use_container_width=True):
                    st.info("Resposta registrada!")

            with col2:
                if st.button("⏹️ Finalizar", use_container_width=True):
                    st.warning("Simulado finalizado!")

    def show_materials(self):
        """Mostra materiais disponíveis"""
        st.markdown("#### 📚 Materiais")

        materials = st.session_state.offline_data['cached_materials']

        if not materials:
            st.info("📚 Nenhum material em cache")
            return

        st.write(f"📊 **{len(materials)} materiais** disponíveis offline")

        for material in materials:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    st.write(f"📄 **{material['title']}**")
                    st.write(f"Tipo: {material['type']} | Tamanho: {material['size']}")

                with col2:
                    if st.button("📖 Abrir", key=f"open_{material['id']}", use_container_width=True):
                        st.success("📖 Material aberto!")

                with col3:
                    if st.button("📥 Download", key=f"download_{material['id']}", use_container_width=True):
                        st.success("📥 Download iniciado!")

                st.divider()

    # Métodos auxiliares

    def force_sync(self):
        """Força sincronização"""
        st.session_state.sync_status = SyncStatus.SYNCING
        st.success("🔄 Sincronização iniciada...")
        # Simular sincronização
        import time
        time.sleep(1)
        st.session_state.sync_status = SyncStatus.SYNCED
        st.rerun()

    def toggle_offline_mode(self):
        """Alterna modo offline"""
        current_mode = st.session_state.mobile_settings['offline_mode']
        st.session_state.mobile_settings['offline_mode'] = not current_mode

        if not current_mode:
            st.session_state.sync_status = SyncStatus.OFFLINE
            st.info("📴 Modo offline ativado")
        else:
            st.session_state.sync_status = SyncStatus.SYNCED
            st.info("🌐 Modo online ativado")

        st.rerun()

    def mark_notification_read(self, notification_id: str):
        """Marca notificação como lida"""
        for notification in st.session_state.push_notifications:
            if notification['id'] == notification_id:
                notification['read'] = True
                break
        st.success("✅ Notificação marcada como lida")
        st.rerun()

    def delete_notification(self, notification_id: str):
        """Exclui notificação"""
        st.session_state.push_notifications = [
            n for n in st.session_state.push_notifications
            if n['id'] != notification_id
        ]
        st.success("🗑️ Notificação excluída")
        st.rerun()

    def filter_notifications(self, filter_type: str, filter_status: str, filter_date: str) -> List[Dict[str, Any]]:
        """Filtra notificações"""
        notifications = st.session_state.push_notifications.copy()

        # Filtrar por tipo
        if filter_type != "Todas":
            type_mapping = {
                "Lembretes": NotificationType.STUDY_REMINDER,
                "Mensagens": NotificationType.GROUP_MESSAGE,
                "Alertas": NotificationType.DEADLINE_ALERT,
                "Conquistas": NotificationType.ACHIEVEMENT
            }
            if filter_type in type_mapping:
                notifications = [n for n in notifications if n['type'] == type_mapping[filter_type]]

        # Filtrar por status
        if filter_status == "Não Lidas":
            notifications = [n for n in notifications if not n['read']]
        elif filter_status == "Lidas":
            notifications = [n for n in notifications if n['read']]

        # Filtrar por data
        now = datetime.now()
        if filter_date == "Hoje":
            notifications = [n for n in notifications if n['timestamp'].date() == now.date()]
        elif filter_date == "Esta Semana":
            week_start = now - timedelta(days=now.weekday())
            notifications = [n for n in notifications if n['timestamp'] >= week_start]
        elif filter_date == "Este Mês":
            month_start = now.replace(day=1)
            notifications = [n for n in notifications if n['timestamp'] >= month_start]

        return notifications

    def clear_offline_cache(self):
        """Limpa cache offline"""
        st.session_state.offline_data['cached_materials'] = []
        st.success("🗑️ Cache limpo com sucesso!")
        st.rerun()

    def start_study_session(self, minutes: int):
        """Inicia sessão de estudo"""
        # Em uma implementação real, isso iniciaria um timer real
        st.session_state.study_session = {
            'start_time': datetime.now(),
            'duration': minutes,
            'active': True
        }

    def rate_flashcard(self, card_id: str, difficulty: str):
        """Avalia flashcard"""
        # Atualizar dados do flashcard baseado na avaliação
        for card in st.session_state.offline_data['flashcards']:
            if card['id'] == card_id:
                card['last_reviewed'] = datetime.now()
                card['difficulty'] = difficulty
                break

        st.success(f"✅ Flashcard avaliado como: {difficulty}")

    def remove_cached_material(self, material_id: str):
        """Remove material do cache"""
        st.session_state.offline_data['cached_materials'] = [
            m for m in st.session_state.offline_data['cached_materials']
            if m['id'] != material_id
        ]
        st.success("🗑️ Material removido do cache")
        st.rerun()

    def render_real_time_sync(self):
        """Renderiza sincronização em tempo real"""
        st.markdown("### 🔄 Sincronização em Tempo Real")

        # Status de conexão
        connection_status = st.session_state.device_info['connection']

        if connection_status == 'wifi':
            st.success("📶 Conectado via WiFi - Sincronização rápida")
        elif connection_status == '4g':
            st.info("📱 Conectado via 4G - Sincronização normal")
        else:
            st.warning("📴 Sem conexão - Modo offline ativo")

        # Configurações de sincronização
        st.markdown("#### ⚙️ Configurações")

        sync_frequency = st.selectbox(
            "Frequência de Sincronização",
            ["real_time", "every_5min", "every_15min", "manual"],
            format_func=lambda x: {
                "real_time": "⚡ Tempo Real",
                "every_5min": "🔄 A cada 5 minutos",
                "every_15min": "⏰ A cada 15 minutos",
                "manual": "👤 Manual"
            }[x]
        )

        data_saver = st.checkbox("💾 Modo Economia de Dados")

        if data_saver:
            st.info("📱 Sincronização apenas via WiFi")

        # Estatísticas de sincronização
        st.markdown("#### 📊 Estatísticas")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🔄 Sincronizações Hoje", "47")

        with col2:
            st.metric("📊 Dados Transferidos", "12.3 MB")

        with col3:
            st.metric("⏱️ Última Sync", "Agora")

        # Log de sincronização
        st.markdown("#### 📜 Log de Atividades")

        sync_logs = [
            {"time": "14:32", "action": "📊 Progresso sincronizado", "status": "✅"},
            {"time": "14:30", "action": "💬 Mensagens de grupo", "status": "✅"},
            {"time": "14:28", "action": "🃏 Flashcards atualizados", "status": "✅"},
            {"time": "14:25", "action": "📚 Novos materiais", "status": "✅"},
            {"time": "14:20", "action": "🔔 Notificações", "status": "⚠️"}
        ]

        for log in sync_logs:
            st.write(f"{log['time']} - {log['action']} {log['status']}")

    def render_settings(self):
        """Renderiza configurações do mobile companion"""
        st.markdown("### ⚙️ Configurações Mobile")

        settings = st.session_state.mobile_settings

        # Configurações de notificação
        st.markdown("#### 🔔 Notificações")

        notifications_enabled = st.checkbox(
            "Habilitar Notificações Push",
            value=settings['notifications_enabled']
        )

        if notifications_enabled:
            st.success("✅ Notificações habilitadas")

            # Tipos de notificação
            st.write("**Tipos de Notificação:**")

            notification_types = [
                ("⏰", "Lembretes de Estudo"),
                ("💬", "Mensagens de Grupo"),
                ("🚨", "Alertas de Prazo"),
                ("🏆", "Conquistas"),
                ("🎓", "Mensagens de Mentor"),
                ("📚", "Novos Materiais")
            ]

            for icon, label in notification_types:
                st.checkbox(f"{icon} {label}", value=True)

        # Configurações de sincronização
        st.markdown("#### 🔄 Sincronização")

        sync_frequency = st.selectbox(
            "Frequência",
            ["real_time", "every_5min", "every_15min", "manual"],
            index=0,
            format_func=lambda x: {
                "real_time": "⚡ Tempo Real",
                "every_5min": "🔄 A cada 5 minutos",
                "every_15min": "⏰ A cada 15 minutos",
                "manual": "👤 Manual"
            }[x]
        )

        data_saver = st.checkbox("💾 Modo Economia de Dados", value=settings['data_saver'])

        # Configurações de interface
        st.markdown("#### 🎨 Interface")

        dark_mode = st.checkbox("🌙 Modo Escuro", value=settings['dark_mode'])

        # Ações rápidas personalizáveis
        st.markdown("#### ⚡ Ações Rápidas")

        available_actions = [
            ("⏱️", "Timer de Estudo", "study_timer"),
            ("🃏", "Flashcards", "flashcards"),
            ("📝", "Notas", "notes"),
            ("📊", "Progresso", "progress"),
            ("🎯", "Simulado", "mock_exam"),
            ("📚", "Materiais", "materials"),
            ("💬", "Chat", "chat"),
            ("🏆", "Conquistas", "achievements")
        ]

        st.write("**Selecione até 4 ações rápidas:**")

        selected_actions = []
        for icon, label, key in available_actions:
            if st.checkbox(f"{icon} {label}", value=key in settings['quick_actions']):
                selected_actions.append(key)

        if len(selected_actions) > 4:
            st.warning("⚠️ Máximo de 4 ações rápidas permitidas")

        # Salvar configurações
        if st.button("💾 Salvar Configurações", use_container_width=True):
            st.session_state.mobile_settings.update({
                'notifications_enabled': notifications_enabled,
                'sync_frequency': sync_frequency,
                'data_saver': data_saver,
                'dark_mode': dark_mode,
                'quick_actions': selected_actions[:4]
            })

            st.success("✅ Configurações salvas com sucesso!")
            st.rerun()

    def render(self):
        """Método principal de renderização"""
        st.markdown("# 📱 Mobile Companion")
        st.markdown("*Versão responsiva com notificações push e sincronização em tempo real*")

        # Tabs principais
        tabs = st.tabs([
            "📱 Dashboard",
            "🔔 Notificações",
            "📴 Modo Offline",
            "🔄 Sincronização",
            "⚙️ Configurações"
        ])

        with tabs[0]:
            self.render_mobile_dashboard()

        with tabs[1]:
            self.render_push_notifications()

        with tabs[2]:
            self.render_offline_mode()

        with tabs[3]:
            self.render_real_time_sync()

        with tabs[4]:
            self.render_settings()
