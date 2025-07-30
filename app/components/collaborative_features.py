"""
Recursos Colaborativos - Fase 2
Sistema de grupos de estudo, mentoria e compartilhamento de materiais
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

class GroupType(Enum):
    """Tipos de grupos de estudo"""
    PUBLICO = "público"
    PRIVADO = "privado"
    MENTORIA = "mentoria"
    SIMULADO = "simulado"

class MemberRole(Enum):
    """Papéis dos membros no grupo"""
    ADMIN = "admin"
    MODERADOR = "moderador"
    MENTOR = "mentor"
    MEMBRO = "membro"
    MENTORADO = "mentorado"

class MessageType(Enum):
    """Tipos de mensagens no chat"""
    TEXTO = "texto"
    ARQUIVO = "arquivo"
    LINK = "link"
    QUESTAO = "questao"
    SISTEMA = "sistema"

class CollaborativeFeatures:
    """Sistema de recursos colaborativos"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializa estado da sessão"""
        if 'study_groups' not in st.session_state:
            st.session_state.study_groups = self.generate_sample_groups()
        
        if 'user_groups' not in st.session_state:
            st.session_state.user_groups = self.get_user_groups()
        
        if 'mentorship_matches' not in st.session_state:
            st.session_state.mentorship_matches = self.generate_mentorship_data()
        
        if 'shared_materials' not in st.session_state:
            st.session_state.shared_materials = self.generate_sample_materials()
        
        if 'group_messages' not in st.session_state:
            st.session_state.group_messages = self.generate_sample_messages()
        
        if 'collaboration_stats' not in st.session_state:
            st.session_state.collaboration_stats = self.generate_collaboration_stats()
    
    def render_collaborative_dashboard(self):
        """Renderiza dashboard principal dos recursos colaborativos"""
        st.title("👥 Recursos Colaborativos")
        st.markdown("**Conecte-se, aprenda e cresça junto com outros concurseiros!**")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_groups = len(st.session_state.study_groups)
            st.metric("🏘️ Grupos Ativos", total_groups, delta="+3 esta semana")
        
        with col2:
            user_groups = len(st.session_state.user_groups)
            st.metric("👤 Meus Grupos", user_groups, delta="+1 novo")
        
        with col3:
            mentorship_active = len([m for m in st.session_state.mentorship_matches if m['status'] == 'ativo'])
            st.metric("🎓 Mentorias Ativas", mentorship_active, delta="+2 matches")
        
        with col4:
            shared_materials = len(st.session_state.shared_materials)
            st.metric("📚 Materiais Compartilhados", shared_materials, delta="+15 novos")
        
        st.divider()
        
        # Tabs principais
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏘️ Grupos de Estudo",
            "🎓 Sistema de Mentoria", 
            "📚 Materiais Compartilhados",
            "💬 Chat e Comunicação",
            "📊 Analytics Colaborativos"
        ])
        
        with tab1:
            self.render_study_groups()
        
        with tab2:
            self.render_mentorship_system()
        
        with tab3:
            self.render_shared_materials()
        
        with tab4:
            self.render_communication_hub()
        
        with tab5:
            self.render_collaboration_analytics()
    
    def generate_sample_groups(self) -> List[Dict[str, Any]]:
        """Gera grupos de estudo de exemplo"""
        concursos = [
            "Concurso Público Federal", "INSS 2024", "Receita Federal", 
            "Polícia Federal", "Tribunal de Justiça", "Prefeitura Municipal",
            "IBGE 2024", "Banco Central", "Ministério Público", "TCU"
        ]
        
        materias = [
            "Direito Constitucional", "Direito Administrativo", "Português",
            "Matemática", "Raciocínio Lógico", "Informática", "Atualidades",
            "Direito Penal", "Direito Civil", "Contabilidade"
        ]
        
        groups = []
        for i in range(15):
            group = {
                'id': str(uuid.uuid4()),
                'name': f"Grupo {random.choice(concursos)}",
                'description': f"Estudo focado em {random.choice(materias)} para {random.choice(concursos)}",
                'type': random.choice(list(GroupType)),
                'members_count': random.randint(5, 50),
                'max_members': random.randint(20, 100),
                'created_date': datetime.now() - timedelta(days=random.randint(1, 90)),
                'last_activity': datetime.now() - timedelta(hours=random.randint(1, 48)),
                'admin': f"Admin{i+1}",
                'tags': random.sample(materias, random.randint(2, 4)),
                'activity_level': random.choice(['Alta', 'Média', 'Baixa']),
                'success_rate': random.uniform(0.6, 0.95),
                'avg_study_hours': random.randint(15, 40),
                'is_member': random.choice([True, False])
            }
            groups.append(group)
        
        return groups
    
    def get_user_groups(self) -> List[Dict[str, Any]]:
        """Obtém grupos do usuário atual"""
        all_groups = st.session_state.study_groups
        user_groups = [group for group in all_groups if group['is_member']]
        
        # Adicionar informações específicas do usuário
        for group in user_groups:
            group['user_role'] = random.choice(list(MemberRole))
            group['join_date'] = datetime.now() - timedelta(days=random.randint(1, 60))
            group['contributions'] = random.randint(5, 50)
            group['last_seen'] = datetime.now() - timedelta(hours=random.randint(1, 24))
        
        return user_groups
    
    def generate_mentorship_data(self) -> List[Dict[str, Any]]:
        """Gera dados de mentoria"""
        mentorships = []
        
        for i in range(8):
            mentorship = {
                'id': str(uuid.uuid4()),
                'mentor_name': f"Mentor {i+1}",
                'mentor_expertise': random.choice([
                    "Direito Constitucional", "Matemática", "Português", 
                    "Direito Administrativo", "Contabilidade"
                ]),
                'mentor_rating': random.uniform(4.2, 5.0),
                'mentor_experience': f"{random.randint(3, 15)} anos",
                'mentee_name': f"Estudante {i+1}" if i < 4 else None,
                'status': random.choice(['ativo', 'disponível', 'pausado']),
                'sessions_completed': random.randint(0, 20),
                'next_session': datetime.now() + timedelta(days=random.randint(1, 7)),
                'match_score': random.uniform(0.7, 0.98),
                'specialties': random.sample([
                    "Preparação para provas", "Técnicas de estudo", "Gestão do tempo",
                    "Motivação", "Estratégia de concursos", "Revisão de conteúdo"
                ], random.randint(2, 4)),
                'availability': random.choice([
                    "Manhã", "Tarde", "Noite", "Fins de semana", "Flexível"
                ])
            }
            mentorships.append(mentorship)
        
        return mentorships
    
    def generate_sample_materials(self) -> List[Dict[str, Any]]:
        """Gera materiais compartilhados de exemplo"""
        materials = []
        
        tipos = ["PDF", "Vídeo", "Áudio", "Planilha", "Mapa Mental", "Resumo"]
        materias = [
            "Direito Constitucional", "Português", "Matemática", 
            "Raciocínio Lógico", "Informática", "Atualidades"
        ]
        
        for i in range(25):
            material = {
                'id': str(uuid.uuid4()),
                'title': f"Material de {random.choice(materias)} - Tópico {i+1}",
                'type': random.choice(tipos),
                'subject': random.choice(materias),
                'author': f"Usuário{random.randint(1, 20)}",
                'upload_date': datetime.now() - timedelta(days=random.randint(1, 30)),
                'downloads': random.randint(10, 500),
                'rating': random.uniform(3.5, 5.0),
                'size': f"{random.randint(1, 50)} MB",
                'description': f"Material completo sobre tópicos importantes de {random.choice(materias)}",
                'tags': random.sample(materias, random.randint(1, 3)),
                'verified': random.choice([True, False]),
                'premium': random.choice([True, False]),
                'comments_count': random.randint(0, 25),
                'group_id': random.choice([g['id'] for g in st.session_state.study_groups[:5]])
            }
            materials.append(material)
        
        return materials
    
    def generate_sample_messages(self) -> Dict[str, List[Dict[str, Any]]]:
        """Gera mensagens de exemplo para grupos"""
        messages_by_group = {}
        
        for group in st.session_state.study_groups[:5]:  # Apenas primeiros 5 grupos
            messages = []
            
            for i in range(random.randint(10, 30)):
                message = {
                    'id': str(uuid.uuid4()),
                    'author': f"Membro{random.randint(1, 10)}",
                    'content': self.generate_sample_message_content(),
                    'timestamp': datetime.now() - timedelta(
                        hours=random.randint(1, 72),
                        minutes=random.randint(0, 59)
                    ),
                    'type': random.choice(list(MessageType)),
                    'reactions': random.randint(0, 15),
                    'replies': random.randint(0, 5),
                    'edited': random.choice([True, False])
                }
                messages.append(message)
            
            # Ordenar por timestamp
            messages.sort(key=lambda x: x['timestamp'], reverse=True)
            messages_by_group[group['id']] = messages
        
        return messages_by_group
    
    def generate_sample_message_content(self) -> str:
        """Gera conteúdo de mensagem de exemplo"""
        message_templates = [
            "Alguém tem material sobre {}?",
            "Acabei de resolver uma questão difícil de {}!",
            "Vamos fazer um simulado de {} amanhã?",
            "Encontrei um ótimo resumo sobre {}",
            "Dúvida sobre {}: alguém pode ajudar?",
            "Compartilhando dica importante sobre {}",
            "Sessão de estudos de {} às 19h, quem topa?",
            "Resultado do último simulado: {} acertos!",
            "Motivação do dia: persistência é a chave!",
            "Link útil para estudar {}"
        ]
        
        materias = [
            "Direito Constitucional", "Português", "Matemática", 
            "Raciocínio Lógico", "Informática", "Atualidades"
        ]
        
        template = random.choice(message_templates)
        if "{}" in template:
            return template.format(random.choice(materias))
        return template
    
    def generate_collaboration_stats(self) -> Dict[str, Any]:
        """Gera estatísticas de colaboração"""
        return {
            'weekly_activity': {
                'messages_sent': random.randint(150, 300),
                'materials_shared': random.randint(10, 25),
                'new_connections': random.randint(5, 15),
                'study_sessions': random.randint(8, 20)
            },
            'engagement_by_day': {
                'Segunda': random.randint(20, 40),
                'Terça': random.randint(25, 45),
                'Quarta': random.randint(30, 50),
                'Quinta': random.randint(25, 45),
                'Sexta': random.randint(20, 40),
                'Sábado': random.randint(35, 55),
                'Domingo': random.randint(30, 50)
            },
            'popular_subjects': {
                'Direito Constitucional': random.randint(80, 120),
                'Português': random.randint(70, 110),
                'Matemática': random.randint(60, 100),
                'Raciocínio Lógico': random.randint(50, 90),
                'Informática': random.randint(40, 80),
                'Atualidades': random.randint(45, 85)
            },
            'mentorship_success': {
                'matches_made': random.randint(15, 30),
                'sessions_completed': random.randint(80, 150),
                'satisfaction_rate': random.uniform(0.85, 0.98),
                'avg_improvement': random.uniform(0.15, 0.35)
            }
        }
    
    def render_study_groups(self):
        """Renderiza seção de grupos de estudo"""
        st.subheader("🏘️ Grupos de Estudo")
        
        # Filtros e busca
        col1, col2, col3 = st.columns(3)
        
        with col1:
            search_term = st.text_input("🔍 Buscar grupos:", placeholder="Digite o nome ou matéria...")
        
        with col2:
            filter_type = st.selectbox(
                "Tipo de grupo:",
                ["Todos"] + [t.value.title() for t in GroupType]
            )
        
        with col3:
            sort_by = st.selectbox(
                "Ordenar por:",
                ["Atividade Recente", "Mais Membros", "Taxa de Sucesso", "Criação"]
            )
        
        # Botão para criar novo grupo
        if st.button("➕ Criar Novo Grupo", type="primary"):
            self.show_create_group_modal()
        
        st.divider()
        
        # Filtrar grupos
        filtered_groups = self.filter_groups(st.session_state.study_groups, search_term, filter_type, sort_by)
        
        # Tabs para diferentes visualizações
        tab1, tab2 = st.tabs(["📋 Lista de Grupos", "👤 Meus Grupos"])
        
        with tab1:
            self.render_groups_list(filtered_groups)
        
        with tab2:
            self.render_user_groups()
    
    def filter_groups(self, groups: List[Dict[str, Any]], search_term: str, filter_type: str, sort_by: str) -> List[Dict[str, Any]]:
        """Filtra e ordena grupos"""
        # groups já é passado como parâmetro
        
        # Filtro por busca
        if search_term:
            groups = [
                g for g in groups 
                if search_term.lower() in g['name'].lower() 
                or search_term.lower() in g['description'].lower()
                or any(search_term.lower() in tag.lower() for tag in g['tags'])
            ]
        
        # Filtro por tipo
        if filter_type != "Todos":
            groups = [g for g in groups if g['type'].value.title() == filter_type]
        
        # Ordenação
        if sort_by == "Atividade Recente":
            groups.sort(key=lambda x: x['last_activity'], reverse=True)
        elif sort_by == "Mais Membros":
            groups.sort(key=lambda x: x['members_count'], reverse=True)
        elif sort_by == "Taxa de Sucesso":
            groups.sort(key=lambda x: x['success_rate'], reverse=True)
        elif sort_by == "Criação":
            groups.sort(key=lambda x: x['created_date'], reverse=True)
        
        return groups

    def render_groups_list(self, groups: List[Dict[str, Any]]):
        """Renderiza lista de grupos"""
        if not groups:
            st.info("🔍 Nenhum grupo encontrado com os filtros aplicados.")
            return

        # Mostrar grupos em cards
        for i in range(0, len(groups), 2):
            cols = st.columns(2)

            for j, col in enumerate(cols):
                if i + j < len(groups):
                    group = groups[i + j]

                    with col:
                        with st.container():
                            # Header do card
                            st.markdown(f"### 🏘️ {group['name']}")

                            # Badges de status
                            col_badge1, col_badge2, col_badge3 = st.columns(3)

                            with col_badge1:
                                type_color = {
                                    GroupType.PUBLICO: "🟢",
                                    GroupType.PRIVADO: "🔒",
                                    GroupType.MENTORIA: "🎓",
                                    GroupType.SIMULADO: "📝"
                                }
                                st.markdown(f"{type_color[group['type']]} {group['type'].value.title()}")

                            with col_badge2:
                                activity_color = {
                                    'Alta': '🔥', 'Média': '⚡', 'Baixa': '💤'
                                }
                                st.markdown(f"{activity_color[group['activity_level']]} {group['activity_level']}")

                            with col_badge3:
                                if group['is_member']:
                                    st.markdown("✅ Membro")
                                else:
                                    st.markdown("👤 Visitante")

                            # Descrição
                            st.write(group['description'])

                            # Métricas
                            col_m1, col_m2, col_m3 = st.columns(3)

                            with col_m1:
                                st.metric("👥 Membros", f"{group['members_count']}/{group['max_members']}")

                            with col_m2:
                                st.metric("📈 Taxa Sucesso", f"{group['success_rate']:.1%}")

                            with col_m3:
                                hours_ago = (datetime.now() - group['last_activity']).total_seconds() / 3600
                                if hours_ago < 1:
                                    activity_text = "Agora"
                                elif hours_ago < 24:
                                    activity_text = f"{int(hours_ago)}h atrás"
                                else:
                                    activity_text = f"{int(hours_ago/24)}d atrás"
                                st.metric("🕒 Atividade", activity_text)

                            # Tags
                            if group['tags']:
                                st.markdown("**Tags:** " + " • ".join([f"`{tag}`" for tag in group['tags']]))

                            # Botões de ação
                            col_btn1, col_btn2 = st.columns(2)

                            with col_btn1:
                                if group['is_member']:
                                    if st.button(f"💬 Entrar", key=f"enter_{group['id']}", use_container_width=True):
                                        st.session_state.selected_group = group['id']
                                        st.success(f"Entrando no grupo {group['name']}")
                                        st.rerun()
                                else:
                                    if st.button(f"➕ Participar", key=f"join_{group['id']}", use_container_width=True):
                                        self.join_group(group['id'])
                                        st.success(f"Solicitação enviada para {group['name']}")
                                        st.rerun()

                            with col_btn2:
                                if st.button(f"👁️ Visualizar", key=f"view_{group['id']}", use_container_width=True):
                                    self.show_group_details(group)

                            st.divider()

    def render_user_groups(self):
        """Renderiza grupos do usuário"""
        user_groups = st.session_state.user_groups

        if not user_groups:
            st.info("👥 Você ainda não participa de nenhum grupo.")
            st.markdown("**Dica:** Explore a aba 'Lista de Grupos' para encontrar grupos interessantes!")
            return

        st.write(f"**Você participa de {len(user_groups)} grupos:**")

        for group in user_groups:
            with st.expander(f"🏘️ {group['name']} - {group['user_role'].value.title()}", expanded=False):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(f"**Descrição:** {group['description']}")
                    st.write(f"**Participando desde:** {group['join_date'].strftime('%d/%m/%Y')}")
                    st.write(f"**Suas contribuições:** {group['contributions']} mensagens")
                    st.write(f"**Última visita:** {group['last_seen'].strftime('%d/%m/%Y às %H:%M')}")

                with col2:
                    st.metric("👥 Membros", group['members_count'])
                    st.metric("📊 Atividade", group['activity_level'])

                    # Botões de ação
                    if st.button(f"💬 Abrir Chat", key=f"chat_{group['id']}", use_container_width=True):
                        st.session_state.selected_group = group['id']
                        st.session_state.current_tab = "chat"
                        st.rerun()

                    if group['user_role'] in [MemberRole.ADMIN, MemberRole.MODERADOR]:
                        if st.button(f"⚙️ Gerenciar", key=f"manage_{group['id']}", use_container_width=True):
                            self.show_group_management(group)

    def show_create_group_modal(self):
        """Mostra modal para criar novo grupo"""
        with st.form("create_group_form"):
            st.subheader("➕ Criar Novo Grupo")

            col1, col2 = st.columns(2)

            with col1:
                group_name = st.text_input("Nome do grupo:", placeholder="Ex: Estudo INSS 2024")
                group_type = st.selectbox("Tipo do grupo:", [t.value.title() for t in GroupType])
                max_members = st.slider("Máximo de membros:", 5, 100, 20)

            with col2:
                group_description = st.text_area(
                    "Descrição:",
                    placeholder="Descreva o objetivo e foco do grupo...",
                    height=100
                )
                tags = st.multiselect(
                    "Tags (matérias):",
                    ["Direito Constitucional", "Português", "Matemática", "Raciocínio Lógico",
                     "Informática", "Atualidades", "Direito Administrativo", "Direito Penal"]
                )

            # Configurações avançadas
            with st.expander("⚙️ Configurações Avançadas"):
                require_approval = st.checkbox("Exigir aprovação para novos membros", value=True)
                allow_file_sharing = st.checkbox("Permitir compartilhamento de arquivos", value=True)
                enable_voice_chat = st.checkbox("Habilitar chat de voz", value=False)
                study_schedule = st.text_input("Cronograma de estudos:", placeholder="Ex: Seg-Sex 19h-21h")

            submitted = st.form_submit_button("🚀 Criar Grupo", type="primary")

            if submitted:
                if group_name and group_description:
                    new_group = {
                        'id': str(uuid.uuid4()),
                        'name': group_name,
                        'description': group_description,
                        'type': GroupType(group_type.lower()),
                        'members_count': 1,  # Criador
                        'max_members': max_members,
                        'created_date': datetime.now(),
                        'last_activity': datetime.now(),
                        'admin': "Você",
                        'tags': tags,
                        'activity_level': 'Baixa',
                        'success_rate': 0.0,
                        'avg_study_hours': 0,
                        'is_member': True,
                        'settings': {
                            'require_approval': require_approval,
                            'allow_file_sharing': allow_file_sharing,
                            'enable_voice_chat': enable_voice_chat,
                            'study_schedule': study_schedule
                        }
                    }

                    st.session_state.study_groups.append(new_group)
                    st.session_state.user_groups.append({
                        **new_group,
                        'user_role': MemberRole.ADMIN,
                        'join_date': datetime.now(),
                        'contributions': 0,
                        'last_seen': datetime.now()
                    })

                    st.success(f"✅ Grupo '{group_name}' criado com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Por favor, preencha nome e descrição do grupo.")

    def join_group(self, group_id: str):
        """Solicita participação em grupo"""
        # Encontrar o grupo
        group = next((g for g in st.session_state.study_groups if g['id'] == group_id), None)

        if group:
            # Simular processo de entrada
            group['is_member'] = True
            group['members_count'] += 1

            # Adicionar aos grupos do usuário
            user_group = {
                **group,
                'user_role': MemberRole.MEMBRO,
                'join_date': datetime.now(),
                'contributions': 0,
                'last_seen': datetime.now()
            }

            st.session_state.user_groups.append(user_group)

    def show_group_details(self, group: Dict[str, Any]):
        """Mostra detalhes do grupo em modal"""
        st.markdown(f"## 🏘️ {group['name']}")

        # Informações básicas
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("👥 Membros", f"{group['members_count']}/{group['max_members']}")
            st.metric("📈 Taxa de Sucesso", f"{group['success_rate']:.1%}")

        with col2:
            st.metric("📚 Horas de Estudo/Semana", f"{group['avg_study_hours']}h")
            st.metric("🕒 Criado há", f"{(datetime.now() - group['created_date']).days} dias")

        with col3:
            st.metric("👑 Admin", group['admin'])
            st.metric("🎯 Atividade", group['activity_level'])

        # Descrição e tags
        st.markdown("### 📝 Descrição")
        st.write(group['description'])

        if group['tags']:
            st.markdown("### 🏷️ Tags")
            st.markdown(" • ".join([f"`{tag}`" for tag in group['tags']]))

        # Atividade recente (simulada)
        st.markdown("### 📊 Atividade Recente")

        recent_activities = [
            f"📝 {random.randint(5, 15)} mensagens nas últimas 24h",
            f"📚 {random.randint(2, 8)} materiais compartilhados esta semana",
            f"🎯 {random.randint(1, 5)} simulados realizados",
            f"👥 {random.randint(1, 3)} novos membros este mês"
        ]

        for activity in recent_activities:
            st.write(f"• {activity}")

    def render_mentorship_system(self):
        """Renderiza sistema de mentoria"""
        st.subheader("🎓 Sistema de Mentoria")

        # Tabs do sistema de mentoria
        tab1, tab2, tab3 = st.tabs(["🔍 Encontrar Mentor", "👨‍🏫 Minhas Mentorias", "📊 Estatísticas"])

        with tab1:
            self.render_mentor_search()

        with tab2:
            self.render_user_mentorships()

        with tab3:
            self.render_mentorship_stats()

    def render_mentor_search(self):
        """Renderiza busca por mentores"""
        st.write("### 🔍 Encontrar o Mentor Ideal")

        # Filtros de busca
        col1, col2, col3 = st.columns(3)

        with col1:
            expertise_filter = st.selectbox(
                "Área de especialidade:",
                ["Todas"] + ["Direito Constitucional", "Matemática", "Português",
                           "Direito Administrativo", "Contabilidade", "Raciocínio Lógico"]
            )

        with col2:
            availability_filter = st.selectbox(
                "Disponibilidade:",
                ["Qualquer"] + ["Manhã", "Tarde", "Noite", "Fins de semana", "Flexível"]
            )

        with col3:
            min_rating = st.slider("Avaliação mínima:", 1.0, 5.0, 4.0, 0.1)

        # Filtrar mentores
        mentors = [m for m in st.session_state.mentorship_matches if m['status'] == 'disponível']

        if expertise_filter != "Todas":
            mentors = [m for m in mentors if m['mentor_expertise'] == expertise_filter]

        if availability_filter != "Qualquer":
            mentors = [m for m in mentors if m['availability'] == availability_filter]

        mentors = [m for m in mentors if m['mentor_rating'] >= min_rating]

        # Ordenar por rating
        mentors.sort(key=lambda x: x['mentor_rating'], reverse=True)

        st.write(f"**{len(mentors)} mentores encontrados:**")

        # Mostrar mentores
        for mentor in mentors:
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.markdown(f"### 👨‍🏫 {mentor['mentor_name']}")
                    st.write(f"**Especialidade:** {mentor['mentor_expertise']}")
                    st.write(f"**Experiência:** {mentor['mentor_experience']}")

                    # Especialidades
                    if mentor['specialties']:
                        st.markdown("**Especialidades:** " + " • ".join([f"`{spec}`" for spec in mentor['specialties']]))

                with col2:
                    st.metric("⭐ Avaliação", f"{mentor['mentor_rating']:.1f}/5.0")
                    st.metric("📅 Disponibilidade", mentor['availability'])
                    st.metric("🎯 Match", f"{mentor['match_score']:.0%}")

                with col3:
                    st.metric("📚 Sessões", mentor['sessions_completed'])

                    if st.button(f"🤝 Solicitar Mentoria", key=f"request_{mentor['id']}", use_container_width=True):
                        self.request_mentorship(mentor['id'])
                        st.success(f"Solicitação enviada para {mentor['mentor_name']}!")
                        st.rerun()

                    if st.button(f"👁️ Ver Perfil", key=f"profile_{mentor['id']}", use_container_width=True):
                        self.show_mentor_profile(mentor)

                st.divider()

    def render_user_mentorships(self):
        """Renderiza mentorias do usuário"""
        active_mentorships = [m for m in st.session_state.mentorship_matches if m['status'] == 'ativo']

        if not active_mentorships:
            st.info("🎓 Você não possui mentorias ativas no momento.")
            st.markdown("**Dica:** Use a aba 'Encontrar Mentor' para solicitar uma mentoria!")
            return

        st.write(f"**Você possui {len(active_mentorships)} mentorias ativas:**")

        for mentorship in active_mentorships:
            with st.expander(f"🎓 Mentoria com {mentorship['mentor_name']}", expanded=True):
                col1, col2 = st.columns([2, 1])

                with col1:
                    st.write(f"**Especialidade:** {mentorship['mentor_expertise']}")
                    st.write(f"**Próxima sessão:** {mentorship['next_session'].strftime('%d/%m/%Y às %H:%M')}")
                    st.write(f"**Sessões realizadas:** {mentorship['sessions_completed']}")

                    # Progresso da mentoria
                    progress = min(100, mentorship['sessions_completed'] * 5)  # 5% por sessão
                    st.progress(progress / 100)
                    st.write(f"Progresso: {progress}%")

                with col2:
                    st.metric("⭐ Avaliação", f"{mentorship['mentor_rating']:.1f}")
                    st.metric("🎯 Compatibilidade", f"{mentorship['match_score']:.0%}")

                    # Botões de ação
                    if st.button(f"💬 Chat", key=f"chat_mentor_{mentorship['id']}", use_container_width=True):
                        st.info("Abrindo chat com mentor...")

                    if st.button(f"📅 Agendar", key=f"schedule_{mentorship['id']}", use_container_width=True):
                        st.info("Abrindo agenda...")

                    if st.button(f"⭐ Avaliar", key=f"rate_{mentorship['id']}", use_container_width=True):
                        self.show_rating_modal(mentorship)

    def render_mentorship_stats(self):
        """Renderiza estatísticas de mentoria"""
        stats = st.session_state.collaboration_stats['mentorship_success']

        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("🤝 Matches Realizados", stats['matches_made'])

        with col2:
            st.metric("📚 Sessões Completadas", stats['sessions_completed'])

        with col3:
            st.metric("😊 Taxa de Satisfação", f"{stats['satisfaction_rate']:.1%}")

        with col4:
            st.metric("📈 Melhoria Média", f"+{stats['avg_improvement']:.1%}")

        # Gráfico de evolução
        st.markdown("### 📊 Evolução das Mentorias")

        # Simular dados de evolução
        dates = pd.date_range(end=datetime.now(), periods=12, freq='M')
        mentorship_data = []

        for date in dates:
            mentorship_data.append({
                'Mês': date.strftime('%b/%Y'),
                'Matches': random.randint(8, 25),
                'Sessões': random.randint(40, 120),
                'Satisfação': random.uniform(0.8, 0.98)
            })

        df_mentorship = pd.DataFrame(mentorship_data)

        # Gráfico de barras
        fig_mentorship = px.bar(
            df_mentorship,
            x='Mês',
            y=['Matches', 'Sessões'],
            title="Evolução Mensal das Mentorias",
            barmode='group'
        )

        st.plotly_chart(fig_mentorship, use_container_width=True)

        # Distribuição por especialidade
        st.markdown("### 🎯 Mentorias por Especialidade")

        specialties_data = {
            'Direito Constitucional': random.randint(15, 30),
            'Matemática': random.randint(12, 25),
            'Português': random.randint(10, 20),
            'Direito Administrativo': random.randint(8, 18),
            'Contabilidade': random.randint(6, 15),
            'Raciocínio Lógico': random.randint(5, 12)
        }

        fig_specialties = px.pie(
            values=list(specialties_data.values()),
            names=list(specialties_data.keys()),
            title="Distribuição de Mentorias por Área"
        )

        st.plotly_chart(fig_specialties, use_container_width=True)

    def request_mentorship(self, mentor_id: str):
        """Solicita mentoria com mentor"""
        # Encontrar mentor
        mentor = next((m for m in st.session_state.mentorship_matches if m['id'] == mentor_id), None)

        if mentor:
            # Simular processo de solicitação
            mentor['status'] = 'ativo'
            mentor['mentee_name'] = "Você"
            mentor['sessions_completed'] = 0
            mentor['next_session'] = datetime.now() + timedelta(days=random.randint(1, 7))

    def show_mentor_profile(self, mentor: Dict[str, Any]):
        """Mostra perfil detalhado do mentor"""
        st.markdown(f"## 👨‍🏫 Perfil: {mentor['mentor_name']}")

        col1, col2 = st.columns([2, 1])

        with col1:
            st.write(f"**Especialidade Principal:** {mentor['mentor_expertise']}")
            st.write(f"**Experiência:** {mentor['mentor_experience']}")
            st.write(f"**Disponibilidade:** {mentor['availability']}")

            if mentor['specialties']:
                st.markdown("**Áreas de Atuação:**")
                for specialty in mentor['specialties']:
                    st.write(f"• {specialty}")

        with col2:
            st.metric("⭐ Avaliação", f"{mentor['mentor_rating']:.1f}/5.0")
            st.metric("📚 Sessões Realizadas", mentor['sessions_completed'])
            st.metric("🎯 Compatibilidade", f"{mentor['match_score']:.0%}")

        # Depoimentos simulados
        st.markdown("### 💬 Depoimentos")
        testimonials = [
            "Excelente mentor! Me ajudou muito com Direito Constitucional.",
            "Muito paciente e didático. Recomendo!",
            "Sessões muito produtivas e bem estruturadas."
        ]

        for testimonial in testimonials[:2]:
            st.info(f"💭 \"{testimonial}\"")

    def show_rating_modal(self, mentorship: Dict[str, Any]):
        """Mostra modal de avaliação"""
        with st.form(f"rating_form_{mentorship['id']}"):
            st.subheader(f"⭐ Avaliar Mentoria com {mentorship['mentor_name']}")

            rating = st.slider("Nota geral:", 1, 5, 5)

            aspects = {
                "Didática": st.slider("Didática:", 1, 5, 5),
                "Pontualidade": st.slider("Pontualidade:", 1, 5, 5),
                "Conhecimento": st.slider("Conhecimento:", 1, 5, 5),
                "Comunicação": st.slider("Comunicação:", 1, 5, 5)
            }

            feedback = st.text_area("Comentários:", placeholder="Deixe seu feedback sobre a mentoria...")

            submitted = st.form_submit_button("📝 Enviar Avaliação")

            if submitted:
                st.success("✅ Avaliação enviada com sucesso!")
                st.balloons()

    def render_shared_materials(self):
        """Renderiza materiais compartilhados"""
        st.subheader("📚 Materiais Compartilhados")

        # Filtros
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            search_materials = st.text_input("🔍 Buscar materiais:", placeholder="Digite o título ou matéria...")

        with col2:
            type_filter = st.selectbox("Tipo:", ["Todos", "PDF", "Vídeo", "Áudio", "Planilha", "Mapa Mental", "Resumo"])

        with col3:
            subject_filter = st.selectbox(
                "Matéria:",
                ["Todas", "Direito Constitucional", "Português", "Matemática", "Raciocínio Lógico", "Informática", "Atualidades"]
            )

        with col4:
            sort_materials = st.selectbox("Ordenar por:", ["Mais Recentes", "Mais Baixados", "Melhor Avaliados", "Tamanho"])

        # Botão para upload
        if st.button("📤 Compartilhar Material", type="primary"):
            self.show_upload_modal()

        st.divider()

        # Filtrar materiais
        filtered_materials = self.filter_materials(st.session_state.shared_materials, search_materials, type_filter, subject_filter, sort_materials)

        # Mostrar materiais
        if not filtered_materials:
            st.info("📚 Nenhum material encontrado com os filtros aplicados.")
            return

        st.write(f"**{len(filtered_materials)} materiais encontrados:**")

        for material in filtered_materials:
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])

                with col1:
                    # Ícone por tipo
                    type_icons = {
                        "PDF": "📄", "Vídeo": "🎥", "Áudio": "🎵",
                        "Planilha": "📊", "Mapa Mental": "🧠", "Resumo": "📝"
                    }
                    icon = type_icons.get(material['type'], "📄")

                    st.markdown(f"### {icon} {material['title']}")
                    st.write(f"**Autor:** {material['author']} | **Matéria:** {material['subject']}")
                    st.write(material['description'])

                    # Tags
                    if material['tags']:
                        st.markdown("**Tags:** " + " • ".join([f"`{tag}`" for tag in material['tags']]))

                    # Badges
                    badges = []
                    if material['verified']:
                        badges.append("✅ Verificado")
                    if material['premium']:
                        badges.append("⭐ Premium")

                    if badges:
                        st.markdown(" | ".join(badges))

                with col2:
                    st.metric("⭐ Avaliação", f"{material['rating']:.1f}/5.0")
                    st.metric("📥 Downloads", material['downloads'])
                    st.metric("💬 Comentários", material['comments_count'])

                with col3:
                    st.metric("📁 Tamanho", material['size'])
                    upload_days = (datetime.now() - material['upload_date']).days
                    st.metric("📅 Upload", f"{upload_days}d atrás")

                    # Botões de ação
                    if st.button(f"📥 Baixar", key=f"download_{material['id']}", use_container_width=True):
                        st.success(f"Download iniciado: {material['title']}")

                    if st.button(f"⭐ Avaliar", key=f"rate_material_{material['id']}", use_container_width=True):
                        self.show_material_rating(material)

                st.divider()

    def filter_materials(self, materials: List[Dict[str, Any]], search: str, type_filter: str, subject_filter: str, sort_by: str) -> List[Dict[str, Any]]:
        """Filtra e ordena materiais"""
        # materials já é passado como parâmetro

        # Filtro por busca
        if search:
            materials = [
                m for m in materials
                if search.lower() in m['title'].lower()
                or search.lower() in m['subject'].lower()
                or search.lower() in m['description'].lower()
            ]

        # Filtro por tipo
        if type_filter != "Todos":
            materials = [m for m in materials if m['type'] == type_filter]

        # Filtro por matéria
        if subject_filter != "Todas":
            materials = [m for m in materials if m['subject'] == subject_filter]

        # Ordenação
        if sort_by == "Mais Recentes":
            materials.sort(key=lambda x: x['upload_date'], reverse=True)
        elif sort_by == "Mais Baixados":
            materials.sort(key=lambda x: x['downloads'], reverse=True)
        elif sort_by == "Melhor Avaliados":
            materials.sort(key=lambda x: x['rating'], reverse=True)
        elif sort_by == "Tamanho":
            materials.sort(key=lambda x: float(x['size'].split()[0]), reverse=True)

        return materials

    def show_upload_modal(self):
        """Mostra modal de upload de material"""
        with st.form("upload_material_form"):
            st.subheader("📤 Compartilhar Material")

            col1, col2 = st.columns(2)

            with col1:
                title = st.text_input("Título do material:", placeholder="Ex: Resumo de Direito Constitucional")
                material_type = st.selectbox("Tipo:", ["PDF", "Vídeo", "Áudio", "Planilha", "Mapa Mental", "Resumo"])
                subject = st.selectbox(
                    "Matéria:",
                    ["Direito Constitucional", "Português", "Matemática", "Raciocínio Lógico", "Informática", "Atualidades"]
                )

            with col2:
                description = st.text_area("Descrição:", placeholder="Descreva o conteúdo do material...", height=100)
                tags = st.multiselect(
                    "Tags:",
                    ["Direito Constitucional", "Português", "Matemática", "Raciocínio Lógico", "Informática", "Atualidades"]
                )
                group_share = st.selectbox("Compartilhar com grupo:", ["Público"] + [g['name'] for g in st.session_state.user_groups])

            # Upload do arquivo
            uploaded_file = st.file_uploader("Selecionar arquivo:", type=['pdf', 'docx', 'pptx', 'xlsx', 'mp4', 'mp3'])

            # Configurações
            with st.expander("⚙️ Configurações Avançadas"):
                allow_comments = st.checkbox("Permitir comentários", value=True)
                require_rating = st.checkbox("Exigir avaliação para download", value=False)
                premium_content = st.checkbox("Conteúdo premium", value=False)

            submitted = st.form_submit_button("🚀 Compartilhar", type="primary")

            if submitted:
                if title and description and uploaded_file:
                    new_material = {
                        'id': str(uuid.uuid4()),
                        'title': title,
                        'type': material_type,
                        'subject': subject,
                        'author': "Você",
                        'upload_date': datetime.now(),
                        'downloads': 0,
                        'rating': 0.0,
                        'size': f"{random.randint(1, 50)} MB",
                        'description': description,
                        'tags': tags,
                        'verified': False,
                        'premium': premium_content,
                        'comments_count': 0,
                        'group_id': None if group_share == "Público" else "group_id"
                    }

                    st.session_state.shared_materials.append(new_material)
                    st.success(f"✅ Material '{title}' compartilhado com sucesso!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Por favor, preencha todos os campos obrigatórios.")

    def show_material_rating(self, material: Dict[str, Any]):
        """Mostra modal de avaliação de material"""
        with st.form(f"material_rating_{material['id']}"):
            st.subheader(f"⭐ Avaliar: {material['title']}")

            rating = st.slider("Nota geral:", 1, 5, 5)

            criteria = {
                "Qualidade do Conteúdo": st.slider("Qualidade do Conteúdo:", 1, 5, 5),
                "Clareza": st.slider("Clareza:", 1, 5, 5),
                "Utilidade": st.slider("Utilidade:", 1, 5, 5),
                "Organização": st.slider("Organização:", 1, 5, 5)
            }

            comment = st.text_area("Comentário:", placeholder="Deixe um comentário sobre o material...")

            submitted = st.form_submit_button("📝 Enviar Avaliação")

            if submitted:
                st.success("✅ Avaliação enviada com sucesso!")

    def render_communication_hub(self):
        """Renderiza hub de comunicação"""
        st.subheader("💬 Chat e Comunicação")

        # Seletor de grupo
        user_groups = st.session_state.user_groups

        if not user_groups:
            st.info("💬 Você precisa participar de grupos para usar o chat.")
            return

        selected_group_name = st.selectbox(
            "Selecionar grupo:",
            [g['name'] for g in user_groups]
        )

        # Encontrar grupo selecionado
        selected_group = next((g for g in user_groups if g['name'] == selected_group_name), None)

        if not selected_group:
            return

        # Mostrar chat do grupo
        self.render_group_chat(selected_group)

    def render_group_chat(self, group: Dict[str, Any]):
        """Renderiza chat do grupo"""
        st.markdown(f"### 💬 Chat: {group['name']}")

        # Área de mensagens
        messages = st.session_state.group_messages.get(group['id'], [])

        # Container para mensagens
        chat_container = st.container()

        with chat_container:
            if not messages:
                st.info("💬 Nenhuma mensagem ainda. Seja o primeiro a enviar!")
            else:
                # Mostrar últimas 20 mensagens
                for message in messages[-20:]:
                    self.render_chat_message(message)

        st.divider()

        # Área de envio
        col1, col2 = st.columns([4, 1])

        with col1:
            new_message = st.text_input(
                "Digite sua mensagem:",
                placeholder="Escreva sua mensagem...",
                key=f"message_input_{group['id']}"
            )

        with col2:
            if st.button("📤 Enviar", key=f"send_{group['id']}", use_container_width=True):
                if new_message.strip():
                    self.send_message(group['id'], new_message)
                    st.rerun()

        # Botões de ação rápida
        st.markdown("**Ações Rápidas:**")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("📚 Compartilhar Material", key=f"share_material_{group['id']}"):
                st.info("Abrindo compartilhamento de material...")

        with col2:
            if st.button("🎯 Criar Simulado", key=f"create_quiz_{group['id']}"):
                st.info("Criando simulado em grupo...")

        with col3:
            if st.button("📅 Agendar Estudo", key=f"schedule_study_{group['id']}"):
                st.info("Agendando sessão de estudo...")

        with col4:
            if st.button("🔔 Notificar Todos", key=f"notify_all_{group['id']}"):
                st.info("Enviando notificação para o grupo...")

    def render_chat_message(self, message: Dict[str, Any]):
        """Renderiza uma mensagem do chat"""
        # Determinar se é mensagem do usuário
        is_user_message = message['author'] == "Você" or random.choice([True, False])

        # Estilo da mensagem
        if is_user_message:
            # Mensagem do usuário (direita)
            st.markdown(f"""
            <div style="text-align: right; margin: 10px 0;">
                <div style="background-color: #007bff; color: white; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;">
                    <strong>Você</strong><br>
                    {message['content']}
                </div>
                <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                    {message['timestamp'].strftime('%H:%M')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Mensagem de outros (esquerda)
            st.markdown(f"""
            <div style="text-align: left; margin: 10px 0;">
                <div style="background-color: #f1f1f1; color: black; padding: 10px; border-radius: 15px; display: inline-block; max-width: 70%;">
                    <strong>{message['author']}</strong><br>
                    {message['content']}
                </div>
                <div style="font-size: 0.8em; color: #666; margin-top: 5px;">
                    {message['timestamp'].strftime('%H:%M')} • {message['reactions']} ❤️
                </div>
            </div>
            """, unsafe_allow_html=True)

    def send_message(self, group_id: str, content: str):
        """Envia mensagem para o grupo"""
        new_message = {
            'id': str(uuid.uuid4()),
            'author': "Você",
            'content': content,
            'timestamp': datetime.now(),
            'type': MessageType.TEXTO,
            'reactions': 0,
            'replies': 0,
            'edited': False
        }

        if group_id not in st.session_state.group_messages:
            st.session_state.group_messages[group_id] = []

        st.session_state.group_messages[group_id].append(new_message)

    def render_collaboration_analytics(self):
        """Renderiza analytics colaborativos"""
        st.subheader("📊 Analytics Colaborativos")

        stats = st.session_state.collaboration_stats

        # Métricas da semana
        st.markdown("### 📈 Atividade Semanal")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("💬 Mensagens", stats['weekly_activity']['messages_sent'], delta="+25")

        with col2:
            st.metric("📚 Materiais", stats['weekly_activity']['materials_shared'], delta="+5")

        with col3:
            st.metric("🤝 Conexões", stats['weekly_activity']['new_connections'], delta="+3")

        with col4:
            st.metric("📖 Sessões", stats['weekly_activity']['study_sessions'], delta="+8")

        # Gráfico de engajamento por dia
        st.markdown("### 📊 Engajamento por Dia da Semana")

        engagement_data = stats['engagement_by_day']

        fig_engagement = px.bar(
            x=list(engagement_data.keys()),
            y=list(engagement_data.values()),
            title="Atividade por Dia da Semana",
            labels={'x': 'Dia', 'y': 'Atividade'},
            color=list(engagement_data.values()),
            color_continuous_scale="Blues"
        )

        st.plotly_chart(fig_engagement, use_container_width=True)

        # Matérias mais populares
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🎯 Matérias Mais Estudadas")

            popular_subjects = stats['popular_subjects']

            fig_subjects = px.pie(
                values=list(popular_subjects.values()),
                names=list(popular_subjects.keys()),
                title="Distribuição por Matéria"
            )

            st.plotly_chart(fig_subjects, use_container_width=True)

        with col2:
            st.markdown("### 🏆 Ranking de Grupos")

            # Simular ranking de grupos
            top_groups = sorted(
                st.session_state.study_groups,
                key=lambda x: x['members_count'] * x['success_rate'],
                reverse=True
            )[:5]

            for i, group in enumerate(top_groups, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}º"
                st.write(f"{medal} **{group['name']}** - {group['members_count']} membros, {group['success_rate']:.1%} sucesso")

        # Insights e recomendações
        st.markdown("### 💡 Insights e Recomendações")

        insights = [
            "🔥 **Pico de atividade**: Sábados são os dias mais ativos para estudos em grupo",
            "📚 **Matéria em alta**: Direito Constitucional teve 25% mais atividade esta semana",
            "🤝 **Networking**: Você pode se conectar com 12 novos colegas com interesses similares",
            "⭐ **Oportunidade**: 3 mentores especialistas estão disponíveis na sua área de interesse",
            "📈 **Progresso**: Grupos colaborativos têm 40% mais taxa de aprovação"
        ]

        for insight in insights:
            st.info(insight)

    def get_user_groups(self) -> List[Dict[str, Any]]:
        """Retorna grupos do usuário"""
        if 'user_groups' not in st.session_state:
            st.session_state.user_groups = []
        return st.session_state.user_groups

    def generate_sample_message_content(self) -> str:
        """Gera conteúdo de mensagem de exemplo"""
        messages = [
            "Alguém tem material sobre Direito Constitucional?",
            "Vamos fazer um simulado em grupo hoje às 19h?",
            "Compartilhei um resumo de Português na biblioteca",
            "Quem pode me ajudar com essa questão de matemática?",
            "Ótima explicação! Muito obrigado pela ajuda",
            "Pessoal, criei um cronograma de estudos para a semana",
            "Encontrei uma videoaula excelente sobre esse tema",
            "Alguém quer formar dupla para revisão?",
            "Parabéns pela aprovação! Inspiração para todos nós",
            "Dica: essa banca sempre cobra esse tipo de questão"
        ]
        return random.choice(messages)
