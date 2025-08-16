"""
Analisador Profissional de Edital - Agente Concurseiro v2.0
Sistema de análise de alta precisão com extração específica de dados
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
import fitz  # PyMuPDF
import pdfplumber

class EditalAnalyzerPro:
    """Analisador profissional com extração de alta precisão"""
    
    def __init__(self):
        self.debug = True
        
        # Padrões específicos para diferentes tipos de informação
        self.patterns_orgao = [
            r"PREFEITURA\s+MUNICIPAL\s+(?:DE|DA)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"CÂMARA\s+MUNICIPAL\s+(?:DE|DA)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"TRIBUNAL\s+(?:DE\s+JUSTIÇA|REGIONAL)\s+(?:DO|DA|DE)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"MINISTÉRIO\s+PÚBLICO\s+(?:DO|DA|DE)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"SECRETARIA\s+(?:MUNICIPAL\s+|ESTADUAL\s+)?(?:DE|DA)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"FUNDAÇÃO\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"INSTITUTO\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"UNIVERSIDADE\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"AUTARQUIA\s+([A-ZÁÊÇÕ\s\-]{3,50})"
        ]
        
        self.patterns_banca = {
            "CESPE/CEBRASPE": [r"CESPE", r"CEBRASPE", r"CENTRO\s+DE\s+SELEÇÃO"],
            "FCC": [r"FUNDAÇÃO\s+CARLOS\s+CHAGAS", r"FCC"],
            "FGV": [r"FUNDAÇÃO\s+GETÚLIO\s+VARGAS", r"FGV"],
            "VUNESP": [r"VUNESP", r"FUNDAÇÃO\s+VUNESP"],
            "CONSULPLAN": [r"CONSULPLAN"],
            "QUADRIX": [r"QUADRIX"],
            "AOCP": [r"AOCP"],
            "IBFC": [r"IBFC"],
            "IDECAN": [r"IDECAN"],
            "INSTITUTO\s+AOCP": [r"INSTITUTO\s+AOCP"]
        }

    def extrair_texto_multiplo(self, arquivo_pdf) -> Tuple[str, Dict]:
        """Extrai texto usando múltiplas técnicas para máxima precisão"""
        arquivo_pdf.seek(0)
        
        resultados = {
            "metodos_tentados": [],
            "metodo_sucesso": "",
            "qualidade_extracao": "Baixa",
            "total_paginas": 0,
            "caracteres_extraidos": 0,
            "estrutura_detectada": False
        }
        
        texto_final = ""
        
        # Método 1: PyMuPDF com análise de estrutura
        try:
            st.info("🔍 Tentativa 1: PyMuPDF com análise estrutural...")
            arquivo_pdf.seek(0)
            doc = fitz.open(stream=arquivo_pdf.read(), filetype="pdf")
            
            texto_estruturado = ""
            estruturas_encontradas = []
            
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                
                # Extrai texto com informações de posição
                blocks = page.get_text("dict")
                
                texto_pagina = ""
                for block in blocks["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                texto = span["text"].strip()
                                if texto:
                                    # Detecta estruturas importantes
                                    if self._detectar_estrutura_importante(texto):
                                        estruturas_encontradas.append(texto)
                                        texto_pagina += f"\n[ESTRUTURA] {texto}\n"
                                    else:
                                        texto_pagina += texto + " "
                
                if texto_pagina.strip():
                    texto_estruturado += f"\n=== PÁGINA {page_num + 1} ===\n"
                    texto_estruturado += texto_pagina + "\n"
            
            doc.close()
            
            if len(texto_estruturado) > 1000:
                texto_final = texto_estruturado
                resultados["metodo_sucesso"] = "PyMuPDF Estrutural"
                resultados["qualidade_extracao"] = "Muito Alta"
                resultados["estrutura_detectada"] = len(estruturas_encontradas) > 0
                
                if self.debug:
                    st.success(f"✅ PyMuPDF: {len(estruturas_encontradas)} estruturas importantes detectadas")
            
            resultados["metodos_tentados"].append("PyMuPDF")
            
        except Exception as e:
            st.warning(f"⚠️ PyMuPDF falhou: {str(e)}")
        
        # Método 2: pdfplumber com análise de tabelas
        if not texto_final:
            try:
                st.info("🔍 Tentativa 2: pdfplumber com análise de tabelas...")
                arquivo_pdf.seek(0)
                
                with pdfplumber.open(io.BytesIO(arquivo_pdf.read())) as pdf:
                    texto_completo = ""
                    tabelas_encontradas = 0
                    
                    for i, page in enumerate(pdf.pages):
                        # Extrai texto normal
                        texto_pagina = page.extract_text()
                        
                        # Extrai tabelas
                        tabelas = page.extract_tables()
                        
                        if texto_pagina:
                            texto_completo += f"\n=== PÁGINA {i + 1} ===\n"
                            texto_completo += texto_pagina + "\n"
                        
                        # Processa tabelas encontradas
                        if tabelas:
                            tabelas_encontradas += len(tabelas)
                            texto_completo += f"\n[TABELAS ENCONTRADAS: {len(tabelas)}]\n"
                            
                            for j, tabela in enumerate(tabelas):
                                texto_completo += f"\n--- TABELA {j+1} ---\n"
                                for linha in tabela:
                                    if linha:
                                        linha_limpa = [str(cell) if cell else "" for cell in linha]
                                        texto_completo += " | ".join(linha_limpa) + "\n"
                
                if len(texto_completo) > 1000:
                    texto_final = texto_completo
                    resultados["metodo_sucesso"] = "pdfplumber com Tabelas"
                    resultados["qualidade_extracao"] = "Alta"
                    
                    if self.debug:
                        st.success(f"✅ pdfplumber: {tabelas_encontradas} tabelas extraídas")
                
                resultados["metodos_tentados"].append("pdfplumber")
                
            except Exception as e:
                st.warning(f"⚠️ pdfplumber falhou: {str(e)}")
        
        # Método 3: PyPDF2 como fallback
        if not texto_final:
            try:
                st.info("🔍 Tentativa 3: PyPDF2 (fallback)...")
                arquivo_pdf.seek(0)
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(arquivo_pdf.read()))
                
                texto_completo = ""
                for i, pagina in enumerate(pdf_reader.pages):
                    texto_pagina = pagina.extract_text()
                    
                    if texto_pagina.strip():
                        texto_completo += f"\n=== PÁGINA {i + 1} ===\n"
                        texto_completo += texto_pagina + "\n"
                
                texto_final = texto_completo
                resultados["metodo_sucesso"] = "PyPDF2"
                resultados["qualidade_extracao"] = "Média"
                resultados["metodos_tentados"].append("PyPDF2")
                
            except Exception as e:
                st.error(f"❌ Todos os métodos falharam: {str(e)}")
                return "", resultados
        
        # Atualiza estatísticas finais
        resultados["caracteres_extraidos"] = len(texto_final)
        resultados["total_paginas"] = texto_final.count("=== PÁGINA")
        
        return texto_final, resultados

    def _detectar_estrutura_importante(self, texto: str) -> bool:
        """Detecta se o texto contém estruturas importantes"""
        estruturas_importantes = [
            r"CARGO", r"FUNÇÃO", r"EMPREGO", r"VAGAS?", r"SALÁRIO", r"REMUNERAÇÃO",
            r"ESCOLARIDADE", r"REQUISITOS?", r"ATRIBUIÇÕES?", r"CONTEÚDO\s+PROGRAMÁTICO",
            r"CRONOGRAMA", r"INSCRIÇÕES?", r"PROVA", r"EDITAL", r"ANEXO"
        ]
        
        texto_upper = texto.upper()
        return any(re.search(pattern, texto_upper) for pattern in estruturas_importantes)

    def analisar_edital_profissional(self, texto: str) -> Dict:
        """Análise profissional completa do edital"""
        
        st.subheader("🎯 Análise Profissional em Andamento")
        
        # Cria barra de progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # 1. Identificação do órgão (10%)
        status_text.text("🏢 Identificando órgão...")
        progress_bar.progress(10)
        orgao_info = self._identificar_orgao_preciso(texto)
        
        # 2. Identificação da banca (20%)
        status_text.text("🏛️ Identificando banca organizadora...")
        progress_bar.progress(20)
        banca_info = self._identificar_banca_precisa(texto)
        
        # 3. Extração de cargos (40%)
        status_text.text("💼 Extraindo cargos e informações...")
        progress_bar.progress(40)
        cargos_info = self._extrair_cargos_precisos(texto)
        
        # 4. Informações gerais (60%)
        status_text.text("📋 Coletando informações gerais...")
        progress_bar.progress(60)
        info_gerais = self._extrair_informacoes_gerais(texto)
        
        # 5. Cronograma (80%)
        status_text.text("📅 Montando cronograma...")
        progress_bar.progress(80)
        cronograma = self._extrair_cronograma_preciso(texto)
        
        # 6. Finalização (100%)
        status_text.text("✅ Finalizando análise...")
        progress_bar.progress(100)
        
        # Limpa elementos de progresso
        progress_bar.empty()
        status_text.empty()
        
        resultado = {
            "orgao": orgao_info,
            "banca": banca_info,
            "cargos": cargos_info,
            "informacoes_gerais": info_gerais,
            "cronograma": cronograma,
            "qualidade_analise": self._avaliar_qualidade_analise(orgao_info, banca_info, cargos_info),
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        return resultado

    def _identificar_orgao_preciso(self, texto: str) -> Dict:
        """Identificação precisa do órgão"""
        texto_upper = texto.upper()
        
        orgaos_encontrados = []
        contextos = []
        
        for pattern in self.patterns_orgao:
            matches = re.finditer(pattern, texto_upper)
            for match in matches:
                orgao = match.group(1).strip()
                
                # Busca contexto (100 caracteres antes e depois)
                start = max(0, match.start() - 100)
                end = min(len(texto), match.end() + 100)
                contexto = texto[start:end]
                
                if len(orgao) > 3 and orgao not in [o["nome"] for o in orgaos_encontrados]:
                    orgaos_encontrados.append({
                        "nome": orgao,
                        "tipo": self._classificar_tipo_orgao(match.group(0)),
                        "contexto": contexto,
                        "confianca": self._calcular_confianca_orgao(contexto)
                    })
        
        # Ordena por confiança
        orgaos_encontrados.sort(key=lambda x: x["confianca"], reverse=True)
        
        resultado = {
            "orgao_principal": orgaos_encontrados[0] if orgaos_encontrados else {"nome": "NÃO IDENTIFICADO", "tipo": "Desconhecido", "confianca": 0},
            "outros_orgaos": orgaos_encontrados[1:5],  # Máximo 5 outros
            "total_encontrados": len(orgaos_encontrados)
        }
        
        if self.debug and orgaos_encontrados:
            st.success(f"✅ Órgão identificado: {resultado['orgao_principal']['nome']} (Confiança: {resultado['orgao_principal']['confianca']:.1f})")
        
        return resultado

    def _classificar_tipo_orgao(self, texto_match: str) -> str:
        """Classifica o tipo de órgão"""
        texto_upper = texto_match.upper()
        
        if "PREFEITURA" in texto_upper:
            return "Prefeitura Municipal"
        elif "CÂMARA" in texto_upper:
            return "Câmara Municipal"
        elif "TRIBUNAL" in texto_upper:
            return "Tribunal"
        elif "MINISTÉRIO" in texto_upper:
            return "Ministério Público"
        elif "SECRETARIA" in texto_upper:
            return "Secretaria"
        elif "FUNDAÇÃO" in texto_upper:
            return "Fundação"
        elif "INSTITUTO" in texto_upper:
            return "Instituto"
        elif "UNIVERSIDADE" in texto_upper:
            return "Universidade"
        else:
            return "Outros"

    def _calcular_confianca_orgao(self, contexto: str) -> float:
        """Calcula confiança da identificação do órgão"""
        score = 5.0  # Base
        
        contexto_upper = contexto.upper()
        
        # Indicadores positivos
        if "EDITAL" in contexto_upper:
            score += 2.0
        if "CONCURSO" in contexto_upper:
            score += 2.0
        if "PÚBLICO" in contexto_upper:
            score += 1.0
        if re.search(r"\d{4}", contexto):  # Ano
            score += 1.0
        
        return min(10.0, score)

    def _identificar_banca_precisa(self, texto: str) -> Dict:
        """Identificação precisa da banca"""
        texto_upper = texto.upper()
        
        bancas_encontradas = []
        
        for banca, patterns in self.patterns_banca.items():
            for pattern in patterns:
                matches = list(re.finditer(pattern, texto_upper))
                if matches:
                    # Busca contexto da primeira ocorrência
                    match = matches[0]
                    start = max(0, match.start() - 50)
                    end = min(len(texto), match.end() + 50)
                    contexto = texto[start:end]
                    
                    bancas_encontradas.append({
                        "nome": banca,
                        "ocorrencias": len(matches),
                        "contexto": contexto,
                        "confianca": len(matches) * 2.0  # Mais ocorrências = mais confiança
                    })
                    break
        
        # Ordena por confiança
        bancas_encontradas.sort(key=lambda x: x["confianca"], reverse=True)
        
        resultado = {
            "banca_principal": bancas_encontradas[0] if bancas_encontradas else {"nome": "NÃO IDENTIFICADA", "confianca": 0},
            "outras_bancas": bancas_encontradas[1:3],
            "total_encontradas": len(bancas_encontradas)
        }
        
        if self.debug and bancas_encontradas:
            st.success(f"✅ Banca identificada: {resultado['banca_principal']['nome']} (Confiança: {resultado['banca_principal']['confianca']:.1f})")
        
        return resultado

    def _extrair_cargos_precisos(self, texto: str) -> Dict:
        """Extração precisa de cargos com todas as informações"""
        
        # Padrões mais específicos para cargos
        patterns_cargo = [
            # Padrões em tabelas
            r"(?:CÓDIGO|CÓD\.?)\s*\|\s*(?:CARGO|FUNÇÃO)\s*\|\s*(?:VAGAS?)\s*\|\s*(?:SALÁRIO|REMUNERAÇÃO)",
            
            # Padrões diretos
            r"CARGO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,100})",
            r"FUNÇÃO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,100})",
            
            # Padrões específicos
            r"((?:AGENTE|ANALISTA|TÉCNICO|AUXILIAR|ASSISTENTE|ESPECIALISTA|INSPETOR|FISCAL|AUDITOR|PROFESSOR|COORDENADOR|DIRETOR|GERENTE|SUPERVISOR|SECRETÁRIO|OPERADOR|MOTORISTA)\s+(?:DE\s+|EM\s+|ADMINISTRATIVO|JUDICIÁRIO|MUNICIPAL|ESCOLAR|TRIBUTÁRIO|PEDAGÓGICO)?[A-ZÁÊÇÕ\s\-]*)",
        ]
        
        cargos_encontrados = {}
        texto_upper = texto.upper()
        
        # Busca por seções de cargos
        secoes_cargo = self._encontrar_secoes_cargo(texto)
        
        for secao in secoes_cargo:
            cargos_secao = self._processar_secao_cargo(secao)
            cargos_encontrados.update(cargos_secao)
        
        # Se não encontrou seções específicas, busca no texto geral
        if not cargos_encontrados:
            for pattern in patterns_cargo:
                matches = re.finditer(pattern, texto_upper)
                for match in matches:
                    if len(match.groups()) > 0:
                        cargo_nome = match.group(1).strip()
                        cargo_limpo = self._limpar_nome_cargo(cargo_nome)
                        
                        if self._validar_cargo(cargo_limpo):
                            detalhes = self._extrair_detalhes_cargo_contexto(texto, cargo_limpo, match.start(), match.end())
                            cargos_encontrados[cargo_limpo] = detalhes
        
        # Ordena cargos por qualidade das informações
        cargos_ordenados = self._ordenar_cargos_qualidade(cargos_encontrados)
        
        resultado = {
            "total_cargos": len(cargos_ordenados),
            "cargos_detalhados": cargos_ordenados,
            "qualidade_extracao": self._avaliar_qualidade_cargos(cargos_ordenados)
        }
        
        if self.debug:
            st.success(f"✅ {len(cargos_ordenados)} cargos extraídos com detalhes")
        
        return resultado

    def _encontrar_secoes_cargo(self, texto: str) -> List[str]:
        """Encontra seções específicas que contêm informações de cargos"""
        secoes = []
        
        # Padrões para identificar seções de cargo
        patterns_secao = [
            r"(?:QUADRO\s+DE\s+VAGAS|TABELA.*?CARGOS|ANEXO.*?CARGOS)(.*?)(?=ANEXO|CAPÍTULO|SEÇÃO|$)",
            r"(?:CARGOS?\s+E\s+VAGAS?)(.*?)(?=ANEXO|CAPÍTULO|SEÇÃO|$)",
            r"(?:DESCRIÇÃO\s+DOS\s+CARGOS?)(.*?)(?=ANEXO|CAPÍTULO|SEÇÃO|$)"
        ]
        
        for pattern in patterns_secao:
            matches = re.finditer(pattern, texto.upper(), re.DOTALL)
            for match in matches:
                secao = match.group(1)
                if len(secao) > 200:  # Só considera seções substanciais
                    secoes.append(secao)
        
        return secoes

    def _processar_secao_cargo(self, secao: str) -> Dict:
        """Processa uma seção específica de cargos"""
        cargos = {}
        
        # Divide a seção em blocos por cargo
        blocos = re.split(r'\n(?=(?:CARGO|FUNÇÃO|CÓDIGO))', secao)
        
        for bloco in blocos:
            if len(bloco) > 50:  # Só processa blocos substanciais
                cargo_info = self._extrair_info_bloco_cargo(bloco)
                if cargo_info and cargo_info["nome"]:
                    cargos[cargo_info["nome"]] = cargo_info
        
        return cargos

    def _extrair_info_bloco_cargo(self, bloco: str) -> Optional[Dict]:
        """Extrai informações de um bloco específico de cargo"""
        info = {
            "nome": "",
            "codigo": "Não informado",
            "vagas": "Não informado",
            "salario": "Não informado",
            "escolaridade": "Não informado",
            "carga_horaria": "Não informado",
            "requisitos": [],
            "atribuicoes": [],
            "conteudo_programatico": {}
        }
        
        bloco_upper = bloco.upper()
        
        # Extrai nome do cargo
        nome_patterns = [
            r"CARGO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,100})",
            r"FUNÇÃO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,100})",
            r"^([A-ZÁÊÇÕ\s\-]{10,100})"  # Primeira linha se for nome do cargo
        ]
        
        for pattern in nome_patterns:
            match = re.search(pattern, bloco_upper)
            if match:
                nome = self._limpar_nome_cargo(match.group(1))
                if self._validar_cargo(nome):
                    info["nome"] = nome
                    break
        
        if not info["nome"]:
            return None
        
        # Extrai código
        codigo_match = re.search(r"(?:CÓDIGO|CÓD\.?)\s*[:\-]?\s*(\w+)", bloco_upper)
        if codigo_match:
            info["codigo"] = codigo_match.group(1)
        
        # Extrai vagas
        vagas_patterns = [
            r"(\d+)\s*(?:VAGA|VAGAS)",
            r"VAGAS?\s*[:\-]\s*(\d+)",
            r"QUANTIDADE\s*[:\-]\s*(\d+)"
        ]
        
        for pattern in vagas_patterns:
            match = re.search(pattern, bloco_upper)
            if match:
                info["vagas"] = match.group(1)
                break
        
        # Extrai salário
        salario_patterns = [
            r"R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"(?:SALÁRIO|REMUNERAÇÃO|VENCIMENTO)\s*[:\-]?\s*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)"
        ]
        
        for pattern in salario_patterns:
            match = re.search(pattern, bloco)
            if match:
                info["salario"] = f"R$ {match.group(1)}"
                break
        
        # Extrai escolaridade
        escolaridade_patterns = [
            r"(?:ESCOLARIDADE|FORMAÇÃO|REQUISITO).*?((?:SUPERIOR|MÉDIO|FUNDAMENTAL)\s+COMPLETO)",
            r"(ENSINO\s+(?:SUPERIOR|MÉDIO|FUNDAMENTAL))",
            r"(NÍVEL\s+(?:SUPERIOR|MÉDIO|FUNDAMENTAL))",
            r"(GRADUAÇÃO|PÓS-GRADUAÇÃO)"
        ]
        
        for pattern in escolaridade_patterns:
            match = re.search(pattern, bloco_upper)
            if match:
                info["escolaridade"] = match.group(1).title()
                break
        
        # Extrai carga horária
        ch_patterns = [
            r"(\d+)\s*(?:HORAS?|H)\s*(?:SEMANAIS?|POR\s+SEMANA|/SEMANA)",
            r"CARGA\s+HORÁRIA\s*[:\-]?\s*(\d+)\s*(?:HORAS?|H)"
        ]
        
        for pattern in ch_patterns:
            match = re.search(pattern, bloco_upper)
            if match:
                info["carga_horaria"] = f"{match.group(1)}h/semana"
                break
        
        # Extrai requisitos
        if "REQUISITO" in bloco_upper:
            req_section = re.search(r"REQUISITOS?[:\-]?(.*?)(?=ATRIBUIÇÕES?|DESCRIÇÃO|CONTEÚDO|$)", bloco, re.DOTALL | re.IGNORECASE)
            if req_section:
                requisitos_text = req_section.group(1)
                req_items = re.findall(r"[-•]\s*([^\n\r]{10,300})", requisitos_text)
                info["requisitos"] = [req.strip() for req in req_items[:10]]
        
        # Extrai atribuições
        if "ATRIBUIÇ" in bloco_upper:
            attr_section = re.search(r"ATRIBUIÇÕES?[:\-]?(.*?)(?=REQUISITOS?|CONTEÚDO|$)", bloco, re.DOTALL | re.IGNORECASE)
            if attr_section:
                atribuicoes_text = attr_section.group(1)
                attr_items = re.findall(r"[-•]\s*([^\n\r]{10,300})", atribuicoes_text)
                info["atribuicoes"] = [attr.strip() for attr in attr_items[:10]]
        
        return info

    def _limpar_nome_cargo(self, nome_raw: str) -> str:
        """Limpa e normaliza nome do cargo"""
        nome = nome_raw.strip()
        
        # Remove caracteres especiais
        nome = re.sub(r'[^\w\s\-]', ' ', nome)
        nome = re.sub(r'\s+', ' ', nome)
        nome = nome.strip(' -')
        
        # Capitaliza corretamente
        palavras = nome.split()
        palavras_capitalizadas = []
        
        preposicoes = ['DE', 'DA', 'DO', 'E', 'EM', 'PARA', 'COM', 'NA', 'NO']
        
        for palavra in palavras:
            if palavra.upper() in preposicoes:
                palavras_capitalizadas.append(palavra.lower())
            else:
                palavras_capitalizadas.append(palavra.capitalize())
        
        return ' '.join(palavras_capitalizadas)

    def _validar_cargo(self, cargo: str) -> bool:
        """Valida se é um nome de cargo válido"""
        if len(cargo) < 5 or len(cargo) > 150:
            return False
        
        # Palavras que invalidam um cargo
        palavras_invalidas = [
            'EDITAL', 'CONCURSO', 'PÚBLICO', 'ANEXO', 'PÁGINA', 'ITEM', 'CAPÍTULO',
            'SEÇÃO', 'ARTIGO', 'PARÁGRAFO', 'INCISO', 'ALÍNEA', 'TABELA'
        ]
        
        cargo_upper = cargo.upper()
        if any(palavra in cargo_upper for palavra in palavras_invalidas):
            return False
        
        # Deve conter pelo menos uma palavra típica de cargo
        palavras_cargo = [
            'AGENTE', 'ANALISTA', 'TÉCNICO', 'AUXILIAR', 'ASSISTENTE', 'ESPECIALISTA',
            'INSPETOR', 'FISCAL', 'AUDITOR', 'PROFESSOR', 'COORDENADOR', 'DIRETOR',
            'GERENTE', 'SUPERVISOR', 'SECRETÁRIO', 'OPERADOR', 'MOTORISTA', 'VIGILANTE'
        ]
        
        return any(palavra in cargo_upper for palavra in palavras_cargo)

    def _extrair_detalhes_cargo_contexto(self, texto: str, cargo: str, start_pos: int, end_pos: int) -> Dict:
        """Extrai detalhes de um cargo baseado no contexto"""
        # Busca contexto ampliado (1000 caracteres antes e depois)
        context_start = max(0, start_pos - 1000)
        context_end = min(len(texto), end_pos + 1000)
        contexto = texto[context_start:context_end]
        
        return self._extrair_info_bloco_cargo(contexto) or {
            "nome": cargo,
            "codigo": "Não informado",
            "vagas": "Não informado",
            "salario": "Não informado",
            "escolaridade": "Não informado",
            "carga_horaria": "Não informado",
            "requisitos": [],
            "atribuicoes": [],
            "conteudo_programatico": {}
        }

    def _ordenar_cargos_qualidade(self, cargos: Dict) -> Dict:
        """Ordena cargos pela qualidade das informações extraídas"""
        def calcular_score_qualidade(info):
            score = 0
            
            # Pontos por informação disponível
            if info.get("vagas", "Não informado") != "Não informado":
                score += 3
            if info.get("salario", "Não informado") != "Não informado":
                score += 3
            if info.get("escolaridade", "Não informado") != "Não informado":
                score += 2
            if info.get("carga_horaria", "Não informado") != "Não informado":
                score += 1
            if info.get("codigo", "Não informado") != "Não informado":
                score += 1
            
            # Pontos por listas de requisitos/atribuições
            score += len(info.get("requisitos", [])) * 0.5
            score += len(info.get("atribuicoes", [])) * 0.5
            
            return score
        
        # Calcula score para cada cargo
        cargos_com_score = []
        for nome, info in cargos.items():
            score = calcular_score_qualidade(info)
            cargos_com_score.append((nome, info, score))
        
        # Ordena por score (maior primeiro)
        cargos_com_score.sort(key=lambda x: x[2], reverse=True)
        
        # Retorna dicionário ordenado
        return {nome: info for nome, info, score in cargos_com_score}

    def _avaliar_qualidade_cargos(self, cargos: Dict) -> str:
        """Avalia a qualidade geral da extração de cargos"""
        if not cargos:
            return "Muito Baixa"
        
        total_cargos = len(cargos)
        cargos_com_info_completa = 0
        
        for info in cargos.values():
            campos_preenchidos = 0
            if info.get("vagas", "Não informado") != "Não informado":
                campos_preenchidos += 1
            if info.get("salario", "Não informado") != "Não informado":
                campos_preenchidos += 1
            if info.get("escolaridade", "Não informado") != "Não informado":
                campos_preenchidos += 1
            
            if campos_preenchidos >= 2:
                cargos_com_info_completa += 1
        
        percentual_completo = (cargos_com_info_completa / total_cargos) * 100
        
        if percentual_completo >= 80:
            return "Muito Alta"
        elif percentual_completo >= 60:
            return "Alta"
        elif percentual_completo >= 40:
            return "Média"
        elif percentual_completo >= 20:
            return "Baixa"
        else:
            return "Muito Baixa"

    def _extrair_informacoes_gerais(self, texto: str) -> Dict:
        """Extrai informações gerais do edital"""
        info = {}
        
        # Taxa de inscrição
        taxa_patterns = [
            r"TAXA\s+DE\s+INSCRIÇÃO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"VALOR\s+DA\s+INSCRIÇÃO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"INSCRIÇÃO.*?VALOR.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)"
        ]
        
        for pattern in taxa_patterns:
            match = re.search(pattern, texto, re.IGNORECASE | re.DOTALL)
            if match:
                info["taxa_inscricao"] = f"R$ {match.group(1)}"
                break
        else:
            info["taxa_inscricao"] = "Não informado"
        
        # Local de inscrição
        local_patterns = [
            r"INSCRIÇÕES?.*?(?:SITE|ENDEREÇO|LOCAL).*?([A-Za-z0-9\.\-]+\.[a-z]{2,})",
            r"(?:SITE|PORTAL).*?INSCRIÇÕES?.*?([A-Za-z0-9\.\-]+\.[a-z]{2,})",
            r"www\.([A-Za-z0-9\.\-]+\.[a-z]{2,})"
        ]
        
        for pattern in local_patterns:
            match = re.search(pattern, texto, re.IGNORECASE)
            if match:
                info["local_inscricao"] = match.group(1)
                break
        else:
            info["local_inscricao"] = "Não informado"
        
        return info

    def _extrair_cronograma_preciso(self, texto: str) -> Dict:
        """Extrai cronograma com máxima precisão"""
        cronograma = {}
        
        # Padrões mais específicos para datas
        eventos_patterns = {
            "Publicação do Edital": [
                r"PUBLICAÇÃO\s+(?:DO\s+)?EDITAL.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"EDITAL.*?PUBLICADO.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
            ],
            "Início das Inscrições": [
                r"INÍCIO\s+DAS\s+INSCRIÇÕES.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"INSCRIÇÕES.*?(?:INÍCIO|ABERTURA).*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"PERÍODO\s+DE\s+INSCRIÇÕES?.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
            ],
            "Fim das Inscrições": [
                r"(?:FIM|TÉRMINO|ENCERRAMENTO)\s+DAS\s+INSCRIÇÕES.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"INSCRIÇÕES.*?(?:ATÉ|FINAL|TÉRMINO).*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
            ],
            "Data da Prova": [
                r"(?:DATA\s+DA\s+)?PROVA.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"APLICAÇÃO\s+(?:DA\s+|DAS\s+)?PROVAS?.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"EXAME.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
            ],
            "Divulgação do Resultado": [
                r"(?:DIVULGAÇÃO\s+(?:DO\s+)?|PUBLICAÇÃO\s+(?:DO\s+)?)RESULTADO.*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})",
                r"RESULTADO.*?(?:DIVULGADO|PUBLICADO).*?(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4})"
            ]
        }
        
        for evento, patterns in eventos_patterns.items():
            data_encontrada = None
            
            for pattern in patterns:
                matches = re.findall(pattern, texto, re.IGNORECASE | re.DOTALL)
                if matches:
                    # Pega a primeira data encontrada
                    data_encontrada = matches[0]
                    break
            
            cronograma[evento] = data_encontrada if data_encontrada else "Não informado"
        
        return cronograma

    def _avaliar_qualidade_analise(self, orgao_info: Dict, banca_info: Dict, cargos_info: Dict) -> str:
        """Avalia a qualidade geral da análise"""
        score = 0
        
        # Pontos por órgão identificado
        if orgao_info["orgao_principal"]["nome"] != "NÃO IDENTIFICADO":
            score += 2
        
        # Pontos por banca identificada
        if banca_info["banca_principal"]["nome"] != "NÃO IDENTIFICADA":
            score += 2
        
        # Pontos por cargos extraídos
        if cargos_info["total_cargos"] > 0:
            score += 3
            
            # Pontos extras por qualidade dos cargos
            if cargos_info["qualidade_extracao"] == "Muito Alta":
                score += 3
            elif cargos_info["qualidade_extracao"] == "Alta":
                score += 2
            elif cargos_info["qualidade_extracao"] == "Média":
                score += 1
        
        # Classificação final
        if score >= 8:
            return "Excelente"
        elif score >= 6:
            return "Boa"
        elif score >= 4:
            return "Regular"
        elif score >= 2:
            return "Baixa"
        else:
            return "Muito Baixa"

def render_edital_analyzer_pro():
    """Renderiza o analisador profissional de edital"""
    st.header("🎯 Analisador Profissional de Edital")
    st.write("Sistema de **análise de alta precisão** com extração específica e detalhada")
    
    analyzer = EditalAnalyzerPro()
    
    # Informações sobre capacidades
    st.info("💡 **Capacidades do Analisador Profissional:**")
    col_cap1, col_cap2, col_cap3 = st.columns(3)
    
    with col_cap1:
        st.write("**🔍 Extração Avançada:**")
        st.write("• PyMuPDF com análise estrutural")
        st.write("• pdfplumber para tabelas")
        st.write("• Múltiplos métodos de backup")
    
    with col_cap2:
        st.write("**📊 Análise Precisa:**")
        st.write("• Identificação de órgão e banca")
        st.write("• Extração completa de cargos")
        st.write("• Cronograma detalhado")
    
    with col_cap3:
        st.write("**🎯 Informações Específicas:**")
        st.write("• Vagas, salários, requisitos")
        st.write("• Escolaridade e carga horária")
        st.write("• Atribuições e conteúdo")
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "📄 Faça upload do edital (PDF)",
        type=['pdf'],
        help="Sistema profissional com múltiplas técnicas de extração"
    )
    
    if uploaded_file is not None:
        # Extração de texto com múltiplos métodos
        with st.spinner("🔍 Extraindo texto com técnicas avançadas..."):
            texto_edital, stats_extracao = analyzer.extrair_texto_multiplo(uploaded_file)
        
        if texto_edital and len(texto_edital.strip()) > 500:
            # Mostra estatísticas da extração
            st.subheader("📊 Estatísticas da Extração")
            
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            
            with col_stat1:
                st.metric("Método de Sucesso", stats_extracao["metodo_sucesso"])
            
            with col_stat2:
                st.metric("Qualidade", stats_extracao["qualidade_extracao"])
            
            with col_stat3:
                st.metric("Páginas Processadas", stats_extracao["total_paginas"])
            
            with col_stat4:
                st.metric("Caracteres Extraídos", f"{stats_extracao['caracteres_extraidos']:,}")
            
            # Mostra métodos tentados
            if stats_extracao["metodos_tentados"]:
                st.write(f"**Métodos tentados:** {', '.join(stats_extracao['metodos_tentados'])}")
            
            if stats_extracao["estrutura_detectada"]:
                st.success("✅ Estruturas importantes detectadas no documento!")
            
            # Botão para análise profissional
            if st.button("🚀 Iniciar Análise Profissional", type="primary"):
                
                # Análise completa
                resultado = analyzer.analisar_edital_profissional(texto_edital)
                
                # Salva resultado no session state
                st.session_state.analise_profissional = resultado
                
                st.success(f"✅ Análise profissional concluída! Qualidade: **{resultado['qualidade_analise']}**")
                st.rerun()
            
            # Opção para mostrar texto extraído
            if st.checkbox("📄 Mostrar texto extraído (Debug)"):
                with st.expander("Texto Completo Extraído"):
                    st.text_area("Conteúdo:", texto_edital[:3000] + "..." if len(texto_edital) > 3000 else texto_edital, height=400)
        
        else:
            st.error("❌ Extração de texto insuficiente. Verifique se o PDF não está protegido.")
    
    # Exibe resultado da análise profissional
    if 'analise_profissional' in st.session_state:
        resultado = st.session_state.analise_profissional
        
        st.divider()
        st.header("🎯 Resultado da Análise Profissional")
        
        # Métricas principais
        col_main1, col_main2, col_main3, col_main4 = st.columns(4)
        
        with col_main1:
            st.metric("🏢 Órgão", resultado["orgao"]["orgao_principal"]["nome"][:20] + "..." if len(resultado["orgao"]["orgao_principal"]["nome"]) > 20 else resultado["orgao"]["orgao_principal"]["nome"])
        
        with col_main2:
            st.metric("🏛️ Banca", resultado["banca"]["banca_principal"]["nome"])
        
        with col_main3:
            st.metric("💼 Cargos Encontrados", resultado["cargos"]["total_cargos"])
        
        with col_main4:
            st.metric("📊 Qualidade da Análise", resultado["qualidade_analise"])
        
        # Detalhes do órgão
        st.subheader("🏢 Informações do Órgão")
        orgao_info = resultado["orgao"]["orgao_principal"]
        
        col_org1, col_org2 = st.columns(2)
        
        with col_org1:
            st.write(f"**Nome:** {orgao_info['nome']}")
            st.write(f"**Tipo:** {orgao_info.get('tipo', 'Não classificado')}")
            st.write(f"**Confiança:** {orgao_info.get('confianca', 0):.1f}/10")
        
        with col_org2:
            if resultado["orgao"]["outros_orgaos"]:
                st.write("**Outros órgãos mencionados:**")
                for outro in resultado["orgao"]["outros_orgaos"][:3]:
                    st.write(f"• {outro['nome']}")
        
        # Detalhes da banca
        st.subheader("🏛️ Banca Organizadora")
        banca_info = resultado["banca"]["banca_principal"]
        
        col_banca1, col_banca2 = st.columns(2)
        
        with col_banca1:
            st.write(f"**Banca:** {banca_info['nome']}")
            st.write(f"**Confiança:** {banca_info.get('confianca', 0):.1f}/10")
        
        with col_banca2:
            if resultado["banca"]["outras_bancas"]:
                st.write("**Outras bancas mencionadas:**")
                for outra in resultado["banca"]["outras_bancas"]:
                    st.write(f"• {outra['nome']}")
        
        # Cargos detalhados
        st.subheader("💼 Cargos Identificados")
        
        if resultado["cargos"]["cargos_detalhados"]:
            # Seletor de cargo para visualização
            nomes_cargos = list(resultado["cargos"]["cargos_detalhados"].keys())
            cargo_selecionado = st.selectbox(
                "Selecione um cargo para ver detalhes:",
                options=nomes_cargos,
                help="Escolha o cargo para visualizar informações completas"
            )
            
            # Exibe detalhes do cargo selecionado
            if cargo_selecionado:
                detalhes_cargo = resultado["cargos"]["cargos_detalhados"][cargo_selecionado]
                
                st.write(f"### 📋 Detalhes: {cargo_selecionado}")
                
                # Informações básicas do cargo
                col_cargo1, col_cargo2, col_cargo3 = st.columns(3)
                
                with col_cargo1:
                    st.metric("👥 Vagas", detalhes_cargo.get("vagas", "N/I"))
                    st.metric("🆔 Código", detalhes_cargo.get("codigo", "N/I"))
                
                with col_cargo2:
                    st.metric("💰 Salário", detalhes_cargo.get("salario", "N/I"))
                    st.metric("⏰ Carga Horária", detalhes_cargo.get("carga_horaria", "N/I"))
                
                with col_cargo3:
                    st.metric("🎓 Escolaridade", detalhes_cargo.get("escolaridade", "N/I"))
                
                # Requisitos e atribuições
                col_req_attr1, col_req_attr2 = st.columns(2)
                
                with col_req_attr1:
                    if detalhes_cargo.get("requisitos"):
                        st.write("**📋 Requisitos:**")
                        for req in detalhes_cargo["requisitos"][:5]:
                            st.write(f"• {req}")
                
                with col_req_attr2:
                    if detalhes_cargo.get("atribuicoes"):
                        st.write("**⚙️ Atribuições:**")
                        for attr in detalhes_cargo["atribuicoes"][:5]:
                            st.write(f"• {attr}")
            
            # Tabela resumo de todos os cargos
            with st.expander("📊 Tabela Resumo de Todos os Cargos"):
                dados_tabela = []
                for nome, detalhes in resultado["cargos"]["cargos_detalhados"].items():
                    dados_tabela.append({
                        "Cargo": nome,
                        "Código": detalhes.get("codigo", "N/I"),
                        "Vagas": detalhes.get("vagas", "N/I"),
                        "Salário": detalhes.get("salario", "N/I"),
                        "Escolaridade": detalhes.get("escolaridade", "N/I"),
                        "Carga Horária": detalhes.get("carga_horaria", "N/I")
                    })
                
                df_cargos = pd.DataFrame(dados_tabela)
                st.dataframe(df_cargos, use_container_width=True)
        
        else:
            st.warning("⚠️ Nenhum cargo foi identificado com detalhes suficientes.")
        
        # Cronograma
        st.subheader("📅 Cronograma do Concurso")
        cronograma = resultado["cronograma"]
        
        # Tabela do cronograma
        dados_cronograma = []
        for evento, data in cronograma.items():
            status = "✅ Informado" if data != "Não informado" else "❌ Não informado"
            dados_cronograma.append({
                "Evento": evento,
                "Data": data,
                "Status": status
            })
        
        df_cronograma = pd.DataFrame(dados_cronograma)
        st.dataframe(df_cronograma, use_container_width=True)
        
        # Informações gerais
        if resultado.get("informacoes_gerais"):
            st.subheader("📋 Informações Gerais")
            info_gerais = resultado["informacoes_gerais"]
            
            col_info1, col_info2 = st.columns(2)
            
            with col_info1:
                st.write(f"**💳 Taxa de Inscrição:** {info_gerais.get('taxa_inscricao', 'N/I')}")
            
            with col_info2:
                st.write(f"**🌐 Local de Inscrição:** {info_gerais.get('local_inscricao', 'N/I')}")
        
        # Botões de ação
        col_btn1, col_btn2, col_btn3 = st.columns(3)
        
        with col_btn1:
            if st.button("🔄 Nova Análise"):
                del st.session_state.analise_profissional
                st.rerun()
        
        with col_btn2:
            if st.button("📥 Baixar Relatório JSON"):
                relatorio_json = json.dumps(resultado, ensure_ascii=False, indent=2, default=str)
                st.download_button(
                    label="💾 Download JSON",
                    data=relatorio_json,
                    file_name=f"analise_profissional_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        with col_btn3:
            if st.button("📄 Relatório Markdown"):
                # Gera relatório em markdown
                relatorio_md = f"""
