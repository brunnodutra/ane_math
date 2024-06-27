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
        '7° ano-Números e operações': ['Números racionais', 'Operações com frações'],
        '7° ano-Álgebra': ['Equações do 2º grau', 'Funções'],
        '7° ano-Geometria': ['Áreas de figuras planas', 'Teorema de Pitágoras'],
        '7° ano-Grandezas e medidas': ['Medidas de área', 'Medidas de volume'],
        '7° ano-Probabilidade e estatística': ['Probabilidade simples', 'Distribuição de frequência'],
        '8° ano-Números e operações': ['Números irracionais', 'Radiciação'],
        '8° ano-Álgebra': ['Polinômios', 'Sistema de equações lineares'],
        '8° ano-Geometria': ['Ângulos', 'Transformações geométricas'],
        '8° ano-Grandezas e medidas': ['Medidas de tempo', 'Escalas'],
        '8° ano-Probabilidade e estatística': ['Análise combinatória', 'Interpretação de dados'],
        '9° ano-Números e operações': ['Potenciação', 'Logaritmos'],
        '9° ano-Álgebra': ['Funções exponenciais', 'Progressões aritméticas'],
        '9° ano-Geometria': ['Relações entre arcos e ângulos na circunferência de um círculo', 'Semelhança de triângulos'],
        '9° ano-Grandezas e medidas': ['Unidades de medida utilizadas na informática', 'Volume de prismas e cilindros'],
    }

    selected_ano = st.sidebar.selectbox("Ano", options_ano)
    selected_unidades_tematicas = st.sidebar.selectbox("Unidades temáticas", unidades_tematicas[selected_ano])
    index_objeto_conhecimento = f"{selected_ano}-{selected_unidades_tematicas}"
    selected_objeto_conhecimento = st.sidebar.selectbox("Objetos de conhecimento", objetos_conhecimento[index_objeto_conhecimento])
    
    contexto = st.sidebar.text_area("Descreva o contexto para as questões")

    prompt_template = """
    Tarefa 1 - Geração de Questão de Matemática:
    "Por favor, gere uma questão de matemática para alunos do {ano} ano, focada em {unidade_tematica}, que explore {objeto_conhecimento}. Inclua parâmetros variáveis para permitir ajustes na dificuldade da questão."
    
    Tarefa 2 - Solução Detalhada:
    "Para a questão gerada anteriormente, forneça uma solução detalhada passo a passo, explicando cada etapa do processo de resolução da questão. Use uma linguagem clara e acessível para estudantes do {ano} ano."
    
    Tarefa 3 - Feedback Personalizado:
    "Baseado em uma resposta hipotética de um estudante que cometeu um erro comum ao resolver a questão, forneça feedback construtivo. Explique o erro, sua correção e forneça dicas para evitar esse tipo de engano no futuro."
    
    Considerações:
    - Forneça uma breve introdução ou contexto para cada questão.
    - As alternativas devem ser plausíveis e desafiadoras.
    - Inclua a resposta correta e uma breve explicação sobre por que essa resposta está correta.
    - Certifique-se de que as questões estão alinhadas com o conteúdo esperado para o {ano} ano.
    - Use formatação clara e consistente para apresentar as questões e respostas.
    """

    ane_prompt = prompt_template.format(
        ano=selected_ano,
        unidade_tematica=selected_unidades_tematicas,
        objeto_conhecimento=selected_objeto_conhecimento,
        contexto=contexto
    )

    system_prompt_ane = """
    Como um assistente de professor, você deve criar avaliações de alta qualidade que ajudem a promover uma compreensão profunda do conteúdo. Suas respostas devem ser precisas, claras e alinhadas com o contexto fornecido. Utilize formatação Markdown para organizar as perguntas e respostas.
    """

    if st.sidebar.button('Gerar atividades'):
        with st.spinner("Gerando atividades..."):
            response = generate_llama3_response(ane_prompt, system_prompt_ane)
            if response:
                st.markdown(response)

if __name__ == "__main__":
    main()
