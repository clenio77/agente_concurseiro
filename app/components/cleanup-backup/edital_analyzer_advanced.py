"""
Analisador Avançado de Edital - Versão Específica
Sistema que realmente extrai informações específicas do edital
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import re
from typing import Dict, List, Tuple, Optional
import PyPDF2
import io

class EditalAnalyzerAdvanced:
    """Analisador avançado que extrai informações reais do edital"""
    
    def __init__(self):
        self.debug_mode = True
    
    def extrair_texto_completo_pdf(self, arquivo_pdf) -> str:
        """Extrai todo o texto do PDF com máxima precisão"""
        try:
            arquivo_pdf.seek(0)
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(arquivo_pdf.read()))
            
            texto_completo = ""
            total_paginas = len(pdf_reader.pages)
            
            st.info(f"📄 PDF possui {total_paginas} páginas. Extraindo texto...")
            
            progress_bar = st.progress(0)
            
            for i, pagina in enumerate(pdf_reader.pages):
                try:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina.strip():
                        texto_completo += f"\n=== PÁGINA {i+1} ===\n"
                        texto_completo += texto_pagina + "\n"
                    
                    # Atualiza barra de progresso
                    progress_bar.progress((i + 1) / total_paginas)
                    
                except Exception as e:
                    st.warning(f"⚠️ Erro na página {i+1}: {str(e)}")
                    continue
            
            progress_bar.empty()
            
            if len(texto_completo.strip()) < 100:
                st.error("❌ Texto extraído muito pequeno. PDF pode estar protegido ou ser uma imagem.")
                return ""
            
            st.success(f"✅ Texto extraído: {len(texto_completo)} caracteres, {len(texto_completo.split())} palavras")
            return texto_completo
            
        except Exception as e:
            st.error(f"❌ Erro ao processar PDF: {str(e)}")
            return ""
    
    def analisar_edital_completo(self, texto: str) -> Dict:
        """Análise completa e específica do edital"""
        
        st.subheader("🔍 Análise Detalhada do Edital")
        
        # 1. IDENTIFICAÇÃO DO ÓRGÃO
        st.write("### 🏢 Identificando Órgão...")
        orgao_info = self._identificar_orgao_especifico(texto)
        
        # 2. IDENTIFICAÇÃO DE CARGOS
        st.write("### 💼 Identificando Cargos...")
        cargos_info = self._identificar_cargos_especificos(texto)
        
        # 3. INFORMAÇÕES BÁSICAS
        st.write("### 📋 Extraindo Informações Básicas...")
        info_basicas = self._extrair_informacoes_especificas(texto)
        
        # 4. CONTEÚDO PROGRAMÁTICO
        st.write("### 📚 Analisando Conteúdo Programático...")
        conteudo_info = self._extrair_conteudo_real(texto)
        
        # 5. CRONOGRAMA E DATAS
        st.write("### 📅 Identificando Cronograma...")
        cronograma_info = self._extrair_cronograma_completo(texto)
        
        return {
            "orgao": orgao_info,
            "cargos": cargos_info,
            "informacoes_basicas": info_basicas,
            "conteudo_programatico": conteudo_info,
            "cronograma": cronograma_info,
            "texto_original": texto[:1000] + "..." if len(texto) > 1000 else texto
        }
    
    def _identificar_orgao_especifico(self, texto: str) -> Dict:
        """Identifica o órgão com máxima precisão"""
        texto_upper = texto.upper()
        
        # Busca por padrões muito específicos
        patterns_orgao = [
            # Prefeituras
            r"PREFEITURA\s+MUNICIPAL\s+DE\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"PREFEITURA\s+DE\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            
            # Câmaras
            r"CÂMARA\s+MUNICIPAL\s+DE\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            
            # Tribunais
            r"TRIBUNAL\s+DE\s+JUSTIÇA\s+(?:DO|DA|DE)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"TRIBUNAL\s+REGIONAL\s+(?:DO|DA|DE)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            
            # Ministério Público
            r"MINISTÉRIO\s+PÚBLICO\s+(?:DO|DA|DE)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            
            # Secretarias
            r"SECRETARIA\s+(?:MUNICIPAL\s+|ESTADUAL\s+)?(?:DE|DA)\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            
            # Outros órgãos
            r"FUNDAÇÃO\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"INSTITUTO\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"UNIVERSIDADE\s+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"AUTARQUIA\s+([A-ZÁÊÇÕ\s\-]{3,50})"
        ]
        
        orgaos_encontrados = []
        
        for pattern in patterns_orgao:
            matches = re.findall(pattern, texto_upper)
            for match in matches:
                orgao = match.strip()
                if len(orgao) > 2 and orgao not in orgaos_encontrados:
                    orgaos_encontrados.append(orgao)
        
        # Busca por contexto adicional
        contexto_orgao = ""
        if orgaos_encontrados:
            primeiro_orgao = orgaos_encontrados[0]
            # Busca por mais informações sobre o órgão
            pattern_contexto = rf"({primeiro_orgao}.*?)(?:\n.*?\n|\.|;)"
            match_contexto = re.search(pattern_contexto, texto_upper)
            if match_contexto:
                contexto_orgao = match_contexto.group(1)
        
        resultado = {
            "orgaos_identificados": orgaos_encontrados,
            "orgao_principal": orgaos_encontrados[0] if orgaos_encontrados else "NÃO IDENTIFICADO",
            "contexto": contexto_orgao,
            "confianca": "Alta" if orgaos_encontrados else "Baixa"
        }
        
        # Debug
        if self.debug_mode:
            st.write(f"**🔍 Órgãos encontrados:** {orgaos_encontrados}")
            if contexto_orgao:
                st.write(f"**📝 Contexto:** {contexto_orgao[:200]}...")
        
        return resultado
    
    def _identificar_cargos_especificos(self, texto: str) -> Dict:
        """Identifica cargos com máxima precisão"""
        texto_upper = texto.upper()
        
        # Padrões específicos para diferentes tipos de cargo
        patterns_cargo = [
            # Padrões diretos
            r"CARGO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,80})",
            r"FUNÇÃO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,80})",
            r"EMPREGO\s*[:\-]\s*([A-ZÁÊÇÕ\s\-]{5,80})",
            
            # Padrões com contexto
            r"PARA\s+O\s+CARGO\s+DE\s+([A-ZÁÊÇÕ\s\-]{5,80})",
            r"DO\s+CARGO\s+DE\s+([A-ZÁÊÇÕ\s\-]{5,80})",
            r"CONCURSO\s+PARA\s+([A-ZÁÊÇÕ\s\-]{5,80})",
            
            # Cargos específicos comuns
            r"(AGENTE\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(ANALISTA\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(TÉCNICO\s+(?:EM\s+|DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(AUXILIAR\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(ASSISTENTE\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(ESPECIALISTA\s+(?:EM\s+|DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(INSPETOR\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(FISCAL\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(AUDITOR\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(PROFESSOR\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(COORDENADOR\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(DIRETOR\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(GERENTE\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})",
            r"(SUPERVISOR\s+(?:DE\s+)?[A-ZÁÊÇÕ\s\-]{5,50})"
        ]
        
        cargos_encontrados = []
        cargos_detalhados = {}
        
        for pattern in patterns_cargo:
            matches = re.findall(pattern, texto_upper)
            for match in matches:
                cargo = match.strip()
                cargo = re.sub(r'\s+', ' ', cargo)  # Normaliza espaços
                
                # Filtra cargos válidos
                if (len(cargo) > 5 and len(cargo) < 100 and
                    not any(palavra in cargo for palavra in ['EDITAL', 'CONCURSO', 'PÚBLICO', 'ANEXO', 'PÁGINA']) and
                    cargo not in cargos_encontrados):
                    
                    cargos_encontrados.append(cargo)
                    
                    # Busca informações adicionais sobre o cargo
                    info_cargo = self._extrair_info_cargo(texto_upper, cargo)
                    cargos_detalhados[cargo] = info_cargo
        
        resultado = {
            "cargos_identificados": cargos_encontrados,
            "total_cargos": len(cargos_encontrados),
            "detalhes_cargos": cargos_detalhados,
            "confianca": "Alta" if cargos_encontrados else "Baixa"
        }
        
        # Debug
        if self.debug_mode:
            st.write(f"**🔍 Cargos encontrados:** {len(cargos_encontrados)}")
            for cargo in cargos_encontrados[:5]:  # Mostra apenas os primeiros 5
                st.write(f"• {cargo}")
        
        return resultado
    
    def _extrair_info_cargo(self, texto: str, cargo: str) -> Dict:
        """Extrai informações específicas sobre um cargo"""
        info = {
            "vagas": "Não informado",
            "salario": "Não informado",
            "escolaridade": "Não informado",
            "carga_horaria": "Não informado"
        }
        
        # Busca por informações próximas ao cargo
        pattern_contexto = rf"{re.escape(cargo)}.{{0,500}}"
        match = re.search(pattern_contexto, texto, re.IGNORECASE | re.DOTALL)
        
        if match:
            contexto = match.group(0)
            
            # Extrai vagas
            vaga_match = re.search(r"(\d+)\s*(?:VAGA|VAGAS)", contexto, re.IGNORECASE)
            if vaga_match:
                info["vagas"] = vaga_match.group(1)
            
            # Extrai salário
            salario_match = re.search(r"R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)", contexto)
            if salario_match:
                info["salario"] = f"R$ {salario_match.group(1)}"
            
            # Extrai escolaridade
            escolaridade_patterns = [
                r"(SUPERIOR\s+COMPLETO)",
                r"(MÉDIO\s+COMPLETO)",
                r"(FUNDAMENTAL\s+COMPLETO)",
                r"(ENSINO\s+SUPERIOR)",
                r"(ENSINO\s+MÉDIO)",
                r"(NÍVEL\s+SUPERIOR)",
                r"(NÍVEL\s+MÉDIO)"
            ]
            
            for pattern in escolaridade_patterns:
                match_esc = re.search(pattern, contexto, re.IGNORECASE)
                if match_esc:
                    info["escolaridade"] = match_esc.group(1)
                    break
            
            # Extrai carga horária
            ch_match = re.search(r"(\d+)\s*(?:HORAS?|H)\s*(?:SEMANAIS?|POR\s+SEMANA)", contexto, re.IGNORECASE)
            if ch_match:
                info["carga_horaria"] = f"{ch_match.group(1)}h/semana"
        
        return info
    
    def _extrair_informacoes_especificas(self, texto: str) -> Dict:
        """Extrai informações básicas específicas"""
        info = {}
        
        # Taxa de inscrição
        taxa_patterns = [
            r"TAXA\s+DE\s+INSCRIÇÃO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"VALOR\s+DA\s+INSCRIÇÃO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"INSCRIÇÃO.*?R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)"
        ]
        
        for pattern in taxa_patterns:
            match = re.search(pattern, texto, re.IGNORECASE | re.DOTALL)
            if match:
                info["taxa_inscricao"] = f"R$ {match.group(1)}"
                break
        else:
            info["taxa_inscricao"] = "Não informado"
        
        # Período de inscrições
        inscricao_patterns = [
            r"INSCRIÇÕES.*?(\d{1,2}/\d{1,2}/\d{4}).*?(\d{1,2}/\d{1,2}/\d{4})",
            r"PERÍODO.*?INSCRIÇÃO.*?(\d{1,2}/\d{1,2}/\d{4}).*?(\d{1,2}/\d{1,2}/\d{4})"
        ]
        
        for pattern in inscricao_patterns:
            match = re.search(pattern, texto, re.IGNORECASE | re.DOTALL)
            if match:
                info["periodo_inscricoes"] = {
                    "inicio": match.group(1),
                    "fim": match.group(2)
                }
                break
        else:
            info["periodo_inscricoes"] = {"inicio": "Não informado", "fim": "Não informado"}
        
        # Data da prova
        prova_patterns = [
            r"PROVA.*?(\d{1,2}/\d{1,2}/\d{4})",
            r"EXAME.*?(\d{1,2}/\d{1,2}/\d{4})",
            r"DATA.*?PROVA.*?(\d{1,2}/\d{1,2}/\d{4})"
        ]
        
        for pattern in prova_patterns:
            match = re.search(pattern, texto, re.IGNORECASE | re.DOTALL)
            if match:
                info["data_prova"] = match.group(1)
                break
        else:
            info["data_prova"] = "Não informado"
        
        # Debug
        if self.debug_mode:
            st.write("**📋 Informações extraídas:**")
            for chave, valor in info.items():
                st.write(f"• **{chave}:** {valor}")
        
        return info
    
    def _extrair_conteudo_real(self, texto: str) -> Dict:
        """Extrai o conteúdo programático real do edital"""
        conteudo = {}
        texto_upper = texto.upper()
        
        # Busca pela seção de conteúdo programático
        secoes_patterns = [
            r"CONTEÚDO\s+PROGRAMÁTICO(.*?)(?=ANEXO|CRONOGRAMA|BIBLIOGRAFIA|EDITAL\s+N|$)",
            r"PROGRAMA\s+DAS\s+PROVAS(.*?)(?=ANEXO|CRONOGRAMA|BIBLIOGRAFIA|EDITAL\s+N|$)",
            r"CONTEÚDO\s+DAS\s+PROVAS(.*?)(?=ANEXO|CRONOGRAMA|BIBLIOGRAFIA|EDITAL\s+N|$)",
            r"DISCIPLINAS\s+E\s+CONTEÚDOS(.*?)(?=ANEXO|CRONOGRAMA|BIBLIOGRAFIA|EDITAL\s+N|$)"
        ]
        
        secao_conteudo = ""
        for pattern in secoes_patterns:
            match = re.search(pattern, texto_upper, re.DOTALL)
            if match:
                secao_conteudo = match.group(1)
                st.success(f"✅ Seção de conteúdo encontrada! ({len(secao_conteudo)} caracteres)")
                break
        
        if not secao_conteudo:
            st.warning("⚠️ Seção específica não encontrada. Analisando texto completo...")
            secao_conteudo = texto_upper
        
        # Extrai matérias específicas
        materias_patterns = {
            "Português": [
                r"PORTUGUÊS[:\s]*(.*?)(?=MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|LEGISLAÇÃO|$)",
                r"LÍNGUA\s+PORTUGUESA[:\s]*(.*?)(?=MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|LEGISLAÇÃO|$)"
            ],
            "Matemática": [
                r"MATEMÁTICA[:\s]*(.*?)(?=PORTUGUÊS|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|LEGISLAÇÃO|$)"
            ],
            "Direito Constitucional": [
                r"DIREITO\s+CONSTITUCIONAL[:\s]*(.*?)(?=DIREITO\s+ADMINISTRATIVO|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|CONHECIMENTOS|$)"
            ],
            "Direito Administrativo": [
                r"DIREITO\s+ADMINISTRATIVO[:\s]*(.*?)(?=DIREITO\s+CONSTITUCIONAL|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|CONHECIMENTOS|$)"
            ],
            "Informática": [
                r"INFORMÁTICA[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|LEGISLAÇÃO|$)",
                r"NOÇÕES\s+DE\s+INFORMÁTICA[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|LEGISLAÇÃO|$)"
            ],
            "Conhecimentos Específicos": [
                r"CONHECIMENTOS\s+ESPECÍFICOS[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|RACIOCÍNIO|ATUALIDADES|$)"
            ],
            "Legislação": [
                r"LEGISLAÇÃO[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)"
            ],
            "Atualidades": [
                r"ATUALIDADES[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|LEGISLAÇÃO|$)"
            ]
        }
        
        for materia, patterns in materias_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, secao_conteudo, re.DOTALL)
                if match:
                    conteudo_materia = match.group(1).strip()
                    
                    if len(conteudo_materia) > 30:  # Só considera se tem conteúdo substancial
                        topicos = self._extrair_topicos_reais(conteudo_materia)
                        if topicos:
                            conteudo[materia] = topicos
                        break
        
        # Debug
        if self.debug_mode:
            st.write(f"**📚 Matérias encontradas:** {len(conteudo)}")
            for materia, topicos in conteudo.items():
                st.write(f"• **{materia}:** {len(topicos)} tópicos")
        
        return conteudo
    
    def _extrair_topicos_reais(self, texto_materia: str) -> List[str]:
        """Extrai tópicos reais de uma seção de matéria"""
        topicos = []
        
        # Padrões para diferentes formatações
        patterns_topicos = [
            r'(\d+\.?\d*\.?\s+[^\n\r]{10,200})',  # 1. Tópico ou 1.1 Tópico
            r'([a-z]\)\s*[^\n\r]{10,200})',       # a) Tópico
            r'([-•]\s*[^\n\r]{10,200})',          # - Tópico ou • Tópico
            r'([A-ZÁÊÇÕ][^\n\r.]{15,200}\.)',     # Frases que terminam com ponto
            r'([A-ZÁÊÇÕ][^\n\r;]{15,200};)',      # Frases que terminam com ponto e vírgula
        ]
        
        for pattern in patterns_topicos:
            matches = re.findall(pattern, texto_materia)
            for match in matches:
                topico = match.strip()
                # Limpa numeração e marcadores
                topico = re.sub(r'^\d+\.?\d*\.?\s*', '', topico)
                topico = re.sub(r'^[a-z]\)\s*', '', topico)
                topico = re.sub(r'^[-•]\s*', '', topico)
                
                if (len(topico) > 10 and len(topico) < 300 and
                    topico not in topicos and
                    not topico.upper().startswith(('ANEXO', 'PÁGINA', 'EDITAL'))):
                    topicos.append(topico)
        
        # Se não encontrou tópicos formatados, divide por quebras de linha
        if not topicos:
            linhas = texto_materia.split('\n')
            for linha in linhas:
                linha = linha.strip()
                if len(linha) > 15 and len(linha) < 300:
                    topicos.append(linha)
        
        return topicos[:25]  # Limita a 25 tópicos por matéria
    
    def _extrair_cronograma_completo(self, texto: str) -> Dict:
        """Extrai cronograma completo do edital"""
        cronograma = {}
        
        # Busca por datas importantes
        eventos_patterns = {
            "Publicação do Edital": [
                r"PUBLICAÇÃO.*?(\d{1,2}/\d{1,2}/\d{4})",
                r"EDITAL.*?PUBLICADO.*?(\d{1,2}/\d{1,2}/\d{4})"
            ],
            "Início das Inscrições": [
                r"INÍCIO.*?INSCRIÇÕES.*?(\d{1,2}/\d{1,2}/\d{4})",
                r"INSCRIÇÕES.*?INÍCIO.*?(\d{1,2}/\d{1,2}/\d{4})"
            ],
            "Fim das Inscrições": [
                r"(?:FIM|TÉRMINO|FINAL).*?INSCRIÇÕES.*?(\d{1,2}/\d{1,2}/\d{4})",
                r"INSCRIÇÕES.*?(?:ATÉ|FINAL).*?(\d{1,2}/\d{1,2}/\d{4})"
            ],
            "Data da Prova": [
                r"PROVA.*?(\d{1,2}/\d{1,2}/\d{4})",
                r"EXAME.*?(\d{1,2}/\d{1,2}/\d{4})",
                r"APLICAÇÃO.*?PROVA.*?(\d{1,2}/\d{1,2}/\d{4})"
            ],
            "Resultado": [
                r"RESULTADO.*?(\d{1,2}/\d{1,2}/\d{4})",
                r"DIVULGAÇÃO.*?RESULTADO.*?(\d{1,2}/\d{1,2}/\d{4})"
            ]
        }
        
        for evento, patterns in eventos_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, texto, re.IGNORECASE | re.DOTALL)
                if match:
                    cronograma[evento] = match.group(1)
                    break
            else:
                cronograma[evento] = "Não informado"
        
        # Debug
        if self.debug_mode:
            st.write("**📅 Cronograma extraído:**")
            for evento, data in cronograma.items():
                st.write(f"• **{evento}:** {data}")
        
        return cronograma

def render_edital_analyzer_advanced():
    """Renderiza o analisador avançado de edital"""
    st.header("🔍 Análise Avançada de Edital")
    st.write("Sistema que extrai informações **reais e específicas** do seu edital")
    
    analyzer = EditalAnalyzerAdvanced()
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "📄 Faça upload do edital (PDF)",
        type=['pdf'],
        help="Envie o arquivo PDF do edital para análise detalhada e específica"
    )
    
    if uploaded_file is not None:
        # Extrai texto completo
        texto_edital = analyzer.extrair_texto_completo_pdf(uploaded_file)
        
        if texto_edital and len(texto_edital.strip()) > 100:
            
            # Opção de debug
            debug_mode = st.checkbox("🔧 Modo Debug (mostrar detalhes da extração)", value=False)
            analyzer.debug_mode = debug_mode
            
            # Botão para iniciar análise
            if st.button("🚀 Iniciar Análise Completa", type="primary"):
                
                with st.spinner("🤖 Analisando edital em detalhes..."):
                    # Análise completa
                    resultado = analyzer.analisar_edital_completo(texto_edital)
                
                # Exibe resultados
                st.success("✅ Análise concluída!")
                
                # Informações do Órgão
                st.subheader("🏢 Órgão Identificado")
                orgao_info = resultado["orgao"]
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Órgão Principal", orgao_info["orgao_principal"])
                    st.metric("Confiança", orgao_info["confianca"])
                
                with col2:
                    if len(orgao_info["orgaos_identificados"]) > 1:
                        st.write("**Outros órgãos encontrados:**")
                        for orgao in orgao_info["orgaos_identificados"][1:]:
                            st.write(f"• {orgao}")
                
                # Informações dos Cargos
                st.subheader("💼 Cargos Identificados")
                cargos_info = resultado["cargos"]
                
                if cargos_info["cargos_identificados"]:
                    st.metric("Total de Cargos", cargos_info["total_cargos"])
                    
                    # Tabela de cargos
                    dados_cargos = []
                    for cargo in cargos_info["cargos_identificados"]:
                        detalhes = cargos_info["detalhes_cargos"].get(cargo, {})
                        dados_cargos.append({
                            "Cargo": cargo,
                            "Vagas": detalhes.get("vagas", "N/I"),
                            "Salário": detalhes.get("salario", "N/I"),
                            "Escolaridade": detalhes.get("escolaridade", "N/I"),
                            "Carga Horária": detalhes.get("carga_horaria", "N/I")
                        })
                    
                    df_cargos = pd.DataFrame(dados_cargos)
                    st.dataframe(df_cargos, use_container_width=True)
                else:
                    st.warning("⚠️ Nenhum cargo específico foi identificado")
                
                # Informações Básicas
                st.subheader("📋 Informações Básicas")
                info_basicas = resultado["informacoes_basicas"]
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Taxa de Inscrição", info_basicas.get("taxa_inscricao", "N/I"))
                
                with col2:
                    periodo = info_basicas.get("periodo_inscricoes", {})
                    st.write("**Período de Inscrições:**")
                    st.write(f"Início: {periodo.get('inicio', 'N/I')}")
                    st.write(f"Fim: {periodo.get('fim', 'N/I')}")
                
                with col3:
                    st.metric("Data da Prova", info_basicas.get("data_prova", "N/I"))
                
                # Conteúdo Programático
                st.subheader("📚 Conteúdo Programático Extraído")
                conteudo = resultado["conteudo_programatico"]
                
                if conteudo:
                    # Gráfico de distribuição
                    materias = list(conteudo.keys())
                    num_topicos = [len(topicos) for topicos in conteudo.values()]
                    
                    fig = px.bar(
                        x=materias,
                        y=num_topicos,
                        title="📊 Número de Tópicos por Matéria",
                        labels={"x": "Matérias", "y": "Número de Tópicos"}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detalhes por matéria
                    for materia, topicos in conteudo.items():
                        with st.expander(f"📖 {materia} ({len(topicos)} tópicos)"):
                            for i, topico in enumerate(topicos, 1):
                                st.write(f"{i}. {topico}")
                else:
                    st.warning("⚠️ Conteúdo programático não foi encontrado ou não está estruturado")
                
                # Cronograma
                st.subheader("📅 Cronograma do Concurso")
                cronograma = resultado["cronograma"]
                
                # Tabela do cronograma
                dados_cronograma = []
                for evento, data in cronograma.items():
                    dados_cronograma.append({
                        "Evento": evento,
                        "Data": data,
                        "Status": "✅ Informado" if data != "Não informado" else "❌ Não informado"
                    })
                
                df_cronograma = pd.DataFrame(dados_cronograma)
                st.dataframe(df_cronograma, use_container_width=True)
                
                # Opção para baixar relatório
                if st.button("📥 Gerar Relatório Completo"):
                    relatorio = f"""
