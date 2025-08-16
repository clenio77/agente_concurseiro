"""
Analisador Automático de Edital - Agente Concurseiro v2.0
Sistema que extrai cargos automaticamente e permite análise específica por cargo
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
from typing import Dict, List, Tuple, Optional
import PyPDF2
import io
import json
from datetime import datetime

# Tentar importar bibliotecas avançadas de PDF
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    PYMUPDF_AVAILABLE = False

class EditalAnalyzerAuto:
    """Analisador automático de editais com extração inteligente"""
    
    def __init__(self):
        self.cargos_patterns = [
            # Padrões específicos para identificar cargos
            r"(?:CARGO|FUNÇÃO|EMPREGO)[\s:]*([A-ZÁÊÇÕ\s\-]{5,80})",
            r"(?:PARA\s+O\s+CARGO\s+DE|PARA\s+A\s+FUNÇÃO\s+DE)[\s:]*([A-ZÁÊÇÕ\s\-]{5,80})",
            r"(?:DO\s+CARGO\s+DE|DA\s+FUNÇÃO\s+DE)[\s:]*([A-ZÁÊÇÕ\s\-]{5,80})",
            r"(?:CONCURSO\s+PARA)[\s:]*([A-ZÁÊÇÕ\s\-]{5,80})",
            
            # Cargos específicos comuns
            r"(AGENTE\s+(?:DE\s+|ADMINISTRATIVO|COMUNITÁRIO|FISCAL|PÚBLICO|MUNICIPAL)[\s\w]*)",
            r"(ANALISTA\s+(?:DE\s+|ADMINISTRATIVO|JUDICIÁRIO|TÉCNICO|MUNICIPAL)[\s\w]*)",
            r"(TÉCNICO\s+(?:EM\s+|DE\s+|ADMINISTRATIVO|JUDICIÁRIO|MUNICIPAL)[\s\w]*)",
            r"(AUXILIAR\s+(?:DE\s+|ADMINISTRATIVO|JUDICIÁRIO|MUNICIPAL)[\s\w]*)",
            r"(ASSISTENTE\s+(?:DE\s+|ADMINISTRATIVO|SOCIAL|MUNICIPAL)[\s\w]*)",
            r"(ESPECIALISTA\s+(?:EM\s+|DE\s+)[\s\w]*)",
            r"(INSPETOR\s+(?:DE\s+|ESCOLAR|MUNICIPAL)[\s\w]*)",
            r"(FISCAL\s+(?:DE\s+|MUNICIPAL|TRIBUTÁRIO)[\s\w]*)",
            r"(AUDITOR\s+(?:DE\s+|FISCAL|MUNICIPAL)[\s\w]*)",
            r"(PROFESSOR\s+(?:DE\s+|MUNICIPAL|EDUCAÇÃO)[\s\w]*)",
            r"(COORDENADOR\s+(?:DE\s+|PEDAGÓGICO|MUNICIPAL)[\s\w]*)",
            r"(DIRETOR\s+(?:DE\s+|ESCOLAR|MUNICIPAL)[\s\w]*)",
            r"(GERENTE\s+(?:DE\s+)[\s\w]*)",
            r"(SUPERVISOR\s+(?:DE\s+)[\s\w]*)",
            r"(SECRETÁRIO\s+(?:DE\s+|ESCOLAR|MUNICIPAL)[\s\w]*)",
            r"(OPERADOR\s+(?:DE\s+)[\s\w]*)",
            r"(MOTORISTA\s+(?:DE\s+|MUNICIPAL)[\s\w]*)",
            r"(VIGILANTE\s+(?:MUNICIPAL)?)",
            r"(ZELADOR\s+(?:MUNICIPAL)?)",
            r"(SERVENTE\s+(?:DE\s+|MUNICIPAL)[\s\w]*)",
            r"(GARI\s+(?:MUNICIPAL)?)",
            r"(COVEIRO\s+(?:MUNICIPAL)?)"
        ]
        
        self.stop_words = [
            'EDITAL', 'CONCURSO', 'PÚBLICO', 'ANEXO', 'PÁGINA', 'ITEM', 'SUBITEM',
            'CAPÍTULO', 'SEÇÃO', 'ARTIGO', 'PARÁGRAFO', 'INCISO', 'ALÍNEA'
        ]

    def extrair_texto_avancado(self, arquivo_pdf) -> Tuple[str, Dict]:
        """Extrai texto usando múltiplas bibliotecas para máxima precisão"""
        arquivo_pdf.seek(0)
        
        resultados = {
            "metodo_usado": "",
            "total_paginas": 0,
            "caracteres_extraidos": 0,
            "qualidade": "Baixa"
        }
        
        texto_final = ""
        
        # Método 1: PyMuPDF (mais preciso)
        if PYMUPDF_AVAILABLE:
            try:
                st.info("🔍 Usando PyMuPDF para extração avançada...")
                arquivo_pdf.seek(0)
                doc = fitz.open(stream=arquivo_pdf.read(), filetype="pdf")
                
                texto_completo = ""
                for page_num in range(len(doc)):
                    page = doc.load_page(page_num)
                    texto_pagina = page.get_text()
                    
                    if texto_pagina.strip():
                        texto_completo += f"\n=== PÁGINA {page_num + 1} ===\n"
                        texto_completo += texto_pagina + "\n"
                
                doc.close()
                
                if len(texto_completo) > 500:
                    texto_final = texto_completo
                    resultados["metodo_usado"] = "PyMuPDF"
                    resultados["qualidade"] = "Alta"
                
            except Exception as e:
                st.warning(f"⚠️ PyMuPDF falhou: {str(e)}")
        
        # Método 2: pdfplumber (boa para tabelas)
        if not texto_final and PDFPLUMBER_AVAILABLE:
            try:
                st.info("🔍 Usando pdfplumber para extração...")
                arquivo_pdf.seek(0)
                
                with pdfplumber.open(io.BytesIO(arquivo_pdf.read())) as pdf:
                    texto_completo = ""
                    for i, page in enumerate(pdf.pages):
                        texto_pagina = page.extract_text()
                        
                        if texto_pagina:
                            texto_completo += f"\n=== PÁGINA {i + 1} ===\n"
                            texto_completo += texto_pagina + "\n"
                
                if len(texto_completo) > 500:
                    texto_final = texto_completo
                    resultados["metodo_usado"] = "pdfplumber"
                    resultados["qualidade"] = "Média-Alta"
                
            except Exception as e:
                st.warning(f"⚠️ pdfplumber falhou: {str(e)}")
        
        # Método 3: PyPDF2 (fallback)
        if not texto_final:
            try:
                st.info("🔍 Usando PyPDF2 como fallback...")
                arquivo_pdf.seek(0)
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(arquivo_pdf.read()))
                
                texto_completo = ""
                for i, pagina in enumerate(pdf_reader.pages):
                    texto_pagina = pagina.extract_text()
                    
                    if texto_pagina.strip():
                        texto_completo += f"\n=== PÁGINA {i + 1} ===\n"
                        texto_completo += texto_pagina + "\n"
                
                texto_final = texto_completo
                resultados["metodo_usado"] = "PyPDF2"
                resultados["qualidade"] = "Média"
                
            except Exception as e:
                st.error(f"❌ Todos os métodos falharam: {str(e)}")
                return "", resultados
        
        # Atualiza estatísticas
        resultados["caracteres_extraidos"] = len(texto_final)
        resultados["total_paginas"] = texto_final.count("=== PÁGINA")
        
        return texto_final, resultados

    def extrair_cargos_automaticamente(self, texto: str) -> Dict:
        """Extrai todos os cargos automaticamente do texto"""
        st.info("🎯 Extraindo cargos automaticamente...")
        
        cargos_encontrados = set()
        cargos_detalhados = {}
        texto_upper = texto.upper()
        
        # Aplica todos os padrões de cargo
        for pattern in self.cargos_patterns:
            matches = re.findall(pattern, texto_upper, re.IGNORECASE)
            
            for match in matches:
                cargo_raw = match.strip()
                cargo_limpo = self._limpar_cargo(cargo_raw)
                
                if self._validar_cargo(cargo_limpo):
                    cargos_encontrados.add(cargo_limpo)
        
        # Busca adicional por contexto
        cargos_contexto = self._buscar_cargos_por_contexto(texto_upper)
        cargos_encontrados.update(cargos_contexto)
        
        # Extrai detalhes de cada cargo
        for cargo in cargos_encontrados:
            detalhes = self._extrair_detalhes_cargo(texto, cargo)
            cargos_detalhados[cargo] = detalhes
        
        # Ordena cargos por relevância
        cargos_ordenados = self._ordenar_cargos_por_relevancia(cargos_detalhados)
        
        resultado = {
            "total_encontrados": len(cargos_ordenados),
            "cargos": cargos_ordenados,
            "detalhes": cargos_detalhados,
            "confianca": self._calcular_confianca(cargos_ordenados, texto)
        }
        
        st.success(f"✅ {len(cargos_ordenados)} cargos identificados automaticamente!")
        
        return resultado

    def _limpar_cargo(self, cargo_raw: str) -> str:
        """Limpa e normaliza nome do cargo"""
        cargo = cargo_raw.strip()
        
        # Remove caracteres indesejados
        cargo = re.sub(r'[^\w\s\-]', ' ', cargo)
        cargo = re.sub(r'\s+', ' ', cargo)
        cargo = cargo.strip(' -')
        
        # Capitaliza corretamente
        palavras = cargo.split()
        palavras_capitalizadas = []
        
        for palavra in palavras:
            if palavra.upper() in ['DE', 'DA', 'DO', 'E', 'EM', 'PARA', 'COM']:
                palavras_capitalizadas.append(palavra.lower())
            else:
                palavras_capitalizadas.append(palavra.capitalize())
        
        return ' '.join(palavras_capitalizadas)

    def _validar_cargo(self, cargo: str) -> bool:
        """Valida se é um cargo válido"""
        if len(cargo) < 5 or len(cargo) > 100:
            return False
        
        # Verifica se contém stop words
        cargo_upper = cargo.upper()
        for stop_word in self.stop_words:
            if stop_word in cargo_upper:
                return False
        
        # Verifica se tem pelo menos uma palavra significativa
        palavras_significativas = ['AGENTE', 'ANALISTA', 'TÉCNICO', 'AUXILIAR', 'ASSISTENTE', 
                                 'ESPECIALISTA', 'INSPETOR', 'FISCAL', 'AUDITOR', 'PROFESSOR',
                                 'COORDENADOR', 'DIRETOR', 'GERENTE', 'SUPERVISOR', 'SECRETÁRIO',
                                 'OPERADOR', 'MOTORISTA', 'VIGILANTE', 'ZELADOR', 'SERVENTE']
        
        return any(palavra in cargo_upper for palavra in palavras_significativas)

    def _buscar_cargos_por_contexto(self, texto: str) -> set:
        """Busca cargos por contexto específico"""
        cargos_contexto = set()
        
        # Padrões de contexto que indicam cargos
        contextos = [
            r"QUADRO\s+DE\s+VAGAS.*?([A-ZÁÊÇÕ\s\-]{10,80})",
            r"TABELA.*?CARGOS.*?([A-ZÁÊÇÕ\s\-]{10,80})",
            r"ANEXO.*?CARGOS.*?([A-ZÁÊÇÕ\s\-]{10,80})",
            r"VAGAS\s+PARA.*?([A-ZÁÊÇÕ\s\-]{10,80})",
            r"CÓDIGO.*?CARGO.*?([A-ZÁÊÇÕ\s\-]{10,80})"
        ]
        
        for pattern in contextos:
            matches = re.findall(pattern, texto, re.DOTALL | re.IGNORECASE)
            for match in matches:
                cargo_limpo = self._limpar_cargo(match)
                if self._validar_cargo(cargo_limpo):
                    cargos_contexto.add(cargo_limpo)
        
        return cargos_contexto

    def _extrair_detalhes_cargo(self, texto: str, cargo: str) -> Dict:
        """Extrai detalhes específicos de um cargo"""
        detalhes = {
            "vagas": "Não informado",
            "salario": "Não informado",
            "escolaridade": "Não informado",
            "carga_horaria": "Não informado",
            "requisitos": [],
            "atribuicoes": []
        }
        
        # Busca contexto do cargo (500 caracteres antes e depois)
        pattern_contexto = rf".{{0,500}}{re.escape(cargo)}.{{0,500}}"
        match = re.search(pattern_contexto, texto, re.IGNORECASE | re.DOTALL)
        
        if match:
            contexto = match.group(0)
            
            # Extrai vagas
            vaga_patterns = [
                rf"{re.escape(cargo)}.*?(\d+)\s*(?:VAGA|VAGAS)",
                r"(\d+)\s*(?:VAGA|VAGAS).*?" + re.escape(cargo),
                r"VAGAS?\s*[:\-]\s*(\d+)"
            ]
            
            for pattern in vaga_patterns:
                vaga_match = re.search(pattern, contexto, re.IGNORECASE)
                if vaga_match:
                    detalhes["vagas"] = vaga_match.group(1)
                    break
            
            # Extrai salário
            salario_patterns = [
                r"R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
                r"SALÁRIO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
                r"REMUNERAÇÃO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
                r"VENCIMENTO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)"
            ]
            
            for pattern in salario_patterns:
                salario_match = re.search(pattern, contexto, re.IGNORECASE)
                if salario_match:
                    detalhes["salario"] = f"R$ {salario_match.group(1)}"
                    break
            
            # Extrai escolaridade
            escolaridade_patterns = [
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
            
            for pattern in escolaridade_patterns:
                esc_match = re.search(pattern, contexto, re.IGNORECASE)
                if esc_match:
                    detalhes["escolaridade"] = esc_match.group(1).title()
                    break
            
            # Extrai carga horária
            ch_patterns = [
                r"(\d+)\s*(?:HORAS?|H)\s*(?:SEMANAIS?|POR\s+SEMANA)",
                r"(\d+)\s*H\s*SEMANAIS?",
                r"CARGA\s+HORÁRIA.*?(\d+)\s*(?:HORAS?|H)"
            ]
            
            for pattern in ch_patterns:
                ch_match = re.search(pattern, contexto, re.IGNORECASE)
                if ch_match:
                    detalhes["carga_horaria"] = f"{ch_match.group(1)}h/semana"
                    break
            
            # Extrai requisitos básicos
            if "REQUISITO" in contexto.upper():
                req_section = re.search(r"REQUISITOS?.*?(?=ATRIBUIÇÕES?|DESCRIÇÃO|$)", contexto, re.IGNORECASE | re.DOTALL)
                if req_section:
                    requisitos_text = req_section.group(0)
                    # Extrai itens de requisitos
                    req_items = re.findall(r"[-•]\s*([^\n\r]{10,200})", requisitos_text)
                    detalhes["requisitos"] = [req.strip() for req in req_items[:5]]
            
            # Extrai atribuições básicas
            if "ATRIBUIÇ" in contexto.upper():
                attr_section = re.search(r"ATRIBUIÇÕES?.*?(?=REQUISITOS?|DESCRIÇÃO|$)", contexto, re.IGNORECASE | re.DOTALL)
                if attr_section:
                    atribuicoes_text = attr_section.group(0)
                    # Extrai itens de atribuições
                    attr_items = re.findall(r"[-•]\s*([^\n\r]{10,200})", atribuicoes_text)
                    detalhes["atribuicoes"] = [attr.strip() for attr in attr_items[:5]]
        
        return detalhes

    def _ordenar_cargos_por_relevancia(self, cargos_detalhados: Dict) -> List[str]:
        """Ordena cargos por relevância (mais informações = mais relevante)"""
        def calcular_score(cargo, detalhes):
            score = 0
            
            # Pontos por informações disponíveis
            if detalhes["vagas"] != "Não informado":
                score += 3
            if detalhes["salario"] != "Não informado":
                score += 3
            if detalhes["escolaridade"] != "Não informado":
                score += 2
            if detalhes["carga_horaria"] != "Não informado":
                score += 1
            if detalhes["requisitos"]:
                score += len(detalhes["requisitos"])
            if detalhes["atribuicoes"]:
                score += len(detalhes["atribuicoes"])
            
            # Pontos por tipo de cargo (mais comuns primeiro)
            cargo_upper = cargo.upper()
            if any(palavra in cargo_upper for palavra in ['AGENTE', 'ANALISTA', 'TÉCNICO']):
                score += 2
            
            return score
        
        cargos_com_score = [(cargo, calcular_score(cargo, detalhes)) 
                           for cargo, detalhes in cargos_detalhados.items()]
        
        cargos_ordenados = sorted(cargos_com_score, key=lambda x: x[1], reverse=True)
        
        return [cargo for cargo, score in cargos_ordenados]

    def _calcular_confianca(self, cargos: List[str], texto: str) -> str:
        """Calcula nível de confiança da extração"""
        if not cargos:
            return "Muito Baixa"
        
        # Verifica se há indicadores de qualidade no texto
        indicadores_qualidade = [
            "QUADRO DE VAGAS", "TABELA", "ANEXO", "CÓDIGO DO CARGO",
            "SALÁRIO", "REMUNERAÇÃO", "ESCOLARIDADE", "REQUISITOS"
        ]
        
        score_qualidade = sum(1 for indicador in indicadores_qualidade 
                             if indicador in texto.upper())
        
        if len(cargos) >= 3 and score_qualidade >= 4:
            return "Alta"
        elif len(cargos) >= 2 and score_qualidade >= 2:
            return "Média"
        elif len(cargos) >= 1:
            return "Baixa"
        else:
            return "Muito Baixa"

    def analisar_cargo_especifico(self, texto: str, cargo_selecionado: str) -> Dict:
        """Análise detalhada de um cargo específico"""
        st.info(f"🔍 Analisando cargo específico: **{cargo_selecionado}**")
        
        # Extrai detalhes completos do cargo
        detalhes_cargo = self._extrair_detalhes_cargo(texto, cargo_selecionado)
        
        # Extrai conteúdo programático específico para o cargo
        conteudo_programatico = self._extrair_conteudo_por_cargo(texto, cargo_selecionado)
        
        # Extrai cronograma específico
        cronograma = self._extrair_cronograma_cargo(texto, cargo_selecionado)
        
        # Identifica banca organizadora
        banca = self._identificar_banca(texto)
        
        # Extrai informações do órgão
        orgao = self._identificar_orgao(texto)
        
        resultado = {
            "cargo": cargo_selecionado,
            "detalhes": detalhes_cargo,
            "conteudo_programatico": conteudo_programatico,
            "cronograma": cronograma,
            "banca": banca,
            "orgao": orgao,
            "data_analise": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        
        return resultado

    def _extrair_conteudo_por_cargo(self, texto: str, cargo: str) -> Dict:
        """Extrai conteúdo programático específico para um cargo"""
        conteudo = {}
        
        # Busca seção específica do cargo
        cargo_pattern = rf"{re.escape(cargo)}.*?(?=CARGO|FUNÇÃO|ANEXO|$)"
        cargo_section = re.search(cargo_pattern, texto, re.IGNORECASE | re.DOTALL)
        
        if cargo_section:
            secao_cargo = cargo_section.group(0)
        else:
            secao_cargo = texto  # Usa texto completo se não encontrar seção específica
        
        # Padrões para matérias
        materias_patterns = {
            "Português": [
                r"PORTUGUÊS[:\s]*(.*?)(?=MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)",
                r"LÍNGUA\s+PORTUGUESA[:\s]*(.*?)(?=MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)"
            ],
            "Matemática": [
                r"MATEMÁTICA[:\s]*(.*?)(?=PORTUGUÊS|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)"
            ],
            "Direito Constitucional": [
                r"DIREITO\s+CONSTITUCIONAL[:\s]*(.*?)(?=DIREITO\s+ADMINISTRATIVO|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|CONHECIMENTOS|$)"
            ],
            "Direito Administrativo": [
                r"DIREITO\s+ADMINISTRATIVO[:\s]*(.*?)(?=DIREITO\s+CONSTITUCIONAL|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|CONHECIMENTOS|$)"
            ],
            "Informática": [
                r"INFORMÁTICA[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)"
            ],
            "Conhecimentos Específicos": [
                r"CONHECIMENTOS\s+ESPECÍFICOS[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|RACIOCÍNIO|ATUALIDADES|$)"
            ]
        }
        
        for materia, patterns in materias_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, secao_cargo.upper(), re.DOTALL)
                if match:
                    conteudo_materia = match.group(1).strip()
                    
                    if len(conteudo_materia) > 30:
                        topicos = self._extrair_topicos(conteudo_materia)
                        if topicos:
                            conteudo[materia] = topicos
                        break
        
        return conteudo

    def _extrair_topicos(self, texto_materia: str) -> List[str]:
        """Extrai tópicos de uma matéria"""
        topicos = []
        
        # Padrões para tópicos
        patterns = [
            r'(\d+\.?\d*\.?\s+[^\n\r]{10,200})',  # 1. Tópico
            r'([a-z]\)\s*[^\n\r]{10,200})',       # a) Tópico
            r'([-•]\s*[^\n\r]{10,200})',          # - Tópico
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, texto_materia)
            for match in matches:
                topico = match.strip()
                topico = re.sub(r'^\d+\.?\d*\.?\s*', '', topico)
                topico = re.sub(r'^[a-z]\)\s*', '', topico)
                topico = re.sub(r'^[-•]\s*', '', topico)
                
                if len(topico) > 10 and topico not in topicos:
                    topicos.append(topico)
        
        return topicos[:20]

    def _extrair_cronograma_cargo(self, texto: str, cargo: str) -> Dict:
        """Extrai cronograma específico para o cargo"""
        cronograma = {}
        
        # Eventos importantes
        eventos = {
            "Inscrições": r"INSCRIÇÕES.*?(\d{1,2}/\d{1,2}/\d{4}).*?(\d{1,2}/\d{1,2}/\d{4})",
            "Prova": r"PROVA.*?(\d{1,2}/\d{1,2}/\d{4})",
            "Resultado": r"RESULTADO.*?(\d{1,2}/\d{1,2}/\d{4})"
        }
        
        for evento, pattern in eventos.items():
            match = re.search(pattern, texto, re.IGNORECASE | re.DOTALL)
            if match:
                if evento == "Inscrições" and len(match.groups()) == 2:
                    cronograma[evento] = {
                        "inicio": match.group(1),
                        "fim": match.group(2)
                    }
                else:
                    cronograma[evento] = match.group(1)
            else:
                cronograma[evento] = "Não informado"
        
        return cronograma

    def _identificar_banca(self, texto: str) -> str:
        """Identifica banca organizadora"""
        bancas = {
            "CESPE/CEBRASPE": ["CESPE", "CEBRASPE"],
            "FCC": ["FUNDAÇÃO CARLOS CHAGAS", "FCC"],
            "FGV": ["FUNDAÇÃO GETÚLIO VARGAS", "FGV"],
            "VUNESP": ["VUNESP"],
            "CONSULPLAN": ["CONSULPLAN"],
            "QUADRIX": ["QUADRIX"],
            "AOCP": ["AOCP"],
            "IBFC": ["IBFC"]
        }
        
        texto_upper = texto.upper()
        
        for banca, identificadores in bancas.items():
            if any(identificador in texto_upper for identificador in identificadores):
                return banca
        
        return "Não identificada"

    def _identificar_orgao(self, texto: str) -> str:
        """Identifica órgão do concurso"""
        patterns = [
            r"PREFEITURA\s+MUNICIPAL\s+DE\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"CÂMARA\s+MUNICIPAL\s+DE\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"TRIBUNAL\s+DE\s+JUSTIÇA\s+(?:DO|DA|DE)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"MINISTÉRIO\s+PÚBLICO\s+(?:DO|DA|DE)\s+([A-ZÁÊÇÕ\s\-]{3,50})"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto.upper())
            if match:
                return match.group(1).strip()
        
        return "Não identificado"

def render_edital_analyzer_auto():
    """Renderiza o analisador automático de edital"""
    st.header("🤖 Analisador Automático de Edital")
    st.write("Sistema que **extrai cargos automaticamente** e permite análise específica por cargo")
    
    analyzer = EditalAnalyzerAuto()
    
    # Informações sobre bibliotecas disponíveis
    col_info1, col_info2, col_info3 = st.columns(3)
    
    with col_info1:
        status_pymupdf = "✅ Disponível" if PYMUPDF_AVAILABLE else "❌ Não instalado"
        st.info(f"**PyMuPDF:** {status_pymupdf}")
    
    with col_info2:
        status_pdfplumber = "✅ Disponível" if PDFPLUMBER_AVAILABLE else "❌ Não instalado"
        st.info(f"**pdfplumber:** {status_pdfplumber}")
    
    with col_info3:
        st.info("**PyPDF2:** ✅ Disponível")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "📄 Faça upload do edital (PDF)",
        type=['pdf'],
        help="O sistema extrairá automaticamente todos os cargos disponíveis"
    )
    
    if uploaded_file is not None:
        # Extração automática de texto
        with st.spinner("🔍 Extraindo texto do PDF com máxima precisão..."):
            texto_edital, stats_extracao = analyzer.extrair_texto_avancado(uploaded_file)
        
        if texto_edital and len(texto_edital.strip()) > 100:
            # Mostra estatísticas da extração
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            
            with col_stat1:
                st.metric("Método Usado", stats_extracao["metodo_usado"])
            
            with col_stat2:
                st.metric("Páginas", stats_extracao["total_paginas"])
            
            with col_stat3:
                st.metric("Caracteres", f"{stats_extracao['caracteres_extraidos']:,}")
            
            with col_stat4:
                st.metric("Qualidade", stats_extracao["qualidade"])
            
            # Extração automática de cargos
            with st.spinner("🎯 Extraindo cargos automaticamente..."):
                resultado_cargos = analyzer.extrair_cargos_automaticamente(texto_edital)
            
            if resultado_cargos["total_encontrados"] > 0:
                st.success(f"🎉 **{resultado_cargos['total_encontrados']} cargos** identificados automaticamente!")
                st.info(f"**Confiança da extração:** {resultado_cargos['confianca']}")
                
                # Seleção de cargo para análise detalhada
                st.subheader("🎯 Selecione o Cargo para Análise Detalhada")
                
                # Cria lista de opções com informações básicas
                opcoes_cargo = []
                for cargo in resultado_cargos["cargos"]:
                    detalhes = resultado_cargos["detalhes"][cargo]
                    vagas = detalhes["vagas"]
                    salario = detalhes["salario"]
                    
                    info_extra = []
                    if vagas != "Não informado":
                        info_extra.append(f"{vagas} vagas")
                    if salario != "Não informado":
                        info_extra.append(salario)
                    
                    if info_extra:
                        opcao = f"{cargo} ({', '.join(info_extra)})"
                    else:
                        opcao = cargo
                    
                    opcoes_cargo.append(opcao)
                
                cargo_selecionado_display = st.selectbox(
                    "Escolha o cargo que deseja analisar:",
                    options=opcoes_cargo,
                    help="Selecione o cargo para ver análise completa com conteúdo programático"
                )
                
                # Extrai o nome real do cargo (remove informações extras)
                cargo_selecionado = cargo_selecionado_display.split(" (")[0]
                
                # Mostra preview dos cargos encontrados
                with st.expander("👀 Ver todos os cargos encontrados"):
                    for i, cargo in enumerate(resultado_cargos["cargos"], 1):
                        detalhes = resultado_cargos["detalhes"][cargo]
                        
                        col_cargo1, col_cargo2, col_cargo3 = st.columns([2, 1, 1])
                        
                        with col_cargo1:
                            st.write(f"**{i}. {cargo}**")
                        
                        with col_cargo2:
                            st.write(f"Vagas: {detalhes['vagas']}")
                        
                        with col_cargo3:
                            st.write(f"Salário: {detalhes['salario']}")
                
                # Botão para análise detalhada
                if st.button("🔍 Analisar Cargo Selecionado", type="primary"):
                    
                    with st.spinner(f"🤖 Analisando {cargo_selecionado} em detalhes..."):
                        analise_completa = analyzer.analisar_cargo_especifico(texto_edital, cargo_selecionado)
                    
                    # Salva no session state
                    st.session_state.analise_cargo = analise_completa
                    
                    st.success("✅ Análise completa realizada!")
                    st.rerun()
            
            else:
                st.warning("⚠️ Nenhum cargo foi identificado automaticamente.")
                st.info("💡 Isso pode acontecer se o PDF for uma imagem ou tiver formatação muito específica.")
                
                # Opção para análise manual
                if st.button("🔧 Tentar Análise Manual"):
                    st.write("### 📄 Texto Extraído (para análise manual)")
                    st.text_area("Conteúdo:", texto_edital[:2000] + "..." if len(texto_edital) > 2000 else texto_edital, height=300)
        
        else:
            st.error("❌ Não foi possível extrair texto suficiente do PDF.")
            st.info("💡 Verifique se o PDF não está protegido ou se é uma imagem escaneada.")
    
    # Exibe análise completa se disponível
    if 'analise_cargo' in st.session_state:
        analise = st.session_state.analise_cargo
        
        st.divider()
        st.header(f"📊 Análise Completa: {analise['cargo']}")
        
        # Informações básicas
        col_info1, col_info2, col_info3 = st.columns(3)
        
        with col_info1:
            st.metric("🏢 Órgão", analise["orgao"])
            st.metric("🏛️ Banca", analise["banca"])
        
        with col_info2:
            detalhes = analise["detalhes"]
            st.metric("👥 Vagas", detalhes["vagas"])
            st.metric("💰 Salário", detalhes["salario"])
        
        with col_info3:
            st.metric("🎓 Escolaridade", detalhes["escolaridade"])
            st.metric("⏰ Carga Horária", detalhes["carga_horaria"])
        
        # Conteúdo Programático
        if analise["conteudo_programatico"]:
            st.subheader("📚 Conteúdo Programático")
            
            # Gráfico de distribuição
            materias = list(analise["conteudo_programatico"].keys())
            num_topicos = [len(topicos) for topicos in analise["conteudo_programatico"].values()]
            
            if materias:
                fig = px.bar(
                    x=materias,
                    y=num_topicos,
                    title="📊 Tópicos por Matéria",
                    labels={"x": "Matérias", "y": "Número de Tópicos"}
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Detalhes por matéria
                for materia, topicos in analise["conteudo_programatico"].items():
                    with st.expander(f"📖 {materia} ({len(topicos)} tópicos)"):
                        for i, topico in enumerate(topicos, 1):
                            st.write(f"{i}. {topico}")
        
        # Cronograma
        st.subheader("📅 Cronograma")
        cronograma = analise["cronograma"]
        
        for evento, info in cronograma.items():
            if isinstance(info, dict):
                st.write(f"**{evento}:** {info['inicio']} a {info['fim']}")
            else:
                st.write(f"**{evento}:** {info}")
        
        # Requisitos e Atribuições
        col_req, col_attr = st.columns(2)
        
        with col_req:
            if detalhes["requisitos"]:
                st.subheader("📋 Requisitos")
                for req in detalhes["requisitos"]:
                    st.write(f"• {req}")
        
        with col_attr:
            if detalhes["atribuicoes"]:
                st.subheader("⚙️ Atribuições")
                for attr in detalhes["atribuicoes"]:
                    st.write(f"• {attr}")
        
        # Botão para nova análise
        if st.button("🔄 Analisar Outro Cargo"):
            del st.session_state.analise_cargo
            st.rerun()
        
        # Botão para download do relatório
        if st.button("📥 Baixar Relatório Completo"):
            relatorio = f"""
