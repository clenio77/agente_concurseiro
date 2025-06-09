import json
from typing import Dict, List
from datetime import datetime, timedelta
import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

class PerformanceAnalysisTool:
    def __init__(self):
        self.name = "PerformanceAnalysisTool"
        self.description = "Analisa o desempenho do estudante e faz previsões"
    
    def analyze_performance_trend(self, performance_history: List[Dict]) -> Dict:
        """Analisa tendência de desempenho ao longo do tempo"""
        if not performance_history or len(performance_history) < 2:
            return {
                "trend": "insufficient_data",
                "slope": 0,
                "prediction_next": None,
                "confidence": 0
            }
        
        # Extrair datas e pontuações
        dates = []
        scores = []
        
        for entry in performance_history:
            if "date" in entry and "overall_score" in entry:
                try:
                    date = datetime.strptime(entry["date"], "%Y-%m-%d")
                    dates.append(date)
                    scores.append(entry["overall_score"])
                except:
                    pass
        
        if len(dates) < 2:
            return {
                "trend": "insufficient_data",
                "slope": 0,
                "prediction_next": None,
                "confidence": 0
            }
        
        # Converter datas para números (dias desde a primeira data)
        first_date = min(dates)
        days = [(date - first_date).days for date in dates]
        
        # Preparar dados para regressão
        X = np.array(days).reshape(-1, 1)
        y = np.array(scores)
        
        # Ajustar modelo de regressão linear
        model = LinearRegression()
        model.fit(X, y)
        
        # Calcular coeficiente de determinação (R²)
        r_squared = model.score(X, y)
        
        # Calcular previsão para próxima avaliação (7 dias após a última)
        last_day = max(days)
        next_day = last_day + 7
        prediction_next = float(model.predict(np.array([[next_day]]))[0])
        
        # Determinar tendência
        slope = model.coef_[0]
        
        if slope > 1:
            trend = "strong_improvement"
        elif slope > 0.5:
            trend = "improvement"
        elif slope > 0.1:
            trend = "slight_improvement"
        elif slope > -0.1:
            trend = "stable"
        elif slope > -0.5:
            trend = "slight_decline"
        elif slope > -1:
            trend = "decline"
        else:
            trend = "strong_decline"
        
        return {
            "trend": trend,
            "slope": float(slope),
            "prediction_next": round(prediction_next, 1),
            "confidence": round(r_squared, 2),
            "days_analyzed": len(days)
        }
    
    def identify_weak_subjects(self, performance_history: List[Dict]) -> List[Dict]:
        """Identifica matérias com desempenho abaixo do esperado"""
        if not performance_history:
            return []
        
        # Extrair pontuações por matéria do histórico mais recente
        latest_entry = performance_history[-1]
        
        if "subject_scores" not in latest_entry:
            return []
        
        subject_scores = latest_entry["subject_scores"]
        
        # Calcular média geral
        overall_avg = sum(subject_scores.values()) / len(subject_scores)
        
        # Identificar matérias abaixo da média
        weak_subjects = []
        
        for subject, score in subject_scores.items():
            if score < overall_avg - 10:  # Mais de 10 pontos abaixo da média
                weak_subjects.append({
                    "subject": subject,
                    "score": score,
                    "gap": round(overall_avg - score, 1),
                    "severity": "high" if (overall_avg - score) > 20 else "medium"
                })
            elif score < overall_avg - 5:  # 5-10 pontos abaixo da média
                weak_subjects.append({
                    "subject": subject,
                    "score": score,
                    "gap": round(overall_avg - score, 1),
                    "severity": "low"
                })
        
        # Ordenar por severidade e gap
        weak_subjects.sort(key=lambda x: (0 if x["severity"] == "high" else 1 if x["severity"] == "medium" else 2, -x["gap"]))
        
        return weak_subjects
    
    def predict_future_performance(self, performance_history: List[Dict], 
                                 study