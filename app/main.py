import streamlit as st
from crew import run_crew
import json

st.title("Assistente de Preparação para Concursos Públicos")

# Entrada do usuário
cargo = st.text_input("Cargo")
concurso = st.text_input("Concurso")
banca = st.text_input("Banca")
cidade = st.text_input("Cidade")
study_hours = st.number_input("Horas de Estudo Semanais", min_value=1, max_value=40, value=10)
study_months = st.number_input("Duração do Estudo (Meses)", min_value=1, max_value=12, value=6)

if st.button("Gerar Plano de Estudos e Simulado"):
    if cargo and concurso and banca and cidade:
        with st.spinner("Processando..."):
            result = run_crew(cargo, concurso, banca, cidade, study_hours, study_months)
        
        # Criar abas para diferentes seções
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Plano de Estudos", "Simulado", "Repetição Espaçada", "Previsão de Desempenho", "Resumo"])
        
        with tab1:
            st.subheader("Plano de Estudos")
            try:
                study_plan = json.loads(result['study_plan'])
                st.json(result['study_plan'])
                
                # Mostrar cronograma semanal se disponível
                if "weekly_schedule" in study_plan:
                    st.subheader("Cronograma Semanal")
                    for week in study_plan["weekly_schedule"][:4]:  # Mostrar primeiras 4 semanas
                        st.write(f"**Semana {week['week']}**: {week['phase']}")
                        st.write(f"Foco: {week['focus']}")
                        st.write("Matérias:")
                        for subject, data in week['subjects'].items():
                            st.write(f"- {subject}: {data['hours']} horas ({data['activity']})")
                        st.write("---")
            except:
                st.json(result['study_plan'])
        
        with tab2:
            st.subheader("Simulado")
            st.text(result['mock_exam'])
        
        with tab3:
            st.subheader("Plano de Repetição Espaçada")
            try:
                spaced_plan = json.loads(result['spaced_repetition_plan'])
                
                # Mostrar itens para hoje
                if "today" in spaced_plan:
                    st.write(f"**Itens para revisão hoje:** {len(spaced_plan['today'])}")
                    for item in spaced_plan['today'][:5]:  # Mostrar primeiros 5 itens
                        st.write(f"- {item['content']} ({item['subject']}, Prioridade: {item['priority']})")
                
                # Mostrar estatísticas
                if "metadata" in spaced_plan:
                    st.write("**Estatísticas:**")
                    st.write(f"Total de itens: {spaced_plan['metadata']['total_items']}")
                    if "priority_distribution" in spaced_plan["metadata"]:
                        st.write("Distribuição por prioridade:")
                        for priority, count in spaced_plan["metadata"]["priority_distribution"].items():
                            st.write(f"- {priority}: {count} itens")
                
                st.json(result['spaced_repetition_plan'])
            except:
                st.json(result['spaced_repetition_plan'])
        
        with tab4:
            st.subheader("Previsão de Desempenho")
            try:
                prediction = json.loads(result['performance_prediction'])
                
                # Mostrar previsões principais
                if "predictions" in prediction:
                    pred = prediction["predictions"]
                    st.write(f"**Pontuação prevista:** {pred.get('overall_score', 0)}")
                    st.write(f"**Probabilidade de sucesso:** {pred.get('success_probability', 0) * 100:.1f}%")
                    st.write(f"**Taxa de melhoria:** {pred.get('improvement_rate', 0)} pontos por avaliação")
                    
                    # Matérias críticas
                    if "critical_subjects" in pred and pred["critical_subjects"]:
                        st.write("**Matérias críticas:**")
                        for subject in pred["critical_subjects"]:
                            st.write(f"- {subject}")
                
                # Mostrar plano de melhoria
                if "improvement_plan" in prediction:
                    plan = prediction["improvement_plan"]
                    st.subheader("Plano de Melhoria")
                    
                    if "critical_interventions" in plan:
                        st.write("**Intervenções recomendadas:**")
                        for intervention in plan["critical_interventions"]:
                            st.write(f"- {intervention['subject']}: {intervention['action']} ({intervention['expected_improvement']} de melhoria)")
                
                st.json(result['performance_prediction'])
            except:
                st.json(result['performance_prediction'])
        
        with tab5:
            st.subheader("Resumo do Plano")
            st.write(f"**Cargo:** {cargo}")
            st.write(f"**Concurso:** {concurso}")
            st.write(f"**Banca:** {banca}")
            st.write(f"**Cidade:** {cidade}")
            st.write(f"**Horas semanais:** {study_hours}")
            st.write(f"**Duração:** {study_months} meses")
            
            # Mostrar resumo das previsões
            try:
                prediction = json.loads(result['performance_prediction'])
                if "summary" in prediction:
                    st.write(f"**Previsão:** {prediction['summary']}")
            except:
                pass
    else:
        st.error("Preencha todos os campos.")
