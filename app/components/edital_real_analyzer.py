"""
Analisador Real de Edital - Agente Concurseiro v2.0
Sistema que realmente extrai informações específicas do edital
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import re
from typing import Dict, List, Tuple, Optional
import PyPDF2
import io
import json
from datetime import datetime

# Importa bibliotecas avançadas se disponíveis
try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

class EditalRealAnalyzer:
    """Analisador que extrai informações reais do edital"""
    
    def __init__(self):
        self.debug_mode = True
        
    def extrair_texto_completo(self, arquivo_pdf) -> str:
        """Extrai texto completo do PDF usando o melhor método disponível"""
        arquivo_pdf.seek(0)
        
        # Tenta PyMuPDF primeiro (mais preciso)
        if PYMUPDF_AVAILABLE:
            try:
                st.info("🔍 Usando PyMuPDF para extração...")
                doc = fitz.open(stream=arquivo_pdf.read(), filetype="pdf")
                
                texto_completo = ""
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    texto_pagina = page.get_text()
                    
                    if texto_pagina.strip():
                        texto_completo += f"\n=== PÁGINA {page_num + 1} ===\n"
                        texto_completo += texto_pagina + "\n"
                
                doc.close()
                
                if len(texto_completo) > 1000:
                    st.success(f"✅ PyMuPDF: {len(texto_completo)} caracteres extraídos")
                    return texto_completo
                    
            except Exception as e:
                st.warning(f"⚠️ PyMuPDF falhou: {str(e)}")
        
        # Tenta pdfplumber
        if PDFPLUMBER_AVAILABLE:
            try:
                st.info("🔍 Usando pdfplumber...")
                arquivo_pdf.seek(0)
                
                with pdfplumber.open(io.BytesIO(arquivo_pdf.read())) as pdf:
                    texto_completo = ""
                    for i, page in enumerate(pdf.pages):
                        texto_pagina = page.extract_text()
                        
                        if texto_pagina:
                            texto_completo += f"\n=== PÁGINA {i + 1} ===\n"
                            texto_completo += texto_pagina + "\n"
                
                if len(texto_completo) > 1000:
                    st.success(f"✅ pdfplumber: {len(texto_completo)} caracteres extraídos")
                    return texto_completo
                    
            except Exception as e:
                st.warning(f"⚠️ pdfplumber falhou: {str(e)}")
        
        # Fallback para PyPDF2
        try:
            st.info("🔍 Usando PyPDF2...")
            arquivo_pdf.seek(0)
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(arquivo_pdf.read()))
            
            texto_completo = ""
            for i, pagina in enumerate(pdf_reader.pages):
                texto_pagina = pagina.extract_text()
                
                if texto_pagina.strip():
                    texto_completo += f"\n=== PÁGINA {i + 1} ===\n"
                    texto_completo += texto_pagina + "\n"
            
            st.success(f"✅ PyPDF2: {len(texto_completo)} caracteres extraídos")
            return texto_completo
            
        except Exception as e:
            st.error(f"❌ Todos os métodos falharam: {str(e)}")
            return ""
    
    def analisar_edital_real(self, texto: str) -> Dict:
        """Análise real do edital com extração específica"""
        
        st.subheader("🔍 Análise Real do Edital")
        
        # Mostra preview do texto para debug
        if self.debug_mode:
            with st.expander("🔧 Debug - Preview do Texto Extraído"):
                st.text_area("Primeiros 2000 caracteres:", texto[:2000], height=200)
        
        # Análise passo a passo
        resultado = {}
        
        # 1. Busca informações básicas
        st.write("### 🏢 Buscando informações do órgão...")
        resultado["orgao"] = self._buscar_orgao_real(texto)
        
        st.write("### 🏛️ Identificando banca...")
        resultado["banca"] = self._buscar_banca_real(texto)
        
        st.write("### 💼 Extraindo cargos...")
        resultado["cargos"] = self._extrair_cargos_reais(texto)
        
        st.write("### 💰 Buscando informações salariais...")
        resultado["salarios"] = self._extrair_salarios_reais(texto)
        
        st.write("### 👥 Contando vagas...")
        resultado["vagas"] = self._extrair_vagas_reais(texto)
        
        st.write("### 📅 Montando cronograma...")
        resultado["cronograma"] = self._extrair_cronograma_real(texto)
        
        st.write("### 📋 Buscando requisitos...")
        resultado["requisitos"] = self._extrair_requisitos_reais(texto)
        
        return resultado
    
    def _buscar_orgao_real(self, texto: str) -> Dict:
        """Busca real do órgão no texto"""
        
        # Converte para maiúsculo para busca
        texto_upper = texto.upper()
        
        # Lista de padrões específicos encontrados em editais reais
        patterns_orgao = [
            # Prefeituras
            r"PREFEITURA\s+MUNICIPAL\s+(?:DE|DA)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"PREFEITURA\s+(?:DE|DA)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"MUNICÍPIO\s+(?:DE|DA)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            
            # Outros órgãos
            r"CÂMARA\s+MUNICIPAL\s+(?:DE|DA)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"TRIBUNAL\s+(?:DE\s+JUSTIÇA|REGIONAL)\s+(?:DO|DA|DE)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"SECRETARIA\s+(?:MUNICIPAL\s+)?(?:DE|DA)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"FUNDAÇÃO\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"INSTITUTO\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            
            # Padrões genéricos
            r"CONCURSO\s+PÚBLICO\s+(?:PARA\s+)?(?:A\s+|O\s+)?([A-ZÁÊÇÕ\s\-]{5,50})",
            r"EDITAL\s+(?:DE\s+)?CONCURSO\s+(?:PÚBLICO\s+)?(?:PARA\s+)?(?:A\s+|O\s+)?([A-ZÁÊÇÕ\s\-]{5,50})"
        ]
        
        orgaos_encontrados = []
        
        for pattern in patterns_orgao:
            matches = re.findall(pattern, texto_upper)
            for match in matches:
                orgao_limpo = match.strip()
                if len(orgao_limpo) > 3 and orgao_limpo not in orgaos_encontrados:
                    orgaos_encontrados.append(orgao_limpo)
        
        # Debug
        if self.debug_mode:
            st.write(f"**🔍 Órgãos encontrados:** {orgaos_encontrados}")
        
        return {
            "orgaos_encontrados": orgaos_encontrados,
            "orgao_principal": orgaos_encontrados[0] if orgaos_encontrados else "NÃO IDENTIFICADO"
        }
    
    def _buscar_banca_real(self, texto: str) -> Dict:
        """Busca real da banca no texto"""
        
        texto_upper = texto.upper()
        
        # Bancas conhecidas com suas variações
        bancas_patterns = {
            "CESPE/CEBRASPE": [r"CESPE", r"CEBRASPE", r"CENTRO\s+DE\s+SELEÇÃO"],
            "FCC": [r"FUNDAÇÃO\s+CARLOS\s+CHAGAS", r"FCC"],
            "FGV": [r"FUNDAÇÃO\s+GETÚLIO\s+VARGAS", r"FGV"],
            "VUNESP": [r"VUNESP", r"FUNDAÇÃO\s+VUNESP"],
            "CONSULPLAN": [r"CONSULPLAN"],
            "QUADRIX": [r"QUADRIX"],
            "AOCP": [r"AOCP"],
            "IBFC": [r"IBFC"],
            "IDECAN": [r"IDECAN"],
            "INSTITUTO AOCP": [r"INSTITUTO\s+AOCP"],
            "FUNDEP": [r"FUNDEP"],
            "IADES": [r"IADES"],
            "IBADE": [r"IBADE"]
        }
        
        bancas_encontradas = []
        
        for banca, patterns in bancas_patterns.items():
            for pattern in patterns:
                if re.search(pattern, texto_upper):
                    bancas_encontradas.append(banca)
                    break
        
        # Debug
        if self.debug_mode:
            st.write(f"**🔍 Bancas encontradas:** {bancas_encontradas}")
        
        return {
            "bancas_encontradas": bancas_encontradas,
            "banca_principal": bancas_encontradas[0] if bancas_encontradas else "NÃO IDENTIFICADA"
        }
    
    def _extrair_cargos_reais(self, texto: str) -> Dict:
        """Extração real de cargos do texto"""
        
        texto_upper = texto.upper()
        
        # Padrões específicos para cargos
        patterns_cargo = [
            # Padrões diretos
            r"CARGO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,100})",
            r"FUNÇÃO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,100})",
            r"EMPREGO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,100})",
            
            # Padrões com contexto
            r"(?:PARA\s+O\s+CARGO\s+DE|PARA\s+A\s+FUNÇÃO\s+DE)\s*([A-ZÁÊÇÕ\s\-]{5,100})",
            r"(?:DO\s+CARGO\s+DE|DA\s+FUNÇÃO\s+DE)\s*([A-ZÁÊÇÕ\s\-]{5,100})",
            
            # Cargos específicos comuns
            r"(AGENTE\s+(?:ADMINISTRATIVO|COMUNITÁRIO|FISCAL|PÚBLICO|MUNICIPAL|DE\s+[A-ZÁÊÇÕ\s]+))",
            r"(ANALISTA\s+(?:ADMINISTRATIVO|JUDICIÁRIO|TÉCNICO|MUNICIPAL|DE\s+[A-ZÁÊÇÕ\s]+))",
            r"(TÉCNICO\s+(?:EM\s+|DE\s+|ADMINISTRATIVO|JUDICIÁRIO|MUNICIPAL|[A-ZÁÊÇÕ\s]+))",
            r"(AUXILIAR\s+(?:DE\s+|ADMINISTRATIVO|JUDICIÁRIO|MUNICIPAL|[A-ZÁÊÇÕ\s]+))",
            r"(ASSISTENTE\s+(?:DE\s+|ADMINISTRATIVO|SOCIAL|MUNICIPAL|[A-ZÁÊÇÕ\s]+))",
            r"(ESPECIALISTA\s+(?:EM\s+|DE\s+)[A-ZÁÊÇÕ\s]+)",
            r"(INSPETOR\s+(?:DE\s+|ESCOLAR|MUNICIPAL|[A-ZÁÊÇÕ\s]+))",
            r"(FISCAL\s+(?:DE\s+|MUNICIPAL|TRIBUTÁRIO|[A-ZÁÊÇÕ\s]+))",
            r"(AUDITOR\s+(?:DE\s+|FISCAL|MUNICIPAL|[A-ZÁÊÇÕ\s]+))",
            r"(PROFESSOR\s+(?:DE\s+|MUNICIPAL|EDUCAÇÃO|[A-ZÁÊÇÕ\s]+))",
            r"(COORDENADOR\s+(?:DE\s+|PEDAGÓGICO|MUNICIPAL|[A-ZÁÊÇÕ\s]+))",
            r"(DIRETOR\s+(?:DE\s+|ESCOLAR|MUNICIPAL|[A-ZÁÊÇÕ\s]+))",
            r"(SECRETÁRIO\s+(?:DE\s+|ESCOLAR|MUNICIPAL|[A-ZÁÊÇÕ\s]+))",
            r"(MOTORISTA\s+(?:DE\s+|MUNICIPAL)?)",
            r"(VIGILANTE\s+(?:MUNICIPAL)?)",
            r"(ZELADOR\s+(?:MUNICIPAL)?)",
            r"(SERVENTE\s+(?:DE\s+|MUNICIPAL)?)",
            r"(GARI\s+(?:MUNICIPAL)?)"
        ]
        
        cargos_encontrados = set()
        
        for pattern in patterns_cargo:
            matches = re.findall(pattern, texto_upper)
            for match in matches:
                cargo_limpo = self._limpar_cargo(match)
                if self._validar_cargo(cargo_limpo):
                    cargos_encontrados.add(cargo_limpo)
        
        # Converte para lista ordenada
        cargos_lista = sorted(list(cargos_encontrados))
        
        # Debug
        if self.debug_mode:
            st.write(f"**🔍 Cargos encontrados:** {len(cargos_lista)}")
            for cargo in cargos_lista[:10]:  # Mostra apenas os primeiros 10
                st.write(f"• {cargo}")
        
        return {
            "total_cargos": len(cargos_lista),
            "cargos_lista": cargos_lista
        }
    
    def _limpar_cargo(self, cargo_raw: str) -> str:
        """Limpa e normaliza nome do cargo"""
        cargo = cargo_raw.strip()
        
        # Remove caracteres especiais
        cargo = re.sub(r'[^\w\s\-]', ' ', cargo)
        cargo = re.sub(r'\s+', ' ', cargo)
        cargo = cargo.strip(' -')
        
        # Capitaliza corretamente
        palavras = cargo.split()
        palavras_capitalizadas = []
        
        preposicoes = ['DE', 'DA', 'DO', 'E', 'EM', 'PARA', 'COM', 'NA', 'NO']
        
        for palavra in palavras:
            if palavra.upper() in preposicoes:
                palavras_capitalizadas.append(palavra.lower())
            else:
                palavras_capitalizadas.append(palavra.capitalize())
        
        return ' '.join(palavras_capitalizadas)
    
    def _validar_cargo(self, cargo: str) -> bool:
        """Valida se é um cargo válido"""
        if len(cargo) < 5 or len(cargo) > 150:
            return False
        
        # Palavras que invalidam
        palavras_invalidas = [
            'EDITAL', 'CONCURSO', 'PÚBLICO', 'ANEXO', 'PÁGINA', 'ITEM',
            'CAPÍTULO', 'SEÇÃO', 'ARTIGO', 'PARÁGRAFO'
        ]
        
        cargo_upper = cargo.upper()
        if any(palavra in cargo_upper for palavra in palavras_invalidas):
            return False
        
        # Deve ter pelo menos uma palavra típica de cargo
        palavras_cargo = [
            'AGENTE', 'ANALISTA', 'TÉCNICO', 'AUXILIAR', 'ASSISTENTE',
            'ESPECIALISTA', 'INSPETOR', 'FISCAL', 'AUDITOR', 'PROFESSOR',
            'COORDENADOR', 'DIRETOR', 'SECRETÁRIO', 'MOTORISTA', 'VIGILANTE'
        ]
        
        return any(palavra in cargo_upper for palavra in palavras_cargo)
    
    def _extrair_salarios_reais(self, texto: str) -> Dict:
        """Extrai informações salariais reais"""
        
        # Padrões para salários
        patterns_salario = [
            r"R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"SALÁRIO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"REMUNERAÇÃO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"VENCIMENTO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)"
        ]
        
        salarios_encontrados = []
        
        for pattern in patterns_salario:
            matches = re.findall(pattern, texto)
            for match in matches:
                salario = f"R$ {match}"
                if salario not in salarios_encontrados:
                    salarios_encontrados.append(salario)
        
        # Debug
        if self.debug_mode:
            st.write(f"**🔍 Salários encontrados:** {salarios_encontrados}")
        
        return {
            "salarios_encontrados": salarios_encontrados,
            "total_salarios": len(salarios_encontrados)
        }
    
    def _extrair_vagas_reais(self, texto: str) -> Dict:
        """Extrai informações de vagas reais"""
        
        texto_upper = texto.upper()
        
        # Padrões para vagas
        patterns_vagas = [
            r"(\d+)\s*(?:VAGA|VAGAS)",
            r"(?:VAGA|VAGAS)\s*[:\-]\s*(\d+)",
            r"TOTAL\s+DE\s+(\d+)\s+(?:VAGA|VAGAS)",
            r"QUANTIDADE\s*[:\-]\s*(\d+)"
        ]
        
        vagas_encontradas = []
        
        for pattern in patterns_vagas:
            matches = re.findall(pattern, texto_upper)
            for match in matches:
                if match.isdigit() and int(match) > 0:
                    vagas_encontradas.append(int(match))
        
        # Debug
        if self.debug_mode:
            st.write(f"**🔍 Vagas encontradas:** {vagas_encontradas}")
        
        return {
            "vagas_encontradas": vagas_encontradas,
            "total_vagas": sum(vagas_encontradas) if vagas_encontradas else 0
        }
    
    def _extrair_cronograma_real(self, texto: str) -> Dict:
        """Extrai cronograma real do edital"""
        
        # Padrões para datas
        patterns_datas = {
            "Publicação": [
                r"PUBLICAÇÃO.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"EDITAL.*?PUBLICADO.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
            ],
            "Inscrições": [
                r"INSCRIÇÕES.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}).*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"PERÍODO.*?INSCRIÇÃO.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
            ],
            "Prova": [
                r"PROVA.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"APLICAÇÃO.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"EXAME.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
            ],
            "Resultado": [
                r"RESULTADO.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"DIVULGAÇÃO.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
            ]
        }
        
        cronograma = {}
        
        for evento, patterns in patterns_datas.items():
            datas_encontradas = []
            
            for pattern in patterns:
                matches = re.findall(pattern, texto, re.IGNORECASE | re.DOTALL)
                datas_encontradas.extend(matches)
            
            if datas_encontradas:
                if isinstance(datas_encontradas[0], tuple):
                    cronograma[evento] = list(datas_encontradas[0])
                else:
                    cronograma[evento] = datas_encontradas[0]
            else:
                cronograma[evento] = "Não informado"
        
        # Debug
        if self.debug_mode:
            st.write(f"**🔍 Cronograma encontrado:** {cronograma}")
        
        return cronograma
    
    def _extrair_requisitos_reais(self, texto: str) -> Dict:
        """Extrai requisitos reais do edital"""
        
        texto_upper = texto.upper()
        
        # Padrões para escolaridade
        patterns_escolaridade = [
            r"(SUPERIOR\s+COMPLETO)",
            r"(MÉDIO\s+COMPLETO)",
            r"(FUNDAMENTAL\s+COMPLETO)",
            r"(ENSINO\s+SUPERIOR)",
            r"(ENSINO\s+MÉDIO)",
            r"(NÍVEL\s+SUPERIOR)",
            r"(NÍVEL\s+MÉDIO)",
            r"(GRADUAÇÃO)",
            r"(PÓS-GRADUAÇÃO)"
        ]
        
        escolaridades_encontradas = []
        
        for pattern in patterns_escolaridade:
            matches = re.findall(pattern, texto_upper)
            for match in matches:
                if match not in escolaridades_encontradas:
                    escolaridades_encontradas.append(match)
        
        # Padrões para carga horária
        patterns_ch = [
            r"(\d+)\s*(?:HORAS?|H)\s*(?:SEMANAIS?|POR\s+SEMANA)",
            r"CARGA\s+HORÁRIA.*?(\d+)\s*(?:HORAS?|H)"
        ]
        
        cargas_horarias = []
        
        for pattern in patterns_ch:
            matches = re.findall(pattern, texto_upper)
            for match in matches:
                ch = f"{match}h/semana"
                if ch not in cargas_horarias:
                    cargas_horarias.append(ch)
        
        # Debug
        if self.debug_mode:
            st.write(f"**🔍 Escolaridades:** {escolaridades_encontradas}")
            st.write(f"**🔍 Cargas horárias:** {cargas_horarias}")
        
        return {
            "escolaridades": escolaridades_encontradas,
            "cargas_horarias": cargas_horarias
        }

def render_edital_real_analyzer():
    """Renderiza o analisador real de edital"""
    st.header("🎯 Analisador Real de Edital")
    st.write("Sistema que **realmente extrai** informações específicas do seu edital")
    
    analyzer = EditalRealAnalyzer()
    
    # Informações sobre bibliotecas
    col_lib1, col_lib2, col_lib3 = st.columns(3)
    
    with col_lib1:
        status_pymupdf = "✅ Disponível" if PYMUPDF_AVAILABLE else "❌ Instalar: pip install PyMuPDF"
        st.info(f"**PyMuPDF:** {status_pymupdf}")
    
    with col_lib2:
        status_pdfplumber = "✅ Disponível" if PDFPLUMBER_AVAILABLE else "❌ Instalar: pip install pdfplumber"
        st.info(f"**pdfplumber:** {status_pdfplumber}")
    
    with col_lib3:
        st.info("**PyPDF2:** ✅ Sempre disponível")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "📄 Faça upload do edital (PDF)",
        type=['pdf'],
        help="Sistema que realmente lê e processa o conteúdo específico do seu edital"
    )
    
    if uploaded_file is not None:
        # Extração de texto
        with st.spinner("🔍 Extraindo texto do PDF..."):
            texto_edital = analyzer.extrair_texto_completo(uploaded_file)
        
        if texto_edital and len(texto_edital.strip()) > 500:
            
            # Estatísticas da extração
            st.success(f"✅ Texto extraído: {len(texto_edital)} caracteres, {len(texto_edital.split())} palavras")
            
            # Botão para análise
            if st.button("🚀 Analisar Edital Real", type="primary"):
                
                with st.spinner("🤖 Processando informações específicas do edital..."):
                    resultado = analyzer.analisar_edital_real(texto_edital)
                
                # Salva resultado
                st.session_state.resultado_real = resultado
                st.session_state.texto_edital = texto_edital
                
                st.success("✅ Análise real concluída!")
                st.rerun()
        
        else:
            st.error("❌ Não foi possível extrair texto suficiente do PDF.")
    
    # Exibe resultado da análise real
    if 'resultado_real' in st.session_state:
        resultado = st.session_state.resultado_real
        
        st.divider()
        st.header("📊 Resultado da Análise Real")
        
        # Métricas principais
        col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
        
        with col_metric1:
            st.metric("🏢 Órgão", resultado["orgao"]["orgao_principal"][:15] + "..." if len(resultado["orgao"]["orgao_principal"]) > 15 else resultado["orgao"]["orgao_principal"])
        
        with col_metric2:
            st.metric("🏛️ Banca", resultado["banca"]["banca_principal"])
        
        with col_metric3:
            st.metric("💼 Cargos", resultado["cargos"]["total_cargos"])
        
        with col_metric4:
            st.metric("👥 Total Vagas", resultado["vagas"]["total_vagas"])
        
        # Detalhes do órgão
        st.subheader("🏢 Órgão Identificado")
        orgao_info = resultado["orgao"]
        
        st.write(f"**Órgão Principal:** {orgao_info['orgao_principal']}")
        
        if len(orgao_info["orgaos_encontrados"]) > 1:
            st.write("**Outros órgãos mencionados:**")
            for orgao in orgao_info["orgaos_encontrados"][1:]:
                st.write(f"• {orgao}")
        
        # Detalhes da banca
        st.subheader("🏛️ Banca Organizadora")
        banca_info = resultado["banca"]
        
        st.write(f"**Banca Principal:** {banca_info['banca_principal']}")
        
        if len(banca_info["bancas_encontradas"]) > 1:
            st.write("**Outras bancas mencionadas:**")
            for banca in banca_info["bancas_encontradas"][1:]:
                st.write(f"• {banca}")
        
        # Cargos identificados
        st.subheader("💼 Cargos Identificados")
        cargos_info = resultado["cargos"]
        
        if cargos_info["cargos_lista"]:
            # Seletor de cargo
            cargo_selecionado = st.selectbox(
                "Selecione um cargo para análise detalhada:",
                options=cargos_info["cargos_lista"],
                help="Escolha o cargo que deseja analisar em detalhes"
            )
            
            # Lista todos os cargos
            with st.expander(f"📋 Ver todos os {cargos_info['total_cargos']} cargos encontrados"):
                for i, cargo in enumerate(cargos_info["cargos_lista"], 1):
                    st.write(f"{i}. {cargo}")
        
        else:
            st.warning("⚠️ Nenhum cargo específico foi identificado.")
        
        # Informações salariais
        st.subheader("💰 Informações Salariais")
        salarios_info = resultado["salarios"]
        
        if salarios_info["salarios_encontrados"]:
            col_sal1, col_sal2 = st.columns(2)
            
            with col_sal1:
                st.write("**Salários encontrados:**")
                for salario in salarios_info["salarios_encontrados"]:
                    st.write(f"• {salario}")
            
            with col_sal2:
                st.metric("Total de Salários", salarios_info["total_salarios"])
        else:
            st.info("ℹ️ Nenhuma informação salarial específica foi encontrada.")
        
        # Informações de vagas
        st.subheader("👥 Informações de Vagas")
        vagas_info = resultado["vagas"]
        
        if vagas_info["vagas_encontradas"]:
            col_vag1, col_vag2 = st.columns(2)
            
            with col_vag1:
                st.write("**Vagas por cargo/seção:**")
                for vaga in vagas_info["vagas_encontradas"]:
                    st.write(f"• {vaga} vagas")
            
            with col_vag2:
                st.metric("Total Geral", vagas_info["total_vagas"])
        else:
            st.info("ℹ️ Nenhuma informação específica de vagas foi encontrada.")
        
        # Cronograma
        st.subheader("📅 Cronograma")
        cronograma = resultado["cronograma"]
        
        # Tabela do cronograma
        dados_cronograma = []
        for evento, data in cronograma.items():
            if isinstance(data, list):
                data_str = f"{data[0]} a {data[1]}" if len(data) == 2 else str(data)
            else:
                data_str = str(data)
            
            status = "✅ Encontrado" if data_str != "Não informado" else "❌ Não encontrado"
            
            dados_cronograma.append({
                "Evento": evento,
                "Data/Período": data_str,
                "Status": status
            })
        
        df_cronograma = pd.DataFrame(dados_cronograma)
        st.dataframe(df_cronograma, use_container_width=True)
        
        # Requisitos
        st.subheader("📋 Requisitos Identificados")
        requisitos = resultado["requisitos"]
        
        col_req1, col_req2 = st.columns(2)
        
        with col_req1:
            if requisitos["escolaridades"]:
                st.write("**🎓 Escolaridades encontradas:**")
                for esc in requisitos["escolaridades"]:
                    st.write(f"• {esc}")
            else:
                st.info("ℹ️ Nenhuma escolaridade específica encontrada.")
        
        with col_req2:
            if requisitos["cargas_horarias"]:
                st.write("**⏰ Cargas horárias encontradas:**")
                for ch in requisitos["cargas_horarias"]:
                    st.write(f"• {ch}")
            else:
                st.info("ℹ️ Nenhuma carga horária específica encontrada.")
        
        # Botões de ação
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🔄 Nova Análise"):
                del st.session_state.resultado_real
                if 'texto_edital' in st.session_state:
                    del st.session_state.texto_edital
                st.rerun()
        
        with col_btn2:
            if st.button("📄 Ver Texto Extraído"):
                if 'texto_edital' in st.session_state:
                    with st.expander("📄 Texto Completo do Edital"):
                        st.text_area("Conteúdo completo:", st.session_state.texto_edital, height=400)
        
        with col_btn3:
            if st.button("📥 Baixar Relatório"):
                relatorio = f"""
