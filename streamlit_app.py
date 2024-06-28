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

    options_ano = ['6° ano', '7° ano']
    unidades_tematicas = {
        '6° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
        '7° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística']
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
        '7° ano-Probabilidade e estatística': ['Probabilidade simples', 'Distribuição de frequência']
    }

    selected_ano = st.sidebar.selectbox("Ano", options_ano)
    selected_unidades_tematicas = st.sidebar.selectbox("Unidades temáticas", unidades_tematicas[selected_ano])
    index_objeto_conhecimento = f"{selected_ano}-{selected_unidades_tematicas}"
    selected_objeto_conhecimento = st.sidebar.selectbox("Objetos de conhecimento", objetos_conhecimento[index_objeto_conhecimento])
    
    contexto = st.sidebar.text_area("Descreva o contexto para as questões")

    # Debugging output
    st.write("Selected Year:", selected_ano)
    st.write("Selected Thematic Units:", selected_unidades_tematicas)
    st.write("Selected Knowledge Object:", selected_objeto_conhecimento)
    st.write("Context:", contexto)

    prompt_template = """
    Tarefa 1 - Geração de Questão de Matemática:
    "Por favor, gere uma questão de matemática de múltipla escolha para alunos do {ano} ano, focada em {unidade_tematica}, que explore {objeto_conhecimento}. A questão deve incluir uma introdução contextual para ajudar os alunos a entenderem o problema. Proporcione quatro alternativas plausíveis, uma das quais deve ser a resposta correta. Inclua parâmetros variáveis para permitir ajustes na dificuldade da questão. Use a seguinte estrutura:

    1. Introdução/Contexto: [Forneça um cenário breve e claro relacionado à questão]
    2. Enunciado da Questão: [Descreva a questão matemática]
    3. Alternativas:
       A) [Alternativa 1]
       B) [Alternativa 2]
       C) [Alternativa 3]
       D) [Alternativa 4]
    4. Resposta Correta: [Indique a alternativa correta]"

    Tarefa 2 - Solução Detalhada:
    "Para a questão gerada anteriormente, forneça uma solução detalhada passo a passo, explicando cada etapa do processo de resolução da questão. Use uma linguagem clara e acessível para estudantes do {ano} ano. Siga a estrutura abaixo:

    1. Passo 1: [Descrição da primeira etapa]
    2. Passo 2: [Descrição da segunda etapa]
    3. Passo 3: [Descrição da terceira etapa, se aplicável]
    4. Resumo: [Resumo do processo e resultado final]"

    Tarefa 3 - Feedback Personalizado:
    "Baseado em uma resposta hipotética de um estudante que cometeu um erro comum ao resolver a questão, forneça feedback construtivo. Explique o erro, sua correção e forneça dicas para evitar esse tipo de engano no futuro. Use a seguinte estrutura:

    1. Erro Comum: [Descreva o erro que o estudante cometeu]
    2. Correção: [Explique a correção do erro]
    3. Dicas: [Forneça dicas práticas para evitar esse tipo de erro no futuro]"

    Considerações:
    - Forneça uma breve introdução ou contexto para cada questão.
    - As alternativas devem ser plausíveis e desafiadoras.
    - Inclua a resposta correta e uma breve explicação sobre por que essa resposta está correta.
    - Certifique-se de que as questões estão alinhadas com o conteúdo esperado para o {ano} ano.
    - Use formatação clara e consistente para apresentar as questões e respostas.

    ### Instruções Avançadas:
    1. Utilize linguagem de alta precisão e evite ambiguidades.
    2. Certifique-se de que cada passo na solução é lógico e sequencial.
    3. Ao criar alternativas, inclua erros comuns que os estudantes possam cometer para testá-los de forma mais eficaz.
    4. Na explicação da resposta correta, forneça insights sobre por que as outras alternativas estão erradas.
    5. Use formatação Markdown para organizar as perguntas e respostas de maneira clara e legível.

    ### Exemplos de Questões e Soluções:

    #### Exemplo de Questão:
    **Questão:** 
    Resolva a equação do segundo grau: \\(x^2 - 5x + 6 = 0\\). Quais são as soluções para \\(x\\)?

    **Alternativas:**
    A) \\(x = 2\\) e \\(x = 3\\)  
    B) \\(x = 1\\) e \\(x = 6\\)  
    C) \\(x = -2\\) e \\(x = -3\\)  
    D) \\(x = 0\\) e \\(x = 5\\)

    **Resposta Correta:** 
    A) \\(x = 2\\) e \\(x = 3\\)

    #### Exemplo de Solução Detalhada:
    **Solução:**
    1. **Identifique os coeficientes:** \\(a = 1\\), \\(b = -5\\), \\(c = 6\\).
    2. **Calcule o discriminante (Δ):** \\(\\Delta = b^2 - 4ac = (-5)^2 - 4(1)(6) = 25 - 24 = 1\\).
    3. **Calcule as raízes usando a fórmula de Bhaskara:**  
       \\(x = \\frac{{-b \\pm \\sqrt{{\\Delta}}}}{2a}\\)
    4. **Calcule a primeira raiz (x₁):**  
       \\(x₁ = \\frac{{-(-5) + \\sqrt{1}}}{2(1)} = \\frac{5 + 1}{2} = \\frac{6}{2} = 3\\)
    5. **Calcule a segunda raiz (x₂):**  
       \\(x₂ = \\frac{{-(-5) - \\sqrt{1}}}{2(1)} = \\frac{5 - 1}{2} = \\frac{4}{2} = 2\\)

    Portanto, as soluções para a equação \\(x^2 - 5x + 6 = 0\\) são \\(x = 2\\) e \\(x = 3\\).

    #### Exemplo de Feedback Personalizado:
    **Erro Comum:**
    O estudante calculou o discriminante (Δ) como \\(b^2 - 4ac = (-5)^2 + 4(1)(6) = 25 + 24 = 49\\), em vez de \\(25 - 24 = 1\\).

    **Correção:**
    Explique ao estudante que a fórmula correta é \\(b^2 - 4ac\\), onde a subtração é crucial. Portanto, a correção seria:
    \\[
    \\Delta = (-5)^2 - 4(1)(6) = 25 - 24 = 1
    \\]

    **Dicas:**
    Para evitar esse tipo de erro no futuro, sempre escreva a fórmula completa e substitua os valores com cuidado, prestando atenção aos sinais. Praticar mais problemas de equações quadráticas pode ajudar a familiarizar-se com o processo.
    """

    # Ensure context is not empty to avoid formatting issues
    if not contexto:
        contexto = "Sem contexto adicional."

    try:
        ane_prompt = prompt_template.format(
            ano=selected_ano,
            unidade_tematica=selected_unidades_tematicas,
            objeto_conhecimento=selected_objeto_conhecimento,
            contexto=contexto
        )
        st.write("Generated Prompt:", ane_prompt)
    except KeyError as e:
        st.error(f"Erro ao formatar o prompt: variável {e} não encontrada. Verifique se todas as variáveis estão definidas corretamente.")
        return
    except ValueError as ve:
        st.error(f"Erro de formatação do prompt: {ve}")
        return

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
