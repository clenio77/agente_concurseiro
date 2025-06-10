import streamlit as st
import os
import asyncio
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Imports da aplicação
from crew import run_crew
from utils.dashboard import render_dashboard
from utils.config import load_config
from pages.simulado import render_simulado_page
from pages.analytics import render_analytics_page
from pages.redacao import render_redacao_page

# Imports de produção
from db.database import init_database, db_manager
from auth.auth_manager import auth_manager
from monitoring.metrics import setup_monitoring, track_business_event
from backup.backup_manager import backup_manager, schedule_backups

# Load configuration
config = load_config()

# Inicializar sistema de produção
@st.cache_resource
def initialize_production_systems():
    """Inicializa sistemas de produção"""
    logger.info("🚀 Inicializando sistemas de produção...")

    try:
        # Inicializar banco de dados
        if not init_database():
            st.error("❌ Falha na inicialização do banco de dados")
            st.stop()

        # Configurar monitoramento
        setup_monitoring()

        # Agendar backups
        schedule_backups()

        logger.info("✅ Sistemas de produção inicializados")
        return True

    except Exception as e:
        logger.error(f"❌ Erro na inicialização: {e}")
        st.error(f"Erro na inicialização do sistema: {e}")
        st.stop()

# Inicializar sistemas
if os.getenv("ENVIRONMENT") == "production":
    initialize_production_systems()

st.set_page_config(
    page_title="Assistente de Preparação para Concursos",
    page_icon="📚",
    layout="wide"
)

# Inicializar estado da sessão
if 'user_authenticated' not in st.session_state:
    st.session_state.user_authenticated = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'auth_token' not in st.session_state:
    st.session_state.auth_token = None

# Função para autenticação robusta
def authenticate_user(email_or_username: str, password: str) -> bool:
    """Autentica usuário usando sistema robusto"""
    try:
        # Obter IP do cliente (simulado no Streamlit)
        client_ip = "127.0.0.1"  # Em produção, seria obtido do request

        result = auth_manager.authenticate_user(email_or_username, password, client_ip)

        if result["success"]:
            st.session_state.user_authenticated = True
            st.session_state.current_user = result["user"]["username"]
            st.session_state.auth_token = result["access_token"]
            st.session_state.user_data = result["user"]

            # Registrar evento de negócio
            track_business_event("user_login", username=result["user"]["username"])

            return True
        else:
            st.error(f"❌ {result['error']}")
            return False

    except Exception as e:
        st.error(f"❌ Erro na autenticação: {e}")
        return False

def register_user(email: str, username: str, password: str, full_name: str = None) -> bool:
    """Registra novo usuário"""
    try:
        result = auth_manager.create_user(
            email=email,
            username=username,
            password=password,
            full_name=full_name
        )

        if result["success"]:
            st.success("✅ Usuário criado com sucesso! Faça login para continuar.")

            # Registrar evento de negócio
            track_business_event("user_registered", username=username)

            return True
        else:
            st.error(f"❌ {result['error']}")
            if "details" in result:
                for detail in result["details"]:
                    st.error(f"• {detail}")
            return False

    except Exception as e:
        st.error(f"❌ Erro no registro: {e}")
        return False

# Sidebar for navigation
st.sidebar.title("🎓 Agente Concurseiro")

# Sistema de autenticação robusto
if not st.session_state.user_authenticated:
    st.sidebar.subheader("🔐 Acesso ao Sistema")

    # Tabs para login e registro
    auth_tab = st.sidebar.radio("", ["Login", "Criar Conta"], horizontal=True)

    if auth_tab == "Login":
        with st.sidebar.form("login_form"):
            st.markdown("**Fazer Login**")
            email_or_username = st.text_input("Email ou Usuário")
            password = st.text_input("Senha", type="password")

            if st.form_submit_button("🚀 Entrar", use_container_width=True):
                if email_or_username and password:
                    if authenticate_user(email_or_username, password):
                        st.experimental_rerun()
                else:
                    st.error("Preencha todos os campos")

    else:  # Criar Conta
        with st.sidebar.form("register_form"):
            st.markdown("**Criar Nova Conta**")
            email = st.text_input("Email")
            username = st.text_input("Nome de Usuário")
            full_name = st.text_input("Nome Completo")
            password = st.text_input("Senha", type="password")
            confirm_password = st.text_input("Confirmar Senha", type="password")

            if st.form_submit_button("📝 Criar Conta", use_container_width=True):
                if email and username and password and confirm_password:
                    if password != confirm_password:
                        st.error("Senhas não coincidem")
                    else:
                        register_user(email, username, password, full_name)
                else:
                    st.error("Preencha todos os campos obrigatórios")

    # Mostrar apenas página de login
    st.title("🎓 Assistente de Preparação para Concursos")
    st.markdown("""
    ### Bem-vindo ao seu assistente pessoal de estudos!

    **Funcionalidades disponíveis:**
    - 📊 Dashboard personalizado com acompanhamento de progresso
    - 📝 Geração inteligente de planos de estudo
    - 🎯 Simulados adaptativos baseados em bancas específicas
    - ✍️ Avaliação automática de redações
    - 📚 Recomendações personalizadas de materiais
    - 🔄 Sistema de repetição espaçada para memorização

    **Faça login para começar seus estudos!**
    """)

    st.info("💡 **Dica:** Use qualquer usuário e senha para acessar o sistema de demonstração.")

