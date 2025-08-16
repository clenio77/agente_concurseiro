"""
Análise Completa de Edital - Agente Concurseiro v2.0
Sistema avançado de análise e extração de informações de editais
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re
import json
from typing import Dict, List, Tuple, Optional
import PyPDF2
import io

class EditalAnalyzerComplete:
    """Analisador completo de editais com funcionalidades avançadas"""
    
    def __init__(self):
        self.bancas_conhecidas = {
            "CESPE/CEBRASPE": {
                "estilo": "Questões longas, interpretativas, pegadinhas sutis",
                "caracteristicas": ["Textos longos", "Múltipla escolha", "Certo/Errado"],
                "dificuldade": "Alta",
                "areas_forte": ["Direito", "Administração", "Português"]
            },
            "FCC": {
                "estilo": "Questões diretas, conhecimento técnico",
                "caracteristicas": ["Objetivas", "Técnicas", "Múltipla escolha"],
                "dificuldade": "Média-Alta",
                "areas_forte": ["Contabilidade", "Administração", "Direito"]
            },
            "FGV": {
                "estilo": "Questões elaboradas, raciocínio lógico",
                "caracteristicas": ["Analíticas", "Contextualizadas", "Múltipla escolha"],
                "dificuldade": "Alta",
                "areas_forte": ["Economia", "Administração", "Direito"]
            },
            "VUNESP": {
                "estilo": "Questões práticas, aplicação do conhecimento",
                "caracteristicas": ["Práticas", "Diretas", "Múltipla escolha"],
                "dificuldade": "Média",
                "areas_forte": ["Educação", "Saúde", "Segurança"]
            }
        }
        
        self.materias_padrao = {
            "Português": ["gramática", "interpretação", "redação", "literatura"],
            "Matemática": ["aritmética", "álgebra", "geometria", "estatística"],
            "Direito Constitucional": ["princípios", "direitos fundamentais", "organização do estado"],
            "Direito Administrativo": ["atos administrativos", "licitações", "contratos"],
            "Informática": ["hardware", "software", "internet", "segurança"],
            "Atualidades": ["política", "economia", "sociedade", "meio ambiente"],
            "Raciocínio Lógico": ["lógica proposicional", "sequências", "problemas"],
            "Conhecimentos Específicos": ["área técnica", "legislação específica"]
        }

    def extrair_texto_pdf(self, arquivo_pdf) -> str:
        """Extrai texto de arquivo PDF com múltiplas tentativas"""
        try:
            # Primeira tentativa com PyPDF2
            arquivo_pdf.seek(0)  # Reset file pointer
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(arquivo_pdf.read()))
            texto_completo = ""
            
            for i, pagina in enumerate(pdf_reader.pages):
                try:
                    texto_pagina = pagina.extract_text()
                    if texto_pagina.strip():
                        texto_completo += f"\n--- PÁGINA {i+1} ---\n"
                        texto_completo += texto_pagina + "\n"
                except Exception as e:
                    st.warning(f"Erro ao extrair página {i+1}: {str(e)}")
                    continue
            
            # Se não conseguiu extrair texto suficiente, tenta com pdfplumber
            if len(texto_completo.strip()) < 100:
                try:
                    import pdfplumber
                    arquivo_pdf.seek(0)
                    with pdfplumber.open(io.BytesIO(arquivo_pdf.read())) as pdf:
                        texto_completo = ""
                        for i, page in enumerate(pdf.pages):
                            try:
                                texto_pagina = page.extract_text()
                                if texto_pagina:
                                    texto_completo += f"\n--- PÁGINA {i+1} ---\n"
                                    texto_completo += texto_pagina + "\n"
                            except:
                                continue
                except ImportError:
                    st.warning("pdfplumber não disponível. Usando apenas PyPDF2.")
            
            return texto_completo
        except Exception as e:
            st.error(f"Erro ao extrair texto do PDF: {str(e)}")
            return ""

    def identificar_banca(self, texto: str) -> str:
        """Identifica a banca organizadora do concurso"""
        texto_upper = texto.upper()
        
        for banca in self.bancas_conhecidas.keys():
            if banca.upper() in texto_upper:
                return banca
        
        # Busca por variações
        if "CEBRASPE" in texto_upper or "CESPE" in texto_upper:
            return "CESPE/CEBRASPE"
        elif "FUNDAÇÃO CARLOS CHAGAS" in texto_upper:
            return "FCC"
        elif "FUNDAÇÃO GETÚLIO VARGAS" in texto_upper:
            return "FGV"
        
        return "Não identificada"

    def extrair_informacoes_basicas(self, texto: str) -> Dict:
        """Extrai informações básicas do edital"""
        info = {
            "orgao": self._extrair_orgao(texto),
            "cargo": self._extrair_cargo(texto),
            "vagas": self._extrair_vagas(texto),
            "salario": self._extrair_salario(texto),
            "escolaridade": self._extrair_escolaridade(texto),
            "inscricoes": self._extrair_periodo_inscricoes(texto),
            "prova": self._extrair_data_prova(texto),
            "taxa_inscricao": self._extrair_taxa_inscricao(texto)
        }
        return info

    def _extrair_orgao(self, texto: str) -> str:
        """Extrai o órgão do concurso com múltiplos padrões"""
        # Limpa o texto para melhor processamento
        texto_limpo = re.sub(r'\s+', ' ', texto.upper())
        
        patterns = [
            # Padrões específicos para órgãos
            r"(?:PREFEITURA\s+(?:MUNICIPAL\s+)?(?:DE|DA)\s+)([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:CÂMARA\s+MUNICIPAL\s+(?:DE|DA)\s+)([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:TRIBUNAL\s+(?:DE\s+)?(?:JUSTIÇA|CONTAS)\s*(?:DO|DA|DE)?\s*)([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:MINISTÉRIO\s+(?:PÚBLICO|DA)\s*)([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:SECRETARIA\s+(?:DE|DA)\s*)([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:FUNDAÇÃO\s+)([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:INSTITUTO\s+)([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:UNIVERSIDADE\s+)([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:ÓRGÃO|ORGAO|ENTIDADE)[\s:]+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"CONCURSO\s+PÚBLICO[\s\n]*(?:PARA\s+)?([A-ZÁÊÇÕ\s\-]{5,50})",
            r"EDITAL[\s\w]*[\s\n]*(?:DE\s+)?(?:CONCURSO\s+)?(?:PÚBLICO\s+)?(?:PARA\s+)?([A-ZÁÊÇÕ\s\-]{5,50})"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, texto_limpo)
            for match in matches:
                orgao = match.strip()
                # Filtra resultados muito genéricos
                if len(orgao) > 3 and not any(palavra in orgao for palavra in ['EDITAL', 'CONCURSO', 'PÚBLICO']):
                    return orgao
        
        # Busca por nomes específicos conhecidos
        orgaos_conhecidos = [
            'COLETORA RECONHECIDA PELO MINISTÉRIO',
            'TRIBUNAL DE JUSTIÇA',
            'PREFEITURA MUNICIPAL',
            'CÂMARA MUNICIPAL',
            'MINISTÉRIO PÚBLICO',
            'SECRETARIA DE',
            'FUNDAÇÃO',
            'INSTITUTO',
            'UNIVERSIDADE'
        ]
        
        for orgao in orgaos_conhecidos:
            if orgao in texto_limpo:
                # Tenta extrair o nome completo
                pattern = rf"{orgao}\s+([A-ZÁÊÇÕ\s\-]{{3,30}})"
                match = re.search(pattern, texto_limpo)
                if match:
                    return f"{orgao} {match.group(1).strip()}"
                return orgao
        
        return "Não identificado"

    def _extrair_cargo(self, texto: str) -> List[str]:
        """Extrai os cargos disponíveis com padrões mais específicos"""
        cargos = []
        texto_upper = texto.upper()
        
        # Padrões mais específicos para cargos
        patterns = [
            # Padrões diretos
            r"CARGO[\s:]+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"FUNÇÃO[\s:]+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"EMPREGO[\s:]+([A-ZÁÊÇÕ\s\-]{3,50})",
            
            # Padrões com contexto
            r"(?:PARA\s+O\s+CARGO\s+DE|PARA\s+A\s+FUNÇÃO\s+DE)[\s:]+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:DO\s+CARGO\s+DE|DA\s+FUNÇÃO\s+DE)[\s:]+([A-ZÁÊÇÕ\s\-]{3,50})",
            r"(?:CONCURSO\s+PARA)[\s:]+([A-ZÁÊÇÕ\s\-]{3,50})",
            
            # Padrões específicos para diferentes tipos de cargo
            r"(AGENTE\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(ANALISTA\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(TÉCNICO\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(AUXILIAR\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(ASSISTENTE\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(ESPECIALISTA\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(INSPETOR\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(FISCAL\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(AUDITOR\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(PROFESSOR\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(COORDENADOR\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(DIRETOR\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(GERENTE\s+[A-ZÁÊÇÕ\s\-]{3,30})",
            r"(SUPERVISOR\s+[A-ZÁÊÇÕ\s\-]{3,30})"
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, texto_upper)
            for match in matches:
                cargo = match.strip()
                # Limpa e valida o cargo
                cargo = re.sub(r'\s+', ' ', cargo)  # Remove espaços extras
                cargo = cargo.strip(' -')  # Remove traços e espaços das bordas
                
                # Filtra cargos muito genéricos ou inválidos
                if (len(cargo) > 3 and 
                    not any(palavra in cargo for palavra in ['EDITAL', 'CONCURSO', 'PÚBLICO', 'ANEXO']) and
                    cargo not in cargos):
                    cargos.append(cargo)
        
        # Se não encontrou cargos específicos, busca por padrões mais gerais
        if not cargos:
            # Busca por linhas que podem conter nomes de cargos
            linhas = texto_upper.split('\n')
            for linha in linhas:
                linha = linha.strip()
                # Procura por linhas que começam com palavras típicas de cargo
                if any(linha.startswith(palavra) for palavra in ['AGENTE', 'ANALISTA', 'TÉCNICO', 'AUXILIAR', 'ASSISTENTE']):
                    if len(linha) < 100:  # Evita linhas muito longas
                        cargos.append(linha)
        
        # Remove duplicatas e limita
        cargos_unicos = []
        for cargo in cargos:
            if cargo not in cargos_unicos:
                cargos_unicos.append(cargo)
        
        return cargos_unicos[:10] if cargos_unicos else ["Não identificado"]

    def _extrair_vagas(self, texto: str) -> str:
        """Extrai número de vagas"""
        patterns = [
            r"(\d+)\s*(?:VAGA|VAGAS)",
            r"(?:VAGA|VAGAS)[\s:]*(\d+)",
            r"TOTAL DE (\d+) VAGAS"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto.upper())
            if match:
                return match.group(1)
        
        return "Não informado"

    def _extrair_salario(self, texto: str) -> str:
        """Extrai informações salariais"""
        patterns = [
            r"R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"SALÁRIO[\s:]*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"REMUNERAÇÃO[\s:]*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto)
            if match:
                return f"R$ {match.group(1)}"
        
        return "Não informado"

    def _extrair_escolaridade(self, texto: str) -> str:
        """Extrai requisitos de escolaridade"""
        patterns = [
            r"(?:ESCOLARIDADE|FORMAÇÃO)[\s:]*([A-ZÁÊÇÕ\s]+)",
            r"(?:NÍVEL|GRAU)[\s:]*([A-ZÁÊÇÕ\s]+)",
            r"(?:SUPERIOR|MÉDIO|FUNDAMENTAL)[\s\w]*(?:COMPLETO|INCOMPLETO)?"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto.upper())
            if match:
                return match.group(1).strip() if match.groups() else match.group(0)
        
        return "Não informado"

    def _extrair_periodo_inscricoes(self, texto: str) -> Dict:
        """Extrai período de inscrições"""
        patterns = [
            r"INSCRIÇÕES[\s\w]*(\d{1,2}/\d{1,2}/\d{4})[\s\w]*(\d{1,2}/\d{1,2}/\d{4})",
            r"(\d{1,2}/\d{1,2}/\d{4})[\s\w]*(\d{1,2}/\d{1,2}/\d{4})"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto)
            if match:
                return {
                    "inicio": match.group(1),
                    "fim": match.group(2)
                }
        
        return {"inicio": "Não informado", "fim": "Não informado"}

    def _extrair_data_prova(self, texto: str) -> str:
        """Extrai data da prova"""
        patterns = [
            r"PROVA[\s\w]*(\d{1,2}/\d{1,2}/\d{4})",
            r"EXAME[\s\w]*(\d{1,2}/\d{1,2}/\d{4})",
            r"(\d{1,2}/\d{1,2}/\d{4})[\s\w]*PROVA"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto)
            if match:
                return match.group(1)
        
        return "Não informado"

    def _extrair_taxa_inscricao(self, texto: str) -> str:
        """Extrai taxa de inscrição"""
        patterns = [
            r"TAXA[\s\w]*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)",
            r"INSCRIÇÃO[\s\w]*R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, texto)
            if match:
                return f"R$ {match.group(1)}"
        
        return "Não informado"

    def extrair_conteudo_programatico(self, texto: str) -> Dict:
        """Extrai conteúdo programático detalhado do texto real do edital"""
        conteudo = {}
        texto_upper = texto.upper()
        
        # Padrões mais específicos para encontrar seções de conteúdo
        patterns_secao = [
            r"CONTEÚDO\s+PROGRAMÁTICO(.*?)(?=ANEXO|CRONOGRAMA|BIBLIOGRAFIA|EDITAL|$)",
            r"PROGRAMA\s+DAS\s+PROVAS(.*?)(?=ANEXO|CRONOGRAMA|BIBLIOGRAFIA|EDITAL|$)",
            r"CONTEÚDO\s+DAS\s+PROVAS(.*?)(?=ANEXO|CRONOGRAMA|BIBLIOGRAFIA|EDITAL|$)",
            r"MATÉRIAS\s+E\s+CONTEÚDOS(.*?)(?=ANEXO|CRONOGRAMA|BIBLIOGRAFIA|EDITAL|$)",
            r"DISCIPLINAS(.*?)(?=ANEXO|CRONOGRAMA|BIBLIOGRAFIA|EDITAL|$)"
        ]
        
        secao_conteudo = ""
        for pattern in patterns_secao:
            match = re.search(pattern, texto_upper, re.DOTALL)
            if match:
                secao_conteudo = match.group(1)
                st.info(f"✅ Seção de conteúdo programático encontrada! ({len(secao_conteudo)} caracteres)")
                break
        
        if not secao_conteudo:
            # Tenta buscar por padrões mais gerais
            patterns_gerais = [
                r"(PORTUGUÊS.*?(?=MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|$))",
                r"(MATEMÁTICA.*?(?=PORTUGUÊS|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|$))",
                r"(DIREITO\s+CONSTITUCIONAL.*?(?=DIREITO\s+ADMINISTRATIVO|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|$))",
                r"(DIREITO\s+ADMINISTRATIVO.*?(?=DIREITO\s+CONSTITUCIONAL|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|$))",
                r"(INFORMÁTICA.*?(?=PORTUGUÊS|MATEMÁTICA|DIREITO|CONHECIMENTOS|RACIOCÍNIO|$))",
                r"(CONHECIMENTOS\s+ESPECÍFICOS.*?(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|$))"
            ]
            
            for pattern in patterns_gerais:
                matches = re.findall(pattern, texto_upper, re.DOTALL)
                for match in matches:
                    if len(match) > 50:  # Só considera se tem conteúdo substancial
                        secao_conteudo += match + "\n\n"
        
        if secao_conteudo:
            # Extrai matérias específicas do texto real
            conteudo = self._extrair_materias_reais(secao_conteudo, texto)
        else:
            st.warning("⚠️ Não foi possível encontrar seção de conteúdo programático específica. Usando análise geral do texto.")
            # Fallback: analisa o texto completo
            conteudo = self._analisar_texto_completo(texto)
        
        return conteudo

    def _extrair_materias_reais(self, secao_conteudo: str, texto_completo: str) -> Dict:
        """Extrai matérias e tópicos reais do conteúdo programático"""
        conteudo = {}
        
        # Padrões para identificar matérias
        materias_patterns = {
            "Português": [
                r"PORTUGUÊS[:\s]*(.*?)(?=MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)",
                r"LÍNGUA\s+PORTUGUESA[:\s]*(.*?)(?=MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)"
            ],
            "Matemática": [
                r"MATEMÁTICA[:\s]*(.*?)(?=PORTUGUÊS|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)",
                r"MATEMÁTICA\s+E\s+RACIOCÍNIO[:\s]*(.*?)(?=PORTUGUÊS|DIREITO|INFORMÁTICA|CONHECIMENTOS|ATUALIDADES|$)"
            ],
            "Direito Constitucional": [
                r"DIREITO\s+CONSTITUCIONAL[:\s]*(.*?)(?=DIREITO\s+ADMINISTRATIVO|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|CONHECIMENTOS|$)",
                r"CONSTITUCIONAL[:\s]*(.*?)(?=ADMINISTRATIVO|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|CONHECIMENTOS|$)"
            ],
            "Direito Administrativo": [
                r"DIREITO\s+ADMINISTRATIVO[:\s]*(.*?)(?=DIREITO\s+CONSTITUCIONAL|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|CONHECIMENTOS|$)",
                r"ADMINISTRATIVO[:\s]*(.*?)(?=CONSTITUCIONAL|PORTUGUÊS|MATEMÁTICA|INFORMÁTICA|CONHECIMENTOS|$)"
            ],
            "Informática": [
                r"INFORMÁTICA[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)",
                r"NOÇÕES\s+DE\s+INFORMÁTICA[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|CONHECIMENTOS|RACIOCÍNIO|ATUALIDADES|$)"
            ],
            "Conhecimentos Específicos": [
                r"CONHECIMENTOS\s+ESPECÍFICOS[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|RACIOCÍNIO|ATUALIDADES|$)",
                r"CONHECIMENTOS\s+TÉCNICOS[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|RACIOCÍNIO|ATUALIDADES|$)"
            ],
            "Raciocínio Lógico": [
                r"RACIOCÍNIO\s+LÓGICO[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|ATUALIDADES|$)",
                r"LÓGICA[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|ATUALIDADES|$)"
            ],
            "Atualidades": [
                r"ATUALIDADES[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS|RACIOCÍNIO|$)",
                r"CONHECIMENTOS\s+GERAIS[:\s]*(.*?)(?=PORTUGUÊS|MATEMÁTICA|DIREITO|INFORMÁTICA|CONHECIMENTOS\s+ESPECÍFICOS|RACIOCÍNIO|$)"
            ]
        }
        
        for materia, patterns in materias_patterns.items():
            topicos_encontrados = []
            
            for pattern in patterns:
                match = re.search(pattern, secao_conteudo.upper(), re.DOTALL)
                if match:
                    conteudo_materia = match.group(1).strip()
                    
                    if len(conteudo_materia) > 20:  # Só considera se tem conteúdo substancial
                        # Extrai tópicos específicos
                        topicos = self._extrair_topicos_especificos(conteudo_materia)
                        topicos_encontrados.extend(topicos)
                        break
            
            if topicos_encontrados:
                # Remove duplicatas e limpa
                topicos_limpos = []
                for topico in topicos_encontrados:
                    topico_limpo = re.sub(r'^\d+\.?\s*', '', topico.strip())
                    topico_limpo = re.sub(r'^[a-z]\)\s*', '', topico_limpo)
                    topico_limpo = re.sub(r'^[-•]\s*', '', topico_limpo)
                    
                    if len(topico_limpo) > 5 and topico_limpo not in topicos_limpos:
                        topicos_limpos.append(topico_limpo)
                
                if topicos_limpos:
                    conteudo[materia] = topicos_limpos[:20]  # Limita a 20 tópicos por matéria
        
        return conteudo

    def _extrair_topicos_especificos(self, texto_materia: str) -> List[str]:
        """Extrai tópicos específicos de uma seção de matéria"""
        topicos = []
        
        # Padrões para diferentes tipos de formatação de tópicos
        patterns_topicos = [
            r'(\d+\.?\d*\.?\s+[^\n\r]+)',  # 1. Tópico ou 1.1 Tópico
            r'([a-z]\)\s*[^\n\r]+)',       # a) Tópico
            r'([-•]\s*[^\n\r]+)',          # - Tópico ou • Tópico
            r'([A-ZÁÊÇÕ][^\n\r.]{10,100}\.)',  # Frases que terminam com ponto
            r'([A-ZÁÊÇÕ][^\n\r;]{10,100};)',   # Frases que terminam com ponto e vírgula
        ]
        
        for pattern in patterns_topicos:
            matches = re.findall(pattern, texto_materia)
            for match in matches:
                topico = match.strip()
                if len(topico) > 10 and len(topico) < 200:  # Filtra tópicos muito curtos ou longos
                    topicos.append(topico)
        
        # Se não encontrou tópicos formatados, divide por quebras de linha
        if not topicos:
            linhas = texto_materia.split('\n')
            for linha in linhas:
                linha = linha.strip()
                if len(linha) > 10 and len(linha) < 200:
                    topicos.append(linha)
        
        return topicos[:15]  # Limita a 15 tópicos

    def _analisar_texto_completo(self, texto: str) -> Dict:
        """Analisa o texto completo quando não encontra seção específica"""
        conteudo = {}
        
        # Busca por palavras-chave relacionadas a cada matéria
        materias_keywords = {
            "Português": [
                "gramática", "ortografia", "acentuação", "concordância", "regência", 
                "crase", "pontuação", "sintaxe", "morfologia", "semântica", "interpretação",
                "redação", "literatura", "figuras de linguagem"
            ],
            "Matemática": [
                "números", "operações", "frações", "porcentagem", "juros", "geometria",
                "álgebra", "equações", "funções", "estatística", "probabilidade"
            ],
            "Direito Constitucional": [
                "constituição", "direitos fundamentais", "organização do estado", "poderes",
                "federalismo", "município", "união", "estado", "princípios constitucionais"
            ],
            "Direito Administrativo": [
                "administração pública", "atos administrativos", "licitação", "contratos",
                "servidores públicos", "processo administrativo", "responsabilidade civil"
            ],
            "Informática": [
                "windows", "word", "excel", "powerpoint", "internet", "email", "navegador",
                "hardware", "software", "segurança", "vírus", "backup"
            ],
            "Conhecimentos Específicos": [
                "legislação específica", "normas técnicas", "procedimentos", "regulamentos"
            ]
        }
        
        texto_lower = texto.lower()
        
        for materia, keywords in materias_keywords.items():
            topicos_encontrados = []
            count_keywords = 0
            
            for keyword in keywords:
                if keyword in texto_lower:
                    count_keywords += 1
                    # Tenta extrair contexto ao redor da palavra-chave
                    pattern = rf'.{{0,50}}{re.escape(keyword)}.{{0,50}}'
                    matches = re.findall(pattern, texto_lower, re.IGNORECASE)
                    
                    for match in matches[:3]:  # Máximo 3 contextos por palavra-chave
                        contexto = match.strip()
                        if len(contexto) > 20:
                            topicos_encontrados.append(contexto.capitalize())
            
            # Se encontrou pelo menos 2 palavras-chave, considera que a matéria está presente
            if count_keywords >= 2:
                if not topicos_encontrados:
                    topicos_encontrados = [f"Tópicos relacionados a {keyword.capitalize()}" for keyword in keywords[:5]]
                
                conteudo[materia] = topicos_encontrados[:10]
        
        return conteudo

    def _extrair_topicos_materia(self, texto: str, materia: str, topicos_base: List[str]) -> List[str]:
        """Extrai tópicos específicos de uma matéria"""
        topicos_encontrados = []
        
        # Busca a seção da matéria
        pattern_materia = rf"{materia.upper()}[\s:]*([^A-Z]*?)(?=[A-Z]{{3,}}|$)"
        match = re.search(pattern_materia, texto.upper())
        
        if match:
            secao_materia = match.group(1)
            
            # Extrai tópicos numerados ou com marcadores
            patterns_topicos = [
                r"(\d+\.?\s*[^\n\d]+)",
                r"([a-z]\)\s*[^\n]+)",
                r"(-\s*[^\n]+)",
                r"(•\s*[^\n]+)"
            ]
            
            for pattern in patterns_topicos:
                matches = re.findall(pattern, secao_materia)
                topicos_encontrados.extend([topico.strip() for topico in matches])
        
        return topicos_encontrados if topicos_encontrados else topicos_base

    def calcular_pesos_materias(self, conteudo: Dict) -> Dict:
        """Calcula pesos estimados das matérias baseado no conteúdo"""
        pesos = {}
        total_topicos = sum(len(topicos) for topicos in conteudo.values())
        
        if total_topicos > 0:
            for materia, topicos in conteudo.items():
                peso = (len(topicos) / total_topicos) * 100
                pesos[materia] = round(peso, 1)
        
        return pesos

    def gerar_cronograma_estudos(self, conteudo: Dict, pesos: Dict, dias_estudo: int = 90) -> Dict:
        """Gera cronograma de estudos personalizado"""
        cronograma = {}
        
        # Calcula horas por matéria baseado no peso
        horas_totais = dias_estudo * 4  # 4 horas/dia média
        
        for materia, peso in pesos.items():
            horas_materia = int((peso / 100) * horas_totais)
            dias_materia = max(1, horas_materia // 4)
            
            cronograma[materia] = {
                "horas_total": horas_materia,
                "dias_estudo": dias_materia,
                "horas_por_dia": min(4, horas_materia // dias_materia) if dias_materia > 0 else 1,
                "topicos": conteudo.get(materia, []),
                "prioridade": "Alta" if peso > 20 else "Média" if peso > 10 else "Baixa"
            }
        
        return cronograma

    def analisar_banca_historico(self, banca: str) -> Dict:
        """Analisa histórico e características da banca"""
        if banca in self.bancas_conhecidas:
            info_banca = self.bancas_conhecidas[banca].copy()
            
            # Adiciona dicas específicas
            info_banca["dicas_estudo"] = self._gerar_dicas_banca(banca)
            info_banca["questoes_exemplo"] = self._gerar_exemplos_questoes(banca)
            
            return info_banca
        
        return {"erro": "Banca não encontrada na base de dados"}

    def _gerar_dicas_banca(self, banca: str) -> List[str]:
        """Gera dicas específicas para cada banca"""
        dicas = {
            "CESPE/CEBRASPE": [
                "Leia com atenção - há pegadinhas sutis",
                "Foque em interpretação de texto",
                "Treine questões Certo/Errado",
                "Atenção aos detalhes nas assertivas"
            ],
            "FCC": [
                "Estude teoria de forma aprofundada",
                "Foque em conhecimento técnico",
                "Pratique questões objetivas",
                "Memorize conceitos importantes"
            ],
            "FGV": [
                "Desenvolva raciocínio analítico",
                "Estude casos práticos",
                "Foque em aplicação do conhecimento",
                "Treine interpretação contextual"
            ],
            "VUNESP": [
                "Estude aplicação prática",
                "Foque em conhecimentos específicos",
                "Pratique questões diretas",
                "Revise legislação atualizada"
            ]
        }
        
        return dicas.get(banca, ["Estude de forma consistente", "Pratique questões regularmente"])

    def _gerar_exemplos_questoes(self, banca: str) -> List[str]:
        """Gera exemplos de questões típicas da banca"""
        exemplos = {
            "CESPE/CEBRASPE": [
                "A Constituição Federal estabelece que todos são iguais perante a lei.",
                "O servidor público pode acumular dois cargos privativos de médico.",
                "A licitação é obrigatória para todas as contratações públicas."
            ],
            "FCC": [
                "Qual o prazo para interposição de recurso administrativo?",
                "São características do ato administrativo:",
                "A respeito dos contratos administrativos, é correto afirmar:"
            ],
            "FGV": [
                "Considerando o caso apresentado, analise as alternativas:",
                "Na situação descrita, o procedimento correto seria:",
                "Com base no contexto, é possível concluir que:"
            ]
        }
        
        return exemplos.get(banca, ["Exemplo não disponível para esta banca"])

def render_edital_analyzer_complete():
    """Renderiza o componente de análise completa de edital"""
    st.header("📋 Análise Completa de Edital")
    
    analyzer = EditalAnalyzerComplete()
    
    # Upload de arquivo
    uploaded_file = st.file_uploader(
        "📄 Faça upload do edital (PDF)",
        type=['pdf'],
        help="Envie o arquivo PDF do edital para análise completa"
    )
    
    if uploaded_file is not None:
        with st.spinner("🔍 Extraindo texto do PDF..."):
            # Extrai texto do PDF
            texto_edital = analyzer.extrair_texto_pdf(uploaded_file)
            
            if texto_edital:
                # Mostra estatísticas do texto extraído
                st.success(f"✅ Texto extraído com sucesso! ({len(texto_edital)} caracteres, {len(texto_edital.split())} palavras)")
                
                # Opção para mostrar texto extraído (debug)
                if st.checkbox("🔍 Mostrar texto extraído (Debug)", help="Visualize o texto que foi extraído do PDF"):
                    with st.expander("📄 Texto Extraído do PDF"):
                        st.text_area("Conteúdo:", texto_edital[:5000] + "..." if len(texto_edital) > 5000 else texto_edital, height=300)
                
                with st.spinner("🤖 Analisando conteúdo do edital..."):
                    # Identifica banca primeiro
                    banca = analyzer.identificar_banca(texto_edital)
                    st.info(f"🏛️ **Banca Identificada:** {banca}")
                    
                    # Extrai informações básicas
                    info_basicas = analyzer.extrair_informacoes_basicas(texto_edital)
                    
                    # Debug das informações extraídas
                    if st.checkbox("🔧 Debug - Informações Extraídas"):
                        st.json(info_basicas)
                    
                    # Extrai conteúdo programático
                    conteudo = analyzer.extrair_conteudo_programatico(texto_edital)
                    
                    # Debug do conteúdo programático
                    if st.checkbox("🔧 Debug - Conteúdo Programático"):
                        st.json(conteudo)
            
            if texto_edital and len(texto_edital.strip()) > 100:
                # Análise completa
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.subheader("📊 Informações Básicas")
                    
                    # Identifica banca
                    banca = analyzer.identificar_banca(texto_edital)
                    st.info(f"🏛️ **Banca:** {banca}")
                    
                    # Extrai informações básicas
                    info_basicas = analyzer.extrair_informacoes_basicas(texto_edital)
                    
                    # Exibe informações em cards
                    col_info1, col_info2 = st.columns(2)
                    
                    with col_info1:
                        st.metric("🏢 Órgão", info_basicas['orgao'])
                        st.metric("💰 Salário", info_basicas['salario'])
                        st.metric("🎓 Escolaridade", info_basicas['escolaridade'])
                    
                    with col_info2:
                        st.metric("👥 Vagas", info_basicas['vagas'])
                        st.metric("💳 Taxa", info_basicas['taxa_inscricao'])
                        st.metric("📅 Prova", info_basicas['prova'])
                    
                    # Cargos disponíveis
                    if isinstance(info_basicas['cargo'], list):
                        st.write("**🎯 Cargos:**")
                        for cargo in info_basicas['cargo']:
                            st.write(f"• {cargo}")
                    
                    # Período de inscrições
                    inscricoes = info_basicas['inscricoes']
                    if isinstance(inscricoes, dict):
                        st.write(f"**📝 Inscrições:** {inscricoes['inicio']} a {inscricoes['fim']}")
                
                with col2:
                    st.subheader("🎯 Análise da Banca")
                    
                    if banca != "Não identificada":
                        analise_banca = analyzer.analisar_banca_historico(banca)
                        
                        st.write(f"**Estilo:** {analise_banca['estilo']}")
                        st.write(f"**Dificuldade:** {analise_banca['dificuldade']}")
                        
                        st.write("**Características:**")
                        for carac in analise_banca['caracteristicas']:
                            st.write(f"• {carac}")
                        
                        st.write("**Áreas Fortes:**")
                        for area in analise_banca['areas_forte']:
                            st.write(f"• {area}")
                
                # Conteúdo Programático
                st.subheader("📚 Conteúdo Programático")
                
                conteudo = analyzer.extrair_conteudo_programatico(texto_edital)
                
                if conteudo:
                    # Calcula pesos
                    pesos = analyzer.calcular_pesos_materias(conteudo)
                    
                    # Gráfico de pesos
                    if pesos:
                        fig_pesos = px.pie(
                            values=list(pesos.values()),
                            names=list(pesos.keys()),
                            title="📊 Distribuição de Peso por Matéria"
                        )
                        st.plotly_chart(fig_pesos, use_container_width=True)
                    
                    # Detalhes por matéria
                    for materia, topicos in conteudo.items():
                        with st.expander(f"📖 {materia} ({pesos.get(materia, 0):.1f}%)"):
                            for topico in topicos[:10]:  # Limita a 10 tópicos
                                st.write(f"• {topico}")
                            
                            if len(topicos) > 10:
                                st.write(f"... e mais {len(topicos) - 10} tópicos")
                
                # Cronograma de Estudos
                st.subheader("📅 Cronograma de Estudos Sugerido")
                
                dias_estudo = st.slider("Dias para estudar:", 30, 180, 90)
                
                if conteudo and pesos:
                    cronograma = analyzer.gerar_cronograma_estudos(conteudo, pesos, dias_estudo)
                    
                    # Tabela do cronograma
                    df_cronograma = pd.DataFrame([
                        {
                            "Matéria": materia,
                            "Horas Total": info["horas_total"],
                            "Dias de Estudo": info["dias_estudo"],
                            "Horas/Dia": info["horas_por_dia"],
                            "Prioridade": info["prioridade"]
                        }
                        for materia, info in cronograma.items()
                    ])
                    
                    st.dataframe(df_cronograma, use_container_width=True)
                    
                    # Gráfico de horas por matéria
                    fig_horas = px.bar(
                        df_cronograma,
                        x="Matéria",
                        y="Horas Total",
                        color="Prioridade",
                        title="⏰ Distribuição de Horas de Estudo"
                    )
                    st.plotly_chart(fig_horas, use_container_width=True)
                
                # Dicas específicas da banca
                if banca != "Não identificada":
                    st.subheader("💡 Dicas Específicas da Banca")
                    
                    analise_banca = analyzer.analisar_banca_historico(banca)
                    
                    col_dicas1, col_dicas2 = st.columns(2)
                    
                    with col_dicas1:
                        st.write("**🎯 Dicas de Estudo:**")
                        for dica in analise_banca.get('dicas_estudo', []):
                            st.write(f"• {dica}")
                    
                    with col_dicas2:
                        st.write("**📝 Exemplos de Questões:**")
                        for exemplo in analise_banca.get('questoes_exemplo', []):
                            st.write(f"• {exemplo}")
            
            else:
                st.error("❌ Não foi possível extrair texto do PDF. Verifique se o arquivo não está protegido.")
    
    else:
        # Demonstração com edital exemplo
        st.info("💡 **Demonstração:** Faça upload de um edital em PDF para ver a análise completa!")
        
        if st.button("🔍 Ver Exemplo de Análise"):
            st.subheader("📋 Exemplo: Concurso Tribunal de Justiça")
            
            # Exemplo de informações básicas
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("🏢 Órgão", "Tribunal de Justiça")
                st.metric("🎯 Cargo", "Analista Judiciário")
            
            with col2:
                st.metric("👥 Vagas", "50")
                st.metric("💰 Salário", "R$ 8.500,00")
            
            with col3:
                st.metric("🏛️ Banca", "CESPE/CEBRASPE")
                st.metric("📅 Prova", "15/12/2024")
            
            # Exemplo de distribuição de matérias
            materias_exemplo = {
                "Português": 25,
                "Direito Constitucional": 20,
                "Direito Administrativo": 20,
                "Conhecimentos Específicos": 15,
                "Informática": 10,
                "Atualidades": 10
            }
            
            fig_exemplo = px.pie(
                values=list(materias_exemplo.values()),
                names=list(materias_exemplo.keys()),
                title="📊 Exemplo: Distribuição de Peso por Matéria"
            )
            st.plotly_chart(fig_exemplo, use_container_width=True)