# RELATÓRIO PROFISSIONAL DE ANÁLISE DE EDITAL

**Data da Análise:** {resultado['timestamp']}
**Qualidade da Análise:** {resultado['qualidade_analise']}

## 🏢 Órgão
**Nome:** {resultado['orgao']['orgao_principal']['nome']}
**Tipo:** {resultado['orgao']['orgao_principal'].get('tipo', 'N/I')}
**Confiança:** {resultado['orgao']['orgao_principal'].get('confianca', 0):.1f}/10

## 🏛️ Banca Organizadora
**Banca:** {resultado['banca']['banca_principal']['nome']}
**Confiança:** {resultado['banca']['banca_principal'].get('confianca', 0):.1f}/10

## 💼 Cargos Identificados ({resultado['cargos']['total_cargos']})

{chr(10).join([f"### {nome}{chr(10)}- **Vagas:** {detalhes.get('vagas', 'N/I')}{chr(10)}- **Salário:** {detalhes.get('salario', 'N/I')}{chr(10)}- **Escolaridade:** {detalhes.get('escolaridade', 'N/I')}{chr(10)}- **Carga Horária:** {detalhes.get('carga_horaria', 'N/I')}{chr(10)}" for nome, detalhes in resultado['cargos']['cargos_detalhados'].items()])}

