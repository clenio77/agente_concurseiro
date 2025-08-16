"""
Sistema de Análise Preditiva de Desempenho
Fornece análise, predição e recomendações baseadas no histórico de estudos do usuário.
"""

import math
import random
from dataclasses import dataclass
from typing import Dict, List

import numpy as np


@dataclass
class PerformanceMetrics:
    """
    Métricas de desempenho do usuário.
    Inclui pontuação geral, por matéria, consistência, eficiência, áreas fortes e fracas.
    """
    overall_score: float
    subject_scores: Dict[str, float]
    consistency_score: float
    improvement_rate: float
    study_efficiency: float
    time_management: float
    weak_areas: List[str]
    strong_areas: List[str]

@dataclass
class Prediction:
    """
    Predição de desempenho do usuário na prova.
    Inclui score previsto, confiança, distribuição de probabilidades, recomendações e fatores de risco.
    """
    predicted_score: float
    confidence: float
    probability_ranges: Dict[str, float]  # ex: {"60-70": 0.2, "70-80": 0.5}
    recommendations: List[str]
    risk_factors: List[str]
    improvement_potential: float

class PerformancePredictor:
    """
    Sistema avançado de análise preditiva de desempenho.
    Realiza análise de métricas, predição de score, recomendações e identificação de riscos.
    """
    def __init__(self):
        self.name = "PerformancePredictor"
        self.description = "Sistema avançado de análise preditiva de desempenho"

        # Pesos para diferentes fatores
        self.weights = {
            'recent_performance': 0.35,
            'consistency': 0.20,
            'improvement_trend': 0.25,
            'study_time': 0.10,
            'subject_balance': 0.10
        }

        # Benchmarks por banca
        self.banca_benchmarks = {
            'CESPE': {
                'passing_score': 60,
                'competitive_score': 75,
                'excellent_score': 85,
                'time_pressure_factor': 1.2,
                'difficulty_factor': 1.1
            },
            'FCC': {
                'passing_score': 60,
                'competitive_score': 70,
                'excellent_score': 80,
                'time_pressure_factor': 1.0,
                'difficulty_factor': 1.0
            },
            'VUNESP': {
                'passing_score': 60,
                'competitive_score': 72,
                'excellent_score': 82,
                'time_pressure_factor': 1.1,
                'difficulty_factor': 1.05
            },
            'FGV': {
                'passing_score': 60,
                'competitive_score': 75,
                'excellent_score': 85,
                'time_pressure_factor': 1.15,
                'difficulty_factor': 1.2
            },
            'IBFC': {
                'passing_score': 60,
                'competitive_score': 70,
                'excellent_score': 80,
                'time_pressure_factor': 1.0,
                'difficulty_factor': 0.95
            }
        }

    def analyze_performance(self, user_data: Dict) -> PerformanceMetrics:
        """
        Analisa o desempenho atual do usuário com base no histórico de simulados, 
        matérias e horas de estudo.
        :param user_data: Dicionário com dados do usuário.
        :return: Instância de PerformanceMetrics.
        """

        # Extrair dados históricos
        mock_scores = user_data.get('mock_exam_scores', [])
        subject_progress = user_data.get('subject_progress', {})
        study_hours = user_data.get('total_study_hours', 0)

        # Calcular pontuação geral
        if mock_scores:
            recent_scores = [exam['score'] for exam in mock_scores[-5:]]  # Últimos 5 simulados
            overall_score = np.mean(recent_scores)
        else:
            overall_score = 0

        # Calcular pontuações por matéria
        subject_scores = {}
        for subject, data in subject_progress.items():
            subject_scores[subject] = data.get('last_score', 0)

        # Calcular consistência (desvio padrão das pontuações)
        if len(mock_scores) >= 3:
            scores = [exam['score'] for exam in mock_scores]
            consistency_score = max(
                0, 100 - (np.std(scores) * 2)
            )  # Inverter: menor desvio = maior consistência
        else:
            consistency_score = 50  # Valor neutro para poucos dados

        # Calcular taxa de melhoria
        improvement_rate = self._calculate_improvement_rate(mock_scores)

        # Calcular eficiência de estudo (pontuação por hora)
        study_efficiency = overall_score / max(study_hours, 1) if study_hours > 0 else 0

        # Calcular gestão de tempo (baseado em simulados completos)
        time_management = self._calculate_time_management(user_data)

        # Identificar áreas fracas e fortes
        weak_areas = [subject for subject, score in subject_scores.items() if score < 60]
        strong_areas = [
            subject for subject, score in subject_scores.items() if score >= 80
        ]

        return PerformanceMetrics(
            overall_score=overall_score,
            subject_scores=subject_scores,
            consistency_score=consistency_score,
            improvement_rate=improvement_rate,
            study_efficiency=study_efficiency,
            time_management=time_management,
            weak_areas=weak_areas,
            strong_areas=strong_areas
        )

    def predict_exam_performance(
        self, user_data: Dict, target_banca: str = 'CESPE', days_until_exam: int = 90
    ) -> Prediction:
        """
        Prediz o desempenho do usuário na prova final, considerando banca, 
        tempo até a prova e histórico.
        :param user_data: Dicionário com dados do usuário.
        :param target_banca: Nome da banca (ex: 'CESPE').
        :param days_until_exam: Dias até a prova.
        :return: Instância de Prediction.
        """

        # Analisar desempenho atual
        metrics = self.analyze_performance(user_data)

        # Obter benchmark da banca
        benchmark = self.banca_benchmarks.get(
            target_banca, self.banca_benchmarks['CESPE']
        )

        # Calcular predição base
        base_prediction = self._calculate_base_prediction(metrics, user_data)

        # Aplicar fatores de ajuste
        adjusted_prediction = self._apply_adjustment_factors(
            base_prediction, metrics, benchmark, days_until_exam
        )

        # Calcular confiança da predição
        confidence = self._calculate_confidence(metrics, user_data)

        # Calcular distribuição de probabilidades
        probability_ranges = self._calculate_probability_distribution(
            adjusted_prediction, confidence
        )

        # Gerar recomendações
        recommendations = self._generate_recommendations(
            metrics, adjusted_prediction, benchmark
        )

        # Identificar fatores de risco
        risk_factors = self._identify_risk_factors(metrics, days_until_exam)

        # Calcular potencial de melhoria
        improvement_potential = self._calculate_improvement_potential(
            metrics, days_until_exam
        )

        return Prediction(
            predicted_score=adjusted_prediction,
            confidence=confidence,
            probability_ranges=probability_ranges,
            recommendations=recommendations,
            risk_factors=risk_factors,
            improvement_potential=improvement_potential
        )

    def _calculate_improvement_rate(self, mock_scores: List[Dict]) -> float:
        """Calcula taxa de melhoria baseada nos simulados"""
        if len(mock_scores) < 2:
            return 0

        scores = [exam['score'] for exam in mock_scores]

        # Regressão linear simples para calcular tendência
        x = np.arange(len(scores))
        y = np.array(scores)

        if len(x) > 1:
            slope = np.polyfit(x, y, 1)[0]
            return slope * 10  # Normalizar para escala mais interpretável

        return 0

    def _calculate_time_management(self, user_data: Dict) -> float:
        """Calcula score de gestão de tempo"""
        # Simulação baseada em dados disponíveis
        simulados_completed = user_data.get('simulados_completed', 0)
        study_hours = user_data.get('total_study_hours', 0)

        if simulados_completed == 0:
            return 50  # Valor neutro

        # Assumir que boa gestão de tempo = mais simulados por hora de estudo
        efficiency = simulados_completed / max(study_hours, 1)

        # Normalizar para 0-100
        return min(100, efficiency * 1000)

    def _calculate_base_prediction(
        self, metrics: PerformanceMetrics, user_data: Dict
    ) -> float:
        """Calcula predição base usando pesos"""

        factors = {
            'recent_performance': metrics.overall_score,
            'consistency': metrics.consistency_score,
            'improvement_trend': 50 + metrics.improvement_rate,  # Centralizar em 50
            'study_time': min(
                100, user_data.get('total_study_hours', 0) * 2
            ),  # Normalizar
            'subject_balance': self._calculate_subject_balance(metrics.subject_scores)
        }

        # Calcular média ponderada
        weighted_sum = sum(factors[factor] * self.weights[factor] for factor in factors)

        return max(0, min(100, weighted_sum))

    def _calculate_subject_balance(self, subject_scores: Dict[str, float]) -> float:
        """Calcula equilíbrio entre matérias"""
        if not subject_scores:
            return 50

        scores = list(subject_scores.values())
        np.mean(scores)
        std_score = np.std(scores)

        # Menor desvio padrão = melhor equilíbrio
        balance_score = max(0, 100 - (std_score * 2))

        return balance_score

    def _apply_adjustment_factors(
        self, base_prediction: float, metrics: PerformanceMetrics,
        benchmark: Dict, days_until_exam: int
    ) -> float:
        """Aplica fatores de ajuste à predição base"""

        adjusted = base_prediction

        # Fator de tempo restante
        if days_until_exam < 30:
            adjusted *= 0.95  # Menos tempo para melhorar
        elif days_until_exam > 180:
            adjusted *= 1.05  # Mais tempo para melhorar

        # Fator de dificuldade da banca
        adjusted *= (2 - benchmark['difficulty_factor'])

        # Fator de pressão de tempo
        adjusted *= (2 - benchmark['time_pressure_factor'])

        # Fator de melhoria contínua
        if metrics.improvement_rate > 5:
            adjusted *= 1.1
        elif metrics.improvement_rate < -5:
            adjusted *= 0.9

        return max(0, min(100, adjusted))

    def _calculate_confidence(
        self, metrics: PerformanceMetrics, user_data: Dict
    ) -> float:
        """Calcula confiança da predição"""

        confidence_factors = []

        # Quantidade de dados
        mock_count = len(user_data.get('mock_exam_scores', []))
        data_confidence = min(100, mock_count * 20)  # Máximo com 5 simulados
        confidence_factors.append(data_confidence)

        # Consistência
        confidence_factors.append(metrics.consistency_score)

        # Tempo de estudo
        study_hours = user_data.get('total_study_hours', 0)
        study_confidence = min(100, study_hours * 2)
        confidence_factors.append(study_confidence)

        # Equilíbrio entre matérias
        balance_confidence = self._calculate_subject_balance(metrics.subject_scores)
        confidence_factors.append(balance_confidence)

        return np.mean(confidence_factors)

    def _calculate_probability_distribution(
        self, prediction: float, confidence: float
    ) -> Dict[str, float]:
        """Calcula distribuição de probabilidades por faixas"""

        # Desvio padrão baseado na confiança
        std_dev = (100 - confidence) / 4

        ranges = {
            "0-40": (0, 40),
            "40-60": (40, 60),
            "60-70": (60, 70),
            "70-80": (70, 80),
            "80-90": (80, 90),
            "90-100": (90, 100)
        }

        probabilities = {}

        for range_name, (low, high) in ranges.items():
            # Calcular probabilidade usando distribuição normal
            prob_low = self._normal_cdf(low, prediction, std_dev)
            prob_high = self._normal_cdf(high, prediction, std_dev)
            probabilities[range_name] = max(0, prob_high - prob_low)

        # Normalizar para somar 1
        total = sum(probabilities.values())
        if total > 0:
            probabilities = {k: v/total for k, v in probabilities.items()}

        return probabilities

    def _normal_cdf(self, x: float, mean: float, std: float) -> float:
        """Função de distribuição cumulativa normal"""
        return 0.5 * (1 + math.erf((x - mean) / (std * math.sqrt(2))))

    def _generate_recommendations(
        self, metrics: PerformanceMetrics, prediction: float, benchmark: Dict
    ) -> List[str]:
        """Gera recomendações personalizadas"""
        recommendations = []

        # Recomendações baseadas na predição
        if prediction < benchmark['passing_score']:
            recommendations.append(
                "🚨 Foque em aumentar o tempo de estudo e revisar conceitos básicos"
            )
            recommendations.append("📚 Priorize as matérias com menor pontuação")
        elif prediction < benchmark['competitive_score']:
            recommendations.append("📈 Você está no caminho certo! Foque em consistência")
            recommendations.append("🎯 Pratique mais simulados para ganhar confiança")
        else:
            recommendations.append("🌟 Excelente! Mantenha o ritmo e foque nos detalhes")
            recommendations.append("🔍 Revise questões que errou para evitar pegadinhas")

        # Recomendações baseadas em áreas fracas
        if metrics.weak_areas:
            recommendations.append(
                f"⚠️ Dedique mais tempo às matérias fracas: {', '.join(metrics.weak_areas)}"
            )

        # Recomendações baseadas na consistência
        if metrics.consistency_score < 70:
            recommendations.append(
                "🎯 Trabalhe na consistência fazendo simulados regulares"
            )

        # Recomendações baseadas na melhoria
        if metrics.improvement_rate < 0:
            recommendations.append(
                "📉 Revise sua estratégia de estudos - considere mudar a abordagem"
            )

        return recommendations

    def _identify_risk_factors(
        self, metrics: PerformanceMetrics, days_until_exam: int
    ) -> List[str]:
        """Identifica fatores de risco"""
        risks = []

        if days_until_exam < 30:
            risks.append("⏰ Pouco tempo restante para melhorias significativas")

        if metrics.consistency_score < 60:
            risks.append("📊 Baixa consistência pode afetar desempenho na prova")

        if metrics.improvement_rate < -3:
            risks.append("📉 Tendência de queda no desempenho")

        if len(metrics.weak_areas) > 2:
            risks.append("📚 Muitas matérias com baixo desempenho")

        if metrics.overall_score < 50:
            risks.append("🎯 Pontuação geral abaixo da média")

        return risks

    def _calculate_improvement_potential(
        self, metrics: PerformanceMetrics, days_until_exam: int
    ) -> float:
        """Calcula potencial de melhoria"""

        # Fatores que influenciam o potencial
        factors = []

        # Tempo disponível
        time_factor = min(100, days_until_exam / 2)  # Máximo com 200 dias
        factors.append(time_factor)

        # Taxa de melhoria atual
        improvement_factor = max(0, 50 + metrics.improvement_rate * 5)
        factors.append(improvement_factor)

        # Margem para melhoria (quanto mais baixo, mais potencial)
        margin_factor = 100 - metrics.overall_score
        factors.append(margin_factor)

        # Consistência (mais consistente = mais previsível melhoria)
        factors.append(metrics.consistency_score)

        return np.mean(factors)

    def generate_study_recommendations(
        self, prediction: Prediction, user_data: Dict
    ) -> Dict:
        """Gera recomendações específicas de estudo"""

        recommendations = {
            "priority_subjects": [],
            "study_schedule": {},
            "focus_areas": [],
            "techniques": []
        }

        # Analisar desempenho por matéria
        subject_progress = user_data.get('subject_progress', {})

        # Priorizar matérias com baixo desempenho
        low_performance = [
            (subj, data['last_score'])
            for subj, data in subject_progress.items()
            if data.get('last_score', 0) < 60
        ]
        low_performance.sort(key=lambda x: x[1])  # Ordenar por pontuação

        recommendations["priority_subjects"] = [subj for subj, _ in low_performance[:3]]

        # Sugerir cronograma baseado na predição
        if prediction.predicted_score < 60:
            recommendations["study_schedule"] = {
                "daily_hours": 6,
                "weekly_simulados": 3,
                "review_frequency": "daily"
            }
        elif prediction.predicted_score < 75:
            recommendations["study_schedule"] = {
                "daily_hours": 4,
                "weekly_simulados": 2,
                "review_frequency": "every_2_days"
            }
        else:
            recommendations["study_schedule"] = {
                "daily_hours": 3,
                "weekly_simulados": 2,
                "review_frequency": "weekly"
            }

        # Áreas de foco baseadas nos riscos
        if "consistência" in str(prediction.risk_factors):
            recommendations["focus_areas"].append(
                "Simulados regulares para melhorar consistência"
            )

        if "tempo" in str(prediction.risk_factors):
            recommendations["focus_areas"].append("Técnicas de gestão de tempo")

        # Técnicas recomendadas
        if prediction.predicted_score < 70:
            recommendations["techniques"] = [
                "Revisão ativa com flashcards",
                "Mapas mentais para memorização",
                "Simulados cronometrados",
                "Análise detalhada de erros"
            ]
        else:
            recommendations["techniques"] = [
                "Questões de alta dificuldade",
                "Revisão de pegadinhas",
                "Simulados de bancas específicas",
                "Técnicas de eliminação"
            ]

        return recommendations