# RELATÓRIO DE ANÁLISE - {analise['cargo']}

**Data da Análise:** {analise['data_analise']}
**Órgão:** {analise['orgao']}
**Banca:** {analise['banca']}

## Informações do Cargo
- **Vagas:** {detalhes['vagas']}
- **Salário:** {detalhes['salario']}
- **Escolaridade:** {detalhes['escolaridade']}
- **Carga Horária:** {detalhes['carga_horaria']}

## Conteúdo Programático
{chr(10).join([f"### {materia}{chr(10)}{chr(10).join([f'- {topico}' for topico in topicos])}" for materia, topicos in analise['conteudo_programatico'].items()])}

## Cronograma
{chr(10).join([f"- **{evento}:** {info}" for evento, info in cronograma.items()])}

## Requisitos
{chr(10).join([f"- {req}" for req in detalhes['requisitos']])}

## Atribuições
{chr(10).join([f"- {attr}" for attr in detalhes['atribuicoes']])}
"""
            
            st.download_button(
                label="📄 Baixar Relatório (Markdown)",
                data=relatorio,
                file_name=f"relatorio_{analise['cargo'].replace(' ', '_')}.md",
                mime="text/markdown"
            )
    
    else:
        # Instruções de uso
        st.info("💡 **Como usar o Analisador Automático:**")
        st.write("""
        1. **📄 Upload**: Faça upload do PDF do edital
        2. **🤖 Extração Automática**: O sistema identifica todos os cargos automaticamente
        3. **🎯 Seleção**: Escolha o cargo que deseja analisar
        4. **📊 Análise Completa**: Receba análise detalhada com conteúdo programático
        5. **📥 Relatório**: Baixe o relatório completo em formato Markdown
        """)
        
        st.warning("⚠️ **Requisitos para melhor funcionamento:**")
        st.write("""
        - PDF deve estar em formato texto (não imagem escaneada)
        - Edital deve ter estrutura organizada com seções claras
        - Para máxima precisão, instale: `pip install PyMuPDF pdfplumber`
        """)