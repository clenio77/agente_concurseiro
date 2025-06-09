import json
import re
from typing import Dict, List
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

class ExamAnalysisTool:
    def __init__(self):
        self.name = "ExamAnalysisTool"
        self.description = "Analisa provas anteriores para identificar padrões e tendências"
        
        # Inicializar NLTK
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
    
    def analyze_exam(self, exam_text: str, banca: str) -> Dict:
        """Analisa uma prova para extrair padrões e estatísticas"""
        result = {
            "question_count": 0,
            "subject_distribution": {},
            "difficulty_distribution": {},
            "question_types": {},
            "common_topics": [],
            "linguistic_patterns": {},
            "banca_patterns": {}
        }
        
        # Extrair questões
        questions = self._extract_questions(exam_text)
        result["question_count"] = len(questions)
        
        # Analisar cada questão
        for question in questions:
            # Classificar por assunto
            subject = self._classify_subject(question)
            result["subject_distribution"][subject] = result["subject_distribution"].get(subject, 0) + 1
            
            # Estimar dificuldade
            difficulty = self._estimate_difficulty(question)
            result["difficulty_distribution"][difficulty] = result["difficulty_distribution"].get(difficulty, 0) + 1
            
            # Classificar tipo de questão
            q_type = self._classify_question_type(question)
            result["question_types"][q_type] = result["question_types"].get(q_type, 0) + 1
        
        # Extrair tópicos comuns
        result["common_topics"] = self._extract_common_topics(exam_text)
        
        # Analisar padrões linguísticos
        result["linguistic_patterns"] = self._analyze_linguistic_patterns(exam_text)
        
        # Identificar padrões específicos da banca
        result["banca_patterns"] = self._identify_banca_patterns(exam_text, banca)
        
        return result
    
    def _extract_questions(self, text: str) -> List[str]:
        """Extrai questões individuais do texto da prova"""
        # Implementação simplificada - em produção usaria regex mais robustos
        questions = []
        
        # Tentar diferentes padrões de numeração de questões
        patterns = [
            r'(?:Questão|QUESTÃO|Questao)\s+(\d+)[.\):-]\s*(.*?)(?=(?:Questão|QUESTÃO|Questao)\s+\d+[.\):-]|$)',
            r'(?:^\d+[.\):-]|\n\d+[.\):-])\s*(.*?)(?=^\d+[.\):-]|\n\d+[.\):-]|$)',
            r'(?:^|\n)(?:[A-Z]|\d+)[.\):-]\s*(.*?)(?=(?:^|\n)(?:[A-Z]|\d+)[.\):-]|$)'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.DOTALL | re.MULTILINE)
            if matches:
                for match in matches:
                    if isinstance(match, tuple):
                        # Se o padrão capturou grupos, pegue o texto da questão
                        question_text = match[-1].strip()
                    else:
                        question_text = match.strip()
                    
                    if len(question_text) > 20:  # Filtrar fragmentos muito curtos
                        questions.append(question_text)
                break
        
        # Fallback se nenhum padrão funcionar
        if not questions:
            # Dividir por parágrafos e tentar identificar questões
            paragraphs = text.split('\n\n')
            for para in paragraphs:
                if len(para.strip()) > 100 and ('?' in para or re.search(r'\([A-E]\)', para)):
                    questions.append(para.strip())
        
        return questions
    
    def _classify_subject(self, question: str) -> str:
        """Classifica a questão por assunto"""
        # Dicionário de palavras-chave por assunto
        subject_keywords = {
            "Português": ["gramática", "interpretação", "texto", "verbo", "substantivo", "adjetivo", "sintaxe"],
            "Matemática": ["equação", "função", "geometria", "trigonometria", "álgebra", "logaritmo"],
            "Direito": ["constituição", "lei", "código", "jurídico", "processo", "penal", "civil"],
            "Informática": ["computador", "software", "hardware", "internet", "rede", "programação"],
            "Conhecimentos Específicos": ["específico", "técnico", "profissional", "especializado"]
        }
        
        # Contar ocorrências de palavras-chave
        question_lower = question.lower()
        subject_scores = {}
        
        for subject, keywords in subject_keywords.items():
            score = sum(1 for keyword in keywords if keyword in question_lower)
            subject_scores[subject] = score
        
        # Retornar o assunto com maior pontuação
        if max(subject_scores.values(), default=0) > 0:
            return max(subject_scores.items(), key=lambda x: x[1])[0]
        else:
            return "Outros"
    
    def _estimate_difficulty(self, question: str) -> str:
        """Estima a dificuldade da questão"""
        # Indicadores de dificuldade
        difficulty_indicators = {
            "Fácil": ["básico", "simples", "direto", "identifique", "assinale"],
            "Média": ["analise", "compare", "explique", "relacione"],
            "Difícil": ["complexo", "avançado", "elabore", "critique", "avalie", "desenvolva"]
        }
        
        # Outros fatores de dificuldade
        question_lower = question.lower()
        word_count = len(word_tokenize(question_lower))
        sentence_count = len(re.split(r'[.!?]+', question_lower))
        avg_sentence_length = word_count / sentence_count if sentence_count > 0 else 0
        
        # Pontuação de dificuldade
        difficulty_score = 0
        
        # Comprimento da questão
        if word_count > 150:
            difficulty_score += 2
        elif word_count > 80:
            difficulty_score += 1
        
        # Comprimento médio das frases
        if avg_sentence_length > 25:
            difficulty_score += 2
        elif avg_sentence_length > 15:
            difficulty_score += 1
        
        # Presença de indicadores de dificuldade
        for level, indicators in difficulty_indicators.items():
            for indicator in indicators:
                if indicator in question_lower:
                    if level == "Fácil":
                        difficulty_score -= 1
                    elif level == "Média":
                        difficulty_score += 0
                    elif level == "Difícil":
                        difficulty_score += 1
        
        # Classificar com base na pontuação
        if difficulty_score >= 3:
            return "Difícil"
        elif difficulty_score >= 1:
            return "Média"
        else:
            return "Fácil"
    
    def _classify_question_type(self, question: str) -> str:
        """Classifica o tipo de questão"""
        question_lower = question.lower()
        
        if "verdadeiro ou falso" in question_lower or "certo ou errado" in question_lower:
            return "Verdadeiro/Falso"
        elif re.search(r'\([A-E]\)', question) or re.search(r'[a-e]\)', question):
            return "Múltipla Escolha"
        elif "assinale" in question_lower and ("alternativa" in question_lower or "opção" in question_lower):
            return "Múltipla Escolha"
        elif "complete" in question_lower or "preencha" in question_lower:
            return "Preenchimento"
        elif "discorra" in question_lower or "disserte" in question_lower or "redija" in question_lower:
            return "Dissertativa"
        else:
            return "Outros"
    
    def _extract_common_topics(self, text: str) -> List[str]:
        """Extrai tópicos comuns do texto da prova"""
        # Tokenizar e remover stopwords
        tokens = word_tokenize(text.lower())
        stop_words = set(stopwords.words('portuguese'))
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        
        # Contar frequência de palavras
        word_freq = Counter(filtered_tokens)
        
        # Extrair tópicos mais comuns (palavras mais frequentes)
        common_words = [word for word, count in word_freq.most_common(20) if len(word) > 3]
        
        return common_words
    
    def _analyze_linguistic_patterns(self, text: str) -> Dict:
        """Analisa padrões linguísticos no texto"""
        patterns = {
            "negativas": len(re.findall(r'\bnão\b|\bnem\b|\bnunca\b|\bjamais\b', text.lower())),
            "condicionais": len(re.findall(r'\bse\b|\bcaso\b|\bquando\b', text.lower())),
            "comparativos": len(re.findall(r'\bmais\b|\bmenos\b|\bmaior\b|\bmenor\b|\bmelhor\b|\bpior\b', text.lower())),
            "exceto": len(re.findall(r'\bexceto\b|\bsalvo\b|\ba não ser\b|\bcom exceção\b', text.lower()))
        }
        
        return patterns
    
    def _identify_banca_patterns(self, text: str, banca: str) -> Dict:
        """Identifica padrões específicos da banca"""
        patterns = {}
        
        banca_lower = banca.lower()
        if "cespe" in banca_lower or "cebraspe" in banca_lower:
            patterns["certo_errado"] = len(re.findall(r'\bcerto\b|\berrado\b', text.lower()))
            patterns["exceto"] = len(re.findall(r'\bexceto\b|\bsalvo\b', text.lower()))
            patterns["julgue"] = len(re.findall(r'\bjulgue\b', text.lower()))
        elif "fcc" in banca_lower:
            patterns["alternativa_correta"] = len(re.findall(r'\balternativa correta\b', text.lower()))
            patterns["considere"] = len(re.findall(r'\bconsidere\b', text.lower()))
        elif "vunesp" in banca_lower:
            patterns["assinale"] = len(re.findall(r'\bassinale\b', text.lower()))
            patterns["correto_afirmar"] = len(re.findall(r'\bcorreto afirmar\b', text.lower()))
        
        return patterns
    
    def generate_study_recommendations(self, analysis: Dict) -> List[Dict]:
        """Gera recomendações de estudo com base na análise"""
        recommendations = []
        
        # Recomendações baseadas na distribuição de assuntos
        if "subject_distribution" in analysis:
            for subject, count in sorted(analysis["subject_distribution"].items(), key=lambda x: x[1], reverse=True):
                percentage = (count / analysis["question_count"]) * 100 if analysis["question_count"] > 0 else 0
                if percentage >= 20:
                    priority = "Alta"
                elif percentage >= 10:
                    priority = "Média"
                else:
                    priority = "Baixa"
                
                recommendations.append({
                    "subject": subject,
                    "percentage": round(percentage, 1),
                    "priority": priority,
                    "recommendation": f"Dedique {priority.lower()} prioridade ao estudo de {subject}."
                })
        
        # Recomendações baseadas nos tipos de questões
        if "question_types" in analysis:
            most_common_type = max(analysis["question_types"].items(), key=lambda x: x[1])[0]
            recommendations.append({
                "focus_area": "Tipo de Questão",
                "recommendation": f"Pratique principalmente questões do tipo {most_common_type}."
            })
        
        # Recomendações baseadas nos padrões da banca
        if "banca_patterns" in analysis and analysis["banca_patterns"]:
            pattern_keys = list(analysis["banca_patterns"].keys())
            if pattern_keys:
                most_common_pattern = max(analysis["banca_patterns"].items(), key=lambda x: x[1])[0]
                recommendations.append({
                    "focus_area": "Padrão da Banca",
                    "recommendation": f"Atenção especial ao padrão '{most_common_pattern.replace('_', ' ')}' frequentemente usado pela banca."
                })
        
        return recommendations
    
    def _run(self, exam_text: str, banca: str) -> str:
        """Interface principal da ferramenta"""
        try:
            # Analisar a prova
            analysis = self.analyze_exam(exam_text, banca)
            
            # Gerar recomendações
            recommendations = self.generate_study_recommendations(analysis)
            
            # Combinar resultados
            result = {
                "analysis": analysis,
                "recommendations": recommendations,
                "summary": f"Análise de prova com {analysis['question_count']} questões da banca {banca}."
            }
            
            return json.dumps(result, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'error': f'Erro na análise da prova: {str(e)}'
            }, indent=2, ensure_ascii=False)