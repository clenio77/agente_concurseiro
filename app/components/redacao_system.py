"""
Sistema de Redação Completo - Agente Concurseiro v2.0
Corretor automático, gerador de exemplos e análise por banca
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
from typing import Dict, List, Tuple, Optional
import json

class RedacaoSystem:
    """Sistema completo de redação para concursos"""
    
    def __init__(self):
        self.criterios_avaliacao = {
            "Adequação ao Tema": {
                "peso": 20,
                "descricao": "Desenvolvimento do tema proposto",
                "pontos": ["Compreensão do tema", "Foco no assunto", "Relevância do conteúdo"]
            },
            "Adequação ao Tipo Textual": {
                "peso": 15,
                "descricao": "Estrutura adequada ao tipo de texto",
                "pontos": ["Dissertativo-argumentativo", "Estrutura clara", "Progressão textual"]
            },
            "Coesão e Coerência": {
                "peso": 20,
                "descricao": "Articulação das ideias",
                "pontos": ["Conectivos adequados", "Sequência lógica", "Unidade temática"]
            },
            "Domínio da Norma Culta": {
                "peso": 20,
                "descricao": "Correção gramatical",
                "pontos": ["Ortografia", "Concordância", "Regência", "Pontuação"]
            },
            "Proposta de Intervenção": {
                "peso": 25,
                "descricao": "Solução para o problema apresentado",
                "pontos": ["Viabilidade", "Detalhamento", "Respeito aos direitos humanos"]
            }
        }
        
        self.bancas_estilo = {
            "CESPE/CEBRASPE": {
                "tipo_preferido": "Dissertativo-argumentativo",
                "extensao": "25-30 linhas",
                "caracteristicas": [
                    "Linguagem formal e impessoal",
                    "Argumentação consistente",
                    "Proposta de intervenção detalhada",
                    "Uso de dados e exemplos"
                ],
                "temas_frequentes": [
                    "Políticas públicas",
                    "Direitos humanos",
                    "Meio ambiente",
                    "Tecnologia e sociedade"
                ]
            },
            "FCC": {
                "tipo_preferido": "Dissertativo-expositivo",
                "extensao": "20-25 linhas",
                "caracteristicas": [
                    "Clareza e objetividade",
                    "Estrutura bem definida",
                    "Linguagem técnica quando necessário",
                    "Exemplos práticos"
                ],
                "temas_frequentes": [
                    "Administração pública",
                    "Ética profissional",
                    "Gestão e liderança",
                    "Inovação tecnológica"
                ]
            },
            "FGV": {
                "tipo_preferido": "Dissertativo-argumentativo",
                "extensao": "25-30 linhas",
                "caracteristicas": [
                    "Análise crítica aprofundada",
                    "Múltiplas perspectivas",
                    "Linguagem elaborada",
                    "Referências contextuais"
                ],
                "temas_frequentes": [
                    "Economia e sociedade",
                    "Globalização",
                    "Sustentabilidade",
                    "Transformação digital"
                ]
            }
        }
        
        self.temas_banco = {
            "Políticas Públicas": {
                "subtemas": [
                    "Saúde pública no Brasil",
                    "Educação e inclusão social",
                    "Segurança pública",
                    "Habitação popular"
                ],
                "argumentos_chave": [
                    "Investimento em infraestrutura",
                    "Capacitação profissional",
                    "Participação social",
                    "Transparência governamental"
                ]
            },
            "Meio Ambiente": {
                "subtemas": [
                    "Mudanças climáticas",
                    "Preservação da Amazônia",
                    "Energia renovável",
                    "Gestão de resíduos"
                ],
                "argumentos_chave": [
                    "Desenvolvimento sustentável",
                    "Educação ambiental",
                    "Tecnologias limpas",
                    "Cooperação internacional"
                ]
            },
            "Tecnologia e Sociedade": {
                "subtemas": [
                    "Inteligência artificial",
                    "Inclusão digital",
                    "Privacidade de dados",
                    "Trabalho remoto"
                ],
                "argumentos_chave": [
                    "Regulamentação adequada",
                    "Capacitação digital",
                    "Ética tecnológica",
                    "Democratização do acesso"
                ]
            }
        }

    def corrigir_redacao(self, texto: str, banca: str = "CESPE/CEBRASPE") -> Dict:
        """Corrige redação automaticamente baseada nos critérios"""
        resultado = {
            "nota_final": 0,
            "notas_criterios": {},
            "feedback_detalhado": {},
            "sugestoes_melhoria": [],
            "pontos_fortes": [],
            "pontos_fracos": []
        }
        
        # Análise por critério
        for criterio, info in self.criterios_avaliacao.items():
            nota_criterio = self._avaliar_criterio(texto, criterio, banca)
            resultado["notas_criterios"][criterio] = nota_criterio
            resultado["nota_final"] += (nota_criterio * info["peso"]) / 100
        
        # Feedback detalhado
        resultado["feedback_detalhado"] = self._gerar_feedback_detalhado(texto, resultado["notas_criterios"])
        
        # Sugestões de melhoria
        resultado["sugestoes_melhoria"] = self._gerar_sugestoes(texto, resultado["notas_criterios"])
        
        # Pontos fortes e fracos
        resultado["pontos_fortes"], resultado["pontos_fracos"] = self._identificar_pontos(resultado["notas_criterios"])
        
        return resultado

    def _avaliar_criterio(self, texto: str, criterio: str, banca: str) -> float:
        """Avalia um critério específico da redação"""
        if criterio == "Adequação ao Tema":
            return self._avaliar_adequacao_tema(texto)
        elif criterio == "Adequação ao Tipo Textual":
            return self._avaliar_tipo_textual(texto, banca)
        elif criterio == "Coesão e Coerência":
            return self._avaliar_coesao_coerencia(texto)
        elif criterio == "Domínio da Norma Culta":
            return self._avaliar_norma_culta(texto)
        elif criterio == "Proposta de Intervenção":
            return self._avaliar_proposta_intervencao(texto)
        
        return 5.0  # Nota padrão

    def _avaliar_adequacao_tema(self, texto: str) -> float:
        """Avalia adequação ao tema"""
        palavras = len(texto.split())
        paragrafos = len([p for p in texto.split('\n') if p.strip()])
        
        # Critérios básicos
        nota = 5.0
        
        if palavras < 150:
            nota -= 2.0  # Texto muito curto
        elif palavras > 400:
            nota -= 1.0  # Texto muito longo
        
        if paragrafos < 3:
            nota -= 1.5  # Poucos parágrafos
        elif paragrafos > 6:
            nota -= 0.5  # Muitos parágrafos
        
        # Verifica desenvolvimento do tema
        if "problema" in texto.lower() or "questão" in texto.lower():
            nota += 1.0
        
        if "sociedade" in texto.lower() or "social" in texto.lower():
            nota += 0.5
        
        return max(0, min(10, nota))

    def _avaliar_tipo_textual(self, texto: str, banca: str) -> float:
        """Avalia adequação ao tipo textual"""
        nota = 5.0
        
        # Verifica estrutura dissertativa
        paragrafos = [p.strip() for p in texto.split('\n') if p.strip()]
        
        if len(paragrafos) >= 4:
            nota += 1.0  # Boa estrutura
        
        # Verifica elementos argumentativos
        conectivos_arg = ["portanto", "assim", "dessa forma", "por isso", "logo", "consequentemente"]
        conectivos_encontrados = sum(1 for c in conectivos_arg if c in texto.lower())
        
        if conectivos_encontrados >= 2:
            nota += 1.0
        elif conectivos_encontrados >= 1:
            nota += 0.5
        
        # Verifica conclusão
        ultimo_paragrafo = paragrafos[-1].lower() if paragrafos else ""
        if any(palavra in ultimo_paragrafo for palavra in ["portanto", "assim", "conclui", "dessa forma"]):
            nota += 1.0
        
        return max(0, min(10, nota))

    def _avaliar_coesao_coerencia(self, texto: str) -> float:
        """Avalia coesão e coerência"""
        nota = 5.0
        
        # Verifica conectivos
        conectivos = [
            "além disso", "por outro lado", "entretanto", "contudo", "todavia",
            "primeiramente", "em seguida", "finalmente", "por fim"
        ]
        
        conectivos_encontrados = sum(1 for c in conectivos if c in texto.lower())
        nota += min(2.0, conectivos_encontrados * 0.5)
        
        # Verifica repetições excessivas
        palavras = texto.lower().split()
        palavras_unicas = set(palavras)
        
        if len(palavras_unicas) / len(palavras) > 0.7:
            nota += 1.0  # Boa variedade lexical
        elif len(palavras_unicas) / len(palavras) < 0.5:
            nota -= 1.0  # Muitas repetições
        
        return max(0, min(10, nota))

    def _avaliar_norma_culta(self, texto: str) -> float:
        """Avalia domínio da norma culta"""
        nota = 8.0  # Começa com nota alta
        
        # Verifica erros comuns
        erros_comuns = [
            ("mas", "mais"),  # Confusão mas/mais
            ("a", "há"),      # Confusão a/há
            ("onde", "aonde") # Confusão onde/aonde
        ]
        
        for erro, correto in erros_comuns:
            if erro in texto.lower() and correto not in texto.lower():
                nota -= 0.5
        
        # Verifica pontuação básica
        if texto.count('.') < 3:
            nota -= 1.0  # Poucos pontos finais
        
        if texto.count(',') < 2:
            nota -= 0.5  # Poucas vírgulas
        
        return max(0, min(10, nota))

    def _avaliar_proposta_intervencao(self, texto: str) -> float:
        """Avalia proposta de intervenção"""
        nota = 3.0
        
        # Verifica presença de proposta
        palavras_proposta = [
            "proposta", "solução", "medida", "ação", "política", "programa",
            "projeto", "iniciativa", "estratégia", "plano"
        ]
        
        propostas_encontradas = sum(1 for p in palavras_proposta if p in texto.lower())
        
        if propostas_encontradas >= 2:
            nota += 3.0
        elif propostas_encontradas >= 1:
            nota += 2.0
        
        # Verifica detalhamento
        if "governo" in texto.lower() or "estado" in texto.lower():
            nota += 1.0  # Menciona agente
        
        if "educação" in texto.lower() or "conscientização" in texto.lower():
            nota += 1.0  # Menciona meio
        
        return max(0, min(10, nota))

    def _gerar_feedback_detalhado(self, texto: str, notas: Dict) -> Dict:
        """Gera feedback detalhado por critério"""
        feedback = {}
        
        for criterio, nota in notas.items():
            if nota >= 8:
                nivel = "Excelente"
                cor = "🟢"
            elif nota >= 6:
                nivel = "Bom"
                cor = "🟡"
            elif nota >= 4:
                nivel = "Regular"
                cor = "🟠"
            else:
                nivel = "Precisa melhorar"
                cor = "🔴"
            
            feedback[criterio] = {
                "nota": nota,
                "nivel": nivel,
                "cor": cor,
                "comentario": self._gerar_comentario_criterio(criterio, nota)
            }
        
        return feedback

    def _gerar_comentario_criterio(self, criterio: str, nota: float) -> str:
        """Gera comentário específico para cada critério"""
        comentarios = {
            "Adequação ao Tema": {
                "alta": "Excelente desenvolvimento do tema proposto!",
                "media": "Tema desenvolvido adequadamente, mas pode ser mais aprofundado.",
                "baixa": "O tema precisa ser mais bem desenvolvido e focado."
            },
            "Adequação ao Tipo Textual": {
                "alta": "Estrutura dissertativa muito bem organizada!",
                "media": "Boa estrutura, mas alguns elementos podem ser melhorados.",
                "baixa": "A estrutura dissertativa precisa ser mais bem definida."
            },
            "Coesão e Coerência": {
                "alta": "Excelente articulação entre as ideias!",
                "media": "Boa coesão, mas alguns conectivos podem ser melhorados.",
                "baixa": "As ideias precisam ser melhor articuladas com conectivos adequados."
            },
            "Domínio da Norma Culta": {
                "alta": "Excelente domínio da norma culta da língua!",
                "media": "Bom domínio, com alguns desvios menores.",
                "baixa": "Há vários desvios da norma culta que precisam ser corrigidos."
            },
            "Proposta de Intervenção": {
                "alta": "Proposta muito bem elaborada e detalhada!",
                "media": "Boa proposta, mas pode ser mais detalhada.",
                "baixa": "A proposta de intervenção precisa ser mais bem desenvolvida."
            }
        }
        
        if nota >= 7:
            nivel = "alta"
        elif nota >= 5:
            nivel = "media"
        else:
            nivel = "baixa"
        
        return comentarios.get(criterio, {}).get(nivel, "Comentário não disponível.")

    def _gerar_sugestoes(self, texto: str, notas: Dict) -> List[str]:
        """Gera sugestões de melhoria"""
        sugestoes = []
        
        for criterio, nota in notas.items():
            if nota < 6:
                if criterio == "Adequação ao Tema":
                    sugestoes.append("📝 Desenvolva mais o tema central da redação")
                elif criterio == "Adequação ao Tipo Textual":
                    sugestoes.append("📋 Organize melhor a estrutura dissertativa (introdução, desenvolvimento, conclusão)")
                elif criterio == "Coesão e Coerência":
                    sugestoes.append("🔗 Use mais conectivos para ligar as ideias (além disso, portanto, entretanto)")
                elif criterio == "Domínio da Norma Culta":
                    sugestoes.append("✏️ Revise a gramática, ortografia e pontuação")
                elif criterio == "Proposta de Intervenção":
                    sugestoes.append("💡 Elabore uma proposta de solução mais detalhada")
        
        return sugestoes

    def _identificar_pontos(self, notas: Dict) -> Tuple[List[str], List[str]]:
        """Identifica pontos fortes e fracos"""
        pontos_fortes = []
        pontos_fracos = []
        
        for criterio, nota in notas.items():
            if nota >= 7:
                pontos_fortes.append(f"✅ {criterio}")
            elif nota < 5:
                pontos_fracos.append(f"❌ {criterio}")
        
        return pontos_fortes, pontos_fracos

    def gerar_exemplo_redacao(self, tema: str, banca: str = "CESPE/CEBRASPE") -> Dict:
        """Gera exemplo de redação baseado no tema e banca"""
        if tema in self.temas_banco:
            info_tema = self.temas_banco[tema]
            estilo_banca = self.bancas_estilo.get(banca, self.bancas_estilo["CESPE/CEBRASPE"])
            
            exemplo = self._construir_exemplo_redacao(tema, info_tema, estilo_banca)
            
            return {
                "tema": tema,
                "banca": banca,
                "exemplo": exemplo,
                "dicas_especificas": estilo_banca["caracteristicas"],
                "extensao_recomendada": estilo_banca["extensao"]
            }
        
        return {"erro": "Tema não encontrado no banco de dados"}

    def _construir_exemplo_redacao(self, tema: str, info_tema: Dict, estilo_banca: Dict) -> str:
        """Constrói exemplo de redação"""
        subtema = info_tema["subtemas"][0]  # Pega o primeiro subtema
        argumentos = info_tema["argumentos_chave"]
        
        exemplo = f"""
