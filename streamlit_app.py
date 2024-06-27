import streamlit as st
import replicate
import os

st.set_page_config(page_title="Gerador de Avaliações de Matemática", layout="wide")

def generate_llama3_response(prompt_input, system_prompt_ane):
    try:
        output = replicate.run(
            "meta/meta-llama-3-70b-instruct",
            input={
                "prompt": f"[INST] <<SYS>>\n{system_prompt_ane}\n<</SYS>>\n\n{prompt_input} [/INST]",
                "temperature": 0.7,
                "top_p": 0.9,
                "repetition_penalty": 1.1
            }
        )
        full_response = ''
        for item in output:
            full_response += item
        return full_response
    except replicate.exceptions.ReplicateError as e:
        st.error(f"Erro ao gerar resposta: {str(e)}")
        return None

def main():
    try:
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
        os.environ['REPLICATE_API_TOKEN'] = replicate_api
    except KeyError:
        st.error("Replicate API token não encontrado. Adicione o token ao arquivo secrets.toml.")
        return

    st.sidebar.title("Gerador de Avaliações")
    st.sidebar.subheader("Selecione as opções para gerar a avaliação")

    options_ano = ['6° ano', '7° ano', '8° ano', '9° ano']
    unidades_tematicas = {
        '6° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
        '7° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
        '8° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
        '9° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
    }

    objetos_conhecimento = {
        '6° ano-Números e operações': ['Adição e subtração de números naturais', 'Multiplicação e divisão de números naturais'],
        '6° ano-Álgebra': ['Expressões algébricas', 'Equações do 1º grau'],
        '6° ano-Geometria': ['Figuras geométricas planas', 'Sólidos geométricos'],
        '6° ano-Grandezas e medidas': ['Medidas de comprimento', 'Medidas de massa'],
        '6° ano-Probabilidade e estatística': ['Experimentos aleatórios', 'Leitura e interpretação de gráficos'],
        '7° ano-Números e operações': ['Números racionais