else:
    # Usuário autenticado - mostrar navegação completa
    st.sidebar.success(f"👤 {st.session_state.current_user}")

    if st.sidebar.button("Sair"):
        st.session_state.user_authenticated = False
        st.session_state.current_user = None
        st.experimental_rerun()

    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "📋 Navegação:",
        ["Dashboard", "Plano de Estudos", "Simulados", "Analytics", "Materiais", "Redação", "Configurações"]
    )

    if page == "Dashboard":
        render_dashboard()

    elif page == "Plano de Estudos":
        st.title("📝 Gerador de Plano de Estudos")

        # Formulário para criação de plano
        with st.form("study_plan_form"):
            col1, col2 = st.columns(2)

            with col1:
                cargo = st.text_input("🎯 Cargo", placeholder="Ex: Analista Judiciário")
                concurso = st.text_input("🏛️ Concurso", placeholder="Ex: TRF 1ª Região")
                banca = st.selectbox("📋 Banca", ["CESPE", "FCC", "VUNESP", "FGV", "IBFC"])

            with col2:
                cidade = st.text_input("🌍 Cidade", placeholder="Ex: Brasília")
                study_hours = st.number_input("⏰ Horas de Estudo Semanais", min_value=5, max_value=60, value=20)
                study_months = st.number_input("📅 Duração do Estudo (Meses)", min_value=1, max_value=24, value=6)

            # Opções avançadas
            with st.expander("⚙️ Opções Avançadas"):
                nivel_conhecimento = st.select_slider(
                    "Nível de Conhecimento Atual",
                    options=["Iniciante", "Básico", "Intermediário", "Avançado"],
                    value="Básico"
                )

                materias_foco = st.multiselect(
                    "Matérias de Maior Interesse",
                    ["Português", "Matemática", "Direito Constitucional", "Direito Administrativo",
                     "Informática", "Conhecimentos Específicos", "Atualidades"],
                    default=["Português", "Direito Constitucional"]
                )

                disponibilidade = st.selectbox(
                    "Disponibilidade de Estudo",
                    ["Manhã", "Tarde", "Noite", "Fins de Semana", "Flexível"]
                )

            submitted = st.form_submit_button("🚀 Gerar Plano de Estudos", use_container_width=True)

            if submitted:
                if cargo and concurso and banca and cidade:
                    with st.spinner("🔄 Gerando seu plano personalizado..."):
                        try:
                            result = run_crew(cargo, concurso, banca, cidade, study_hours, study_months)

                            # Exibir resultados
                            st.success("✅ Plano gerado com sucesso!")

                            # Tabs para organizar resultados
                            tab1, tab2, tab3, tab4 = st.tabs(["📊 Plano de Estudos", "🎯 Simulado", "🔄 Repetição Espaçada", "📈 Previsão de Desempenho"])

                            with tab1:
                                st.subheader("📊 Seu Plano de Estudos Personalizado")
                                try:
                                    import json
                                    plan_data = json.loads(result['study_plan']) if isinstance(result['study_plan'], str) else result['study_plan']

                                    # Mostrar resumo
                                    if 'metadata' in plan_data:
                                        metadata = plan_data['metadata']
                                        col1, col2, col3 = st.columns(3)
                                        col1.metric("📅 Semanas Totais", metadata.get('total_weeks', 'N/A'))
                                        col2.metric("⏰ Horas/Semana", metadata.get('study_hours_per_week', 'N/A'))
                                        col3.metric("🎯 Banca", metadata.get('banca', 'N/A'))

                                    st.json(plan_data)
                                except:
                                    st.text(result['study_plan'])

                            with tab2:
                                st.subheader("🎯 Simulado Gerado")
                                st.text_area("Questões do Simulado", result['mock_exam'], height=300)

                            with tab3:
                                st.subheader("🔄 Plano de Repetição Espaçada")
                                try:
                                    spaced_data = json.loads(result['spaced_repetition_plan']) if isinstance(result['spaced_repetition_plan'], str) else result['spaced_repetition_plan']
                                    st.json(spaced_data)
                                except:
                                    st.text(result['spaced_repetition_plan'])

                            with tab4:
                                st.subheader("📈 Previsão de Desempenho")
                                try:
                                    prediction_data = json.loads(result['performance_prediction']) if isinstance(result['performance_prediction'], str) else result['performance_prediction']
                                    st.json(prediction_data)
                                except:
                                    st.text(result['performance_prediction'])

                        except Exception as e:
                            st.error(f"❌ Erro ao gerar plano: {str(e)}")
                            st.info("💡 Tente novamente ou verifique os dados inseridos.")
                else:
                    st.error("❌ Preencha todos os campos obrigatórios.")

    elif page == "Simulados":
        render_simulado_page()

    elif page == "Analytics":
        render_analytics_page()

    elif page == "Materiais":
        st.title("📚 Materiais de Estudo")
        st.info("🚧 Página em desenvolvimento. Em breve você terá acesso a:")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **📖 Biblioteca Digital:**
            - PDFs de provas anteriores
            - Apostilas organizadas por matéria
            - Resumos e mapas mentais
            - Legislação atualizada
            """)

        with col2:
            st.markdown("""
            **🎥 Conteúdo Multimídia:**
            - Videoaulas recomendadas
            - Podcasts educacionais
            - Infográficos interativos
            - Exercícios práticos
            """)

    elif page == "Redação":
        render_redacao_page()

    elif page == "Configurações":
        st.title("⚙️ Configurações")

        # Configurações do usuário
        st.subheader("👤 Perfil do Usuário")

        col1, col2 = st.columns(2)
        with col1:
            nome_completo = st.text_input("Nome Completo", value=st.session_state.current_user)
            email = st.text_input("Email", placeholder="seu@email.com")
            telefone = st.text_input("Telefone", placeholder="(11) 99999-9999")

        with col2:
            concurso_interesse = st.selectbox("Concurso de Interesse Principal",
                                            ["TRF", "STJ", "Polícia Federal", "Receita Federal", "Outro"])
            nivel_escolaridade = st.selectbox("Escolaridade",
                                            ["Ensino Médio", "Superior Incompleto", "Superior Completo", "Pós-graduação"])
            experiencia_concursos = st.selectbox("Experiência com Concursos",
                                                ["Primeira vez", "Já fiz alguns", "Experiente"])

        # Configurações de estudo
        st.subheader("📚 Preferências de Estudo")

        col1, col2 = st.columns(2)
        with col1:
            horario_preferido = st.multiselect("Horários Preferidos",
                                             ["Manhã (6h-12h)", "Tarde (12h-18h)", "Noite (18h-24h)"],
                                             default=["Manhã (6h-12h)"])
            dias_estudo = st.multiselect("Dias da Semana para Estudo",
                                       ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"],
                                       default=["Segunda", "Terça", "Quarta", "Quinta", "Sexta"])

        with col2:
            meta_horas_dia = st.number_input("Meta de Horas por Dia", min_value=1, max_value=12, value=3)
            tipo_notificacao = st.selectbox("Notificações",
                                          ["Email", "Push", "Ambos", "Desabilitado"])
            tema_interface = st.selectbox("Tema da Interface", ["Claro", "Escuro", "Automático"])

        # Configurações avançadas
        with st.expander("🔧 Configurações Avançadas"):
            auto_save = st.checkbox("Salvamento Automático", value=True)
            analytics = st.checkbox("Permitir Analytics", value=True)
            backup_cloud = st.checkbox("Backup na Nuvem", value=False)

            st.markdown("**🔄 Sincronização:**")
            sync_google = st.checkbox("Google Calendar")
            sync_outlook = st.checkbox("Outlook Calendar")
            sync_notion = st.checkbox("Notion")

        if st.button("💾 Salvar Configurações", use_container_width=True):
            st.success("✅ Configurações salvas com sucesso!")
            st.info("💡 Algumas alterações podem exigir reinicialização da aplicação.")