# RELATÓRIO DE ANÁLISE REAL DO EDITAL

**Data da Análise:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

## 🏢 Órgão
**Principal:** {resultado['orgao']['orgao_principal']}
**Outros:** {', '.join(resultado['orgao']['orgaos_encontrados'][1:]) if len(resultado['orgao']['orgaos_encontrados']) > 1 else 'Nenhum'}

## 🏛️ Banca
**Principal:** {resultado['banca']['banca_principal']}
**Outras:** {', '.join(resultado['banca']['bancas_encontradas'][1:]) if len(resultado['banca']['bancas_encontradas']) > 1 else 'Nenhuma'}

## 💼 Cargos ({resultado['cargos']['total_cargos']})
{chr(10).join([f"- {cargo}" for cargo in resultado['cargos']['cargos_lista']])}

## 💰 Salários
{chr(10).join([f"- {salario}" for salario in resultado['salarios']['salarios_encontrados']])}

## 👥 Vagas
**Total:** {resultado['vagas']['total_vagas']}
**Detalhes:** {', '.join([str(v) for v in resultado['vagas']['vagas_encontradas']])}

## 📅 Cronograma
{chr(10).join([f"- **{evento}:** {data}" for evento, data in resultado['cronograma'].items()])}

## 📋 Requisitos
**Escolaridades:** {', '.join(resultado['requisitos']['escolaridades'])}
**Cargas Horárias:** {', '.join(resultado['requisitos']['cargas_horarias'])}
"""
                
                st.download_button(
                    label="💾 Download Relatório",
                    data=relatorio,
                    file_name=f"relatorio_real_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
    
    else:
        # Instruções
        st.info("💡 **Como funciona o Analisador Real:**")
        st.write("""
        1. **📄 Upload**: Envie o PDF do edital
        2. **🔍 Extração Inteligente**: Sistema usa a melhor técnica disponível
        3. **🎯 Análise Específica**: Busca informações reais no texto extraído
        4. **📊 Resultados Detalhados**: Mostra tudo que foi encontrado
        5. **📥 Relatório**: Baixe o relatório completo
        """)
        
        st.warning("⚠️ **Dicas para melhor resultado:**")
        st.write("""
        - Use PDFs em formato texto (não imagens)
        - Editais bem estruturados funcionam melhor
        - O sistema mostra exatamente o que encontrou no texto
        - Use o modo debug para ver o texto extraído
        """)