TEMA: {subtema}

INTRODUÇÃO:
O {subtema.lower()} representa um dos grandes desafios contemporâneos da sociedade brasileira. Diante da complexidade dessa questão, torna-se fundamental analisar suas múltiplas dimensões e propor soluções efetivas que promovam o desenvolvimento sustentável e a melhoria da qualidade de vida da população.

DESENVOLVIMENTO 1:
Em primeiro lugar, é importante destacar que {argumentos[0].lower()} constitui um elemento essencial para o enfrentamento dessa problemática. A experiência de países desenvolvidos demonstra que políticas bem estruturadas nessa área podem gerar resultados significativos a médio e longo prazo.

DESENVOLVIMENTO 2:
Além disso, {argumentos[1].lower()} emerge como outro fator crucial para o sucesso das iniciativas. A participação ativa da sociedade civil, aliada ao comprometimento do poder público, cria um ambiente propício para a implementação de mudanças estruturais necessárias.

CONCLUSÃO:
Portanto, o enfrentamento do {subtema.lower()} exige uma abordagem integrada que combine {argumentos[0].lower()} e {argumentos[1].lower()}. Cabe ao Estado, em parceria com a sociedade, desenvolver políticas públicas eficazes que garantam não apenas a solução dos problemas atuais, mas também a prevenção de futuras dificuldades nessa área.
"""
        
        return exemplo.strip()

    def analisar_tema_por_banca(self, tema: str) -> Dict:
        """Analisa como diferentes bancas abordam um tema"""
        analise = {}
        
        for banca, info in self.bancas_estilo.items():
            if tema.lower() in [t.lower() for t in info["temas_frequentes"]]:
                analise[banca] = {
                    "probabilidade": "Alta",
                    "abordagem": info["caracteristicas"],
                    "dicas": f"Para {banca}, foque em {info['tipo_preferido'].lower()} com {info['extensao']}"
                }
            else:
                analise[banca] = {
                    "probabilidade": "Média",
                    "abordagem": info["caracteristicas"],
                    "dicas": f"Mesmo não sendo tema frequente, prepare-se com {info['tipo_preferido'].lower()}"
                }
        
        return analise

def render_redacao_system():
    """Renderiza o sistema completo de redação"""
    st.header("✍️ Sistema de Redação Completo")
    
    sistema = RedacaoSystem()
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Corretor Automático",
        "📚 Exemplos por Banca",
        "🎯 Análise de Temas",
        "💡 Dicas e Estratégias"
    ])
    
    with tab1:
        st.subheader("📝 Corretor Automático de Redação")
        
        # Seleção da banca
        banca_selecionada = st.selectbox(
            "🏛️ Selecione a banca:",
            options=list(sistema.bancas_estilo.keys()),
            help="Cada banca tem critérios específicos de avaliação"
        )
        
        # Área de texto para redação
        redacao_texto = st.text_area(
            "✍️ Cole sua redação aqui:",
            height=300,
            placeholder="Digite ou cole o texto da sua redação aqui para correção automática..."
        )
        
        if st.button("🔍 Corrigir Redação", type="primary"):
            if redacao_texto.strip():
                with st.spinner("🤖 Analisando redação..."):
                    resultado = sistema.corrigir_redacao(redacao_texto, banca_selecionada)
                    
                    # Nota final
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.metric(
                            "📊 Nota Final",
                            f"{resultado['nota_final']:.1f}/10",
                            delta=f"{resultado['nota_final'] - 5:.1f}" if resultado['nota_final'] != 5 else None
                        )
                    
                    # Notas por critério
                    st.subheader("📋 Avaliação por Critério")
                    
                    for criterio, info in sistema.criterios_avaliacao.items():
                        nota = resultado['notas_criterios'][criterio]
                        feedback = resultado['feedback_detalhado'][criterio]
                        
                        col1, col2, col3 = st.columns([3, 1, 2])
                        
                        with col1:
                            st.write(f"**{criterio}** (Peso: {info['peso']}%)")
                            st.write(f"_{info['descricao']}_")
                        
                        with col2:
                            st.metric("Nota", f"{nota:.1f}/10")
                        
                        with col3:
                            st.write(f"{feedback['cor']} {feedback['nivel']}")
                            st.write(feedback['comentario'])
                    
                    # Gráfico de desempenho
                    fig_radar = go.Figure()
                    
                    criterios = list(resultado['notas_criterios'].keys())
                    notas = list(resultado['notas_criterios'].values())
                    
                    fig_radar.add_trace(go.Scatterpolar(
                        r=notas,
                        theta=criterios,
                        fill='toself',
                        name='Sua Redação'
                    ))
                    
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 10]
                            )),
                        showlegend=True,
                        title="📊 Gráfico de Desempenho por Critério"
                    )
                    
                    st.plotly_chart(fig_radar, use_container_width=True)
                    
                    # Feedback detalhado
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        if resultado['pontos_fortes']:
                            st.success("**🎯 Pontos Fortes:**")
                            for ponto in resultado['pontos_fortes']:
                                st.write(ponto)
                    
                    with col2:
                        if resultado['pontos_fracos']:
                            st.error("**⚠️ Pontos a Melhorar:**")
                            for ponto in resultado['pontos_fracos']:
                                st.write(ponto)
                    
                    # Sugestões de melhoria
                    if resultado['sugestoes_melhoria']:
                        st.subheader("💡 Sugestões de Melhoria")
                        for sugestao in resultado['sugestoes_melhoria']:
                            st.info(sugestao)
            
            else:
                st.warning("⚠️ Por favor, digite o texto da redação para correção.")
    
    with tab2:
        st.subheader("📚 Exemplos de Redação por Banca")
        
        col1, col2 = st.columns(2)
        
        with col1:
            tema_selecionado = st.selectbox(
                "🎯 Selecione o tema:",
                options=list(sistema.temas_banco.keys())
            )
        
        with col2:
            banca_exemplo = st.selectbox(
                "🏛️ Selecione a banca:",
                options=list(sistema.bancas_estilo.keys()),
                key="banca_exemplo"
            )
        
        if st.button("📝 Gerar Exemplo"):
            exemplo = sistema.gerar_exemplo_redacao(tema_selecionado, banca_exemplo)
            
            if "erro" not in exemplo:
                st.success(f"**📋 Exemplo para {banca_exemplo}**")
                
                # Informações da banca
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info(f"**📏 Extensão:** {exemplo['extensao_recomendada']}")
                
                with col2:
                    st.info(f"**📝 Tema:** {exemplo['tema']}")
                
                # Exemplo de redação
                st.text_area(
                    "✍️ Exemplo de Redação:",
                    value=exemplo['exemplo'],
                    height=400,
                    disabled=True
                )
                
                # Dicas específicas
                st.subheader("💡 Dicas Específicas da Banca")
                for dica in exemplo['dicas_especificas']:
                    st.write(f"• {dica}")
            
            else:
                st.error(exemplo['erro'])
    
    with tab3:
        st.subheader("🎯 Análise de Temas por Banca")
        
        tema_analise = st.selectbox(
            "📚 Selecione um tema para análise:",
            options=list(sistema.temas_banco.keys()),
            key="tema_analise"
        )
        
        if st.button("🔍 Analisar Tema"):
            analise = sistema.analisar_tema_por_banca(tema_analise)
            
            st.subheader(f"📊 Análise: {tema_analise}")
            
            for banca, info in analise.items():
                with st.expander(f"🏛️ {banca} - Probabilidade: {info['probabilidade']}"):
                    st.write("**🎯 Abordagem Típica:**")
                    for abordagem in info['abordagem']:
                        st.write(f"• {abordagem}")
                    
                    st.info(f"💡 **Dica:** {info['dicas']}")
        
        # Informações dos temas
        st.subheader("📚 Banco de Temas")
        
        for tema, info in sistema.temas_banco.items():
            with st.expander(f"📖 {tema}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write("**🎯 Subtemas Frequentes:**")
                    for subtema in info['subtemas']:
                        st.write(f"• {subtema}")
                
                with col2:
                    st.write("**💡 Argumentos-Chave:**")
                    for argumento in info['argumentos_chave']:
                        st.write(f"• {argumento}")
    
    with tab4:
        st.subheader("💡 Dicas e Estratégias")
        
        # Dicas gerais
        st.write("### 📝 Dicas Gerais para Redação")
        
        dicas_gerais = [
            "**Planejamento:** Dedique 5-10 minutos para planejar antes de escrever",
            "**Estrutura:** Mantenha sempre introdução, desenvolvimento e conclusão",
            "**Tema:** Leia o tema com atenção e não fuja do assunto",
            "**Argumentação:** Use dados, exemplos e citações para fortalecer seus argumentos",
            "**Revisão:** Reserve tempo para revisar gramática e coerência",
            "**Proposta:** Sempre apresente uma solução viável e detalhada",
            "**Linguagem:** Use linguagem formal e evite gírias ou expressões coloquiais",
            "**Conectivos:** Use conectivos para ligar ideias e parágrafos"
        ]
        
        for dica in dicas_gerais:
            st.info(dica)
        
        # Dicas por banca
        st.write("### 🏛️ Estratégias Específicas por Banca")
        
        for banca, info in sistema.bancas_estilo.items():
            with st.expander(f"📋 Estratégias para {banca}"):
                st.write(f"**Tipo Preferido:** {info['tipo_preferido']}")
                st.write(f"**Extensão:** {info['extensao']}")
                
                st.write("**Características:**")
                for carac in info['caracteristicas']:
                    st.write(f"• {carac}")
                
                st.write("**Temas Frequentes:**")
                for tema in info['temas_frequentes']:
                    st.write(f"• {tema}")
        
        # Cronograma de estudos para redação
        st.write("### 📅 Cronograma de Estudos - Redação")
        
        cronograma_redacao = {
            "Semana 1-2": "Revisão de estrutura dissertativa e tipos de texto",
            "Semana 3-4": "Prática de introduções e conclusões",
            "Semana 5-6": "Desenvolvimento de argumentação",
            "Semana 7-8": "Prática de propostas de intervenção",
            "Semana 9-10": "Revisão gramatical e correção de textos",
            "Semana 11-12": "Simulados e correção intensiva"
        }
        
        for periodo, atividade in cronograma_redacao.items():
            st.write(f"**{periodo}:** {atividade}")