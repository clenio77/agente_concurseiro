#!/usr/bin/env python3
"""
Componente de Assistente de Voz Inteligente - Fase 3
Sistema de reconhecimento de voz, text-to-speech e conversação natural
"""

import streamlit as st
import json
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from enum import Enum
import random
import re

class VoiceCommandType(Enum):
    """Tipos de comandos de voz"""
    NAVIGATION = "navigation"
    STUDY = "study"
    QUESTION = "question"
    CONTROL = "control"
    INFORMATION = "information"
    CREATION = "creation"

class VoiceLanguage(Enum):
    """Idiomas suportados"""
    PT_BR = "pt-BR"
    EN_US = "en-US"
    ES_ES = "es-ES"
    FR_FR = "fr-FR"

class SpeechQuality(Enum):
    """Qualidade de síntese de voz"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    PREMIUM = "premium"

class VoiceGender(Enum):
    """Gênero da voz"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

class VoiceAssistant:
    """Sistema de Assistente de Voz Inteligente"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializa estado da sessão de voz"""
        if 'voice_settings' not in st.session_state:
            st.session_state.voice_settings = {
                'voice_enabled': True,
                'language': VoiceLanguage.PT_BR.value,
                'speech_rate': 1.0,
                'speech_pitch': 1.0,
                'speech_volume': 0.8,
                'voice_gender': VoiceGender.FEMALE.value,
                'speech_quality': SpeechQuality.HIGH.value,
                'wake_word': 'Agente',
                'continuous_listening': False,
                'noise_cancellation': True,
                'auto_punctuation': True,
                'command_confirmation': True
            }
        
        if 'voice_commands' not in st.session_state:
            st.session_state.voice_commands = self.generate_voice_commands()
        
        if 'voice_history' not in st.session_state:
            st.session_state.voice_history = self.generate_voice_history()
        
        if 'voice_analytics' not in st.session_state:
            st.session_state.voice_analytics = self.generate_voice_analytics()
        
        if 'voice_conversations' not in st.session_state:
            st.session_state.voice_conversations = self.generate_conversations()
        
        if 'voice_status' not in st.session_state:
            st.session_state.voice_status = {
                'listening': False,
                'speaking': False,
                'processing': False,
                'last_command': None,
                'confidence': 0.0,
                'session_active': False
            }
    
    def generate_voice_commands(self) -> List[Dict[str, Any]]:
        """Gera comandos de voz disponíveis"""
        commands = [
            # Navegação
            {
                'id': str(uuid.uuid4()),
                'command': 'Ir para dashboard',
                'type': VoiceCommandType.NAVIGATION,
                'action': 'navigate_dashboard',
                'description': 'Navega para o dashboard principal',
                'examples': ['Ir para dashboard', 'Abrir painel principal', 'Mostrar dashboard'],
                'confidence_required': 0.8,
                'enabled': True
            },
            {
                'id': str(uuid.uuid4()),
                'command': 'Abrir simulados',
                'type': VoiceCommandType.NAVIGATION,
                'action': 'open_mock_exams',
                'description': 'Abre a seção de simulados',
                'examples': ['Abrir simulados', 'Ir para simulados', 'Mostrar provas'],
                'confidence_required': 0.8,
                'enabled': True
            },
            # Estudo
            {
                'id': str(uuid.uuid4()),
                'command': 'Iniciar sessão de estudo',
                'type': VoiceCommandType.STUDY,
                'action': 'start_study_session',
                'description': 'Inicia uma nova sessão de estudo',
                'examples': ['Iniciar estudo', 'Começar sessão', 'Vamos estudar'],
                'confidence_required': 0.7,
                'enabled': True
            },
            {
                'id': str(uuid.uuid4()),
                'command': 'Ler questão',
                'type': VoiceCommandType.STUDY,
                'action': 'read_question',
                'description': 'Lê a questão atual em voz alta',
                'examples': ['Ler questão', 'Leia a pergunta', 'Qual é a questão'],
                'confidence_required': 0.9,
                'enabled': True
            },
            # Controle
            {
                'id': str(uuid.uuid4()),
                'command': 'Pausar',
                'type': VoiceCommandType.CONTROL,
                'action': 'pause',
                'description': 'Pausa a atividade atual',
                'examples': ['Pausar', 'Parar', 'Esperar'],
                'confidence_required': 0.9,
                'enabled': True
            },
            {
                'id': str(uuid.uuid4()),
                'command': 'Continuar',
                'type': VoiceCommandType.CONTROL,
                'action': 'resume',
                'description': 'Continua a atividade pausada',
                'examples': ['Continuar', 'Retomar', 'Prosseguir'],
                'confidence_required': 0.9,
                'enabled': True
            },
            # Informação
            {
                'id': str(uuid.uuid4()),
                'command': 'Qual meu progresso',
                'type': VoiceCommandType.INFORMATION,
                'action': 'show_progress',
                'description': 'Mostra o progresso atual do usuário',
                'examples': ['Qual meu progresso', 'Como estou indo', 'Mostrar estatísticas'],
                'confidence_required': 0.7,
                'enabled': True
            },
            {
                'id': str(uuid.uuid4()),
                'command': 'Próxima revisão',
                'type': VoiceCommandType.INFORMATION,
                'action': 'next_review',
                'description': 'Informa sobre a próxima revisão agendada',
                'examples': ['Próxima revisão', 'Quando revisar', 'Agenda de estudos'],
                'confidence_required': 0.8,
                'enabled': True
            },
            # Criação
            {
                'id': str(uuid.uuid4()),
                'command': 'Criar anotação',
                'type': VoiceCommandType.CREATION,
                'action': 'create_note',
                'description': 'Cria uma nova anotação por ditado',
                'examples': ['Criar anotação', 'Nova nota', 'Anotar isso'],
                'confidence_required': 0.8,
                'enabled': True
            },
            {
                'id': str(uuid.uuid4()),
                'command': 'Agendar revisão',
                'type': VoiceCommandType.CREATION,
                'action': 'schedule_review',
                'description': 'Agenda uma revisão para data específica',
                'examples': ['Agendar revisão', 'Marcar revisão', 'Programar estudo'],
                'confidence_required': 0.7,
                'enabled': True
            }
        ]
        
        return commands
    
    def generate_voice_history(self) -> List[Dict[str, Any]]:
        """Gera histórico de comandos de voz"""
        history = []
        
        for i in range(25):
            command = random.choice(st.session_state.voice_commands)
            
            entry = {
                'id': str(uuid.uuid4()),
                'timestamp': datetime.now() - timedelta(minutes=random.randint(1, 1440)),
                'command': command['command'],
                'type': command['type'],
                'confidence': round(random.uniform(0.7, 1.0), 2),
                'success': random.choice([True, True, True, False]),  # 75% success rate
                'response_time': random.randint(100, 2000),  # ms
                'audio_duration': round(random.uniform(1.0, 5.0), 1),
                'language_detected': st.session_state.voice_settings['language'],
                'noise_level': round(random.uniform(0.1, 0.8), 2),
                'user_feedback': random.choice(['positive', 'neutral', 'negative', None])
            }
            
            history.append(entry)
        
        return sorted(history, key=lambda x: x['timestamp'], reverse=True)
    
    def generate_voice_analytics(self) -> Dict[str, Any]:
        """Gera analytics de uso de voz"""
        return {
            'total_commands': random.randint(200, 1000),
            'success_rate': round(random.uniform(0.85, 0.95), 2),
            'avg_confidence': round(random.uniform(0.80, 0.95), 2),
            'avg_response_time': random.randint(500, 1500),  # ms
            'most_used_command': random.choice(st.session_state.voice_commands)['command'],
            'daily_usage': [random.randint(10, 50) for _ in range(7)],
            'command_distribution': {
                'Navegação': random.randint(25, 35),
                'Estudo': random.randint(30, 45),
                'Controle': random.randint(15, 25),
                'Informação': random.randint(10, 20),
                'Criação': random.randint(5, 15)
            },
            'language_accuracy': {
                'Português': round(random.uniform(0.90, 0.98), 2),
                'Inglês': round(random.uniform(0.85, 0.95), 2),
                'Espanhol': round(random.uniform(0.80, 0.90), 2)
            },
            'user_satisfaction': round(random.uniform(4.3, 4.8), 1),
            'error_types': {
                'Não reconhecido': random.randint(5, 15),
                'Baixa confiança': random.randint(3, 10),
                'Ruído ambiente': random.randint(2, 8),
                'Comando inválido': random.randint(1, 5)
            },
            'improvement_trend': round(random.uniform(0.05, 0.15), 2)
        }
    
    def generate_conversations(self) -> List[Dict[str, Any]]:
        """Gera conversas de exemplo com o assistente"""
        conversations = []
        
        conversation_templates = [
            {
                'topic': 'Direito Constitucional',
                'messages': [
                    {'role': 'user', 'content': 'Explique o princípio da separação dos poderes'},
                    {'role': 'assistant', 'content': 'O princípio da separação dos poderes, criado por Montesquieu, divide o Estado em três poderes independentes: Executivo, Legislativo e Judiciário. Cada poder tem funções específicas e serve como controle dos demais.'},
                    {'role': 'user', 'content': 'Quais são as funções de cada poder?'},
                    {'role': 'assistant', 'content': 'O Poder Executivo administra e executa as leis, o Legislativo cria as leis, e o Judiciário interpreta e aplica as leis. Esse sistema garante equilíbrio e evita concentração de poder.'}
                ]
            },
            {
                'topic': 'Matemática',
                'messages': [
                    {'role': 'user', 'content': 'Como resolver equações do segundo grau?'},
                    {'role': 'assistant', 'content': 'Para resolver equações do segundo grau (ax² + bx + c = 0), você pode usar a fórmula de Bhaskara: x = (-b ± √(b²-4ac)) / 2a. O discriminante (b²-4ac) determina o número de soluções.'},
                    {'role': 'user', 'content': 'Pode dar um exemplo prático?'},
                    {'role': 'assistant', 'content': 'Claro! Para x² - 5x + 6 = 0: a=1, b=-5, c=6. Discriminante = 25-24 = 1. Então x = (5 ± 1)/2, resultando em x₁=3 e x₂=2.'}
                ]
            }
        ]
        
        for i, template in enumerate(conversation_templates):
            conversation = {
                'id': str(uuid.uuid4()),
                'topic': template['topic'],
                'start_time': datetime.now() - timedelta(hours=random.randint(1, 48)),
                'duration': random.randint(5, 30),  # minutos
                'messages': template['messages'],
                'satisfaction_rating': round(random.uniform(4.0, 5.0), 1),
                'voice_quality': round(random.uniform(0.85, 0.98), 2),
                'understanding_rate': round(random.uniform(0.90, 1.0), 2)
            }
            conversations.append(conversation)
        
        return conversations
    
    def render_voice_dashboard(self):
        """Renderiza dashboard principal de voz"""
        st.markdown("#### 🎤 Dashboard do Assistente de Voz")
        
        # Status atual
        status = st.session_state.voice_status
        analytics = st.session_state.voice_analytics
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🎯 Comandos Totais",
                analytics['total_commands'],
                f"+{random.randint(10, 30)} hoje"
            )
        
        with col2:
            st.metric(
                "✅ Taxa de Sucesso",
                f"{analytics['success_rate']*100:.1f}%",
                f"+{random.uniform(1, 3):.1f}%"
            )
        
        with col3:
            st.metric(
                "⚡ Tempo Resposta",
                f"{analytics['avg_response_time']}ms",
                f"-{random.randint(10, 50)}ms"
            )
        
        with col4:
            st.metric(
                "🎯 Confiança Média",
                f"{analytics['avg_confidence']*100:.1f}%",
                f"+{random.uniform(1, 2):.1f}%"
            )
        
        # Status do sistema de voz
        st.markdown("##### 🔊 Status do Sistema")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Status de hardware
            st.markdown("**Hardware de Áudio:**")
            st.success("✅ Microfone: Ativo")
            st.success("✅ Alto-falantes: Funcionando")
            st.success("✅ Cancelamento de ruído: Ativo")
            st.info("ℹ️ Qualidade do sinal: 92%")
        
        with col2:
            # Status de software
            st.markdown("**Processamento de Voz:**")
            st.success("✅ Reconhecimento: Online")
            st.success("✅ Síntese: Operacional")
            st.success("✅ NLP: Ativo")
            st.warning("⚠️ Latência de rede: 120ms")
        
        # Controles de voz em tempo real
        st.markdown("##### 🎙️ Controles de Voz")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🎤 Iniciar Escuta", use_container_width=True):
                st.session_state.voice_status['listening'] = True
                st.success("🎤 Escutando... Diga seu comando!")
        
        with col2:
            if st.button("⏹️ Parar Escuta", use_container_width=True):
                st.session_state.voice_status['listening'] = False
                st.info("⏹️ Escuta interrompida")
        
        with col3:
            if st.button("🔊 Teste de Voz", use_container_width=True):
                st.success("🔊 Olá! Eu sou seu assistente de voz. Como posso ajudar?")
        
        with col4:
            if st.button("⚙️ Calibrar", use_container_width=True):
                st.info("⚙️ Calibrando microfone e alto-falantes...")
        
        # Gráfico de uso diário
        st.markdown("##### 📈 Uso Diário de Comandos")
        
        import plotly.graph_objects as go
        
        days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        usage = analytics['daily_usage']
        
        fig = go.Figure(data=go.Scatter(
            x=days,
            y=usage,
            mode='lines+markers',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(size=8, color='#FF6B6B'),
            fill='tonexty'
        ))
        
        fig.update_layout(
            title="Comandos de Voz por Dia",
            xaxis_title="Dia da Semana",
            yaxis_title="Número de Comandos",
            height=300
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_command_library(self):
        """Renderiza biblioteca de comandos de voz"""
        st.markdown("#### 📋 Biblioteca de Comandos")
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            command_types = [ct.value for ct in VoiceCommandType]
            selected_type = st.selectbox("Tipo de Comando", ["Todos"] + command_types)
        
        with col2:
            enabled_filter = st.selectbox("Status", ["Todos", "Habilitados", "Desabilitados"])
        
        with col3:
            confidence_filter = st.slider("Confiança Mínima", 0.0, 1.0, 0.7)
        
        # Busca
        search_term = st.text_input("🔍 Buscar comando", placeholder="Digite para buscar...")
        
        # Filtrar comandos
        filtered_commands = st.session_state.voice_commands.copy()
        
        if selected_type != "Todos":
            filtered_commands = [c for c in filtered_commands if c['type'].value == selected_type]
        
        if enabled_filter == "Habilitados":
            filtered_commands = [c for c in filtered_commands if c['enabled']]
        elif enabled_filter == "Desabilitados":
            filtered_commands = [c for c in filtered_commands if not c['enabled']]
        
        filtered_commands = [c for c in filtered_commands if c['confidence_required'] >= confidence_filter]
        
        if search_term:
            filtered_commands = [c for c in filtered_commands 
                              if search_term.lower() in c['command'].lower() 
                              or search_term.lower() in c['description'].lower()]
        
        st.write(f"📊 **{len(filtered_commands)} comandos** encontrados")
        
        # Lista de comandos
        for command in filtered_commands:
            with st.expander(f"🎤 {command['command']} ({command['type'].value})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Descrição:** {command['description']}")
                    st.write(f"**Tipo:** {command['type'].value.title()}")
                    st.write(f"**Confiança necessária:** {command['confidence_required']*100:.0f}%")
                    
                    status = "✅ Habilitado" if command['enabled'] else "❌ Desabilitado"
                    st.write(f"**Status:** {status}")
                
                with col2:
                    st.write("**Exemplos de uso:**")
                    for example in command['examples']:
                        st.write(f"• *\"{example}\"*")
                
                # Controles do comando
                col_a, col_b, col_c = st.columns(3)
                
                with col_a:
                    if st.button("🎤 Testar", key=f"test_{command['id']}"):
                        self.test_voice_command(command)
                
                with col_b:
                    if st.button("✏️ Editar", key=f"edit_{command['id']}"):
                        self.edit_voice_command(command)
                
                with col_c:
                    action = "Desabilitar" if command['enabled'] else "Habilitar"
                    if st.button(f"⚙️ {action}", key=f"toggle_{command['id']}"):
                        command['enabled'] = not command['enabled']
                        st.success(f"✅ Comando {action.lower()}ado!")
    
    def render_conversation_interface(self):
        """Renderiza interface de conversação"""
        st.markdown("#### 💬 Conversação Natural")
        
        st.info("🎙️ **Modo Conversação:** Fale naturalmente com o assistente sobre suas dúvidas de estudo")
        
        # Histórico de conversas
        conversations = st.session_state.voice_conversations
        
        if conversations:
            st.markdown("##### 📚 Conversas Recentes")
            
            for conversation in conversations:
                with st.expander(f"💬 {conversation['topic']} - {conversation['start_time'].strftime('%d/%m %H:%M')}"):
                    st.write(f"**Duração:** {conversation['duration']} minutos")
                    st.write(f"**Satisfação:** ⭐ {conversation['satisfaction_rating']}/5.0")
                    st.write(f"**Qualidade de voz:** {conversation['voice_quality']*100:.1f}%")
                    
                    st.markdown("**Conversa:**")
                    
                    for message in conversation['messages']:
                        if message['role'] == 'user':
                            st.markdown(f"**👤 Você:** {message['content']}")
                        else:
                            st.markdown(f"**🤖 Assistente:** {message['content']}")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if st.button("🔊 Reproduzir", key=f"play_{conversation['id']}"):
                            st.success("🔊 Reproduzindo conversa...")
                    
                    with col2:
                        if st.button("📝 Continuar", key=f"continue_{conversation['id']}"):
                            st.info("💬 Continuando conversa...")
        
        # Nova conversa
        st.markdown("##### 🆕 Nova Conversa")
        
        col1, col2 = st.columns(2)
        
        with col1:
            topic = st.selectbox("Tópico", [
                "Direito Constitucional", "Direito Administrativo", "Português",
                "Matemática", "Raciocínio Lógico", "Informática", "Atualidades"
            ])
        
        with col2:
            conversation_mode = st.selectbox("Modo", [
                "Explicação", "Perguntas e Respostas", "Revisão", "Dúvidas"
            ])
        
        user_question = st.text_area("💬 Sua pergunta ou tópico:", 
                                   placeholder="Digite sua pergunta ou diga 'Iniciar conversa por voz'")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🎤 Falar", use_container_width=True):
                st.success("🎤 Escutando sua pergunta...")
                # Simular reconhecimento de voz
                st.info("🤖 Processando sua pergunta sobre " + topic.lower() + "...")
        
        with col2:
            if st.button("💬 Enviar Texto", use_container_width=True):
                if user_question:
                    response = self.generate_ai_response(user_question, topic)
                    st.success("🤖 **Resposta do Assistente:**")
                    st.write(response)
                    st.info("🔊 Reproduzindo resposta em áudio...")
                else:
                    st.error("❌ Digite uma pergunta primeiro")
    
    def generate_ai_response(self, question: str, topic: str) -> str:
        """Gera resposta inteligente baseada na pergunta"""
        responses = {
            "Direito Constitucional": [
                "Excelente pergunta sobre Direito Constitucional! Este é um dos pilares do ordenamento jurídico brasileiro.",
                "No contexto constitucional, é importante considerar os princípios fundamentais da Constituição de 1988.",
                "Esta questão envolve aspectos importantes da organização do Estado e dos direitos fundamentais."
            ],
            "Matemática": [
                "Vamos resolver este problema matemático passo a passo para garantir total compreensão.",
                "Esta é uma questão interessante que envolve conceitos fundamentais da matemática.",
                "Para resolver este tipo de problema, precisamos aplicar os conceitos básicos de forma sistemática."
            ],
            "Português": [
                "Esta é uma questão importante sobre a língua portuguesa e suas regras gramaticais.",
                "Vamos analisar este aspecto da gramática portuguesa de forma clara e objetiva.",
                "Este tópico é fundamental para uma boa comunicação escrita e oral."
            ]
        }
        
        base_responses = responses.get(topic, ["Esta é uma pergunta interessante que merece atenção especial."])
        return random.choice(base_responses) + f" Sobre '{question}', posso explicar que este assunto requer estudo detalhado e prática constante para domínio completo."
    
    def test_voice_command(self, command: Dict[str, Any]):
        """Testa comando de voz"""
        st.success(f"🎤 **Testando comando:** {command['command']}")
        st.info("🤖 **Resposta simulada:** Comando reconhecido com sucesso!")
        
        # Simular execução do comando
        if command['action'] == 'navigate_dashboard':
            st.info("📊 Navegando para o dashboard...")
        elif command['action'] == 'start_study_session':
            st.info("📚 Iniciando sessão de estudo...")
        elif command['action'] == 'read_question':
            st.info("🔊 Lendo questão em voz alta...")
        else:
            st.info(f"⚙️ Executando ação: {command['action']}")
    
    def edit_voice_command(self, command: Dict[str, Any]):
        """Edita comando de voz"""
        st.info(f"✏️ **Editando comando:** {command['command']}")
        
        with st.form(f"edit_command_{command['id']}"):
            new_command = st.text_input("Comando", value=command['command'])
            new_description = st.text_area("Descrição", value=command['description'])
            new_confidence = st.slider("Confiança necessária", 0.0, 1.0, command['confidence_required'])
            
            if st.form_submit_button("💾 Salvar Alterações"):
                command['command'] = new_command
                command['description'] = new_description
                command['confidence_required'] = new_confidence
                st.success("✅ Comando atualizado com sucesso!")
    
    def render_voice_analytics(self):
        """Renderiza analytics de voz"""
        st.markdown("#### 📊 Analytics de Voz")
        
        analytics = st.session_state.voice_analytics
        
        # Métricas detalhadas
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📈 Melhoria Contínua", f"+{analytics['improvement_trend']*100:.1f}%")
            st.metric("😊 Satisfação", f"{analytics['user_satisfaction']:.1f}/5.0")
        
        with col2:
            st.metric("🎯 Comando Mais Usado", analytics['most_used_command'])
            st.metric("⚡ Tempo Médio", f"{analytics['avg_response_time']}ms")
        
        with col3:
            st.metric("✅ Taxa de Sucesso", f"{analytics['success_rate']*100:.1f}%")
            st.metric("🎤 Confiança Média", f"{analytics['avg_confidence']*100:.1f}%")
        
        # Gráficos de distribuição
        import plotly.express as px
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribuição de comandos
            command_dist = analytics['command_distribution']
            
            fig = px.pie(
                values=list(command_dist.values()),
                names=list(command_dist.keys()),
                title="Distribuição de Tipos de Comando"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Precisão por idioma
            lang_accuracy = analytics['language_accuracy']
            
            fig = px.bar(
                x=list(lang_accuracy.keys()),
                y=[acc*100 for acc in lang_accuracy.values()],
                title="Precisão por Idioma (%)",
                labels={'x': 'Idioma', 'y': 'Precisão (%)'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Tipos de erro
        st.markdown("##### ❌ Análise de Erros")
        
        error_types = analytics['error_types']
        
        for error_type, count in error_types.items():
            percentage = (count / sum(error_types.values())) * 100
            st.write(f"**{error_type}:** {count} ocorrências ({percentage:.1f}%)")
    
    def render_voice_settings(self):
        """Renderiza configurações de voz"""
        st.markdown("#### ⚙️ Configurações de Voz")
        
        settings = st.session_state.voice_settings
        
        # Configurações básicas
        st.markdown("##### 🎤 Configurações Básicas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            voice_enabled = st.checkbox("Assistente de Voz Ativo", value=settings['voice_enabled'])
            
            language = st.selectbox(
                "Idioma",
                [lang.value for lang in VoiceLanguage],
                index=[lang.value for lang in VoiceLanguage].index(settings['language'])
            )
            
            voice_gender = st.selectbox(
                "Gênero da Voz",
                [gender.value for gender in VoiceGender],
                index=[gender.value for gender in VoiceGender].index(settings['voice_gender'])
            )
        
        with col2:
            speech_quality = st.selectbox(
                "Qualidade da Síntese",
                [quality.value for quality in SpeechQuality],
                index=[quality.value for quality in SpeechQuality].index(settings['speech_quality'])
            )
            
            wake_word = st.text_input("Palavra de Ativação", value=settings['wake_word'])
            
            continuous_listening = st.checkbox("Escuta Contínua", value=settings['continuous_listening'])
        
        # Configurações avançadas
        st.markdown("##### 🔧 Configurações Avançadas")
        
        speech_rate = st.slider("Velocidade da Fala", 0.5, 2.0, settings['speech_rate'])
        speech_pitch = st.slider("Tom da Voz", 0.5, 2.0, settings['speech_pitch'])
        speech_volume = st.slider("Volume", 0.0, 1.0, settings['speech_volume'])
        
        col1, col2 = st.columns(2)
        
        with col1:
            noise_cancellation = st.checkbox("Cancelamento de Ruído", value=settings['noise_cancellation'])
            auto_punctuation = st.checkbox("Pontuação Automática", value=settings['auto_punctuation'])
        
        with col2:
            command_confirmation = st.checkbox("Confirmação de Comandos", value=settings['command_confirmation'])
        
        # Salvar configurações
        if st.button("💾 Salvar Configurações", use_container_width=True):
            st.session_state.voice_settings.update({
                'voice_enabled': voice_enabled,
                'language': language,
                'speech_rate': speech_rate,
                'speech_pitch': speech_pitch,
                'speech_volume': speech_volume,
                'voice_gender': voice_gender,
                'speech_quality': speech_quality,
                'wake_word': wake_word,
                'continuous_listening': continuous_listening,
                'noise_cancellation': noise_cancellation,
                'auto_punctuation': auto_punctuation,
                'command_confirmation': command_confirmation
            })
            
            st.success("✅ Configurações de voz salvas com sucesso!")
            st.rerun()
    
    def render(self):
        """Método principal de renderização"""
        st.markdown("# 🎤 Assistente de Voz Inteligente")
        st.markdown("*Sistema de reconhecimento de voz, text-to-speech e conversação natural*")
        
        # Verificar suporte de voz
        self.check_voice_support()
        
        # Tabs principais
        tabs = st.tabs([
            "🎯 Dashboard", 
            "📋 Comandos", 
            "💬 Conversação", 
            "📊 Analytics",
            "📜 Histórico",
            "⚙️ Configurações"
        ])
        
        with tabs[0]:
            self.render_voice_dashboard()
        
        with tabs[1]:
            self.render_command_library()
        
        with tabs[2]:
            self.render_conversation_interface()
        
        with tabs[3]:
            self.render_voice_analytics()
        
        with tabs[4]:
            self.render_voice_history()
        
        with tabs[5]:
            self.render_voice_settings()
    
    def check_voice_support(self):
        """Verifica suporte de voz do navegador"""
        st.markdown("#### 🔍 Status de Compatibilidade de Voz")
        
        # Simulação de verificação de suporte
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success("✅ Web Speech API")
        
        with col2:
            st.success("✅ Microfone Disponível")
        
        with col3:
            st.success("✅ Síntese de Voz")
        
        st.info("🎉 **Seu navegador suporta todas as funcionalidades de voz!** Comandos e conversação estão disponíveis.")
    
    def render_voice_history(self):
        """Renderiza histórico de comandos de voz"""
        st.markdown("#### 📜 Histórico de Comandos")
        
        history = st.session_state.voice_history
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_filter = st.date_input("Data", value=datetime.now().date())
        
        with col2:
            success_filter = st.selectbox("Status", ["Todos", "Sucesso", "Falha"])
        
        with col3:
            confidence_filter = st.slider("Confiança Mínima", 0.0, 1.0, 0.0)
        
        # Filtrar histórico
        filtered_history = history.copy()
        
        if success_filter == "Sucesso":
            filtered_history = [h for h in filtered_history if h['success']]
        elif success_filter == "Falha":
            filtered_history = [h for h in filtered_history if not h['success']]
        
        filtered_history = [h for h in filtered_history if h['confidence'] >= confidence_filter]
        
        st.write(f"📊 **{len(filtered_history)} comandos** no histórico")
        
        # Lista do histórico
        for entry in filtered_history[:10]:  # Mostrar apenas os 10 mais recentes
            with st.expander(f"🎤 {entry['command']} - {entry['timestamp'].strftime('%d/%m %H:%M')}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Comando:** {entry['command']}")
                    st.write(f"**Tipo:** {entry['type'].value.title()}")
                    st.write(f"**Confiança:** {entry['confidence']*100:.1f}%")
                    
                    status = "✅ Sucesso" if entry['success'] else "❌ Falha"
                    st.write(f"**Status:** {status}")
                
                with col2:
                    st.write(f"**Tempo de resposta:** {entry['response_time']}ms")
                    st.write(f"**Duração do áudio:** {entry['audio_duration']}s")
                    st.write(f"**Nível de ruído:** {entry['noise_level']*100:.1f}%")
                    
                    if entry['user_feedback']:
                        feedback_icon = {"positive": "👍", "neutral": "😐", "negative": "👎"}
                        st.write(f"**Feedback:** {feedback_icon[entry['user_feedback']]}")
