"""
Página de Redação - Sistema Avançado por Banca
"""

import streamlit as st
import json
import sys
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from tools.writing_tool import WritingTool

def render_redacao_page():
    """Renderiza a página completa de redação"""
    
    st.title("✍️ Sistema Avançado de Redação por Banca")
    st.markdown("Avaliação especializada baseada nos padrões específicos de cada banca organizadora")
    
    # Inicializar ferramenta
    writing_tool = WritingTool()
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Avaliação de Redação",
        "📚 Banco de Temas", 
        "📊 Histórico e Progresso",
        "💡 Dicas por Banca"
    ])
    
    with tab1:
        render_essay_evaluation(writing_tool)
    
    with tab2:
        render_tema_bank(writing_tool)
    
    with tab3:
        render_progress_tracking()
    
    with tab4:
        render_banca_tips(writing_tool)

def render_essay_evaluation(writing_tool):
    """Renderiza seção de avaliação de redação"""
    
    st.subheader("📝 Avaliação Personalizada por Banca")
    
    # Configurações da avaliação
    col1, col2, col3 = st.columns(3)
    
    with col1:
        banca = st.selectbox(
            "🏛️ Banca Organizadora",
            ["CESPE", "FCC", "VUNESP", "FGV", "IBFC"],
            help="Cada banca tem critérios e padrões específicos"
        )
    
    with col2:
        # Obter tipos disponíveis para a banca
        tipos_disponiveis = writing_tool.banca_patterns[banca]['tipos_redacao']
        tipo_redacao = st.selectbox(
            "📄 Tipo de Redação",
            tipos_disponiveis,
            help="Tipo de texto exigido pela banca"
        )
    
    with col3:
        tema_personalizado = st.text_input(
            "🎯 Tema (opcional)",
            placeholder="Ex: Sustentabilidade no setor público",
            help="Deixe em branco para avaliação geral"
        )
    
    # Área de texto para redação
    st.markdown("### ✍️ Sua Redação")
    
    # Mostrar informações da banca selecionada
    banca_info = writing_tool.banca_patterns[banca]
    
    with st.expander(f"ℹ️ Informações sobre {banca}", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Extensão:** {banca_info['extensao_minima']}-{banca_info['extensao_maxima']} linhas")
            st.write(f"**Estrutura:** {banca_info['estrutura_preferida']}")
            st.write(f"**Estilo:** {banca_info['estilo']}")
        
        with col2:
            st.write("**Características valorizadas:**")
            for caracteristica in banca_info['caracteristicas']:
                st.write(f"• {caracteristica.replace('_', ' ').title()}")
    
    # Editor de texto
    redacao_texto = st.text_area(
        "Digite ou cole sua redação aqui:",
        height=400,
        placeholder=f"""Escreva sua redação seguindo os padrões da {banca}:

• Estrutura: {banca_info['estrutura_preferida']}
• Estilo: {banca_info['estilo']}
• Extensão: {banca_info['extensao_minima']}-{banca_info['extensao_maxima']} linhas

Dica: Use linguagem formal e argumentação consistente.""",
        help=f"Redação será avaliada pelos critérios específicos da {banca}"
    )
    
    # Botão de avaliação
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("🚀 Avaliar Redação", use_container_width=True, type="primary"):
            if redacao_texto.strip():
                with st.spinner(f"🔄 Avaliando redação pelos padrões da {banca}..."):
                    # Avaliar redação
                    resultado = writing_tool.evaluate_essay_by_banca(
                        redacao_texto, 
                        banca, 
                        tipo_redacao, 
                        tema_personalizado or None
                    )
                    
                    if "error" in resultado:
                        st.error(f"❌ {resultado['error']}")
                    else:
                        # Salvar resultado na sessão
                        if 'redacao_historico' not in st.session_state:
                            st.session_state.redacao_historico = []
                        
                        st.session_state.redacao_historico.append(resultado)
                        
                        # Exibir resultados
                        render_evaluation_results(resultado)
            else:
                st.warning("⚠️ Digite uma redação para avaliar.")

def render_evaluation_results(resultado):
    """Renderiza resultados da avaliação"""
    
    st.markdown("---")
    st.subheader("📊 Resultado da Avaliação")
    
    # Score principal
    score_final = resultado['score_final']
    
    # Determinar cor e status baseado na nota
    if score_final >= 8.0:
        cor = "green"
        status = "🌟 Excelente"
    elif score_final >= 7.0:
        cor = "blue"
        status = "✅ Bom"
    elif score_final >= 6.0:
        cor = "orange"
        status = "⚠️ Regular"
    else:
        cor = "red"
        status = "🚨 Precisa Melhorar"
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Nota Final", f"{score_final}/10", delta=status)
    
    with col2:
        st.metric("🏛️ Banca", resultado['banca'])
    
    with col3:
        st.metric("📄 Tipo", resultado['tipo_redacao'].replace('_', ' ').title())
    
    with col4:
        analise = resultado['analise_preliminar']
        st.metric("📝 Palavras", analise['num_palavras'])
    
    # Gráfico de scores por critério
    st.subheader("📈 Desempenho por Critério")
    
    criterios = []
    scores = []
    pesos = []
    
    for criterio, data in resultado['scores_por_criterio'].items():
        criterios.append(criterio.replace('_', ' ').title())
        scores.append(data['score_bruto'] * 10)  # Converter para escala 0-10
        pesos.append(data['peso'])
    
    # Criar gráfico de barras
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=criterios,
        y=scores,
        text=[f"{score:.1f}" for score in scores],
        textposition='auto',
        marker_color=['green' if s >= 8 else 'orange' if s >= 6 else 'red' for s in scores],
        name='Pontuação'
    ))
    
    fig.update_layout(
        title="Pontuação por Critério de Avaliação",
        xaxis_title="Critérios",
        yaxis_title="Pontuação (0-10)",
        yaxis=dict(range=[0, 10]),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Feedback detalhado
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💪 Pontos Fortes")
        for ponto in resultado['pontos_fortes']:
            st.success(f"✅ {ponto}")
        
        if not resultado['pontos_fortes']:
            st.info("Continue praticando para desenvolver pontos fortes!")
    
    with col2:
        st.subheader("⚠️ Pontos a Melhorar")
        for ponto in resultado['pontos_fracos']:
            st.warning(f"⚠️ {ponto}")
        
        if not resultado['pontos_fracos']:
            st.success("🎉 Nenhum ponto crítico identificado!")
    
    # Sugestões de melhoria
    if resultado['sugestoes_melhoria']:
        st.subheader("💡 Sugestões de Melhoria")
        
        for i, sugestao in enumerate(resultado['sugestoes_melhoria'], 1):
            st.markdown(f"**{i}.** {sugestao}")
    
    # Adequação à banca
    st.subheader(f"🎯 Adequação aos Padrões da {resultado['banca']}")
    
    adequacao = resultado['adequacao_banca']
    
    for aspecto, avaliacao in adequacao.items():
        if isinstance(avaliacao, dict) and 'status' in avaliacao:
            if avaliacao['status'] == 'adequado':
                st.success(f"✅ {aspecto.replace('_', ' ').title()}: {avaliacao.get('comentario', 'Adequado')}")
            else:
                st.warning(f"⚠️ {aspecto.replace('_', ' ').title()}: {avaliacao.get('comentario', 'Precisa ajustar')}")
    
    # Feedback detalhado por critério
    with st.expander("📋 Feedback Detalhado por Critério"):
        for criterio, feedback in resultado['feedback_detalhado'].items():
            st.markdown(f"**{criterio.replace('_', ' ').title()}:**")
            st.write(feedback)
            st.markdown("---")

def render_tema_bank(writing_tool):
    """Renderiza banco de temas"""
    
    st.subheader("📚 Banco de Temas por Banca")
    st.markdown("Temas reais de concursos anteriores organizados por banca")
    
    # Seletor de banca
    banca_selecionada = st.selectbox(
        "Selecione a banca:",
        list(writing_tool.tema_bank.keys()),
        key="tema_banca"
    )
    
    temas = writing_tool.tema_bank[banca_selecionada]
    
    if temas:
        st.markdown(f"### 📋 Temas da {banca_selecionada}")
        
        for i, tema_info in enumerate(temas, 1):
            with st.expander(f"📝 Tema {i}: {tema_info['tema']}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Tipo:** {tema_info['tipo'].replace('_', ' ').title()}")
                    st.write(f"**Ano:** {tema_info['ano']}")
                    st.write(f"**Cargo:** {tema_info['cargo']}")
                
                with col2:
                    if st.button(f"🚀 Usar este tema", key=f"tema_{i}"):
                        st.session_state.tema_selecionado = tema_info['tema']
                        st.success(f"✅ Tema selecionado: {tema_info['tema']}")
                
                st.markdown("**Contexto:**")
                st.write(tema_info['contexto'])
    else:
        st.info(f"Nenhum tema disponível para {banca_selecionada} no momento.")
    
    # Sugestão de tema personalizado
    st.markdown("### 💡 Sugerir Novo Tema")
    
    with st.form("novo_tema"):
        novo_tema = st.text_input("Tema proposto:")
        contexto = st.text_area("Contexto/Instrução:")
        tipo_sugerido = st.selectbox("Tipo de redação:", ["dissertativo-argumentativo", "texto_tecnico", "relatorio"])
        
        if st.form_submit_button("📤 Enviar Sugestão"):
            if novo_tema and contexto:
                st.success("✅ Sugestão enviada! Obrigado pela contribuição.")
                # Aqui poderia salvar a sugestão em um arquivo ou banco de dados
            else:
                st.warning("⚠️ Preencha tema e contexto.")

def render_progress_tracking():
    """Renderiza acompanhamento de progresso"""
    
    st.subheader("📊 Histórico e Progresso")
    
    if 'redacao_historico' not in st.session_state or not st.session_state.redacao_historico:
        st.info("📝 Nenhuma redação avaliada ainda. Faça sua primeira avaliação na aba 'Avaliação de Redação'!")
        return
    
    historico = st.session_state.redacao_historico
    
    # Métricas gerais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Redações Avaliadas", len(historico))
    
    with col2:
        media_geral = sum(r['score_final'] for r in historico) / len(historico)
        st.metric("📊 Média Geral", f"{media_geral:.1f}/10")
    
    with col3:
        ultima_nota = historico[-1]['score_final']
        if len(historico) > 1:
            penultima_nota = historico[-2]['score_final']
            delta = ultima_nota - penultima_nota
            st.metric("📈 Última Nota", f"{ultima_nota:.1f}/10", delta=f"{delta:+.1f}")
        else:
            st.metric("📈 Última Nota", f"{ultima_nota:.1f}/10")
    
    with col4:
        bancas_usadas = len(set(r['banca'] for r in historico))
        st.metric("🏛️ Bancas Praticadas", bancas_usadas)
    
    # Gráfico de evolução
    st.subheader("📈 Evolução das Notas")
    
    datas = [datetime.fromisoformat(r['timestamp']).strftime('%d/%m %H:%M') for r in historico]
    notas = [r['score_final'] for r in historico]
    bancas = [r['banca'] for r in historico]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=datas,
        y=notas,
        mode='lines+markers',
        name='Evolução',
        text=bancas,
        hovertemplate='<b>%{text}</b><br>Nota: %{y:.1f}<br>Data: %{x}<extra></extra>'
    ))
    
    fig.add_hline(y=7.0, line_dash="dash", line_color="green", annotation_text="Meta: 7.0")
    fig.add_hline(y=6.0, line_dash="dash", line_color="orange", annotation_text="Mínimo: 6.0")
    
    fig.update_layout(
        title="Evolução das Notas ao Longo do Tempo",
        xaxis_title="Data/Hora",
        yaxis_title="Nota (0-10)",
        yaxis=dict(range=[0, 10])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Análise por banca
    st.subheader("🏛️ Desempenho por Banca")
    
    desempenho_banca = {}
    for r in historico:
        banca = r['banca']
        if banca not in desempenho_banca:
            desempenho_banca[banca] = []
        desempenho_banca[banca].append(r['score_final'])
    
    for banca, notas in desempenho_banca.items():
        media = sum(notas) / len(notas)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**{banca}**")
        with col2:
            st.write(f"Média: {media:.1f}")
        with col3:
            st.write(f"Redações: {len(notas)}")

def render_banca_tips(writing_tool):
    """Renderiza dicas específicas por banca"""
    
    st.subheader("💡 Dicas Específicas por Banca")
    st.markdown("Estratégias e características valorizadas por cada banca organizadora")
    
    banca_selecionada = st.selectbox(
        "Selecione a banca para ver dicas:",
        list(writing_tool.banca_patterns.keys()),
        key="tips_banca"
    )
    
    banca_config = writing_tool.banca_patterns[banca_selecionada]
    
    # Informações gerais
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 📋 Características da {banca_selecionada}")
        st.write(f"**Extensão:** {banca_config['extensao_minima']}-{banca_config['extensao_maxima']} linhas")
        st.write(f"**Estrutura preferida:** {banca_config['estrutura_preferida']}")
        st.write(f"**Estilo:** {banca_config['estilo']}")
        
        st.markdown("**Tipos de redação:**")
        for tipo in banca_config['tipos_redacao']:
            st.write(f"• {tipo.replace('_', ' ').title()}")
    
    with col2:
        st.markdown("### 🎯 Características Valorizadas")
        for caracteristica in banca_config['caracteristicas']:
            st.write(f"✅ {caracteristica.replace('_', ' ').title()}")
    
    # Dicas específicas por banca
    dicas_especificas = {
        'CESPE': [
            "Use linguagem técnica e jurídica quando apropriado",
            "Cite legislação e jurisprudência quando relevante",
            "Mantenha impessoalidade e objetividade",
            "Estrutura clássica: introdução, desenvolvimento, conclusão",
            "Evite prolixidade - seja direto e preciso"
        ],
        'FCC': [
            "Desenvolva argumentos extensamente com exemplos",
            "Use norma culta rigorosamente",
            "Varie os conectivos para mostrar domínio linguístico",
            "Conclusão deve ser propositiva",
            "Exemplificação abundante é valorizada"
        ],
        'VUNESP': [
            "Contextualize socialmente o tema",
            "Use exemplos atuais e relevantes",
            "Linguagem acessível mas formal",
            "Propostas viáveis e realistas",
            "Demonstre consciência cidadã"
        ],
        'FGV': [
            "Análise profunda e multifacetada",
            "Considere múltiplas perspectivas",
            "Fundamentação teórica sólida",
            "Raciocínio lógico bem estruturado",
            "Síntese conclusiva bem elaborada"
        ],
        'IBFC': [
            "Clareza e objetividade são essenciais",
            "Argumentos diretos e bem fundamentados",
            "Linguagem simples mas formal",
            "Estrutura clara e bem definida",
            "Conclusão objetiva e direta"
        ]
    }
    
    st.markdown(f"### 💡 Dicas Específicas para {banca_selecionada}")
    
    for i, dica in enumerate(dicas_especificas[banca_selecionada], 1):
        st.markdown(f"**{i}.** {dica}")
    
    # Pesos dos critérios
    st.markdown("### ⚖️ Peso dos Critérios de Avaliação")
    
    pesos = banca_config['peso_criterios']
    
    criterios = list(pesos.keys())
    valores = [pesos[c] * 100 for c in criterios]  # Converter para porcentagem
    
    fig = px.pie(
        values=valores,
        names=[c.replace('_', ' ').title() for c in criterios],
        title=f"Distribuição dos Pesos - {banca_selecionada}"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Exemplo de estrutura
    st.markdown("### 📝 Exemplo de Estrutura Recomendada")
    
    estruturas_exemplo = {
        'CESPE': """
**Parágrafo 1 - Introdução (3-4 linhas)**
- Contextualização do tema
- Apresentação da tese

**Parágrafo 2 - Desenvolvimento I (6-8 linhas)**
- Primeiro argumento
- Fundamentação técnica/jurídica

**Parágrafo 3 - Desenvolvimento II (6-8 linhas)**
- Segundo argumento
- Exemplificação prática

**Parágrafo 4 - Conclusão (3-4 linhas)**
- Retomada da tese
- Síntese dos argumentos
        """,
        'FCC': """
**Parágrafo 1 - Introdução (4-5 linhas)**
- Contextualização ampla
- Apresentação da tese

**Parágrafo 2 - Desenvolvimento I (7-9 linhas)**
- Primeiro argumento desenvolvido
- Exemplos e fundamentação

**Parágrafo 3 - Desenvolvimento II (7-9 linhas)**
- Segundo argumento desenvolvido
- Mais exemplos e detalhamento

**Parágrafo 4 - Desenvolvimento III (6-8 linhas)**
- Terceiro argumento ou contraposição
- Análise crítica

**Parágrafo 5 - Conclusão (4-6 linhas)**
- Síntese dos argumentos
- Proposta de solução
        """
    }
    
    if banca_selecionada in estruturas_exemplo:
        st.markdown(estruturas_exemplo[banca_selecionada])
    else:
        st.info(f"Estrutura específica para {banca_selecionada} em desenvolvimento.")

if __name__ == "__main__":
    render_redacao_page()
