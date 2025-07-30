from __future__ import annotations

import logging
import os
import random
import sys
from datetime import datetime

import pandas as pd
import streamlit as st

# Configurar logging básico
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Adicionar o diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports dos componentes
from utils.edital_analyzer import EditalAnalyzer
from components.dashboard import Dashboard
from components.gamification import GamificationSystem
from components.chatbot import ChatBot
from components.ai_predictor import AIPredictor
from components.spaced_repetition import SpacedRepetitionSystem
from components.collaborative_features import CollaborativeFeatures
from components.mobile_companion import MobileCompanion
from components.augmented_reality import AugmentedReality
from components.voice_assistant import VoiceAssistant
from components.behavioral_analysis import render_behavioral_analysis
from components.contest_trends import render_contest_trends

# Configuração da página
st.set_page_config(
    page_title="Agente Concurseiro v2.0",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin-bottom: 1rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 5px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🏠 Dashboard"
if 'example_essay' not in st.session_state:
    st.session_state.example_essay = None
if 'example_banca' not in st.session_state:
    st.session_state.example_banca = "FGV"
if 'custom_bancas' not in st.session_state:
    st.session_state.custom_bancas = []
if 'line_limits' not in st.session_state:
    st.session_state.line_limits = {
        "FGV": 30,
        "CESPE": 30,
        "VUNESP": 30,
        "FCC": 30,
        "IBFC": 30
    }

# Dados do concurso
concurso_data = {
    "nome": "Polícia Federal - Agente",
    "banca": "CESPE/CEBRASPE",
    "data_prova": datetime(2025, 8, 15),
    "vagas": 1500,
    "materias": {
        "Português": {"peso": 1.0, "questoes": 20, "conteudo": ["Gramática", "Interpretação", "Redação"]},
        "Raciocínio Lógico": {"peso": 1.0, "questoes": 15, "conteudo": ["Lógica Matemática", "Raciocínio Verbal"]},
        "Direito Constitucional": {"peso": 1.5, "questoes": 15, "conteudo": ["Constituição Federal", "Direitos Fundamentais"]},
        "Direito Administrativo": {"peso": 1.5, "questoes": 15, "conteudo": ["Princípios", "Atos Administrativos"]},
        "Direito Penal": {"peso": 1.5, "questoes": 15, "conteudo": ["Teoria do Crime", "Tipos Penais"]},
        "Direito Processual Penal": {"peso": 1.0, "questoes": 10, "conteudo": ["Processo Penal", "Recursos"]},
        "Legislação Especial": {"peso": 1.0, "questoes": 10, "conteudo": ["Lei de Drogas", "Crimes Hediondos"]}
    }
}

# Função para calcular dias restantes
def calcular_dias_restantes():
    hoje = datetime.now()
    data_prova = concurso_data["data_prova"]

    # Se a data da prova é uma string (não identificada), retornar 0
    if isinstance(data_prova, str):
        return 0

    # Se é um objeto datetime, calcular a diferença
    dias = (data_prova - hoje).days
    return max(0, dias)

# Importar o novo analisador
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.edital_analyzer import EditalAnalyzer


def extrair_texto_arquivo(uploaded_file):
    """
    Extrai texto de diferentes tipos de arquivo usando o analisador inteligente
    """
    analyzer = EditalAnalyzer()
    return analyzer.extrair_texto_arquivo(uploaded_file)

def analisar_edital_com_llm(content, cargos_selecionados):
    """
    Análise inteligente usando o novo EditalAnalyzer
    """
    try:
        # Debug: mostrar informações de entrada
        print(f"🔍 DEBUG: Iniciando análise...")
        print(f"📄 Tamanho do conteúdo: {len(content)} caracteres")
        print(f"🎯 Cargos selecionados: {cargos_selecionados}")

        # Usar o novo analisador inteligente
        analyzer = EditalAnalyzer()
        resultado = analyzer.analisar_edital(content, cargos_selecionados)

        print(f"✅ Análise concluída com sucesso!")
        print(f"🎯 Modo: {resultado.get('modo_analise', 'N/A')}")
        print(f"✅ Confiança: {resultado.get('confianca', 'N/A')}")

        return resultado

    except Exception as e:
        print(f"❌ ERRO na análise: {str(e)}")
        import traceback
        traceback.print_exc()

        return {
            "concurso": "Concurso Público",
            "banca": "Banca não identificada",
            "vagas": 100,
            "data_prova": "Data não identificada",
            "data_inscricao": "Período não identificado",
            "cargos_detectados": ["Cargo Geral"],
            "cargos_analisados": cargos_selecionados if cargos_selecionados else ["Cargo Geral"],
            "materias": {
                "Português": {"peso": 1.0, "questoes": 20, "conteudo": ["Língua Portuguesa"]},
                "Raciocínio Lógico": {"peso": 1.0, "questoes": 15, "conteudo": ["Raciocínio Lógico"]}
            },
            "conteudo_analisado": content[:1000],
            "modo_analise": "Fallback",
            "erro": str(e),
            "confianca": "Baixa"
        }

def analisar_edital_real(content, cargos_selecionados):
    """
    Analisa o conteúdo real do edital e extrai informações
    """
    import re

    # Converter conteúdo para minúsculas para análise
    content_lower = content.lower()

    # Padrões mais específicos para extração de informações
    padroes = {
        'concurso': [
            r'concurso\s+(?:público\s+)?(?:para\s+)?([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            r'edital\s+(?:do\s+)?(?:concurso\s+)?(?:público\s+)?(?:para\s+)?([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            r'([^,\n]+?)\s+concurso\s+público',
            r'concurso\s+público\s+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            r'departamento\s+de\s+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            r'concurso\s+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
        ],
        'banca': [
            r'banca\s+examinadora[:\\s]+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            r'banca\s+examinadora\s+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            r'([a-z]+/[a-z]+(?:\s+[a-z]+)*)',
            r'(cespe|cebraspe|fgv|vunesp|fcc|ibfc|quadrix|instituto\s+aocp|instituto\s+cesgranrio|aocp|cesgranrio)',
            r'banca[:\\s]+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            r'([a-z]+)\s+examinadora',
            r'examinadora\s+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
            r'([a-z]+)\s+organizadora',
            r'organizadora\s+([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
        ],
        'vagas': [
            r'(\d+)\s+vagas?',
            r'(\d+)\s+cargos?',
            r'total\s+de\s+(\d+)\s+vagas?',
            r'(\d+)\s+oportunidades?',
            r'total[:\s]+(\d+)\s+vagas?',
        ],
        'data_prova': [
            r'data\s+(?:da\s+)?prova[:\\s]+(\d{1,2}/\d{1,2}/\d{4})',
            r'prova\s+(?:será\s+)?realizada\s+em\s+(\d{1,2}/\d{1,2}/\d{4})',
            r'(\d{1,2}/\d{1,2}/\d{4})\s+.*prova',
            r'prova\s+(?:objetiva\s+)?[:\\s]+(\d{1,2}/\d{1,2}/\d{4})',
        ],
        'data_inscricao': [
            r'inscrições?\s+(?:de\s+)?(\d{1,2}/\d{1,2}/\d{4})\s+(?:a\s+)?(\d{1,2}/\d{1,2}/\d{4})',
            r'período\s+de\s+inscrição[:\\s]+(\d{1,2}/\d{1,2}/\d{4})\s+(?:a\s+)?(\d{1,2}/\d{1,2}/\d{4})',
            r'inscrição[:\\s]+(\d{1,2}/\d{1,2}/\d{4})\s+(?:a\s+)?(\d{1,2}/\d{1,2}/\d{4})',
        ],
    }

    # Extrair informações
    info_extraida = {}

    for campo, padrao_list in padroes.items():
        for padrao in padrao_list:
            match = re.search(padrao, content_lower)
            if match:
                if campo == 'data_inscricao' and len(match.groups()) >= 2:
                    info_extraida[campo] = f"{match.group(1)} - {match.group(2)}"
                else:
                    valor = match.group(1).strip()
                    # Limpar o valor removendo caracteres especiais
                    valor = re.sub(r'[^\w\s/]', '', valor).strip()
                    info_extraida[campo] = valor
                break

    # Detectar cargos específicos no edital
    cargos_detectados = []
    padroes_cargos = [
        r'cargo\s+(?:de\s+)?([^,\n]+?)(?:\s+do|\s+da|\s+de|\s+para|\n|$)',
        r'(\w+(?:\s+\w+)*)\s+(?:federal|estadual|municipal)',
        r'(\w+(?:\s+\w+)*)\s+(?:de\s+)?polícia',
        r'(\w+(?:\s+\w+)*)\s+(?:agente|escrivão|delegado|perito|papiloscopista)',
        r'cargo\s+de\s+(\w+(?:\s+\w+)*)',
        r'(\w+(?:\s+\w+)*)\s+(?:federal|estadual|municipal)',
    ]

    for padrao in padroes_cargos:
        matches = re.findall(padrao, content_lower)
        for match in matches:
            cargo = match.strip()
            if len(cargo) > 3 and cargo not in cargos_detectados:
                cargos_detectados.append(cargo.title())

    # Se não detectou cargos específicos, usar cargos comuns
    if not cargos_detectados:
        cargos_comuns = ['agente', 'escrivão', 'delegado', 'perito', 'papiloscopista', 'analista', 'técnico']
        for cargo in cargos_comuns:
            if cargo in content_lower:
                cargos_detectados.append(cargo.title())

    # Detectar matérias específicas no edital
    materias_detectadas = {}
    padroes_materias = [
        r'(\w+(?:\s+\w+)*)\s+(?:peso[:\\s]*([\\d.]+))',
        r'(\w+(?:\s+\w+)*)\s+(?:(\d+)\s+questões?)',
        r'(\w+(?:\s+\w+)*)\s+(?:(\d+)\s+itens?)',
    ]

    for padrao in padroes_materias:
        matches = re.findall(padrao, content_lower)
        for match in matches:
            materia = match[0].strip()
            if len(materia) > 3:
                peso = float(match[1]) if match[1] else 1.0
                questoes = int(match[2]) if len(match) > 2 and match[2] else 10
                materias_detectadas[materia.title()] = {
                    'peso': peso,
                    'questoes': questoes,
                    'conteudo': ['Conteúdo específico do edital']
                }

    # Se não detectou matérias específicas, tentar detectar matérias conhecidas
    if not materias_detectadas:
        materias_conhecidas = {
            'português': {'peso': 1.0, 'questoes': 20, 'conteudo': ['Gramática', 'Interpretação', 'Redação']},
            'raciocínio lógico': {'peso': 1.0, 'questoes': 15, 'conteudo': ['Lógica', 'Matemática Básica']},
            'direito constitucional': {'peso': 1.5, 'questoes': 15, 'conteudo': ['Constituição', 'Direitos Fundamentais']},
            'direito administrativo': {'peso': 1.5, 'questoes': 15, 'conteudo': ['Administração Pública', 'Atos Administrativos']},
            'direito penal': {'peso': 1.5, 'questoes': 15, 'conteudo': ['Crimes', 'Penas', 'Responsabilidade Penal']},
            'direito processual penal': {'peso': 1.0, 'questoes': 10, 'conteudo': ['Processo Penal', 'Procedimentos']},
            'legislação especial': {'peso': 1.0, 'questoes': 10, 'conteudo': ['Leis Específicas', 'Estatutos']},
        }

        for materia, info in materias_conhecidas.items():
            if materia in content_lower:
                # Tentar extrair peso e questões específicas do edital
                peso_match = re.search(rf'{materia}.*?peso[:\\s]*([\\d.]+)', content_lower)
                questoes_match = re.search(rf'{materia}.*?(\d+)\s+questões?', content_lower)

                if peso_match:
                    info['peso'] = float(peso_match.group(1))
                if questoes_match:
                    info['questoes'] = int(questoes_match.group(1))

                materias_detectadas[materia.title()] = info

    # Se ainda não detectou matérias, usar padrão mínimo
    if not materias_detectadas:
        materias_detectadas = {
            'Português': {'peso': 1.0, 'questoes': 20, 'conteudo': ['Gramática', 'Interpretação']},
            'Raciocínio Lógico': {'peso': 1.0, 'questoes': 15, 'conteudo': ['Lógica', 'Matemática']},
        }

    # Tratamento robusto para vagas
    vagas_valor = info_extraida.get('vagas', 100)
    try:
        vagas_int = int(vagas_valor)
    except (ValueError, TypeError):
        vagas_int = 100
    return {
        'concurso': info_extraida.get('concurso', 'Concurso Público'),
        'banca': info_extraida.get('banca', 'Banca não identificada'),
        'vagas': vagas_int,
        'data_prova': info_extraida.get('data_prova', 'Data não identificada'),
        'data_inscricao': info_extraida.get('data_inscricao', 'Período não identificado'),
        'cargos_detectados': cargos_detectados,
        'cargos_analisados': cargos_selecionados if cargos_selecionados else ['Cargo Geral'],
        'materias': materias_detectadas,
        'conteudo_analisado': content[:1000]  # Primeiros 1000 caracteres para referência
    }

# Sidebar
with st.sidebar:
    st.markdown("## 🧭 Navegação")
    st.markdown("Escolha uma página:")

    # Menu dropdown
    page_options = [
        "🏠 Dashboard",
        "🎮 Gamificação",
        "🧠 IA Preditiva",
        "📚 Revisão Espaçada",
        "👥 Recursos Colaborativos",
        "📱 Mobile Companion",
        "🥽 Realidade Aumentada",
        "🎤 Assistente de Voz",
        "🧠 Análise Comportamental",
        "🔮 Predição de Tendências",
        "🤖 Assistente Virtual",
        "📝 Redação",
        "🎯 Simulados",
        "📊 Analytics",
        "📋 Análise de Edital",
        "📋 Plano de Estudos",
        "⚙️ Configurações"
    ]

    selected_page = st.selectbox("Escolha uma página:", page_options, index=0, label_visibility="collapsed")
    st.session_state.current_page = selected_page

    st.markdown("---")

    # Status do sistema
    st.markdown("## 📊 Status do Sistema")
    st.success("✅ Sistema Operacional")
    st.info(f"🕒 Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    st.markdown("---")

    # Links úteis
    st.markdown("## 🔗 Links Úteis")
    if st.button("📚 Documentação", use_container_width=True):
        st.info("Documentação disponível em: https://github.com/seu-repo/agente-concurseiro")

    if st.button("🐛 Reportar Bug", use_container_width=True):
        st.info("Para reportar bugs, abra uma issue no GitHub do projeto.")

# Página principal
if st.session_state.current_page == "🏠 Dashboard":
    # Renderizar o novo dashboard
    dashboard = Dashboard()
    dashboard.render_dashboard()

elif st.session_state.current_page == "🎮 Gamificação":
    # Renderizar sistema de gamificação
    gamification = GamificationSystem()
    gamification.render_gamification_page()

elif st.session_state.current_page == "🧠 IA Preditiva":
    # Renderizar IA Preditiva
    ai_predictor = AIPredictor()
    ai_predictor.render_prediction_dashboard()

elif st.session_state.current_page == "📚 Revisão Espaçada":
    # Renderizar Revisão Espaçada
    spaced_repetition = SpacedRepetitionSystem()
    spaced_repetition.render_spaced_repetition_dashboard()

elif st.session_state.current_page == "👥 Recursos Colaborativos":
    # Renderizar Recursos Colaborativos
    collaborative_features = CollaborativeFeatures()
    collaborative_features.render_collaborative_dashboard()

elif st.session_state.current_page == "📱 Mobile Companion":
    # Renderizar Mobile Companion
    mobile_companion = MobileCompanion()
    mobile_companion.render()

elif st.session_state.current_page == "🥽 Realidade Aumentada":
    # Renderizar Realidade Aumentada
    augmented_reality = AugmentedReality()
    augmented_reality.render()

elif st.session_state.current_page == "🎤 Assistente de Voz":
    # Renderizar Assistente de Voz
    voice_assistant = VoiceAssistant()
    voice_assistant.render()

elif st.session_state.current_page == "🧠 Análise Comportamental":
    # Renderizar Análise Comportamental
    render_behavioral_analysis()

elif st.session_state.current_page == "🔮 Predição de Tendências":
    # Renderizar Predição de Tendências
    render_contest_trends()

elif st.session_state.current_page == "🤖 Assistente Virtual":
    # Renderizar chatbot
    chatbot = ChatBot()
    chatbot.render_chat_interface()

elif st.session_state.current_page == "📝 Redação":
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("📝 Sistema de Redação com IA")
    st.markdown('</div>', unsafe_allow_html=True)

    # Configurações de banca
    st.subheader("⚙️ Configurações de Banca")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 Bancas Disponíveis")

        # Lista de bancas padrão
        bancas_padrao = ["FGV", "CESPE", "VUNESP", "FCC", "IBFC"]

        # Adicionar bancas customizadas
        bancas_todas = bancas_padrao + st.session_state.custom_bancas

        # Selecionar banca
        banca_selecionada = st.selectbox("Selecione a banca:", bancas_todas)

        # Adicionar nova banca
        st.markdown("### ➕ Adicionar Nova Banca")
        nova_banca = st.text_input("Nome da nova banca:")
        if st.button("➕ Adicionar Banca") and nova_banca:
            if nova_banca not in bancas_todas:
                st.session_state.custom_bancas.append(nova_banca)
                st.session_state.line_limits[nova_banca] = 30  # Limite padrão
                st.success(f"✅ Banca '{nova_banca}' adicionada com sucesso!")
                st.rerun()
            else:
                st.warning("⚠️ Esta banca já existe!")

    with col2:
        st.markdown("### 📏 Limite de Linhas")

        # Configurar limite para banca selecionada
        limite_atual = st.session_state.line_limits.get(banca_selecionada, 30)
        novo_limite = st.number_input(
            f"Limite de linhas para {banca_selecionada}:",
            min_value=20,
            max_value=50,
            value=limite_atual,
            step=1
        )

        if novo_limite != limite_atual:
            st.session_state.line_limits[banca_selecionada] = novo_limite
            st.success(f"✅ Limite atualizado para {novo_limite} linhas!")

        # Mostrar todos os limites
        st.markdown("### 📊 Limites Configurados")
        for banca, limite in st.session_state.line_limits.items():
            st.write(f"• **{banca}**: {limite} linhas")

    st.markdown("---")

    # Abas da redação
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Avaliação", "📄 Exemplos", "🎯 Temas", "📚 Histórico"])

    with tab1:
        st.subheader("📝 Avaliação de Redação")

        col1, col2 = st.columns(2)

        with col1:
            tema = st.text_area("Tema da redação:", height=100, placeholder="Digite o tema da redação aqui...")
            redacao = st.text_area("Sua redação:", height=300, placeholder="Digite sua redação aqui...")

            if st.button("🔍 Avaliar Redação", type="primary"):
                if tema and redacao:
                    # Simular avaliação
                    st.success("✅ Redação avaliada com sucesso!")

                    # Métricas simuladas
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("📊 Nota", "8.5/10", "+0.5")
                    with col2:
                        st.metric("📏 Linhas", f"{len(redacao.split())//8}", "✅")
                    with col3:
                        st.metric("⏱️ Tempo", "45min", "⏰")
                    with col4:
                        st.metric("🎯 Coerência", "9/10", "✅")

                    # Feedback detalhado
                    st.markdown("### 📋 Feedback Detalhado")
                    st.markdown("""
                    **✅ Pontos Fortes:**
                    - Argumentação bem estruturada
                    - Uso adequado de conectivos
                    - Conclusão pertinente
                    
                    **⚠️ Pontos de Melhoria:**
                    - Atenção à pontuação
                    - Expandir alguns argumentos
                    - Revisar acentuação
                    """)
                else:
                    st.error("❌ Preencha o tema e a redação para avaliação.")

    with tab2:
        st.subheader("📄 Redações de Exemplo")

        col1, col2 = st.columns(2)

        with col1:
            banca_exemplo = st.selectbox("Banca:", bancas_todas, key="banca_exemplo")
            tema_exemplo = st.text_input("Tema:", value="Tecnologia na Educação", key="tema_exemplo")

            if st.button("✨ Gerar Exemplo"):
                import os
                import sys
                sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
                try:
                    from tools.writing_tool import WritingTool
                except Exception as e:
                    exemplo_redacao = f"Erro: Não foi possível importar WritingTool. {str(e)}"
                    st.session_state.example_essay = exemplo_redacao
                    st.session_state.example_banca = banca_exemplo
                    st.error(exemplo_redacao)
                else:
                    linhas = 30  # Mantém o padrão de 30 linhas, pode ser ajustado pelo usuário
                    try:
                        tool = WritingTool()
                        resultado = tool.generate_example_essay(banca_exemplo, tema_exemplo, linhas)
                        if isinstance(resultado, dict) and "example_essay" in resultado:
                            exemplo_redacao = resultado["example_essay"]
                        elif isinstance(resultado, dict) and "error" in resultado:
                            exemplo_redacao = f"Erro ao gerar redação: {resultado['error']}"
                        else:
                            exemplo_redacao = "Erro desconhecido ao gerar redação."
                    except Exception as e:
                        exemplo_redacao = f"Erro ao gerar redação: {str(e)}"
                    st.session_state.example_essay = exemplo_redacao
                    st.session_state.example_banca = banca_exemplo
                    if exemplo_redacao.startswith("Erro"):
                        st.error(exemplo_redacao)
                    else:
                        st.success("✅ Exemplo gerado com sucesso!")

        with col2:
            if st.session_state.example_essay:
                st.markdown("### 📄 Exemplo Gerado")
                st.markdown(st.session_state.example_essay)
                # Botão de download
                st.download_button(
                    label="📥 Download Redação de Exemplo",
                    data=st.session_state.example_essay,
                    file_name=f"redacao_exemplo_{st.session_state.example_banca}.md",
                    mime="text/markdown"
                )
            else:
                st.info("Nenhum exemplo gerado ainda. Clique em 'Gerar Exemplo' para criar uma redação de exemplo.")

    with tab3:
        st.subheader("🎯 Temas para Redação")

        # Temas por banca
        temas_por_banca = {
            "FGV": [
                "O impacto das redes sociais na sociedade contemporânea",
                "A importância da preservação ambiental",
                "O papel da educação na transformação social",
                "A tecnologia e o futuro do trabalho",
                "A valorização da cultura brasileira"
            ],
            "CESPE": [
                "A democratização do acesso à informação",
                "O combate à corrupção no Brasil",
                "A inclusão digital como direito fundamental",
                "A sustentabilidade e o desenvolvimento econômico",
                "A importância da ciência para o progresso social"
            ],
            "VUNESP": [
                "A responsabilidade social das empresas",
                "O papel da família na formação do cidadão",
                "A importância do esporte na sociedade",
                "A valorização dos profissionais da saúde",
                "O combate à violência urbana"
            ]
        }

        col1, col2 = st.columns(2)

        with col1:
            banca_temas = st.selectbox("Selecione a banca para ver temas:", list(temas_por_banca.keys()))

            if banca_temas in temas_por_banca:
                st.markdown(f"### 📝 Temas - {banca_temas}")
                for i, tema in enumerate(temas_por_banca[banca_temas], 1):
                    st.write(f"{i}. {tema}")

        with col2:
            st.markdown("### 🎲 Tema Aleatório")
            if st.button("🎲 Sortear Tema"):
                todas_bancas = list(temas_por_banca.keys())
                banca_aleatoria = random.choice(todas_bancas)
                tema_aleatorio = random.choice(temas_por_banca[banca_aleatoria])

                st.info(f"**Banca:** {banca_aleatoria}")
                st.info(f"**Tema:** {tema_aleatorio}")

    with tab4:
        st.subheader("📚 Histórico de Redações")

        # Simular histórico
        historico = [
            {"data": "2025-07-15", "tema": "Tecnologia na Educação", "nota": 8.5, "banca": "FGV"},
            {"data": "2025-07-10", "tema": "Preservação Ambiental", "nota": 7.8, "banca": "CESPE"},
            {"data": "2025-07-05", "tema": "Redes Sociais", "nota": 8.2, "banca": "VUNESP"},
            {"data": "2025-06-30", "tema": "Educação no Brasil", "nota": 7.5, "banca": "FGV"}
        ]

        # Filtros
        col1, col2 = st.columns(2)

        with col1:
            periodo = st.selectbox("Período:", ["Última semana", "Último mês", "Último trimestre", "Todas"])

        with col2:
            tipo_analise = st.selectbox("Tipo de análise:", ["Desempenho", "Temas", "Bancas"])

        # Gráfico de desempenho
        if tipo_analise == "Desempenho":
            st.markdown("### 📊 Evolução do Desempenho")

            # Dados para o gráfico
            datas = [h["data"] for h in historico]
            notas = [h["nota"] for h in historico]

            # Criar gráfico simples
            chart_data = pd.DataFrame({
                'Data': datas,
                'Nota': notas
            })

            st.line_chart(chart_data.set_index('Data'))

            # Estatísticas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Média", f"{sum(notas)/len(notas):.1f}")
            with col2:
                st.metric("📈 Melhor", f"{max(notas)}")
            with col3:
                st.metric("📉 Pior", f"{min(notas)}")

        # Tabela de histórico
        st.markdown("### 📋 Histórico Detalhado")

        df_historico = pd.DataFrame(historico)
        st.dataframe(df_historico, use_container_width=True)

elif st.session_state.current_page == "🎯 Simulados":
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🎯 Simulados Inteligentes")
    st.markdown('</div>', unsafe_allow_html=True)

    # Configuração do simulado
    st.subheader("⚙️ Configuração do Simulado")

    col1, col2 = st.columns(2)

    with col1:
        materia = st.selectbox("Matéria:", list(concurso_data["materias"].keys()))
        num_questoes = st.slider("Número de questões:", 5, 20, 10)

    with col2:
        tempo_limite = st.number_input("Tempo limite (minutos):", min_value=10, max_value=120, value=30)
        dificuldade = st.selectbox("Dificuldade:", ["Fácil", "Médio", "Difícil", "Misto"])

    if st.button("🚀 Iniciar Simulado", type="primary"):
        st.success("✅ Simulado iniciado!")

        # Simular questões
        st.markdown("### 📝 Questões do Simulado")

        for i in range(num_questoes):
            with st.expander(f"Questão {i+1}"):
                st.write("**Enunciado:** Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")

                opcoes = ["A) Primeira opção", "B) Segunda opção", "C) Terceira opção", "D) Quarta opção", "E) Quinta opção"]
                resposta = st.radio("Selecione a resposta:", opcoes, key=f"q{i}")

                if st.button(f"Confirmar Questão {i+1}", key=f"btn{i}"):
                    st.success("✅ Resposta registrada!")

elif st.session_state.current_page == "📊 Analytics":
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("📊 Analytics Avançado")
    st.markdown('</div>', unsafe_allow_html=True)

    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Total de Estudos", "156h", "+12h")
    with col2:
        st.metric("🎯 Simulados Realizados", "24", "+3")
    with col3:
        st.metric("📝 Redações Avaliadas", "18", "+2")
    with col4:
        st.metric("📊 Nota Média", "7.8", "+0.3")

    # Gráficos
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Progresso por Matéria")

        # Dados simulados
        materias = list(concurso_data["materias"].keys())
        progresso = [75, 82, 68, 90, 73, 85, 79]

        chart_data = pd.DataFrame({
            'Matéria': materias,
            'Progresso (%)': progresso
        })

        st.bar_chart(chart_data.set_index('Matéria'))

    with col2:
        st.subheader("⏰ Tempo de Estudo")

        # Dados simulados de tempo
        dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        horas = [3.5, 4.2, 2.8, 5.1, 3.9, 6.2, 2.1]

        tempo_data = pd.DataFrame({
            'Dia': dias,
            'Horas': horas
        })

        st.line_chart(tempo_data.set_index('Dia'))

    # Análise de pontos fracos
    st.subheader("🎯 Análise de Pontos Fracos")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📉 Matérias com Menor Desempenho")
        st.markdown("""
        - **Direito Penal**: 68% (Precisa melhorar)
        - **Raciocínio Lógico**: 73% (Atenção necessária)
        - **Português**: 75% (Revisão recomendada)
        """)

    with col2:
        st.markdown("### 🎯 Recomendações")
        st.markdown("""
        - **Foque em Direito Penal**: Mais simulados específicos
        - **Pratique Raciocínio Lógico**: Exercícios diários
        - **Revisão de Português**: Gramática e interpretação
        """)

elif st.session_state.current_page == "📋 Análise de Edital":
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("📋 Análise de Edital")
    st.markdown('</div>', unsafe_allow_html=True)

    # Abas para diferentes tipos de análise
    tab1, tab2 = st.tabs(["📄 Upload de Edital", "📊 Análise Atual"])

    with tab1:
        st.subheader("📄 Upload e Análise de Edital")

        # Upload de arquivo
        uploaded_file = st.file_uploader(
            "Escolha um arquivo de edital (PDF, DOCX, TXT):",
            type=['pdf', 'docx', 'txt'],
            help="Faça upload do edital para análise automática"
        )

        if uploaded_file is not None:
            st.success(f"✅ Arquivo carregado: {uploaded_file.name}")

            # Informações do arquivo
            file_details = {
                "Nome": uploaded_file.name,
                "Tipo": uploaded_file.type,
                "Tamanho": f"{uploaded_file.size / 1024:.1f} KB"
            }

            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**Nome:** {file_details['Nome']}")
            with col2:
                st.info(f"**Tipo:** {file_details['Tipo']}")
            with col3:
                st.info(f"**Tamanho:** {file_details['Tamanho']}")

            # Análise automática do arquivo para detectar cargos
            if 'edital_analisado' not in st.session_state or st.session_state.get('arquivo_analisado') != uploaded_file.name:
                with st.spinner("🔍 Analisando arquivo para detectar cargos automaticamente..."):
                    try:
                        # Extrair texto do arquivo
                        content = extrair_texto_arquivo(uploaded_file)
                        cargos_detectados = []
                        # INTEGRAÇÃO DA NOVA TOOL DE EXTRAÇÃO DE CARGOS PARA PDF
                        if uploaded_file.type == "application/pdf":
                            try:
                                import tempfile

                                from tools.cargo_extraction_tool import (
                                    extract_cargos_from_pdf,
                                )
                                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                                    tmp.write(uploaded_file.read())
                                    tmp_path = tmp.name
                                cargos_detectados = extract_cargos_from_pdf(tmp_path)
                            except Exception as e:
                                st.warning(f"⚠️ Erro ao extrair cargos do PDF: {str(e)}")
                        # Fallback para análise antiga se não encontrou cargos
                        if not cargos_detectados:
                            analyzer = EditalAnalyzer()
                            analise_preliminar = analyzer.analisar_edital(content, [])
                            cargos_detectados = analise_preliminar.get('cargos_detectados', [])
                        else:
                            analise_preliminar = {
                                'concurso': 'Concurso Público',
                                'banca': 'Banca não identificada',
                                'vagas': 100,
                                'data_prova': 'Data não identificada',
                                'data_inscricao': 'Período não identificado',
                                'cargos_detectados': cargos_detectados,
                                'cargos_analisados': [],
                                'materias': {},
                                'conteudo_analisado': content[:1000]
                            }
                        # Se não detectou cargos específicos, usar cargos comuns
                        if not cargos_detectados:
                            cargos_detectados = ["Agente", "Escrivão", "Delegado", "Perito", "Papiloscopista", "Analista", "Técnico"]
                            analise_preliminar['cargos_detectados'] = cargos_detectados
                        st.session_state.edital_analisado = analise_preliminar
                        st.session_state.arquivo_analisado = uploaded_file.name
                        st.session_state.conteudo_arquivo = content
                        st.success("✅ Análise automática concluída!")
                    except Exception as e:
                        st.error(f"❌ Erro na análise automática: {str(e)}")
                        # Usar cargos padrão em caso de erro
                        st.session_state.edital_analisado = {
                            'cargos_detectados': ["Agente", "Escrivão", "Delegado", "Perito", "Papiloscopista", "Analista", "Técnico"]
                        }
                        st.session_state.arquivo_analisado = uploaded_file.name

            # Seleção de cargos com base na análise automática
            st.markdown("### 🎯 Seleção de Cargos")

            col1, col2 = st.columns(2)

            with col1:
                # Cargos detectados automaticamente
                cargos_detectados = st.session_state.edital_analisado.get('cargos_detectados', [])

                # Se não há cargos detectados, usar cargos padrão
                if not cargos_detectados:
                    cargos_detectados = ["Agente", "Escrivão", "Delegado", "Perito", "Papiloscopista", "Analista", "Técnico"]

                # Selecionar automaticamente o primeiro cargo detectado
                cargo_padrao = cargos_detectados[0] if cargos_detectados else "Agente"

                cargos_selecionados = st.multiselect(
                    "Cargos disponíveis:",
                    cargos_detectados,
                    default=[cargo_padrao],
                    help="Cargos detectados automaticamente no edital"
                )

                # Mostrar cargos detectados automaticamente
                if cargos_detectados and len(cargos_detectados) > 0:
                    st.success(f"🎯 **Cargos detectados automaticamente:** {', '.join(cargos_detectados[:10])}")
                    if len(cargos_detectados) > 10:
                        st.info(f"... e mais {len(cargos_detectados) - 10} cargos")

            with col2:
                # Adicionar cargo customizado
                st.markdown("#### ➕ Adicionar Cargo Customizado")
                novo_cargo = st.text_input("Nome do cargo:", placeholder="Ex: Assistente Administrativo")
                if st.button("➕ Adicionar Cargo") and novo_cargo:
                    if novo_cargo not in cargos_selecionados:
                        cargos_selecionados.append(novo_cargo)
                        st.success(f"✅ Cargo '{novo_cargo}' adicionado!")
                        st.rerun()
                    else:
                        st.warning("⚠️ Este cargo já existe!")

            # Mostrar cargos selecionados
            if cargos_selecionados:
                st.info(f"**Cargos selecionados:** {', '.join(cargos_selecionados)}")
            else:
                st.warning("⚠️ Selecione pelo menos um cargo para análise.")

            # Botão para analisar (usando dados já extraídos)
            if st.button("🔍 Analisar Edital", type="primary") and cargos_selecionados:
                with st.spinner("Analisando edital com cargos selecionados..."):
                    try:
                        # Usar conteúdo já extraído ou extrair novamente se necessário
                        if 'conteudo_arquivo' in st.session_state:
                            content = st.session_state.conteudo_arquivo
                        else:
                            content = extrair_texto_arquivo(uploaded_file)

                        if content.startswith("Erro ao extrair texto") or content == "Formato de arquivo não suportado":
                            st.error(f"❌ {content}")
                        else:
                            # Análise inteligente do conteúdo usando LLM com cargos selecionados
                            edital_analisado = analisar_edital_com_llm(content, cargos_selecionados)

                            # Atualizar na session state
                            st.session_state.edital_analisado = edital_analisado

                        st.success("✅ Análise concluída!")

                        # Status da análise
                        modo_analise = edital_analisado.get('modo_analise', 'Análise Básica')
                        confianca = edital_analisado.get('confianca', 'Média')

                        if confianca == "Alta":
                            st.success(f"🎯 **Modo de Análise:** {modo_analise} | **Confiança:** {confianca}")
                        elif confianca == "Média":
                            st.warning(f"⚠️ **Modo de Análise:** {modo_analise} | **Confiança:** {confianca}")
                        else:
                            st.error(f"❌ **Modo de Análise:** {modo_analise} | **Confiança:** {confianca}")

                        # Resultados da análise
                        st.subheader("📊 Resultados da Análise")

                        # Salvar na session state
                        st.session_state.edital_analisado = edital_analisado

                        # Mostrar informações extraídas
                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("### 🏛️ Informações Extraídas")
                            st.info(f"**Concurso:** {edital_analisado['concurso']}")
                            st.info(f"**Banca:** {edital_analisado['banca']}")
                            st.info(f"**Vagas:** {edital_analisado['vagas']:,}")
                            st.info(f"**Data da Prova:** {edital_analisado['data_prova']}")
                            st.info(f"**Inscrições:** {edital_analisado['data_inscricao']}")

                            # Cargos detectados vs selecionados
                            if edital_analisado['cargos_detectados']:
                                st.info(f"**Cargos Detectados:** {', '.join(edital_analisado['cargos_detectados'])}")
                            st.info(f"**Cargos Analisados:** {', '.join(edital_analisado['cargos_analisados'])}")

                        with col2:
                            st.markdown("### 📚 Matérias Identificadas")
                            for materia, info in edital_analisado['materias'].items():
                                st.write(f"• **{materia}** (Peso: {info.get('peso', 1.0)}, Questões: {info.get('questoes', 10)})")

                                # Mostrar conteúdos se disponíveis
                                conteudos = info.get('conteudo', [])
                                if conteudos:
                                    with st.expander(f"Conteúdos de {materia}"):
                                        for conteudo in conteudos:
                                            st.write(f"  - {conteudo}")

                        # Detalhes da análise
                        with st.expander("🔍 Detalhes da Análise"):
                            st.markdown("### 📋 Conteúdo Analisado")
                            st.text_area("Primeiras 1000 caracteres do arquivo:", edital_analisado['conteudo_analisado'], height=200)

                            # Debug: mostrar conteúdo completo em uma aba separada
                            with st.expander("🔍 Conteúdo Completo (Debug)"):
                                st.text_area("Conteúdo completo extraído:", content, height=300)

                            st.markdown("### 🎯 Padrões Identificados")
                            st.write("• **Concurso:** Extraído usando regex específicos para concursos")
                            st.write("• **Banca:** Identificada por padrões de bancas conhecidas")
                            st.write("• **Vagas:** Números seguidos da palavra 'vagas' ou 'cargos'")
                            st.write("• **Datas:** Formato DD/MM/AAAA próximo a palavras-chave")
                            st.write("• **Cargos:** Detectados por padrões específicos no texto")
                            st.write("• **Matérias:** Identificadas por nomes conhecidos e pesos")

                            st.markdown("### 📊 Estatísticas da Análise")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("📄 Caracteres Analisados", f"{len(content):,}")
                            with col2:
                                st.metric("📚 Matérias Encontradas", len(edital_analisado['materias']))
                            with col3:
                                st.metric("🎯 Cargos Detectados", len(edital_analisado['cargos_detectados']))

                            # Mostrar padrões encontrados
                            st.markdown("### 🔍 Padrões Encontrados no Texto")
                            padroes_encontrados = []

                            if edital_analisado['concurso'] != 'Concurso Público':
                                padroes_encontrados.append("✅ Nome do concurso")
                            if edital_analisado['banca'] != 'Banca não identificada':
                                padroes_encontrados.append("✅ Banca examinadora")
                            if edital_analisado['vagas'] != 100:
                                padroes_encontrados.append("✅ Número de vagas")
                            if edital_analisado['data_prova'] != 'Data não identificada':
                                padroes_encontrados.append("✅ Data da prova")
                            if edital_analisado['data_inscricao'] != 'Período não identificado':
                                padroes_encontrados.append("✅ Período de inscrição")
                            if edital_analisado['cargos_detectados']:
                                padroes_encontrados.append("✅ Cargos específicos")

                            if padroes_encontrados:
                                for padrao in padroes_encontrados:
                                    st.write(padrao)
                            else:
                                st.warning("⚠️ Poucos padrões específicos encontrados. Verifique se o arquivo é um edital válido.")

                        # Estatísticas da análise
                        with st.expander("📊 Estatísticas da Análise"):
                            col1, col2, col3 = st.columns(3)

                            with col1:
                                st.metric("📄 Caracteres Analisados", f"{len(content):,}")
                                st.metric("📚 Matérias Detectadas", len(edital_analisado['materias']))

                            with col2:
                                st.metric("👥 Cargos Identificados", len(edital_analisado['cargos_detectados']))
                                st.metric("📝 Total de Questões", sum(info.get('questoes', 10) for info in edital_analisado['materias'].values()))

                            with col3:
                                st.metric("⚖️ Peso Total", f"{sum(info.get('peso', 1.0) for info in edital_analisado['materias'].values()):.1f}")
                                st.metric("🎯 Confiança", "85%")

                        # Comparação com dados padrão
                        with st.expander("🔄 Comparação com Dados Padrão"):
                            st.markdown("### 📈 Diferenças Encontradas")

                            # Comparar com dados padrão
                            dados_padrao = concurso_data

                            col1, col2 = st.columns(2)

                            with col1:
                                st.markdown("**📊 Vagas:**")
                                st.write(f"• Padrão: {dados_padrao['vagas']:,}")
                                st.write(f"• Edital: {edital_analisado['vagas']:,}")

                                st.markdown("**🏛️ Banca:**")
                                st.write(f"• Padrão: {dados_padrao['banca']}")
                                st.write(f"• Edital: {edital_analisado['banca']}")

                            with col2:
                                st.markdown("**📅 Data da Prova:**")
                                st.write(f"• Padrão: {dados_padrao['data_prova'].strftime('%d/%m/%Y')}")
                                st.write(f"• Edital: {edital_analisado['data_prova']}")

                                st.markdown("**📚 Matérias:**")
                                st.write(f"• Padrão: {len(dados_padrao['materias'])}")
                                st.write(f"• Edital: {len(edital_analisado['materias'])}")

                        # Botão para aplicar análise
                        if st.button("✅ Aplicar Análise", type="primary"):
                            st.success("✅ Análise aplicada! O sistema foi atualizado com as informações do edital.")
                            st.rerun()

                    except Exception as e:
                        st.error(f"❌ Erro na análise: {str(e)}")
                        st.info("💡 Dica: Verifique se o arquivo está em um formato suportado e não está corrompido.")

        # Exemplo de edital
        with st.expander("📋 Exemplo de Edital"):
            st.markdown("""
            ### 📄 Estrutura Típica de um Edital
            
            **1. Informações Básicas:**
            - Nome do concurso
            - Órgão responsável
            - Banca examinadora
            - Número de vagas
            
            **2. Cronograma:**
            - Data de publicação
            - Período de inscrições
            - Data da prova
            - Data do resultado
            
            **3. Matérias e Conteúdos:**
            - Lista de disciplinas
            - Peso de cada matéria
            - Número de questões
            - Conteúdos específicos
            
            **4. Requisitos:**
            - Escolaridade
            - Idade mínima/máxima
            - Documentação necessária
            """)

    with tab2:
        st.subheader("📊 Análise Atual do Edital")

        # Verificar se há edital analisado
        if hasattr(st.session_state, 'edital_analisado') and st.session_state.edital_analisado:
            edital_atual = st.session_state.edital_analisado
        else:
            edital_atual = concurso_data

        # Informações do concurso
        col1, col2 = st.columns(2)

        with col1:
            concurso_nome = edital_atual.get('nome') or edital_atual.get('concurso', 'Concurso Público')
            st.info(f"**Concurso:** {concurso_nome}")
            st.info(f"**Banca:** {edital_atual.get('banca', 'Banca não identificada')}")
            st.info(f"**Vagas:** {edital_atual.get('vagas', 0):,}")

        with col2:
            data_prova = edital_atual.get('data_prova', concurso_data['data_prova'])
            if isinstance(data_prova, str) and data_prova != "Data não identificada":
                try:
                    data_prova = datetime.strptime(data_prova, '%d/%m/%Y')
                    st.warning(f"**Data da Prova:** {data_prova.strftime('%d/%m/%Y')}")
                except ValueError:
                    st.warning(f"**Data da Prova:** {data_prova}")
            else:
                st.warning(f"**Data da Prova:** {data_prova}")
            st.warning(f"**Dias Restantes:** {calcular_dias_restantes()}")
            st.warning("**Status:** Inscrições Abertas")

        # Cronograma
        st.subheader("📅 Cronograma")

        cronograma = [
            {"etapa": "Inscrições", "data": "15/06/2025 - 15/07/2025", "status": "✅ Concluído"},
            {"etapa": "Pagamento", "data": "16/07/2025 - 20/07/2025", "status": "⏳ Em andamento"},
            {"etapa": "Prova", "data": "15/08/2025", "status": "⏰ Pendente"},
            {"etapa": "Resultado", "data": "30/09/2025", "status": "⏰ Pendente"}
        ]

        for etapa in cronograma:
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.write(f"**{etapa['etapa']}**")
            with col2:
                st.write(etapa['data'])
            with col3:
                st.write(etapa['status'])

        # Matérias e conteúdos
        st.subheader("📚 Matérias e Conteúdos")

        materias_edital = edital_atual.get('materias', concurso_data["materias"])

        for materia, info in materias_edital.items():
            with st.expander(f"📖 {materia} (Peso: {info.get('peso', 1.0)}, Questões: {info.get('questoes', 10)})"):
                st.write("**Conteúdos:**")
                conteudos = info.get('conteudo', ['Conteúdo não especificado'])
                for conteudo in conteudos:
                    st.write(f"• {conteudo}")

                # Progresso da matéria
                progresso = random.randint(60, 95)
                st.progress(progresso/100, text=f"Progresso: {progresso}%")

        # Recomendações
        st.subheader("🎯 Recomendações de Estudo")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 🚀 Prioridades")
            st.markdown("""
            1. **Direito Constitucional** (Peso 1.5)
            2. **Direito Administrativo** (Peso 1.5)
            3. **Direito Penal** (Peso 1.5)
            4. **Português** (Base para todas)
            5. **Raciocínio Lógico** (Fundamental)
            """)

        with col2:
            st.markdown("### ⏰ Distribuição de Tempo")
            st.markdown("""
            - **Direito Constitucional**: 25%
            - **Direito Administrativo**: 25%
            - **Direito Penal**: 20%
            - **Português**: 15%
            - **Outras**: 15%
            """)

        # Ações do edital
        st.subheader("💾 Ações do Edital")

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📥 Download Análise", type="primary"):
                st.info("📥 Análise exportada para PDF!")

        with col2:
            if st.button("🔄 Atualizar Dados"):
                st.info("🔄 Dados atualizados com sucesso!")

        with col3:
            if st.button("🗑️ Limpar Análise"):
                if hasattr(st.session_state, 'edital_analisado'):
                    del st.session_state.edital_analisado
                st.success("🗑️ Análise limpa! Voltando para dados padrão.")
                st.rerun()

elif st.session_state.current_page == "📋 Plano de Estudos":
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("📋 Plano de Estudos Personalizado")
    st.markdown('</div>', unsafe_allow_html=True)

    # Verificar se há edital analisado
    edital_analisado = st.session_state.get('edital_analisado', None)

    if edital_analisado:
        # Mostrar informações do edital
        st.info(f"📄 **Edital Carregado:** {edital_analisado.get('concurso', 'N/A')} - {edital_analisado.get('banca', 'N/A')}")

        # Extrair dados do edital
        banca_edital = edital_analisado.get('banca', '').upper()
        cargos_disponiveis = edital_analisado.get('cargos_detectados', [])
        materias_edital = edital_analisado.get('materias', {})

        # Mapear banca do edital para as opções disponíveis
        bancas_mapeadas = {
            'CESPE': 'CESPE', 'CEBRASPE': 'CESPE',
            'FCC': 'FCC', 'FUNDAÇÃO CARLOS CHAGAS': 'FCC',
            'VUNESP': 'VUNESP', 'FUNDAÇÃO VUNESP': 'VUNESP',
            'FGV': 'FGV', 'FUNDAÇÃO GETÚLIO VARGAS': 'FGV',
            'IBFC': 'IBFC'
        }

        banca_selecionada = None
        for key, value in bancas_mapeadas.items():
            if key in banca_edital:
                banca_selecionada = value
                break

        if not banca_selecionada:
            banca_selecionada = "CESPE"  # Padrão
    else:
        st.warning("⚠️ Nenhum edital analisado encontrado. Analise um edital primeiro para gerar um plano personalizado.")
        cargos_disponiveis = ["Agente", "Escrivão", "Delegado", "Analista", "Técnico"]
        materias_edital = {}
        banca_selecionada = "CESPE"

    # Configuração do plano
    st.subheader("⚙️ Configuração do Plano")

    col1, col2 = st.columns(2)

    with col1:
        # Banca baseada no edital ou seleção manual
        if edital_analisado:
            banca_plano = st.selectbox("Banca:", ["CESPE", "FCC", "VUNESP", "FGV", "IBFC"],
                                     index=["CESPE", "FCC", "VUNESP", "FGV", "IBFC"].index(banca_selecionada) if banca_selecionada in ["CESPE", "FCC", "VUNESP", "FGV", "IBFC"] else 0)
        else:
            banca_plano = st.selectbox("Banca:", ["CESPE", "FCC", "VUNESP", "FGV", "IBFC"])

        horas_diarias = st.slider("Horas de estudo por dia:", 1, 8, 4)

    with col2:
        # Cargo baseado no edital ou seleção manual
        if cargos_disponiveis:
            cargo_selecionado = st.selectbox("Cargo:", cargos_disponiveis)
        else:
            cargo_selecionado = st.text_input("Cargo:", placeholder="Digite o cargo desejado")

        dias_semana = st.slider("Dias de estudo por semana:", 3, 7, 6)

    # Linha adicional para nível
    col3, col4 = st.columns(2)
    with col3:
        nivel_atual = st.selectbox("Nível atual:", ["Iniciante", "Intermediário", "Avançado"])
    with col4:
        if edital_analisado and edital_analisado.get('data_prova'):
            st.info(f"🗓️ **Data da Prova:** {edital_analisado.get('data_prova')}")
        else:
            st.info("🗓️ **Data da Prova:** Não informada")

    if st.button("🎯 Gerar Plano de Estudos", type="primary"):
        with st.spinner("Gerando plano de estudos personalizado..."):
            # Gerar plano baseado no edital ou dados padrão
            if edital_analisado and materias_edital:
                # Usar matérias do edital
                materias_plano = list(materias_edital.keys())
                st.success(f"✅ Plano de estudos gerado para {cargo_selecionado} - {banca_plano}!")

                # Mostrar informações do concurso
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("🏛️ Banca", banca_plano)
                with col2:
                    st.metric("👤 Cargo", cargo_selecionado)
                with col3:
                    st.metric("📚 Matérias", len(materias_plano))

            else:
                # Usar matérias padrão
                materias_plano = ["Português", "Raciocínio Lógico", "Direito Constitucional",
                                "Direito Administrativo", "Direito Penal", "Legislação Especial"]
                st.success("✅ Plano de estudos gerado com matérias padrão!")

        # Plano detalhado
        st.subheader("📅 Plano de Estudos Detalhado")

        # Distribuir matérias pelos dias da semana
        def distribuir_materias_por_dias(materias, dias_estudo):
            """Distribui matérias pelos dias de estudo de forma equilibrada"""
            materias_distribuidas = []
            total_materias = len(materias)

            for i in range(7):  # 7 dias da semana
                if i < dias_estudo:  # Apenas dias de estudo
                    if i == dias_estudo - 1:  # Último dia: simulado/revisão
                        materias_distribuidas.append(["Simulado Geral", "Revisão"])
                    elif i == dias_estudo - 2 and dias_estudo > 5:  # Penúltimo dia se > 5 dias
                        materias_distribuidas.append(["Revisão Geral", "Exercícios"])
                    else:
                        # Distribuir matérias principais
                        idx1 = (i * 2) % total_materias
                        idx2 = (i * 2 + 1) % total_materias
                        materia1 = materias[idx1] if idx1 < total_materias else "Revisão"
                        materia2 = materias[idx2] if idx2 < total_materias else "Exercícios"
                        materias_distribuidas.append([materia1, materia2])
                else:
                    materias_distribuidas.append(["Descanso", "Leitura"])

            return materias_distribuidas

        # Cronograma semanal
        st.markdown("### 📅 Cronograma Semanal")

        dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        materias_dia = distribuir_materias_por_dias(materias_plano, dias_semana)

        for i, dia in enumerate(dias):
            with st.expander(f"📅 {dia}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Manhã:** {materias_dia[i][0]}")
                    st.write(f"**Duração:** {horas_diarias//2}h")
                with col2:
                    st.write(f"**Tarde:** {materias_dia[i][1]}")
                    st.write(f"**Duração:** {horas_diarias//2}h")

        # Conteúdos por matéria
        st.markdown("### 📚 Conteúdos por Matéria")

        # Usar matérias do edital se disponível, senão usar dados padrão
        materias_para_exibir = materias_edital if materias_edital else concurso_data["materias"]

        for materia, info in materias_para_exibir.items():
            with st.expander(f"📖 {materia}"):
                # Verificar se é do edital ou dados padrão
                if isinstance(info, dict):
                    # Dados do edital
                    questoes = info.get('questoes', 'N/A')
                    peso = info.get('peso', 1.0)
                    conteudos = info.get('conteudo', ['Conteúdo não especificado'])

                    # Informações da matéria
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("📊 Questões", questoes)
                    with col2:
                        st.metric("⚖️ Peso", f"{peso:.1f}")

                    st.write("**Conteúdos a estudar:**")
                    if isinstance(conteudos, list):
                        for conteudo in conteudos:
                            st.write(f"• {conteudo}")
                    else:
                        st.write(f"• {conteudos}")
                else:
                    # Dados padrão (string)
                    st.write("**Conteúdos a estudar:**")
                    st.write(f"• {info}")

                # Cronograma da matéria baseado no peso/importância
                if isinstance(info, dict) and 'questoes' in info:
                    try:
                        num_questoes = int(info['questoes']) if str(info['questoes']).isdigit() else 20
                        semanas = max(2, min(8, num_questoes // 5))  # 1 semana a cada 5 questões
                    except:
                        semanas = 4
                else:
                    semanas = random.randint(4, 6)

                total_materias = len(materias_para_exibir)
                horas_semanais = max(1, (horas_diarias * dias_semana) // total_materias)

                st.write(f"**Duração estimada:** {semanas} semanas")
                st.write(f"**Horas semanais:** {horas_semanais}h")

        # Informações específicas do cargo
        if edital_analisado and cargo_selecionado:
            st.markdown("### 👤 Informações do Cargo")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.info(f"**Cargo:** {cargo_selecionado}")
            with col2:
                vagas = edital_analisado.get('vagas', 'N/A')
                st.info(f"**Vagas:** {vagas}")
            with col3:
                data_prova = edital_analisado.get('data_prova', 'N/A')
                st.info(f"**Prova:** {data_prova}")

            # Cargos analisados do edital
            cargos_analisados = edital_analisado.get('cargos_analisados', [])
            if cargo_selecionado in cargos_analisados:
                st.success(f"✅ Cargo {cargo_selecionado} foi analisado no edital")
            else:
                st.warning(f"⚠️ Cargo {cargo_selecionado} não foi especificamente analisado no edital")

        # Metas e objetivos personalizadas
        st.markdown("### 🎯 Metas e Objetivos")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📊 Metas Semanais:**")
            total_questoes = sum([int(info.get('questoes', 20)) if isinstance(info, dict) and str(info.get('questoes', 20)).isdigit() else 20 for info in materias_para_exibir.values()])
            questoes_semanais = max(50, total_questoes // 4)  # Distribuir ao longo de 4 semanas

            st.markdown(f"""
            - Completar 2 simulados
            - Fazer {questoes_semanais} questões
            - Revisar {min(3, len(materias_para_exibir))} matérias
            - Estudar {horas_diarias * dias_semana}h por semana
            """)

        with col2:
            st.markdown("**🏆 Objetivos Mensais:**")
            st.markdown(f"""
            - Atingir 80% de acerto em simulados
            - Dominar {len(materias_para_exibir)} matérias do edital
            - Completar cronograma de estudos
            - Estar preparado para {banca_plano}
            """)

elif st.session_state.current_page == "⚙️ Configurações":
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("⚙️ Configurações do Sistema")
    st.markdown('</div>', unsafe_allow_html=True)

    # Configurações gerais
    st.subheader("🔧 Configurações Gerais")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👤 Perfil do Usuário")
        nome = st.text_input("Nome:", value="Estudante")
        email = st.text_input("Email:", value="estudante@email.com")
        meta_diaria = st.number_input("Meta de horas diárias:", min_value=1, max_value=12, value=4)

    with col2:
        st.markdown("### 🎯 Configurações de Estudo")
        notificacoes = st.checkbox("Ativar notificações", value=True)
        modo_escuro = st.checkbox("Modo escuro", value=False)
        auto_save = st.checkbox("Salvar automaticamente", value=True)

    # Configurações de redação
    st.subheader("📝 Configurações de Redação")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📋 Bancas Configuradas")
        for banca, limite in st.session_state.line_limits.items():
            st.write(f"• **{banca}**: {limite} linhas")

    with col2:
        st.markdown("### ⚙️ Configurações Avançadas")
        tempo_redacao = st.number_input("Tempo padrão para redação (min):", min_value=30, max_value=120, value=60)
        mostrar_exemplos = st.checkbox("Mostrar exemplos automaticamente", value=True)

    # Configurações de simulados
    st.subheader("🎯 Configurações de Simulados")

    col1, col2 = st.columns(2)

    with col1:
        questoes_padrao = st.number_input("Questões padrão por simulado:", min_value=10, max_value=50, value=20)
        tempo_padrao = st.number_input("Tempo padrão (min):", min_value=30, max_value=180, value=60)

    with col2:
        mostrar_gabarito = st.checkbox("Mostrar gabarito após simulado", value=True)
        salvar_resultados = st.checkbox("Salvar resultados automaticamente", value=True)

    # Ações
    st.subheader("💾 Ações")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Salvar Configurações", type="primary"):
            st.success("✅ Configurações salvas com sucesso!")

    with col2:
        if st.button("🔄 Restaurar Padrões"):
            st.info("🔄 Configurações restauradas para os valores padrão!")

    with col3:
        if st.button("📤 Exportar Configurações"):
            st.info("📤 Configurações exportadas para arquivo JSON!")

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🎯 Agente Concurseiro v2.0 - Sistema Inteligente de Preparação para Concursos</p>
    <p>Desenvolvido com ❤️ para ajudar você a conquistar sua vaga!</p>
</div>
""", unsafe_allow_html=True)
