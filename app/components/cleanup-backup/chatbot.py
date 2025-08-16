"""
Chatbot Inteligente - Suporte e FAQ
Sistema de chat para tirar dúvidas e fornecer suporte contextual
"""

import streamlit as st
from datetime import datetime
import random
import re
from typing import List, Dict, Any

class ChatBot:
    """Sistema de chatbot inteligente"""
    
    def __init__(self):
        self.initialize_session_state()
        self.faq_database = self.load_faq_database()
        self.context_responses = self.load_context_responses()
    
    def initialize_session_state(self):
        """Inicializa estado da sessão do chat"""
        if 'chat_messages' not in st.session_state:
            st.session_state.chat_messages = [
                {
                    'role': 'assistant',
                    'content': '👋 Olá! Sou seu assistente virtual do Agente Concurseiro. Como posso ajudá-lo hoje?',
                    'timestamp': datetime.now()
                }
            ]
        
        if 'chat_context' not in st.session_state:
            st.session_state.chat_context = 'geral'
    
    def load_faq_database(self) -> Dict[str, Dict[str, Any]]:
        """Carrega base de conhecimento de FAQ"""
        return {
            'como_usar_sistema': {
                'keywords': ['como usar', 'tutorial', 'começar', 'iniciar'],
                'response': """
                🚀 **Como usar o Agente Concurseiro:**
                
                1. **📊 Dashboard**: Acompanhe seu progresso e estatísticas
                2. **📋 Análise de Edital**: Faça upload do PDF do edital para análise automática
                3. **📋 Plano de Estudos**: Crie um cronograma personalizado baseado no edital
                4. **📝 Redação**: Pratique redações com correção automática
                5. **🎯 Simulados**: Resolva questões e teste seus conhecimentos
                6. **🎮 Gamificação**: Ganhe pontos, badges e acompanhe seu ranking
                
                Precisa de ajuda com alguma funcionalidade específica?
                """,
                'category': 'tutorial'
            },
            'analise_edital': {
                'keywords': ['edital', 'pdf', 'analisar', 'upload', 'arquivo'],
                'response': """
                📋 **Como analisar um edital:**
                
                1. Vá para a aba "📋 Análise de Edital"
                2. Faça upload do arquivo PDF do edital
                3. Selecione os cargos de seu interesse
                4. Clique em "Analisar Edital"
                5. O sistema extrairá automaticamente:
                   - Matérias e número de questões
                   - Datas importantes
                   - Informações sobre vagas
                   - Banca organizadora
                
                ✅ **Formatos suportados**: PDF, DOCX, TXT
                
                Está com problemas no upload? Me conte mais detalhes!
                """,
                'category': 'funcionalidade'
            },
            'plano_estudos': {
                'keywords': ['plano', 'cronograma', 'estudos', 'organizar'],
                'response': """
                📚 **Como criar seu plano de estudos:**
                
                1. Primeiro, analise seu edital na aba correspondente
                2. Vá para "📋 Plano de Estudos"
                3. Configure:
                   - Quantos dias por semana vai estudar
                   - Horas disponíveis por dia
                   - Data da prova
                   - Prioridades por matéria
                
                🎯 **O sistema criará automaticamente:**
                - Distribuição equilibrada das matérias
                - Cronograma com datas específicas
                - Metas diárias e semanais
                - Períodos de revisão
                
                Quer dicas para otimizar seus estudos?
                """,
                'category': 'funcionalidade'
            },
            'gamificacao': {
                'keywords': ['pontos', 'badges', 'ranking', 'conquistas', 'nível'],
                'response': """
                🎮 **Sistema de Gamificação:**
                
                **Como ganhar pontos:**
                - Resolver questões: 10-50 pontos cada
                - Completar simulados: 100-300 pontos
                - Manter sequência de estudos: 50 pontos/dia
                - Conquistar badges: 50-1000 pontos
                
                **Tipos de Badges:**
                - 🥉 **Comum**: Primeiros passos, marcos básicos
                - 🥈 **Raro**: Sequências, dedicação
                - 🥇 **Épico**: Alta performance, desafios
                - 💎 **Lendário**: Conquistas excepcionais
                
                **Benefícios:**
                - Acompanhar progresso de forma divertida
                - Competir com outros usuários
                - Manter motivação alta
                
                Quer saber sobre alguma badge específica?
                """,
                'category': 'funcionalidade'
            },
            'problemas_tecnicos': {
                'keywords': ['erro', 'bug', 'problema', 'não funciona', 'travou'],
                'response': """
                🔧 **Solucionando problemas técnicos:**
                
                **Problemas comuns e soluções:**
                
                1. **Erro no upload de PDF:**
                   - Verifique se o arquivo não está corrompido
                   - Tente converter para PDF novamente
                   - Arquivo muito grande? Comprima-o
                
                2. **Página não carrega:**
                   - Atualize a página (F5)
                   - Limpe o cache do navegador
                   - Tente em modo anônimo
                
                3. **Dados não salvam:**
                   - Verifique sua conexão com internet
                   - Não feche a aba durante processamento
                
                4. **Performance lenta:**
                   - Feche outras abas do navegador
                   - Verifique sua conexão
                
                Se o problema persistir, descreva exatamente o que aconteceu!
                """,
                'category': 'suporte'
            },
            'dicas_estudo': {
                'keywords': ['dicas', 'como estudar', 'método', 'técnica', 'concentração'],
                'response': """
                💡 **Dicas de estudo eficiente:**
                
                **📚 Técnicas comprovadas:**
                - **Pomodoro**: 25min estudo + 5min pausa
                - **Revisão espaçada**: Revise em intervalos crescentes
                - **Mapas mentais**: Visualize conexões entre tópicos
                - **Questões**: Pratique muito, é fundamental!
                
                **🎯 Organização:**
                - Defina metas diárias claras
                - Estude sempre no mesmo horário
                - Tenha um local fixo de estudos
                - Elimine distrações (celular, redes sociais)
                
                **🧠 Otimização mental:**
                - Durma bem (7-8h por noite)
                - Faça exercícios físicos
                - Mantenha alimentação saudável
                - Pratique mindfulness/meditação
                
                Quer dicas específicas para alguma matéria?
                """,
                'category': 'dicas'
            }
        }
    
    def load_context_responses(self) -> Dict[str, str]:
        """Respostas baseadas no contexto atual do usuário"""
        return {
            'dashboard': "Vejo que você está no Dashboard! Quer saber como interpretar suas estatísticas ou como melhorar seu desempenho?",
            'edital': "Está analisando um edital? Posso ajudar com o upload, interpretação dos dados ou criação do plano de estudos!",
            'redacao': "Praticando redação? Tenho dicas sobre estrutura, argumentação e como se adaptar ao estilo de cada banca!",
            'simulados': "Fazendo simulados? Posso dar dicas sobre gestão de tempo, estratégias de resolução e análise de erros!",
            'gamificacao': "Explorando a gamificação? Posso explicar como ganhar mais pontos, conquistar badges e subir no ranking!"
        }
    
    def find_best_response(self, user_message: str) -> str:
        """Encontra a melhor resposta baseada na mensagem do usuário"""
        user_message_lower = user_message.lower()
        
        # Verificar correspondências exatas primeiro
        best_match = None
        max_matches = 0
        
        for faq_id, faq_data in self.faq_database.items():
            matches = 0
            for keyword in faq_data['keywords']:
                if keyword in user_message_lower:
                    matches += 1
            
            if matches > max_matches:
                max_matches = matches
                best_match = faq_data
        
        if best_match and max_matches > 0:
            return best_match['response']
        
        # Se não encontrou correspondência, usar resposta genérica
        return self.generate_generic_response(user_message)
    
    def generate_generic_response(self, user_message: str) -> str:
        """Gera resposta genérica quando não encontra correspondência específica"""
        generic_responses = [
            """
            🤔 Não tenho certeza sobre essa questão específica, mas posso ajudar com:
            
            • **Tutorial do sistema** - Como usar cada funcionalidade
            • **Análise de editais** - Upload e interpretação
            • **Planos de estudo** - Criação e otimização
            • **Dicas de estudo** - Técnicas e métodos eficazes
            • **Problemas técnicos** - Soluções para erros comuns
            • **Gamificação** - Pontos, badges e ranking
            
            Sobre qual desses tópicos você gostaria de saber mais?
            """,
            """
            💭 Interessante! Embora eu não tenha uma resposta específica para isso, posso te ajudar com várias outras coisas:
            
            🎯 **Pergunte sobre:**
            - Como usar o sistema
            - Problemas técnicos
            - Dicas de estudo
            - Funcionalidades específicas
            
            O que mais posso esclarecer para você?
            """,
            """
            🔍 Hmm, não encontrei informações específicas sobre isso. Mas estou aqui para ajudar!
            
            **Tente perguntar:**
            - "Como analisar um edital?"
            - "Como criar plano de estudos?"
            - "Estou com erro no sistema"
            - "Dicas para estudar melhor"
            
            Qual dessas opções te interessa?
            """
        ]
        
        return random.choice(generic_responses)
    
    def add_message(self, role: str, content: str):
        """Adiciona mensagem ao histórico do chat"""
        st.session_state.chat_messages.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now()
        })
    
    def render_chat_message(self, message: Dict[str, Any]):
        """Renderiza uma mensagem do chat"""
        is_user = message['role'] == 'user'
        
        # Container da mensagem
        with st.container():
            if is_user:
                # Mensagem do usuário (direita)
                col1, col2 = st.columns([1, 4])
                with col2:
                    st.markdown(f"""
                    <div style="background-color: #007bff; color: white; padding: 10px; border-radius: 15px; margin: 5px 0; text-align: right;">
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
            else:
                # Mensagem do assistente (esquerda)
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"""
                    <div style="background-color: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; border-radius: 15px; margin: 5px 0;">
                        {message['content']}
                    </div>
                    """, unsafe_allow_html=True)
    
    def render_quick_actions(self):
        """Renderiza botões de ações rápidas"""
        st.markdown("**🚀 Perguntas rápidas:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📋 Como analisar edital?", key="quick_edital"):
                self.add_message('user', 'Como analisar edital?')
                response = self.find_best_response('Como analisar edital?')
                self.add_message('assistant', response)
                st.rerun()
        
        with col2:
            if st.button("📚 Dicas de estudo", key="quick_dicas"):
                self.add_message('user', 'Dicas de estudo')
                response = self.find_best_response('Dicas de estudo')
                self.add_message('assistant', response)
                st.rerun()
        
        with col3:
            if st.button("🎮 Como ganhar pontos?", key="quick_pontos"):
                self.add_message('user', 'Como ganhar pontos?')
                response = self.find_best_response('Como ganhar pontos?')
                self.add_message('assistant', response)
                st.rerun()
    
    def render_chat_interface(self):
        """Renderiza interface completa do chat"""
        st.title("🤖 Assistente Virtual")
        st.markdown("Tire suas dúvidas sobre o sistema e receba dicas de estudo!")
        
        # Container do histórico de mensagens
        chat_container = st.container()
        
        with chat_container:
            # Renderizar mensagens existentes
            for message in st.session_state.chat_messages:
                self.render_chat_message(message)
        
        st.divider()
        
        # Ações rápidas
        self.render_quick_actions()
        
        st.divider()
        
        # Input para nova mensagem
        with st.form("chat_form", clear_on_submit=True):
            col1, col2 = st.columns([4, 1])
            
            with col1:
                user_input = st.text_input(
                    "Digite sua pergunta:",
                    placeholder="Ex: Como criar um plano de estudos?",
                    label_visibility="collapsed"
                )
            
            with col2:
                submit_button = st.form_submit_button("Enviar", use_container_width=True)
            
            if submit_button and user_input:
                # Adicionar mensagem do usuário
                self.add_message('user', user_input)
                
                # Gerar resposta
                response = self.find_best_response(user_input)
                self.add_message('assistant', response)
                
                # Recarregar para mostrar novas mensagens
                st.rerun()
        
        # Botão para limpar chat
        if st.button("🗑️ Limpar Conversa", type="secondary"):
            st.session_state.chat_messages = [
                {
                    'role': 'assistant',
                    'content': '👋 Conversa limpa! Como posso ajudá-lo agora?',
                    'timestamp': datetime.now()
                }
            ]
            st.rerun()
        
        # Estatísticas do chat
        st.sidebar.markdown("### 📊 Estatísticas do Chat")
        total_messages = len(st.session_state.chat_messages)
        user_messages = len([m for m in st.session_state.chat_messages if m['role'] == 'user'])
        
        st.sidebar.metric("Total de mensagens", total_messages)
        st.sidebar.metric("Suas perguntas", user_messages)
        
        # Feedback
        st.sidebar.markdown("### 💬 Feedback")
        if st.sidebar.button("👍 Chat útil"):
            st.sidebar.success("Obrigado pelo feedback!")
        if st.sidebar.button("👎 Precisa melhorar"):
            st.sidebar.info("Vamos trabalhar para melhorar!")
