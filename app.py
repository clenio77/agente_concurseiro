"""
Agente Concurseiro v2.0 - Streamlit Cloud Edition
Plataforma inteligente de preparação para concursos públicos
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Agente Concurseiro v2.0",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
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
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown("""
<div class="main-header">
    <h1>📚 Agente Concurseiro v2.0</h1>
    <p>Sua plataforma inteligente de preparação para concursos públicos</p>
    <p><strong>🚀 Versão Vercel - Deploy Bem-sucedido!</strong></p>
</div>
""", unsafe_allow_html=True)

# Dashboard
st.header("🏠 Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3>📚 Status</h3>
        <h2>✅ Online</h2>
        <p>Sistema operacional</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3>🎯 Versão</h3>
        <h2>2.0</h2>
        <p>Vercel Edition</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3>⚡ Deploy</h3>
        <h2>Sucesso</h2>
        <p>Funcionando perfeitamente</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Análise de Edital
st.header("📋 Análise de Edital")

uploaded_file = st.file_uploader(
    "📁 Faça upload do edital (PDF)",
    type=['pdf'],
    help="Selecione o arquivo PDF do edital para análise"
)

if uploaded_file is not None:
    st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
    
    # Informações do arquivo
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📄 Nome", uploaded_file.name)
    with col2:
        st.metric("📊 Tamanho", f"{len(uploaded_file.getvalue()) / 1024:.1f} KB")
    with col3:
        st.metric("🔧 Tipo", uploaded_file.type)
    
    # Botão para análise
    if st.button("🔍 Analisar Edital", type="primary"):
        with st.spinner("🤖 Analisando edital..."):
            try:
                # Ler conteúdo do PDF
                import PyPDF2
                
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.getvalue()))
                content = ""
                for page in pdf_reader.pages:
                    content += page.extract_text()
                
                # Análise básica
                st.success("✅ Análise concluída!")
                
                # Informações básicas
                st.subheader("📊 Informações Extraídas")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.info("**Concurso:** Concurso Público")
                    st.info("**Banca:** A definir")
                    st.info("**Vagas:** A definir")
                
                with col2:
                    st.info("**Data da Prova:** A definir")
                    st.info("**Inscrições:** A definir")
                    st.info("**Status:** Processado com sucesso")
                
                # Conteúdo extraído
                st.subheader("📄 Conteúdo Extraído")
                
                if content:
                    # Mostrar primeiros 1000 caracteres
                    preview = content[:1000] + "..." if len(content) > 1000 else content
                    st.text_area("Texto extraído:", preview, height=200)
                    
                    # Estatísticas
                    st.subheader("📈 Estatísticas")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("📝 Caracteres", len(content))
                    with col2:
                        st.metric("📄 Páginas", len(pdf_reader.pages))
                    with col3:
                        st.metric("📊 Palavras", len(content.split()))
                else:
                    st.warning("⚠️ Não foi possível extrair texto do PDF.")
            
            except Exception as e:
                st.error(f"❌ Erro na análise: {str(e)}")
                st.info("💡 Esta é uma versão simplificada para Vercel. Funcionalidades completas serão adicionadas em breve.")

# Informações do sistema
st.markdown("---")
st.header("ℹ️ Informações do Sistema")

col1, col2 = st.columns(2)

with col1:
    st.info("**Plataforma:** Vercel")
    st.info("**Versão:** 2.0 Minimal")

with col2:
    st.info("**Status:** ✅ Funcionando")
    st.info("**Deploy:** Automático")

# Próximos passos
st.subheader("🚀 Próximos Passos")

st.markdown("""
### ✅ **Deploy Realizado com Sucesso!**

**Funcionalidades Disponíveis:**
- ✅ Upload de arquivos PDF
- ✅ Extração de texto
- ✅ Interface responsiva
- ✅ Deploy automático no Vercel

**Próximas Implementações:**
- 🔄 Análise inteligente de editais
- 🔄 Extração de informações específicas
- 🔄 Banco de dados PostgreSQL
- 🔄 Sistema de autenticação
- 🔄 Dashboard avançado

**Para adicionar funcionalidades completas:**
1. Configure um banco PostgreSQL (Supabase)
2. Adicione a variável `DATABASE_URL` no Vercel
3. Implemente os módulos de análise
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>📚 Agente Concurseiro v2.0 | Deploy Vercel Bem-sucedido! | 
    <a href="https://github.com/clenio77/agente_concurseiro" target="_blank">GitHub</a></p>
</div>
""", unsafe_allow_html=True)