## 📅 Cronograma
{chr(10).join([f"- **{evento}:** {data}" for evento, data in resultado['cronograma'].items()])}

## 📋 Informações Gerais
- **Taxa de Inscrição:** {resultado.get('informacoes_gerais', {}).get('taxa_inscricao', 'N/I')}
- **Local de Inscrição:** {resultado.get('informacoes_gerais', {}).get('local_inscricao', 'N/I')}
"""
                
                st.download_button(
                    label="📄 Download Markdown",
                    data=relatorio_md,
                    file_name=f"relatorio_profissional_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                    mime="text/markdown"
                )
    
    else:
        # Instruções de uso
        st.info("💡 **Como usar o Analisador Profissional:**")
        st.write("""
        1. **📄 Upload**: Faça upload do PDF do edital
        2. **🔍 Extração Avançada**: Sistema usa múltiplas técnicas para máxima precisão
        3. **🎯 Análise Profissional**: Processamento completo com barra de progresso
        4. **📊 Resultados Detalhados**: Visualização completa de todas as informações
        5. **📥 Relatórios**: Download em JSON ou Markdown para uso posterior
        """)
        
        st.warning("⚠️ **Para melhor desempenho:**")
        st.write("""
        - Use PDFs em formato texto (não imagens escaneadas)
        - Editais com estrutura organizada funcionam melhor
        - O sistema detecta automaticamente a melhor técnica de extração
        """)