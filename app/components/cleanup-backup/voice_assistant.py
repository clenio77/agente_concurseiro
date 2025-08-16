"""
🎤 Voice Assistant - Assistente de Voz Inteligente
Componente de reconhecimento de voz e síntese de fala para controle hands-free
"""

import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from enum import Enum
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

class VoiceCommandType(Enum):
    """Tipos de comandos de voz"""
    NAVIGATION = "navigation"
    CONTENT_READ = "content_read"
    QUIZ_CONTROL = "quiz_control"
    STUDY_PLAN = "study_plan"
    ANALYTICS = "analytics"
    SETTINGS = "settings"

class VoiceLanguage(Enum):
    """Idiomas suportados"""
    PT_BR = "pt-BR"
    EN_US = "en-US"
    ES_ES = "es-ES"

class VoiceGender(Enum):
    """Gênero da voz"""
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

class VoiceAssistant:
    """Sistema completo de assistente de voz"""
    
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Inicializar estado da sessão"""
        if 'voice_settings' not in st.session_state:
            st.session_state.voice_settings = {
                'enabled': True,
                'language': VoiceLanguage.PT_BR.value,
                'voice_gender': VoiceGender.FEMALE.value,
                'speech_rate': 1.0,
                'volume': 0.8,
                'auto_read': False,
                'wake_word': "agente",
                'continuous_listening': False
            }
        
        if 'voice_commands' not in st.session_state:
            st.session_state.voice_commands = self.generate_voice_commands()
        
        if 'voice_history' not in st.session_state:
            st.session_state.voice_history = []
        
        if 'voice_analytics' not in st.session_state:
            st.session_state.voice_analytics = self.generate_voice_analytics()
    
    def generate_voice_commands(self) -> List[Dict]:
        """Gerar comandos de voz disponíveis"""
        return [
            {
                'id': 'nav_dashboard',
                'command': 'ir para dashboard',
                'type': VoiceCommandType.NAVIGATION.value,
                'action': 'navigate_to_dashboard',
                'description': 'Navegar para o dashboard principal',
                'examples': ['ir para dashboard', 'abrir dashboard', 'mostrar painel'],
                'confidence': 0.95,
                'usage_count': 45
            },
            {
                'id': 'read_question',
                'command': 'ler questão',
                'type': VoiceCommandType.CONTENT_READ.value,
                'action': 'read_current_question',
                'description': 'Ler a questão atual em voz alta',
                'examples': ['ler questão', 'leia a pergunta', 'fale a questão'],
                'confidence': 0.92,
                'usage_count': 78
            },
            {
                'id': 'start_quiz',
                'command': 'iniciar simulado',
                'type': VoiceCommandType.QUIZ_CONTROL.value,
                'action': 'start_mock_exam',
                'description': 'Iniciar um novo simulado',
                'examples': ['iniciar simulado', 'começar prova', 'novo teste'],
                'confidence': 0.88,
                'usage_count': 32
            },
            {
                'id': 'show_performance',
                'command': 'mostrar desempenho',
                'type': VoiceCommandType.ANALYTICS.value,
                'action': 'show_performance_data',
                'description': 'Exibir métricas de desempenho',
                'examples': ['mostrar desempenho', 'ver performance', 'meus resultados'],
                'confidence': 0.90,
                'usage_count': 56
            },
            {
                'id': 'create_study_plan',
                'command': 'criar plano de estudos',
                'type': VoiceCommandType.STUDY_PLAN.value,
                'action': 'create_study_plan',
                'description': 'Criar novo plano de estudos',
                'examples': ['criar plano', 'novo cronograma', 'planejar estudos'],
                'confidence': 0.85,
                'usage_count': 23
            },
            {
                'id': 'pause_session',
                'command': 'pausar sessão',
                'type': VoiceCommandType.QUIZ_CONTROL.value,
                'action': 'pause_current_session',
                'description': 'Pausar a sessão atual',
                'examples': ['pausar', 'parar', 'interromper'],
                'confidence': 0.93,
                'usage_count': 67
            },
            {
                'id': 'next_question',
                'command': 'próxima questão',
                'type': VoiceCommandType.QUIZ_CONTROL.value,
                'action': 'next_question',
                'description': 'Avançar para próxima questão',
                'examples': ['próxima', 'avançar', 'continuar'],
                'confidence': 0.91,
                'usage_count': 89
            },
            {
                'id': 'repeat_content',
                'command': 'repetir',
                'type': VoiceCommandType.CONTENT_READ.value,
                'action': 'repeat_last_content',
                'description': 'Repetir o último conteúdo lido',
                'examples': ['repetir', 'falar novamente', 'mais uma vez'],
                'confidence': 0.94,
                'usage_count': 34
            },
            {
                'id': 'voice_settings',
                'command': 'configurações de voz',
                'type': VoiceCommandType.SETTINGS.value,
                'action': 'open_voice_settings',
                'description': 'Abrir configurações de voz',
                'examples': ['configurações', 'ajustes de voz', 'opções'],
                'confidence': 0.87,
                'usage_count': 12
            },
            {
                'id': 'help_commands',
                'command': 'ajuda',
                'type': VoiceCommandType.SETTINGS.value,
                'action': 'show_voice_help',
                'description': 'Mostrar comandos disponíveis',
                'examples': ['ajuda', 'comandos', 'o que posso falar'],
                'confidence': 0.96,
                'usage_count': 28
            }
        ]
    
    def generate_voice_analytics(self) -> Dict:
        """Gerar analytics do assistente de voz"""
        return {
            'total_commands': 464,
            'successful_recognitions': 421,
            'accuracy_rate': 90.7,
            'average_response_time': 1.2,
            'most_used_commands': [
                {'command': 'próxima questão', 'count': 89},
                {'command': 'ler questão', 'count': 78},
                {'command': 'pausar sessão', 'count': 67},
                {'command': 'mostrar desempenho', 'count': 56},
                {'command': 'ir para dashboard', 'count': 45}
            ],
            'usage_by_type': {
                'quiz_control': 45.2,
                'content_read': 24.1,
                'navigation': 15.3,
                'analytics': 10.8,
                'study_plan': 3.4,
                'settings': 1.2
            },
            'daily_usage': [
                {'date': '2025-08-01', 'commands': 45},
                {'date': '2025-08-02', 'commands': 52},
                {'date': '2025-08-03', 'commands': 38},
                {'date': '2025-08-04', 'commands': 67},
                {'date': '2025-08-05', 'commands': 41},
                {'date': '2025-08-06', 'commands': 58},
                {'date': '2025-08-07', 'commands': 63}
            ],
            'satisfaction_score': 4.6,
            'error_types': {
                'recognition_failed': 23,
                'command_not_found': 12,
                'network_error': 5,
                'timeout': 3
            }
        }
    
    def process_voice_command(self, command_text: str) -> Dict:
        """Processar comando de voz"""
        command_text = command_text.lower().strip()
        
        # Buscar comando correspondente
        for cmd in st.session_state.voice_commands:
            if any(example in command_text for example in cmd['examples']):
                # Simular execução do comando
                result = {
                    'success': True,
                    'command_id': cmd['id'],
                    'action': cmd['action'],
                    'confidence': cmd['confidence'],
                    'response': f"Executando: {cmd['description']}",
                    'timestamp': datetime.now().isoformat()
                }
                
                # Adicionar ao histórico
                st.session_state.voice_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'command': command_text,
                    'recognized_as': cmd['command'],
                    'success': True,
                    'confidence': cmd['confidence'],
                    'response_time': 1.2
                })
                
                return result
        
        # Comando não reconhecido
        result = {
            'success': False,
            'error': 'Comando não reconhecido',
            'suggestion': 'Tente: "ajuda" para ver comandos disponíveis',
            'timestamp': datetime.now().isoformat()
        }
        
        st.session_state.voice_history.append({
            'timestamp': datetime.now().isoformat(),
            'command': command_text,
            'recognized_as': None,
            'success': False,
            'confidence': 0.0,
            'response_time': 0.8
        })
        
        return result
    
    def text_to_speech_simulation(self, text: str) -> Dict:
        """Simular síntese de voz"""
        settings = st.session_state.voice_settings
        
        # Calcular duração estimada (baseado na velocidade)
        words = len(text.split())
        base_duration = words * 0.6  # 0.6 segundos por palavra
        adjusted_duration = base_duration / settings['speech_rate']
        
        return {
            'text': text,
            'language': settings['language'],
            'voice_gender': settings['voice_gender'],
            'speech_rate': settings['speech_rate'],
            'volume': settings['volume'],
            'estimated_duration': round(adjusted_duration, 1),
            'status': 'ready_to_play'
        }
    
    def get_voice_suggestions(self, context: str = "general") -> List[str]:
        """Obter sugestões de comandos baseadas no contexto"""
        suggestions = {
            'general': [
                "Diga 'ajuda' para ver todos os comandos",
                "Use 'ir para dashboard' para navegar",
                "Fale 'ler questão' para ouvir o conteúdo"
            ],
            'quiz': [
                "Diga 'próxima questão' para avançar",
                "Use 'pausar sessão' para fazer uma pausa",
                "Fale 'ler questão' para ouvir novamente"
            ],
            'dashboard': [
                "Diga 'mostrar desempenho' para ver métricas",
                "Use 'criar plano de estudos' para planejar",
                "Fale 'iniciar simulado' para começar"
            ]
        }
        
        return suggestions.get(context, suggestions['general'])
    
    def render_voice_dashboard(self):
        """Renderizar dashboard do assistente de voz"""
        st.subheader("🎤 Dashboard do Assistente de Voz")
        
        analytics = st.session_state.voice_analytics
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total de Comandos",
                analytics['total_commands'],
                delta="+23 hoje"
            )
        
        with col2:
            st.metric(
                "Taxa de Precisão",
                f"{analytics['accuracy_rate']}%",
                delta="+2.3%"
            )
        
        with col3:
            st.metric(
                "Tempo de Resposta",
                f"{analytics['average_response_time']}s",
                delta="-0.2s"
            )
        
        with col4:
            st.metric(
                "Satisfação",
                f"{analytics['satisfaction_score']}/5.0",
                delta="+0.1"
            )
        
        # Gráficos
        col1, col2 = st.columns(2)
        
        with col1:
            # Comandos mais usados
            most_used = pd.DataFrame(analytics['most_used_commands'])
            fig = px.bar(
                most_used,
                x='count',
                y='command',
                orientation='h',
                title="Comandos Mais Utilizados",
                color='count',
                color_continuous_scale='viridis'
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Uso por tipo
            usage_data = list(analytics['usage_by_type'].items())
            fig = px.pie(
                values=[item[1] for item in usage_data],
                names=[item[0] for item in usage_data],
                title="Distribuição por Tipo de Comando"
            )
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Uso diário
        daily_df = pd.DataFrame(analytics['daily_usage'])
        daily_df['date'] = pd.to_datetime(daily_df['date'])
        
        fig = px.line(
            daily_df,
            x='date',
            y='commands',
            title="Uso Diário do Assistente de Voz",
            markers=True
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
    
    def render_voice_commands(self):
        """Renderizar lista de comandos disponíveis"""
        st.subheader("📋 Comandos Disponíveis")
        
        # Filtros
        col1, col2 = st.columns(2)
        
        with col1:
            command_types = [cmd['type'] for cmd in st.session_state.voice_commands]
            selected_type = st.selectbox(
                "Filtrar por tipo:",
                options=['Todos'] + list(set(command_types)),
                index=0
            )
        
        with col2:
            sort_by = st.selectbox(
                "Ordenar por:",
                options=['Uso', 'Alfabética', 'Confiança'],
                index=0
            )
        
        # Filtrar comandos
        commands = st.session_state.voice_commands
        if selected_type != 'Todos':
            commands = [cmd for cmd in commands if cmd['type'] == selected_type]
        
        # Ordenar comandos
        if sort_by == 'Uso':
            commands = sorted(commands, key=lambda x: x['usage_count'], reverse=True)
        elif sort_by == 'Alfabética':
            commands = sorted(commands, key=lambda x: x['command'])
        elif sort_by == 'Confiança':
            commands = sorted(commands, key=lambda x: x['confidence'], reverse=True)
        
        # Exibir comandos
        for cmd in commands:
            with st.expander(f"🎤 {cmd['command']} (Usado {cmd['usage_count']}x)"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Descrição:** {cmd['description']}")
                    st.write(f"**Tipo:** {cmd['type']}")
                    st.write(f"**Confiança:** {cmd['confidence']:.1%}")
                
                with col2:
                    st.write("**Exemplos de uso:**")
                    for example in cmd['examples']:
                        st.write(f"• {example}")
    
    def render_voice_simulator(self):
        """Renderizar simulador de comandos de voz"""
        st.subheader("🎙️ Simulador de Comandos")
        
        # Interface de simulação
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Input de comando
            command_input = st.text_input(
                "Digite um comando para simular:",
                placeholder="Ex: ler questão, ir para dashboard, mostrar desempenho"
            )
            
            # Botão de processar
            if st.button("🎤 Processar Comando", type="primary"):
                if command_input:
                    with st.spinner("Processando comando..."):
                        time.sleep(1)  # Simular processamento
                        result = self.process_voice_command(command_input)
                        
                        if result['success']:
                            st.success(f"✅ Comando reconhecido: {result['response']}")
                            st.info(f"Confiança: {result['confidence']:.1%}")
                            
                            # Simular síntese de voz
                            tts_result = self.text_to_speech_simulation(result['response'])
                            st.audio("data:audio/wav;base64,UklGRnoGAABXQVZFZm10IBAAAAABAAEAQB8AAEAfAAABAAgAZGF0YQoGAACBhYqFbF1fdJivrJBhNjVgodDbq2EcBj+a2/LDciUFLIHO8tiJNwgZaLvt559NEAxQp+PwtmMcBjiR1/LMeSwFJHfH8N2QQAoUXrTp66hVFApGn+DyvmwhBSuBzvLZiTYIG2m98OScTgwOUarm7blmGgU7k9n1unEiBC13yO/eizEIHWq+8+OWT")
                            st.write(f"🔊 Reproduzindo resposta ({tts_result['estimated_duration']}s)")
                        else:
                            st.error(f"❌ {result['error']}")
                            st.info(f"💡 {result['suggestion']}")
                else:
                    st.warning("Por favor, digite um comando para simular.")
        
        with col2:
            # Sugestões contextuais
            st.write("**💡 Sugestões:**")
            suggestions = self.get_voice_suggestions()
            for suggestion in suggestions:
                st.write(f"• {suggestion}")
    
    def render_voice_history(self):
        """Renderizar histórico de comandos"""
        st.subheader("📜 Histórico de Comandos")
        
        if not st.session_state.voice_history:
            st.info("Nenhum comando executado ainda. Use o simulador para testar!")
            return
        
        # Filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            show_successful = st.checkbox("Mostrar sucessos", value=True)
        
        with col2:
            show_failed = st.checkbox("Mostrar falhas", value=True)
        
        with col3:
            limit = st.selectbox("Mostrar últimos:", [10, 25, 50, 100], index=0)
        
        # Filtrar histórico
        history = st.session_state.voice_history[-limit:]
        
        if not show_successful:
            history = [h for h in history if not h['success']]
        if not show_failed:
            history = [h for h in history if h['success']]
        
        # Exibir histórico
        for i, entry in enumerate(reversed(history)):
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%H:%M:%S")
            
            if entry['success']:
                st.success(
                    f"✅ {timestamp} - '{entry['command']}' → {entry['recognized_as']} "
                    f"(Confiança: {entry['confidence']:.1%}, {entry['response_time']}s)"
                )
            else:
                st.error(
                    f"❌ {timestamp} - '{entry['command']}' → Não reconhecido "
                    f"({entry['response_time']}s)"
                )
    
    def render_voice_settings(self):
        """Renderizar configurações de voz"""
        st.subheader("⚙️ Configurações do Assistente de Voz")
        
        settings = st.session_state.voice_settings
        
        # Configurações gerais
        st.write("**🔧 Configurações Gerais**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['enabled'] = st.checkbox(
                "Assistente de voz ativo",
                value=settings['enabled']
            )
            
            settings['language'] = st.selectbox(
                "Idioma:",
                options=[lang.value for lang in VoiceLanguage],
                index=0
            )
            
            settings['voice_gender'] = st.selectbox(
                "Gênero da voz:",
                options=[gender.value for gender in VoiceGender],
                index=1
            )
        
        with col2:
            settings['speech_rate'] = st.slider(
                "Velocidade da fala:",
                min_value=0.5,
                max_value=2.0,
                value=settings['speech_rate'],
                step=0.1
            )
            
            settings['volume'] = st.slider(
                "Volume:",
                min_value=0.0,
                max_value=1.0,
                value=settings['volume'],
                step=0.1
            )
            
            settings['auto_read'] = st.checkbox(
                "Leitura automática de conteúdo",
                value=settings['auto_read']
            )
        
        # Configurações avançadas
        st.write("**🔬 Configurações Avançadas**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            settings['wake_word'] = st.text_input(
                "Palavra de ativação:",
                value=settings['wake_word']
            )
        
        with col2:
            settings['continuous_listening'] = st.checkbox(
                "Escuta contínua",
                value=settings['continuous_listening']
            )
        
        # Salvar configurações
        if st.button("💾 Salvar Configurações", type="primary"):
            st.session_state.voice_settings = settings
            st.success("✅ Configurações salvas com sucesso!")
        
        # Teste de voz
        st.write("**🧪 Teste de Voz**")
        test_text = st.text_area(
            "Texto para teste:",
            value="Olá! Este é um teste do assistente de voz do Agente Concurseiro."
        )
        
        if st.button("🔊 Testar Síntese de Voz"):
            tts_result = self.text_to_speech_simulation(test_text)
            st.success(f"✅ Teste concluído! Duração estimada: {tts_result['estimated_duration']}s")
            st.json(tts_result)
    
    def render(self):
        """Renderizar componente principal"""
        st.title("🎤 Assistente de Voz Inteligente")
        
        # Verificar se está ativo
        if not st.session_state.voice_settings['enabled']:
            st.warning("⚠️ Assistente de voz desativado. Ative nas configurações.")
        
        # Tabs principais
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 Dashboard",
            "📋 Comandos",
            "🎙️ Simulador",
            "📜 Histórico",
            "⚙️ Configurações",
            "❓ Ajuda"
        ])
        
        with tab1:
            self.render_voice_dashboard()
        
        with tab2:
            self.render_voice_commands()
        
        with tab3:
            self.render_voice_simulator()
        
        with tab4:
            self.render_voice_history()
        
        with tab5:
            self.render_voice_settings()
        
        with tab6:
            st.subheader("❓ Ajuda do Assistente de Voz")
            
            st.markdown("""
            ### 🎤 Como usar o Assistente de Voz
            
            **Comandos Básicos:**
            - **"ler questão"** - Lê a questão atual em voz alta
            - **"próxima questão"** - Avança para a próxima questão
            - **"ir para dashboard"** - Navega para o dashboard
            - **"mostrar desempenho"** - Exibe suas métricas
            - **"pausar sessão"** - Pausa a atividade atual
            
            **Dicas de Uso:**
            - Fale de forma clara e pausada
            - Use a palavra de ativação configurada
            - Aguarde o processamento do comando
            - Verifique o volume e velocidade nas configurações
            
            **Solução de Problemas:**
            - Se o comando não for reconhecido, tente reformular
            - Verifique se o microfone está funcionando
            - Ajuste a sensibilidade nas configurações
            - Use o simulador para testar comandos
            """)

# Função para integração com o sistema principal
def render_voice_assistant():
    """Função para renderizar o assistente de voz"""
    voice_assistant = VoiceAssistant()
    voice_assistant.render()

if __name__ == "__main__":
    render_voice_assistant()