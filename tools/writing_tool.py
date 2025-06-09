import json
from typing import Dict, List

class WritingTool:
    def __init__(self):
        self.name = "WritingTool"
        self.description = "Avalia redações e fornece feedback detalhado"
    
    def evaluate_essay(self, essay_text: str, essay_type: str, criteria: List[str] = None) -> Dict:
        """Avalia uma redação com base em critérios específicos"""
        if not criteria:
            criteria = ["Estrutura", "Argumentação", "Gramática", "Coesão", "Adequação ao tema"]
        
        evaluation = {
            "score": 0,
            "feedback": {},
            "suggestions": [],
            "strengths": [],
            "weaknesses": []
        }
        
        # Avaliação por critério
        for criterion in criteria:
            # Simulação de avaliação - em produção usaria análise mais sofisticada
            if criterion == "Estrutura":
                score = self._evaluate_structure(essay_text)
                feedback = self._generate_structure_feedback(score, essay_text)
            elif criterion == "Argumentação":
                score = self._evaluate_argumentation(essay_text)
                feedback = self._generate_argumentation_feedback(score, essay_text)
            elif criterion == "Gramática":
                score = self._evaluate_grammar(essay_text)
                feedback = self._generate_grammar_feedback(score, essay_text)
            elif criterion == "Coesão":
                score = self._evaluate_cohesion(essay_text)
                feedback = self._generate_cohesion_feedback(score, essay_text)
            elif criterion == "Adequação ao tema":
                score = self._evaluate_theme_adherence(essay_text)
                feedback = self._generate_theme_feedback(score, essay_text)
            else:
                score = 7.0  # Valor padrão
                feedback = "Critério não implementado para avaliação detalhada."
            
            evaluation["feedback"][criterion] = {
                "score": score,
                "comments": feedback
            }
            evaluation["score"] += score
        
        # Calcular média
        evaluation["score"] = round(evaluation["score"] / len(criteria), 1)
        
        # Gerar sugestões, pontos fortes e fracos
        evaluation["suggestions"] = self._generate_suggestions(evaluation["feedback"])
        evaluation["strengths"] = self._identify_strengths(evaluation["feedback"])
        evaluation["weaknesses"] = self._identify_weaknesses(evaluation["feedback"])
        
        return evaluation
    
    def _evaluate_structure(self, text: str) -> float:
        """Avalia a estrutura da redação"""
        # Implementação simplificada
        paragraphs = text.split("\n\n")
        if len(paragraphs) >= 4:  # Introdução, 2+ desenvolvimento, conclusão
            return 8.5
        elif len(paragraphs) == 3:  # Estrutura básica
            return 7.0
        else:
            return 5.0
    
    def _evaluate_argumentation(self, text: str) -> float:
        """Avalia a qualidade da argumentação"""
        # Implementação simplificada
        argument_markers = ["porque", "portanto", "assim", "logo", "dessa forma", 
                           "visto que", "uma vez que", "considerando"]
        count = sum(1 for marker in argument_markers if marker in text.lower())
        if count >= 5:
            return 8.0
        elif count >= 3:
            return 7.0
        else:
            return 6.0
    
    def _evaluate_grammar(self, text: str) -> float:
        """Avalia aspectos gramaticais"""
        # Implementação simplificada
        return 7.5  # Valor padrão
    
    def _evaluate_cohesion(self, text: str) -> float:
        """Avalia coesão textual"""
        # Implementação simplificada
        cohesion_markers = ["entretanto", "contudo", "porém", "todavia", "no entanto",
                           "ademais", "além disso", "outrossim", "por fim", "finalmente"]
        count = sum(1 for marker in cohesion_markers if marker in text.lower())
        if count >= 6:
            return 9.0
        elif count >= 3:
            return 7.5
        else:
            return 6.0
    
    def _evaluate_theme_adherence(self, text: str) -> float:
        """Avalia aderência ao tema"""
        # Implementação simplificada
        return 8.0  # Valor padrão
    
    def _generate_structure_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre estrutura"""
        if score >= 8.0:
            return "Excelente estruturação com introdução clara, desenvolvimento bem organizado e conclusão coesa."
        elif score >= 7.0:
            return "Boa estrutura, mas pode melhorar a organização dos parágrafos e a transição entre ideias."
        else:
            return "Estrutura precisa ser aprimorada. Certifique-se de incluir introdução, desenvolvimento e conclusão bem definidos."
    
    def _generate_argumentation_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre argumentação"""
        if score >= 8.0:
            return "Argumentação sólida com uso eficaz de exemplos e evidências."
        elif score >= 7.0:
            return "Argumentos razoáveis, mas podem ser fortalecidos com mais exemplos concretos."
        else:
            return "Argumentação fraca. Desenvolva melhor suas ideias e utilize exemplos para sustentá-las."
    
    def _generate_grammar_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre gramática"""
        if score >= 8.0:
            return "Excelente domínio das regras gramaticais e ortográficas."
        elif score >= 7.0:
            return "Bom domínio gramatical com poucos erros que não comprometem a compreensão."
        else:
            return "Diversos erros gramaticais e ortográficos que prejudicam a qualidade do texto."
    
    def _generate_cohesion_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre coesão"""
        if score >= 8.0:
            return "Excelente uso de conectivos e elementos de coesão textual."
        elif score >= 7.0:
            return "Boa coesão, mas pode melhorar a transição entre parágrafos."
        else:
            return "Problemas de coesão textual. Utilize mais conectivos para ligar suas ideias."
    
    def _generate_theme_feedback(self, score: float, text: str) -> str:
        """Gera feedback sobre aderência ao tema"""
        if score >= 8.0:
            return "Excelente aderência ao tema proposto, com abordagem completa e relevante."
        elif score >= 7.0:
            return "Boa aderência ao tema, mas alguns aspectos importantes não foram abordados."
        else:
            return "Tangenciamento do tema. Procure abordar o tema de forma mais direta e completa."
    
    def _generate_suggestions(self, feedback: Dict) -> List[str]:
        """Gera sugestões de melhoria"""
        suggestions = []
        for criterion, data in feedback.items():
            if data["score"] < 7.0:
                if criterion == "Estrutura":
                    suggestions.append("Organize seu texto em pelo menos 4 parágrafos: introdução, 2 de desenvolvimento e conclusão.")
                elif criterion == "Argumentação":
                    suggestions.append("Utilize mais conectivos argumentativos e exemplos concretos para fortalecer suas ideias.")
                elif criterion == "Gramática":
                    suggestions.append("Revise cuidadosamente a ortografia e pontuação do texto.")
                elif criterion == "Coesão":
                    suggestions.append("Utilize mais elementos de transição entre parágrafos e ideias.")
                elif criterion == "Adequação ao tema":
                    suggestions.append("Mantenha o foco no tema proposto, evitando digressões.")
        return suggestions
    
    def _identify_strengths(self, feedback: Dict) -> List[str]:
        """Identifica pontos fortes"""
        strengths = []
        for criterion, data in feedback.items():
            if data["score"] >= 8.0:
                strengths.append(f"Excelente {criterion.lower()}")
        return strengths
    
    def _identify_weaknesses(self, feedback: Dict) -> List[str]:
        """Identifica pontos fracos"""
        weaknesses = []
        for criterion, data in feedback.items():
            if data["score"] < 7.0:
                weaknesses.append(f"Fraco desempenho em {criterion.lower()}")
        return weaknesses
    
    def _run(self, essay_text: str, essay_type: str = "Dissertativo-Argumentativo") -> str:
        """Interface principal da ferramenta"""
        try:
            # Definir critérios com base no tipo de redação
            if essay_type == "Dissertativo-Argumentativo":
                criteria = ["Estrutura", "Argumentação", "Gramática", "Coesão", "Adequação ao tema"]
            elif essay_type == "Peça Processual":
                criteria = ["Estrutura", "Fundamentação", "Gramática", "Técnica", "Adequação ao caso"]
            else:
                criteria = ["Estrutura", "Conteúdo", "Gramática", "Coesão", "Adequação"]
            
            # Avaliar redação
            evaluation = self.evaluate_essay(essay_text, essay_type, criteria)
            
            return json.dumps(evaluation, indent=2, ensure_ascii=False)
            
        except Exception as e:
            return json.dumps({
                'error': f'Erro ao avaliar redação: {str(e)}',
                'essay_type': essay_type
            }, indent=2, ensure_ascii=False)