# RELATÓRIO DE ANÁLISE DE EDITAL

## Órgão
{orgao_info['orgao_principal']}

## Cargos Identificados
{chr(10).join([f"- {cargo}" for cargo in cargos_info['cargos_identificados']])}

## Informações Básicas
- Taxa de Inscrição: {info_basicas.get('taxa_inscricao', 'N/I')}
- Data da Prova: {info_basicas.get('data_prova', 'N/I')}

## Conteúdo Programático
{chr(10).join([f"### {materia}{chr(10)}{chr(10).join([f'- {topico}' for topico in topicos])}" for materia, topicos in conteudo.items()])}

## Cronograma
{chr(10).join([f"- {evento}: {data}" for evento, data in cronograma.items()])}
"""
                    
                    st.download_button(
                        label="📄 Baixar Relatório (Markdown)",
                        data=relatorio,
                        file_name=f"relatorio_edital_{orgao_info['orgao_principal'][:20]}.md",
                        mime="text/markdown"
                    )
            
            # Opção para mostrar texto extraído
            if st.checkbox("📄 Mostrar texto extraído do PDF"):
                with st.expander("Texto Completo Extraído"):
                    st.text_area("Conteúdo:", texto_edital, height=400)
        
        else:
            st.error("❌ Não foi possível extrair texto suficiente do PDF. Verifique se o arquivo não está protegido ou corrompido.")
    
    else:
        # Informações sobre o sistema
        st.info("💡 **Como funciona a Análise Avançada:**")
        st.write("""
        1. **Extração Precisa**: Extrai todo o texto do PDF com máxima precisão
        2. **Identificação Específica**: Identifica órgão, cargos e informações reais
        3. **Conteúdo Real**: Extrai o conteúdo programático específico do edital
        4. **Cronograma Detalhado**: Identifica todas as datas importantes
        5. **Relatório Completo**: Gera relatório detalhado para download
        """)
        
        st.warning("⚠️ **Importante**: Este sistema funciona melhor com editais em formato texto (não imagem)")