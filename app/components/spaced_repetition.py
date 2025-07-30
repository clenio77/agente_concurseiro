"""
Sistema de Revisão Espaçada Inteligente - Fase 2
Baseado na curva de esquecimento de Ebbinghaus e algoritmo de Leitner
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import random
import math
from typing import Dict, List, Tuple, Any
from enum import Enum

class DifficultyLevel(Enum):
    """Níveis de dificuldade para questões"""
    MUITO_FACIL = 1
    FACIL = 2
    MEDIO = 3
    DIFICIL = 4
    MUITO_DIFICIL = 5

class ReviewStatus(Enum):
    """Status de revisão"""
    NOVO = "novo"
    APRENDENDO = "aprendendo"
    REVISAO = "revisao"
    DOMINADO = "dominado"

class SpacedRepetitionSystem:
    """Sistema de Revisão Espaçada Inteligente"""
    
    def __init__(self):
        self.initialize_session_state()
        self.base_intervals = {
            DifficultyLevel.MUITO_FACIL: [1, 3, 7, 14, 30, 90],
            DifficultyLevel.FACIL: [1, 4, 9, 21, 45, 120],
            DifficultyLevel.MEDIO: [1, 5, 12, 28, 60, 150],
            DifficultyLevel.DIFICIL: [1, 6, 15, 35, 75, 180],
            DifficultyLevel.MUITO_DIFICIL: [1, 7, 18, 42, 90, 210]
        }
    
    def initialize_session_state(self):
        """Inicializa estado da sessão"""
        if 'spaced_repetition_items' not in st.session_state:
            st.session_state.spaced_repetition_items = self.generate_sample_items()
        
        if 'review_schedule' not in st.session_state:
            st.session_state.review_schedule = self.generate_review_schedule()
        
        if 'study_statistics' not in st.session_state:
            st.session_state.study_statistics = self.initialize_statistics()
        
        if 'current_review_session' not in st.session_state:
            st.session_state.current_review_session = []
    
    def generate_sample_items(self) -> List[Dict[str, Any]]:
        """Gera itens de exemplo para revisão"""
        materias = [
            'Português', 'Matemática', 'Direito Constitucional', 
            'Direito Administrativo', 'Informática', 'Atualidades',
            'Raciocínio Lógico', 'Legislação Específica'
        ]
        
        topics_by_subject = {
            'Português': ['Concordância Verbal', 'Regência', 'Crase', 'Interpretação de Texto', 'Ortografia'],
            'Matemática': ['Porcentagem', 'Juros', 'Geometria', 'Álgebra', 'Estatística'],
            'Direito Constitucional': ['Princípios', 'Direitos Fundamentais', 'Organização do Estado', 'Poder Executivo'],
            'Direito Administrativo': ['Atos Administrativos', 'Licitações', 'Contratos', 'Servidores Públicos'],
            'Informática': ['Windows', 'Excel', 'Word', 'Internet', 'Segurança'],
            'Atualidades': ['Política', 'Economia', 'Meio Ambiente', 'Tecnologia', 'Saúde'],
            'Raciocínio Lógico': ['Sequências', 'Proposições', 'Diagramas', 'Probabilidade'],
            'Legislação Específica': ['Lei 8112/90', 'Constituição', 'Código Civil', 'Lei de Responsabilidade Fiscal']
        }
        
        items = []
        item_id = 1
        
        for materia in materias:
            topics = topics_by_subject.get(materia, ['Tópico Geral'])
            
            for topic in topics:
                # Simular diferentes estágios de aprendizado
                status_weights = [0.3, 0.4, 0.2, 0.1]  # novo, aprendendo, revisao, dominado
                status = np.random.choice(list(ReviewStatus), p=status_weights)
                
                # Dificuldade baseada na matéria
                difficulty_weights = {
                    'Português': [0.1, 0.3, 0.4, 0.15, 0.05],
                    'Matemática': [0.05, 0.2, 0.3, 0.3, 0.15],
                    'Direito Constitucional': [0.1, 0.25, 0.35, 0.25, 0.05],
                    'Direito Administrativo': [0.1, 0.25, 0.35, 0.25, 0.05],
                    'Informática': [0.2, 0.4, 0.3, 0.1, 0.0],
                    'Atualidades': [0.15, 0.35, 0.35, 0.15, 0.0],
                    'Raciocínio Lógico': [0.05, 0.15, 0.3, 0.35, 0.15],
                    'Legislação Específica': [0.1, 0.2, 0.4, 0.25, 0.05]
                }
                
                weights = difficulty_weights.get(materia, [0.2, 0.2, 0.2, 0.2, 0.2])
                difficulty = np.random.choice(list(DifficultyLevel), p=weights)
                
                # Calcular próxima revisão baseada no status
                if status == ReviewStatus.NOVO:
                    next_review = datetime.now()
                elif status == ReviewStatus.APRENDENDO:
                    next_review = datetime.now() + timedelta(days=random.randint(0, 2))
                elif status == ReviewStatus.REVISAO:
                    next_review = datetime.now() + timedelta(days=random.randint(1, 7))
                else:  # DOMINADO
                    next_review = datetime.now() + timedelta(days=random.randint(7, 30))
                
                # Histórico de performance
                attempts = random.randint(1, 10)
                correct_attempts = random.randint(int(attempts * 0.3), attempts)
                
                items.append({
                    'id': item_id,
                    'materia': materia,
                    'topic': topic,
                    'difficulty': difficulty,
                    'status': status,
                    'next_review': next_review,
                    'interval_days': random.randint(1, 30),
                    'ease_factor': round(random.uniform(1.3, 2.5), 2),
                    'attempts': attempts,
                    'correct_attempts': correct_attempts,
                    'success_rate': round(correct_attempts / attempts, 2),
                    'last_reviewed': datetime.now() - timedelta(days=random.randint(0, 30)),
                    'created_at': datetime.now() - timedelta(days=random.randint(1, 90)),
                    'priority_score': random.randint(1, 100)
                })
                
                item_id += 1
        
        return items
    
    def generate_review_schedule(self) -> Dict[str, List[Dict[str, Any]]]:
        """Gera cronograma de revisões"""
        schedule = {}
        
        # Próximos 30 dias
        for i in range(30):
            date = datetime.now() + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            # Filtrar itens para revisão nesta data
            items_for_review = [
                item for item in st.session_state.spaced_repetition_items
                if item['next_review'].date() == date.date()
            ]
            
            # Adicionar novos itens baseado na carga de trabalho
            daily_load = len(items_for_review)
            target_load = random.randint(5, 15)  # 5-15 itens por dia
            
            if daily_load < target_load:
                # Adicionar itens novos ou que precisam de revisão
                available_items = [
                    item for item in st.session_state.spaced_repetition_items
                    if item['status'] == ReviewStatus.NOVO or 
                    (item['next_review'].date() <= date.date() and item not in items_for_review)
                ]
                
                additional_items = random.sample(
                    available_items, 
                    min(target_load - daily_load, len(available_items))
                )
                items_for_review.extend(additional_items)
            
            schedule[date_str] = items_for_review
        
        return schedule
    
    def initialize_statistics(self) -> Dict[str, Any]:
        """Inicializa estatísticas do sistema"""
        return {
            'total_items': len(st.session_state.spaced_repetition_items),
            'items_by_status': self.count_items_by_status(),
            'items_by_difficulty': self.count_items_by_difficulty(),
            'daily_review_count': random.randint(10, 25),
            'average_success_rate': 0.75,
            'streak_days': random.randint(1, 30),
            'total_reviews_completed': random.randint(100, 500),
            'time_saved_minutes': random.randint(60, 300)
        }
    
    def count_items_by_status(self) -> Dict[str, int]:
        """Conta itens por status"""
        counts = {status.value: 0 for status in ReviewStatus}
        
        for item in st.session_state.spaced_repetition_items:
            counts[item['status'].value] += 1
        
        return counts
    
    def count_items_by_difficulty(self) -> Dict[str, int]:
        """Conta itens por dificuldade"""
        counts = {f"Nível {diff.value}": 0 for diff in DifficultyLevel}
        
        for item in st.session_state.spaced_repetition_items:
            counts[f"Nível {item['difficulty'].value}"] += 1
        
        return counts
    
    def calculate_next_review_date(self, item: Dict[str, Any], performance: float) -> datetime:
        """Calcula próxima data de revisão baseada na performance"""
        current_interval = item['interval_days']
        ease_factor = item['ease_factor']
        difficulty = item['difficulty']
        
        # Ajustar ease factor baseado na performance
        if performance >= 0.8:  # Muito bom
            ease_factor = min(2.5, ease_factor + 0.1)
            multiplier = 1.3
        elif performance >= 0.6:  # Bom
            ease_factor = max(1.3, ease_factor)
            multiplier = 1.0
        elif performance >= 0.4:  # Regular
            ease_factor = max(1.3, ease_factor - 0.1)
            multiplier = 0.8
        else:  # Ruim
            ease_factor = max(1.3, ease_factor - 0.2)
            multiplier = 0.6
        
        # Calcular novo intervalo
        base_intervals = self.base_intervals[difficulty]
        current_stage = min(len(base_intervals) - 1, 
                          max(0, int(current_interval / 7)))  # Estágio baseado em semanas
        
        if performance < 0.4:
            # Voltar ao início se performance muito ruim
            new_interval = base_intervals[0]
        else:
            # Avançar no cronograma
            next_stage = min(len(base_intervals) - 1, current_stage + 1)
            new_interval = int(base_intervals[next_stage] * ease_factor * multiplier)
        
        # Adicionar variação aleatória (±20%)
        variation = random.uniform(0.8, 1.2)
        new_interval = max(1, int(new_interval * variation))
        
        return datetime.now() + timedelta(days=new_interval), new_interval, ease_factor
    
    def update_item_after_review(self, item_id: int, correct: bool, time_spent: float):
        """Atualiza item após revisão"""
        for item in st.session_state.spaced_repetition_items:
            if item['id'] == item_id:
                # Atualizar estatísticas
                item['attempts'] += 1
                if correct:
                    item['correct_attempts'] += 1
                
                item['success_rate'] = item['correct_attempts'] / item['attempts']
                item['last_reviewed'] = datetime.now()
                
                # Calcular próxima revisão
                performance = item['success_rate']
                next_review, new_interval, new_ease = self.calculate_next_review_date(item, performance)
                
                item['next_review'] = next_review
                item['interval_days'] = new_interval
                item['ease_factor'] = new_ease
                
                # Atualizar status baseado na performance
                if item['success_rate'] >= 0.9 and item['attempts'] >= 5:
                    item['status'] = ReviewStatus.DOMINADO
                elif item['success_rate'] >= 0.7 and item['attempts'] >= 3:
                    item['status'] = ReviewStatus.REVISAO
                elif item['attempts'] >= 1:
                    item['status'] = ReviewStatus.APRENDENDO
                
                # Atualizar prioridade
                urgency = max(0, (datetime.now() - item['next_review']).days)
                difficulty_factor = item['difficulty'].value / 5
                performance_factor = 1 - item['success_rate']
                
                item['priority_score'] = int(
                    (urgency * 30) + 
                    (difficulty_factor * 40) + 
                    (performance_factor * 30)
                )
                
                break
    
    def get_items_for_today(self) -> List[Dict[str, Any]]:
        """Retorna itens para revisão hoje"""
        today = datetime.now().date()
        
        items_due = [
            item for item in st.session_state.spaced_repetition_items
            if item['next_review'].date() <= today
        ]
        
        # Ordenar por prioridade
        items_due.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return items_due[:20]  # Máximo 20 itens por dia
    
    def get_weekly_forecast(self) -> Dict[str, int]:
        """Retorna previsão semanal de revisões"""
        forecast = {}
        
        for i in range(7):
            date = datetime.now() + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')
            
            items_due = [
                item for item in st.session_state.spaced_repetition_items
                if item['next_review'].date() == date.date()
            ]
            
            forecast[date_str] = len(items_due)
        
        return forecast
    
    def render_spaced_repetition_dashboard(self):
        """Renderiza dashboard do sistema de revisão espaçada"""
        st.title("📚 Revisão Espaçada Inteligente")
        st.markdown("Sistema baseado na curva de esquecimento para otimizar sua retenção de conhecimento")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        items_today = self.get_items_for_today()
        stats = st.session_state.study_statistics
        
        with col1:
            st.metric(
                "📋 Itens para Hoje",
                len(items_today),
                delta=f"Meta: 15 itens"
            )
        
        with col2:
            st.metric(
                "🎯 Taxa de Sucesso",
                f"{stats['average_success_rate']:.1%}",
                delta="+5%" if stats['average_success_rate'] > 0.7 else "-2%"
            )
        
        with col3:
            st.metric(
                "🔥 Sequência de Dias",
                f"{stats['streak_days']} dias",
                delta="Mantendo!" if stats['streak_days'] > 7 else "Continue!"
            )
        
        with col4:
            st.metric(
                "⏱️ Tempo Economizado",
                f"{stats['time_saved_minutes']} min",
                delta="Esta semana"
            )
        
        st.divider()
        
        # Tabs para diferentes funcionalidades
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Revisão Hoje",
            "📊 Estatísticas",
            "📅 Cronograma",
            "⚙️ Configurações",
            "📈 Progresso"
        ])
        
        with tab1:
            self.render_daily_review(items_today)
        
        with tab2:
            self.render_statistics()
        
        with tab3:
            self.render_schedule()
        
        with tab4:
            self.render_settings()
        
        with tab5:
            self.render_progress_analysis()

    def render_daily_review(self, items_today: List[Dict[str, Any]]):
        """Renderiza sessão de revisão diária"""
        st.subheader("📋 Sessão de Revisão - Hoje")

        if not items_today:
            st.success("🎉 Parabéns! Você completou todas as revisões de hoje!")
            st.balloons()

            # Sugerir atividades alternativas
            st.info("💡 **Sugestões para continuar estudando:**")
            st.write("• Revisar itens dominados para reforçar")
            st.write("• Adicionar novos tópicos ao sistema")
            st.write("• Praticar questões de simulados")
            st.write("• Estudar temas de baixa performance")
            return

        # Filtros e configurações
        col1, col2, col3 = st.columns(3)

        with col1:
            filter_subject = st.selectbox(
                "Filtrar por matéria:",
                ["Todas"] + list(set(item['materia'] for item in items_today))
            )

        with col2:
            filter_difficulty = st.selectbox(
                "Filtrar por dificuldade:",
                ["Todas"] + [f"Nível {i}" for i in range(1, 6)]
            )

        with col3:
            sort_by = st.selectbox(
                "Ordenar por:",
                ["Prioridade", "Dificuldade", "Matéria", "Última Revisão"]
            )

        # Aplicar filtros
        filtered_items = items_today

        if filter_subject != "Todas":
            filtered_items = [item for item in filtered_items if item['materia'] == filter_subject]

        if filter_difficulty != "Todas":
            level = int(filter_difficulty.split()[-1])
            filtered_items = [item for item in filtered_items if item['difficulty'].value == level]

        # Aplicar ordenação
        if sort_by == "Dificuldade":
            filtered_items.sort(key=lambda x: x['difficulty'].value, reverse=True)
        elif sort_by == "Matéria":
            filtered_items.sort(key=lambda x: x['materia'])
        elif sort_by == "Última Revisão":
            filtered_items.sort(key=lambda x: x['last_reviewed'])
        # Prioridade já está ordenada por padrão

        st.write(f"**{len(filtered_items)} itens** para revisão:")

        # Modo de revisão
        review_mode = st.radio(
            "Modo de revisão:",
            ["📝 Lista Completa", "🎯 Sessão Focada", "⚡ Revisão Rápida"],
            horizontal=True
        )

        if review_mode == "📝 Lista Completa":
            self.render_complete_review_list(filtered_items)
        elif review_mode == "🎯 Sessão Focada":
            self.render_focused_session(filtered_items)
        else:  # Revisão Rápida
            self.render_quick_review(filtered_items)

    def render_complete_review_list(self, items: List[Dict[str, Any]]):
        """Renderiza lista completa de revisão"""
        st.write("### 📝 Lista Completa de Revisão")

        for i, item in enumerate(items, 1):
            with st.expander(
                f"{i}. {item['materia']} - {item['topic']} "
                f"(Nível {item['difficulty'].value}) - "
                f"Taxa: {item['success_rate']:.1%}",
                expanded=i <= 3
            ):
                col1, col2, col3 = st.columns([2, 1, 1])

                with col1:
                    st.write(f"**Tópico:** {item['topic']}")
                    st.write(f"**Status:** {item['status'].value.title()}")
                    st.write(f"**Última revisão:** {item['last_reviewed'].strftime('%d/%m/%Y')}")

                    # Indicador de urgência
                    days_overdue = (datetime.now() - item['next_review']).days
                    if days_overdue > 0:
                        st.error(f"⚠️ Atrasado há {days_overdue} dias")
                    elif days_overdue == 0:
                        st.warning("📅 Vence hoje")
                    else:
                        st.info(f"📅 Próxima revisão em {abs(days_overdue)} dias")

                with col2:
                    st.metric("Tentativas", item['attempts'])
                    st.metric("Acertos", item['correct_attempts'])
                    st.metric("Taxa Sucesso", f"{item['success_rate']:.1%}")

                with col3:
                    st.metric("Prioridade", item['priority_score'])
                    st.metric("Facilidade", f"{item['ease_factor']:.1f}")
                    st.metric("Intervalo", f"{item['interval_days']} dias")

                # Botões de ação
                col_a, col_b, col_c = st.columns(3)

                with col_a:
                    if st.button(f"✅ Acertei", key=f"correct_{item['id']}"):
                        self.update_item_after_review(item['id'], True, 2.0)
                        st.success("Item marcado como correto!")
                        st.rerun()

                with col_b:
                    if st.button(f"❌ Errei", key=f"incorrect_{item['id']}"):
                        self.update_item_after_review(item['id'], False, 2.0)
                        st.error("Item marcado como incorreto. Será revisado em breve.")
                        st.rerun()

                with col_c:
                    if st.button(f"⏭️ Pular", key=f"skip_{item['id']}"):
                        st.info("Item pulado para próxima sessão.")

    def render_focused_session(self, items: List[Dict[str, Any]]):
        """Renderiza sessão focada de revisão"""
        st.write("### 🎯 Sessão Focada")

        if 'current_session_index' not in st.session_state:
            st.session_state.current_session_index = 0

        if 'session_items' not in st.session_state:
            st.session_state.session_items = items[:10]  # Máximo 10 itens por sessão

        session_items = st.session_state.session_items
        current_index = st.session_state.current_session_index

        if current_index >= len(session_items):
            st.success("🎉 Sessão focada concluída!")
            st.balloons()

            # Estatísticas da sessão
            if 'session_results' in st.session_state:
                results = st.session_state.session_results
                correct = sum(results.values())
                total = len(results)

                st.metric("Performance da Sessão", f"{correct}/{total} ({correct/total:.1%})")

                if correct/total >= 0.8:
                    st.success("Excelente performance! 🌟")
                elif correct/total >= 0.6:
                    st.info("Boa performance! Continue assim! 👍")
                else:
                    st.warning("Performance pode melhorar. Revise os tópicos com dificuldade. 📚")

            # Botão para nova sessão
            if st.button("🔄 Nova Sessão"):
                st.session_state.current_session_index = 0
                st.session_state.session_items = items[10:20] if len(items) > 10 else items
                if 'session_results' in st.session_state:
                    del st.session_state.session_results
                st.rerun()

            return

        # Item atual
        current_item = session_items[current_index]

        # Progresso da sessão
        progress = (current_index + 1) / len(session_items)
        st.progress(progress)
        st.write(f"**Progresso:** {current_index + 1}/{len(session_items)}")

        # Card do item atual
        st.markdown(f"""
        <div style="border: 2px solid #1f77b4; border-radius: 10px; padding: 20px; margin: 10px 0;">
            <h3>📚 {current_item['materia']}</h3>
            <h4>📖 {current_item['topic']}</h4>
            <p><strong>Dificuldade:</strong> Nível {current_item['difficulty'].value}</p>
            <p><strong>Status:</strong> {current_item['status'].value.title()}</p>
            <p><strong>Taxa de Sucesso Atual:</strong> {current_item['success_rate']:.1%}</p>
        </div>
        """, unsafe_allow_html=True)

        # Botões de resposta
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("✅ Acertei", key=f"focused_correct_{current_item['id']}", use_container_width=True):
                self.record_session_result(current_item['id'], True)
                self.update_item_after_review(current_item['id'], True, 1.5)
                st.session_state.current_session_index += 1
                st.rerun()

        with col2:
            if st.button("❌ Errei", key=f"focused_incorrect_{current_item['id']}", use_container_width=True):
                self.record_session_result(current_item['id'], False)
                self.update_item_after_review(current_item['id'], False, 1.5)
                st.session_state.current_session_index += 1
                st.rerun()

        with col3:
            if st.button("⏭️ Próximo", key=f"focused_skip_{current_item['id']}", use_container_width=True):
                st.session_state.current_session_index += 1
                st.rerun()

    def render_quick_review(self, items: List[Dict[str, Any]]):
        """Renderiza revisão rápida"""
        st.write("### ⚡ Revisão Rápida")
        st.info("Marque rapidamente os itens que você domina ou precisa revisar")

        # Dividir em colunas para visualização rápida
        cols = st.columns(2)

        for i, item in enumerate(items[:20]):  # Máximo 20 itens
            col = cols[i % 2]

            with col:
                with st.container():
                    st.write(f"**{item['materia']}** - {item['topic']}")
                    st.write(f"Nível {item['difficulty'].value} | Taxa: {item['success_rate']:.1%}")

                    col_a, col_b = st.columns(2)

                    with col_a:
                        if st.button("✅", key=f"quick_correct_{item['id']}", help="Domino este tópico"):
                            self.update_item_after_review(item['id'], True, 0.5)
                            st.success("✅")

                    with col_b:
                        if st.button("❌", key=f"quick_incorrect_{item['id']}", help="Preciso revisar"):
                            self.update_item_after_review(item['id'], False, 0.5)
                            st.error("❌")

                    st.divider()

    def record_session_result(self, item_id: int, correct: bool):
        """Registra resultado da sessão focada"""
        if 'session_results' not in st.session_state:
            st.session_state.session_results = {}

        st.session_state.session_results[item_id] = correct

    def render_statistics(self):
        """Renderiza estatísticas do sistema"""
        st.subheader("📊 Estatísticas de Aprendizado")

        # Estatísticas por status
        col1, col2 = st.columns(2)

        with col1:
            st.write("#### 📈 Distribuição por Status")
            status_counts = st.session_state.study_statistics['items_by_status']

            # Gráfico de pizza
            fig_status = px.pie(
                values=list(status_counts.values()),
                names=list(status_counts.keys()),
                title="Itens por Status de Aprendizado",
                color_discrete_map={
                    'novo': '#ff7f0e',
                    'aprendendo': '#2ca02c',
                    'revisao': '#1f77b4',
                    'dominado': '#d62728'
                }
            )
            st.plotly_chart(fig_status, use_container_width=True)

        with col2:
            st.write("#### 📊 Distribuição por Dificuldade")
            difficulty_counts = st.session_state.study_statistics['items_by_difficulty']

            # Gráfico de barras
            fig_difficulty = px.bar(
                x=list(difficulty_counts.keys()),
                y=list(difficulty_counts.values()),
                title="Itens por Nível de Dificuldade",
                color=list(difficulty_counts.values()),
                color_continuous_scale="Viridis"
            )
            fig_difficulty.update_layout(showlegend=False)
            st.plotly_chart(fig_difficulty, use_container_width=True)

        # Performance por matéria
        st.write("#### 📚 Performance por Matéria")

        # Calcular estatísticas por matéria
        materia_stats = {}
        for item in st.session_state.spaced_repetition_items:
            materia = item['materia']
            if materia not in materia_stats:
                materia_stats[materia] = {
                    'total_items': 0,
                    'total_attempts': 0,
                    'total_correct': 0,
                    'avg_difficulty': 0,
                    'dominado_count': 0
                }

            stats = materia_stats[materia]
            stats['total_items'] += 1
            stats['total_attempts'] += item['attempts']
            stats['total_correct'] += item['correct_attempts']
            stats['avg_difficulty'] += item['difficulty'].value

            if item['status'] == ReviewStatus.DOMINADO:
                stats['dominado_count'] += 1

        # Calcular médias
        for materia, stats in materia_stats.items():
            if stats['total_attempts'] > 0:
                stats['success_rate'] = stats['total_correct'] / stats['total_attempts']
            else:
                stats['success_rate'] = 0

            stats['avg_difficulty'] = stats['avg_difficulty'] / stats['total_items']
            stats['mastery_rate'] = stats['dominado_count'] / stats['total_items']

        # Criar DataFrame para visualização
        df_materias = pd.DataFrame([
            {
                'Matéria': materia,
                'Taxa de Sucesso': stats['success_rate'],
                'Taxa de Domínio': stats['mastery_rate'],
                'Dificuldade Média': stats['avg_difficulty'],
                'Total de Itens': stats['total_items']
            }
            for materia, stats in materia_stats.items()
        ])

        # Gráfico de radar por matéria
        fig_radar = go.Figure()

        for _, row in df_materias.iterrows():
            fig_radar.add_trace(go.Scatterpolar(
                r=[
                    row['Taxa de Sucesso'] * 100,
                    row['Taxa de Domínio'] * 100,
                    (6 - row['Dificuldade Média']) * 20,  # Inverter dificuldade
                    min(100, row['Total de Itens'] * 5)  # Normalizar total
                ],
                theta=['Taxa de Sucesso', 'Taxa de Domínio', 'Facilidade', 'Volume'],
                fill='toself',
                name=row['Matéria']
            ))

        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=True,
            title="Radar de Performance por Matéria"
        )

        st.plotly_chart(fig_radar, use_container_width=True)

        # Tabela detalhada
        st.write("#### 📋 Detalhamento por Matéria")

        # Formatar DataFrame para exibição
        df_display = df_materias.copy()
        df_display['Taxa de Sucesso'] = df_display['Taxa de Sucesso'].apply(lambda x: f"{x:.1%}")
        df_display['Taxa de Domínio'] = df_display['Taxa de Domínio'].apply(lambda x: f"{x:.1%}")
        df_display['Dificuldade Média'] = df_display['Dificuldade Média'].apply(lambda x: f"{x:.1f}")

        st.dataframe(df_display, use_container_width=True)

    def render_schedule(self):
        """Renderiza cronograma de revisões"""
        st.subheader("📅 Cronograma de Revisões")

        # Previsão semanal
        weekly_forecast = self.get_weekly_forecast()

        col1, col2 = st.columns([2, 1])

        with col1:
            st.write("#### 📊 Previsão dos Próximos 7 Dias")

            # Gráfico de barras da previsão semanal
            dates = list(weekly_forecast.keys())
            counts = list(weekly_forecast.values())

            # Converter datas para formato mais legível
            readable_dates = [
                datetime.strptime(date, '%Y-%m-%d').strftime('%d/%m')
                for date in dates
            ]

            fig_forecast = px.bar(
                x=readable_dates,
                y=counts,
                title="Itens para Revisão por Dia",
                labels={'x': 'Data', 'y': 'Número de Itens'},
                color=counts,
                color_continuous_scale="Blues"
            )

            # Adicionar linha de meta
            fig_forecast.add_hline(y=15, line_dash="dash", line_color="red",
                                 annotation_text="Meta diária: 15 itens")

            st.plotly_chart(fig_forecast, use_container_width=True)

        with col2:
            st.write("#### 📈 Resumo Semanal")

            total_items = sum(counts)
            avg_daily = total_items / 7
            max_day = max(counts)
            min_day = min(counts)

            st.metric("Total da Semana", total_items)
            st.metric("Média Diária", f"{avg_daily:.1f}")
            st.metric("Dia Mais Pesado", max_day)
            st.metric("Dia Mais Leve", min_day)

            # Indicador de carga
            if max_day > 20:
                st.error("⚠️ Carga alta detectada!")
                st.write("Considere redistribuir alguns itens.")
            elif avg_daily > 15:
                st.warning("📊 Carga moderada")
                st.write("Mantenha o ritmo de estudos.")
            else:
                st.success("✅ Carga equilibrada")
                st.write("Cronograma bem distribuído!")

        # Cronograma detalhado
        st.write("#### 📋 Cronograma Detalhado")

        # Seletor de período
        period_option = st.selectbox(
            "Período para visualizar:",
            ["Próximos 7 dias", "Próximos 15 dias", "Próximo mês"]
        )

        if period_option == "Próximos 7 dias":
            days_to_show = 7
        elif period_option == "Próximos 15 dias":
            days_to_show = 15
        else:
            days_to_show = 30

        # Mostrar cronograma por dia
        for i in range(days_to_show):
            date = datetime.now() + timedelta(days=i)
            date_str = date.strftime('%Y-%m-%d')

            items_for_date = [
                item for item in st.session_state.spaced_repetition_items
                if item['next_review'].date() == date.date()
            ]

            if items_for_date or i < 7:  # Sempre mostrar próximos 7 dias
                day_name = date.strftime('%A')
                day_names_pt = {
                    'Monday': 'Segunda-feira',
                    'Tuesday': 'Terça-feira',
                    'Wednesday': 'Quarta-feira',
                    'Thursday': 'Quinta-feira',
                    'Friday': 'Sexta-feira',
                    'Saturday': 'Sábado',
                    'Sunday': 'Domingo'
                }

                day_name_pt = day_names_pt.get(day_name, day_name)

                with st.expander(
                    f"📅 {date.strftime('%d/%m/%Y')} - {day_name_pt} "
                    f"({len(items_for_date)} itens)",
                    expanded=i == 0  # Expandir apenas hoje
                ):
                    if not items_for_date:
                        st.info("🎉 Nenhuma revisão programada para este dia!")
                    else:
                        # Agrupar por matéria
                        items_by_subject = {}
                        for item in items_for_date:
                            subject = item['materia']
                            if subject not in items_by_subject:
                                items_by_subject[subject] = []
                            items_by_subject[subject].append(item)

                        for subject, subject_items in items_by_subject.items():
                            st.write(f"**📚 {subject}** ({len(subject_items)} itens)")

                            for item in subject_items[:5]:  # Mostrar apenas os 5 primeiros
                                priority_icon = "🔴" if item['priority_score'] > 70 else "🟡" if item['priority_score'] > 40 else "🟢"
                                st.write(f"  {priority_icon} {item['topic']} (Nível {item['difficulty'].value})")

                            if len(subject_items) > 5:
                                st.write(f"  ... e mais {len(subject_items) - 5} itens")

                            st.write("")

    def render_settings(self):
        """Renderiza configurações do sistema"""
        st.subheader("⚙️ Configurações do Sistema")

        col1, col2 = st.columns(2)

        with col1:
            st.write("#### 🎯 Metas de Estudo")

            daily_target = st.slider(
                "Meta diária de revisões:",
                min_value=5,
                max_value=50,
                value=15,
                help="Número ideal de itens para revisar por dia"
            )

            session_size = st.slider(
                "Tamanho da sessão focada:",
                min_value=5,
                max_value=20,
                value=10,
                help="Número de itens por sessão focada"
            )

            difficulty_preference = st.selectbox(
                "Priorizar dificuldade:",
                ["Equilibrado", "Itens Difíceis Primeiro", "Itens Fáceis Primeiro"],
                help="Como priorizar itens por dificuldade"
            )

        with col2:
            st.write("#### ⏰ Configurações de Tempo")

            review_time = st.time_input(
                "Horário preferido para revisões:",
                value=datetime.strptime("08:00", "%H:%M").time(),
                help="Horário que você prefere fazer revisões"
            )

            weekend_study = st.checkbox(
                "Estudar nos fins de semana",
                value=True,
                help="Incluir sábados e domingos no cronograma"
            )

            notification_enabled = st.checkbox(
                "Ativar lembretes",
                value=True,
                help="Receber notificações sobre revisões pendentes"
            )

        st.divider()

        st.write("#### 🔧 Configurações Avançadas")

        col3, col4 = st.columns(2)

        with col3:
            ease_factor_adjustment = st.slider(
                "Sensibilidade do algoritmo:",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                help="Quão rapidamente o sistema ajusta intervalos baseado na performance"
            )

            max_interval = st.slider(
                "Intervalo máximo (dias):",
                min_value=30,
                max_value=365,
                value=180,
                help="Maior intervalo possível entre revisões"
            )

        with col4:
            auto_promote = st.checkbox(
                "Promoção automática",
                value=True,
                help="Promover automaticamente itens com boa performance"
            )

            reset_on_error = st.checkbox(
                "Resetar em erro",
                value=False,
                help="Voltar ao início quando errar um item dominado"
            )

        # Botões de ação
        col5, col6, col7 = st.columns(3)

        with col5:
            if st.button("💾 Salvar Configurações", use_container_width=True):
                # Aqui salvaria as configurações
                st.success("✅ Configurações salvas!")

        with col6:
            if st.button("🔄 Restaurar Padrões", use_container_width=True):
                st.info("🔄 Configurações restauradas para o padrão!")

        with col7:
            if st.button("📊 Recalcular Cronograma", use_container_width=True):
                # Recalcular cronograma com novas configurações
                st.session_state.review_schedule = self.generate_review_schedule()
                st.success("📅 Cronograma recalculado!")

    def render_progress_analysis(self):
        """Renderiza análise de progresso"""
        st.subheader("📈 Análise de Progresso")

        # Simular dados históricos de progresso
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')

        progress_data = []
        for date in dates:
            # Simular progresso crescente com variação
            base_progress = min(100, (datetime.now() - dates[0]).days * 2)
            daily_variation = random.uniform(-5, 10)

            progress_data.append({
                'data': date,
                'items_reviewed': random.randint(8, 25),
                'success_rate': random.uniform(0.6, 0.95),
                'time_spent': random.uniform(15, 60),
                'items_mastered': random.randint(0, 5),
                'cumulative_mastered': base_progress + daily_variation
            })

        df_progress = pd.DataFrame(progress_data)

        # Gráficos de progresso
        col1, col2 = st.columns(2)

        with col1:
            st.write("#### 📊 Itens Revisados por Dia")

            fig_reviewed = px.line(
                df_progress,
                x='data',
                y='items_reviewed',
                title="Evolução Diária de Revisões",
                markers=True
            )

            # Adicionar média móvel
            df_progress['items_reviewed_ma'] = df_progress['items_reviewed'].rolling(window=7).mean()

            fig_reviewed.add_trace(
                go.Scatter(
                    x=df_progress['data'],
                    y=df_progress['items_reviewed_ma'],
                    mode='lines',
                    name='Média Móvel (7 dias)',
                    line=dict(color='red', width=2)
                )
            )

            st.plotly_chart(fig_reviewed, use_container_width=True)

        with col2:
            st.write("#### 🎯 Taxa de Sucesso")

            fig_success = px.line(
                df_progress,
                x='data',
                y='success_rate',
                title="Evolução da Taxa de Sucesso",
                markers=True
            )

            # Adicionar linha de meta
            fig_success.add_hline(y=0.8, line_dash="dash", line_color="green",
                                annotation_text="Meta: 80%")

            st.plotly_chart(fig_success, use_container_width=True)

        # Progresso cumulativo
        st.write("#### 📈 Progresso Cumulativo")

        fig_cumulative = make_subplots(
            rows=2, cols=1,
            subplot_titles=('Itens Dominados', 'Tempo de Estudo Acumulado'),
            vertical_spacing=0.1
        )

        # Itens dominados
        fig_cumulative.add_trace(
            go.Scatter(
                x=df_progress['data'],
                y=df_progress['cumulative_mastered'],
                mode='lines+markers',
                name='Itens Dominados',
                fill='tonexty'
            ),
            row=1, col=1
        )

        # Tempo acumulado
        df_progress['cumulative_time'] = df_progress['time_spent'].cumsum()

        fig_cumulative.add_trace(
            go.Scatter(
                x=df_progress['data'],
                y=df_progress['cumulative_time'],
                mode='lines+markers',
                name='Tempo Acumulado (min)',
                line=dict(color='orange')
            ),
            row=2, col=1
        )

        fig_cumulative.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig_cumulative, use_container_width=True)

        # Estatísticas de progresso
        col3, col4, col5, col6 = st.columns(4)

        with col3:
            total_reviewed = df_progress['items_reviewed'].sum()
            st.metric("Total Revisado", f"{total_reviewed} itens")

        with col4:
            avg_success = df_progress['success_rate'].mean()
            st.metric("Taxa Média", f"{avg_success:.1%}")

        with col5:
            total_time = df_progress['time_spent'].sum()
            st.metric("Tempo Total", f"{total_time:.0f} min")

        with col6:
            items_mastered = df_progress['items_mastered'].sum()
            st.metric("Itens Dominados", f"{items_mastered} novos")
