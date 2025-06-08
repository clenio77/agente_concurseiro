import streamlit as st
from crew import run_crew

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
        st.subheader("Plano de Estudos")
        st.json(result['study_plan'])
        st.subheader("Simulado")
        st.text(result['mock_exam'])
    else:
        st.error("Preencha todos os campos.")