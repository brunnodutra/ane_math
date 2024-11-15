import streamlit as st
import replicate
import os

st.set_page_config(page_title="Gerador de Avaliações de Matemática", layout="wide")

def translate_text(text, language):
    translations = {
        'en': {
            "Gerador de Avaliações": "Assessment Generator",
            "Selecione as opções para gerar a avaliação": "Select options to generate the assessment",
            "Ano": "Grade",
            "Unidades temáticas": "Thematic Units",
            "Objetos de conhecimento": "Knowledge Objects",
            "Descreva o contexto para as questões": "Describe the context for the questions",
            "Gerar atividades": "Generate Activities",
            "Gerando atividades...": "Generating activities...",
            "Erro ao gerar resposta": "Error generating response",
            "Erro ao formatar o prompt": "Error formatting prompt",
            "variable not found": "variable not found",
            "check if all variables are defined correctly": "check if all variables are defined correctly",
            "error in formatting prompt": "error in formatting prompt",
            "Sem contexto adicional.": "No additional context.",
            "Como um assistente de professor, você deve criar avaliações de alta qualidade que ajudem a promover uma compreensão profunda do conteúdo. Suas respostas devem ser precisas, claras e alinhadas com o contexto fornecido. Utilize formatação Markdown para organizar as perguntas e respostas.": 
            "As a teaching assistant, you must create high-quality assessments that help promote a deep understanding of the content. Your answers must be accurate, clear, and aligned with the provided context. Use Markdown formatting to organize questions and answers.",
            "Tarefa 1 - Geração de Questão de Matemática:": "Task 1 - Generation of Math Question:",
            "Por favor, gere uma questão de matemática de múltipla escolha para alunos do {ano} ano, focada em {unidade_tematica}, que explore {objeto_conhecimento}. A questão deve incluir uma introdução contextual para ajudar os alunos a entenderem o problema. Proporcione quatro alternativas plausíveis, uma das quais deve ser a resposta correta. Inclua parâmetros variáveis para permitir ajustes na dificuldade da questão. Use a seguinte estrutura:": 
            "Please generate a multiple-choice math question for {ano} grade students, focused on {unidade_tematica}, that explores {objeto_conhecimento}. The question should include a contextual introduction to help students understand the problem. Provide four plausible alternatives, one of which should be the correct answer. Include variable parameters to allow adjustments in the difficulty of the question. Use the following structure:",
            "1. Introdução/Contexto: [Forneça um cenário breve e claro relacionado à questão]": "1. Introduction/Context: [Provide a brief and clear scenario related to the question]",
            "2. Enunciado da Questão: [Descreva a questão matemática]": "2. Question Statement: [Describe the math question]",
            "3. Alternativas:": "3. Alternatives:",
            "A) [Alternativa 1]": "A) [Alternative 1]",
            "B) [Alternativa 2]": "B) [Alternative 2]",
            "C) [Alternativa 3]": "C) [Alternative 3]",
            "D) [Alternativa 4]": "D) [Alternative 4]",
            "4. Resposta Correta: [Indique a alternativa correta]": "4. Correct Answer: [Indicate the correct alternative]",
            "Tarefa 2 - Solução Detalhada:": "Task 2 - Detailed Solution:",
            "Para a questão gerada anteriormente, forneça uma solução detalhada passo a passo, explicando cada etapa do processo de resolução da questão. Use uma linguagem clara e acessível para estudantes do {ano} ano. Siga a estrutura abaixo:": 
            "For the previously generated question, provide a detailed step-by-step solution, explaining each stage of the problem-solving process. Use clear and accessible language for {ano} grade students. Follow the structure below:",
            "1. Passo 1: [Descrição da primeira etapa]": "1. Step 1: [Description of the first step]",
            "2. Passo 2: [Descrição da segunda etapa]": "2. Step 2: [Description of the second step]",
            "3. Passo 3: [Descrição da terceira etapa, se aplicável]": "3. Step 3: [Description of the third step, if applicable]",
            "4. Resumo: [Resumo do processo e resultado final]": "4. Summary: [Summary of the process and final result]",
            "Tarefa 3 - Feedback Personalizado:": "Task 3 - Personalized Feedback:",
            "Baseado em uma resposta hipotética de um estudante que cometeu um erro comum ao resolver a questão, forneça feedback construtivo. Explique o erro, sua correção e forneça dicas para evitar esse tipo de engano no futuro. Use a seguinte estrutura:": 
            "Based on a hypothetical student's response that made a common error while solving the question, provide constructive feedback. Explain the error, its correction, and give tips to avoid this type of mistake in the future. Use the following structure:",
            "1. Erro Comum: [Descreva o erro que o estudante cometeu]": "1. Common Error: [Describe the error the student made]",
            "2. Correção: [Explique a correção do erro]": "2. Correction: [Explain the correction of the error]",
            "3. Dicas: [Forneça dicas práticas para evitar esse tipo de erro no futuro]": "3. Tips: [Provide practical tips to avoid this type of error in the future]"
        },
        'pt': {
            "Gerador de Avaliações": "Gerador de Avaliações",
            "Selecione as opções para gerar a avaliação": "Selecione as opções para gerar a avaliação",
            "Ano": "Ano",
            "Unidades temáticas": "Unidades temáticas",
            "Objetos de conhecimento": "Objetos de conhecimento",
            "Descreva o contexto para as questões": "Descreva o contexto para as questões",
            "Gerar atividades": "Gerar atividades",
            "Gerando atividades...": "Gerando atividades...",
            "Erro ao gerar resposta": "Erro ao gerar resposta",
            "Erro ao formatar o prompt": "Erro ao formatar o prompt",
            "variable not found": "variável não encontrada",
            "check if all variables are defined correctly": "verifique se todas as variáveis estão definidas corretamente",
            "error in formatting prompt": "erro de formatação do prompt",
            "Sem contexto adicional.": "Sem contexto adicional.",
            "Como um assistente de professor, você deve criar avaliações de alta qualidade que ajudem a promover uma compreensão profunda do conteúdo. Suas respostas devem ser precisas, claras e alinhadas com o contexto fornecido. Utilize formatação Markdown para organizar as perguntas e respostas.": 
            "Como um assistente de professor, você deve criar avaliações de alta qualidade que ajudem a promover uma compreensão profunda do conteúdo. Suas respostas devem ser precisas, claras e alinhadas com o contexto fornecido. Utilize formatação Markdown para organizar as perguntas e respostas.",
            "Tarefa 1 - Geração de Questão de Matemática:": "Tarefa 1 - Geração de Questão de Matemática:",
            "Por favor, gere uma questão de matemática de múltipla escolha para alunos do {ano} ano, focada em {unidade_tematica}, que explore {objeto_conhecimento}. A questão deve incluir uma introdução contextual para ajudar os alunos a entenderem o problema. Proporcione quatro alternativas plausíveis, uma das quais deve ser a resposta correta. Inclua parâmetros variáveis para permitir ajustes na dificuldade da questão. Use a seguinte estrutura:": 
            "Por favor, gere uma questão de matemática de múltipla escolha para alunos do {ano} ano, focada em {unidade_tematica}, que explore {objeto_conhecimento}. A questão deve incluir uma introdução contextual para ajudar os alunos a entenderem o problema. Proporcione quatro alternativas plausíveis, uma das quais deve ser a resposta correta. Inclua parâmetros variáveis para permitir ajustes na dificuldade da questão. Use a seguinte estrutura:",
            "1. Introdução/Contexto: [Forneça um cenário breve e claro relacionado à questão]": "1. Introdução/Contexto: [Forneça um cenário breve e claro relacionado à questão]",
            "2. Enunciado da Questão: [Descreva a questão matemática]": "2. Enunciado da Questão: [Descreva a questão matemática]",
            "3. Alternativas:": "3. Alternativas:",
            "A) [Alternativa 1]": "A) [Alternativa 1]",
            "B) [Alternativa 2]": "B) [Alternativa 2]",
            "C) [Alternativa 3]": "C) [Alternativa 3]",
            "D) [Alternativa 4]": "D) [Alternativa 4]",
            "4. Resposta Correta: [Indique a alternativa correta]": "4. Resposta Correta: [Indique a alternativa correta]",
            "Tarefa 2 - Solução Detalhada:": "Tarefa 2 - Solução Detalhada:",
            "Para a questão gerada anteriormente, forneça uma solução detalhada passo a passo, explicando cada etapa do processo de resolução da questão. Use uma linguagem clara e acessível para estudantes do {ano} ano. Siga a estrutura abaixo:": 
            "Para a questão gerada anteriormente, forneça uma solução detalhada passo a passo, explicando cada etapa do processo de resolução da questão. Use uma linguagem clara e acessível para estudantes do {ano} ano. Siga a estrutura abaixo:",
            "1. Passo 1: [Descrição da primeira etapa]": "1. Passo 1: [Descrição da primeira etapa]",
            "2. Passo 2: [Descrição da segunda etapa]": "2. Passo 2: [Descrição da segunda etapa]",
            "3. Passo 3: [Descrição da terceira etapa, se aplicável]": "3. Passo 3: [Descrição da terceira etapa, se aplicável]",
            "4. Resumo: [Resumo do processo e resultado final]": "4. Resumo: [Resumo do processo e resultado final]",
            "Tarefa 3 - Feedback Personalizado:": "Tarefa 3 - Feedback Personalizado:",
            "Baseado em uma resposta hipotética de um estudante que cometeu um erro comum ao resolver a questão, forneça feedback construtivo. Explique o erro, sua correção e forneça dicas para evitar esse tipo de engano no futuro. Use a seguinte estrutura:": 
            "Baseado em uma resposta hipotética de um estudante que cometeu um erro comum ao resolver a questão, forneça feedback construtivo. Explique o erro, sua correção e forneça dicas para evitar esse tipo de engano no futuro. Use a seguinte estrutura:",
            "1. Erro Comum: [Descreva o erro que o estudante cometeu]": "1. Erro Comum: [Descreva o erro que o estudante cometeu]",
            "2. Correção: [Explique a correção do erro]": "2. Correção: [Explique a correção do erro]",
            "3. Dicas: [Forneça dicas práticas para evitar esse tipo de erro no futuro]": "3. Dicas: [Forneça dicas práticas para evitar esse tipo de erro no futuro]"
        }
    }
    return translations[language].get(text, text)

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
        st.error(translate_text("Erro ao gerar resposta", lang_code) + f": {str(e)}")
        return None

def main():
    try:
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
        os.environ['REPLICATE_API_TOKEN'] = replicate_api
    except KeyError:
        st.error("Replicate API token não encontrado. Adicione o token ao arquivo secrets.toml.")
        return

    language = st.sidebar.selectbox("Language / Idioma", ["Português", "English"])
    lang_code = 'pt' if language == "Português" else 'en'

    # Debug message
    st.write("Language Code:", lang_code)

    st.sidebar.title(translate_text("Gerador de Avaliações", lang_code))
    st.sidebar.subheader(translate_text("Selecione as opções para gerar a avaliação", lang_code))

    options_ano = ['6° ano', '7° ano'] if lang_code == 'pt' else ['6th grade', '7th grade']
    unidades_tematicas = {
        '6° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
        '7° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística']
    } if lang_code == 'pt' else {
        '6th grade': ['Numbers and operations', 'Algebra', 'Geometry', 'Quantities and measures', 'Probability and statistics'],
        '7th grade': ['Numbers and operations', 'Algebra', 'Geometry', 'Quantities and measures', 'Probability and statistics']
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
    } if lang_code == 'pt' else {
        '6th grade-Numbers and operations': ['Addition and subtraction of natural numbers', 'Multiplication and division of natural numbers'],
        '6th grade-Algebra': ['Algebraic expressions', 'First-degree equations'],
        '6th grade-Geometry': ['Plane geometric figures', 'Geometric solids'],
        '6th grade-Quantities and measures': ['Length measurements', 'Mass measurements'],
        '6th grade-Probability and statistics': ['Random experiments', 'Graph reading and interpretation'],
        '7th grade-Numbers and operations': ['Rational numbers', 'Operations with fractions'],
        '7th grade-Algebra': ['Second-degree equations', 'Functions'],
        '7th grade-Geometry': ['Area of plane figures', 'Pythagorean theorem'],
        '7th grade-Quantities and measures': ['Area measurements', 'Volume measurements'],
        '7th grade-Probability and statistics': ['Simple probability', 'Frequency distribution']
    }

    selected_ano = st.sidebar.selectbox(translate_text("Ano", lang_code), options_ano)
    selected_unidades_tematicas = st.sidebar.selectbox(translate_text("Unidades temáticas", lang_code), unidades_tematicas[selected_ano])
    index_objeto_conhecimento = f"{selected_ano}-{selected_unidades_tematicas}"
    selected_objeto_conhecimento = st.sidebar.selectbox(translate_text("Objetos de conhecimento", lang_code), objetos_conhecimento[index_objeto_conhecimento])
    
    contexto = st.sidebar.text_area(translate_text("Descreva o contexto para as questões", lang_code))

    prompt_template_pt = """
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
    """

    prompt_template_en = """
    Task 1 - Generation of Math Question:
    "Please generate a multiple-choice math question for {ano} grade students, focused on {unidade_tematica}, that explores {objeto_conhecimento}. The question should include a contextual introduction to help students understand the problem. Provide four plausible alternatives, one of which should be the correct answer. Include variable parameters to allow adjustments in the difficulty of the question. Use the following structure:

    1. Introduction/Context: [Provide a brief and clear scenario related to the question]
    2. Question Statement: [Describe the math question]
    3. Alternatives:
       A) [Alternative 1]
       B) [Alternative 2]
       C) [Alternative 3]
       D) [Alternative 4]
    4. Correct Answer: [Indicate the correct alternative]"

    Task 2 - Detailed Solution:
    "For the previously generated question, provide a detailed step-by-step solution, explaining each stage of the problem-solving process. Use clear and accessible language for {ano} grade students. Follow the structure below:

    1. Step 1: [Description of the first step]
    2. Step 2: [Description of the second step]
    3. Step 3: [Description of the third step, if applicable]
    4. Summary: [Summary of the process and final result]"

    Task 3 - Personalized Feedback:
    "Based on a hypothetical student's response that made a common error while solving the question, provide constructive feedback. Explain the error, its correction, and give tips to avoid this type of mistake in the future. Use the following structure:

    1. Common Error: [Describe the error the student made]
    2. Correction: [Explain the correction of the error]
    3. Tips: [Provide practical tips to avoid this type of error in the future]"
    """

    prompt_template = prompt_template_pt if lang_code == 'pt' else prompt_template_en

    # Ensure context is not empty to avoid formatting issues
    if not contexto:
        contexto = translate_text("Sem contexto adicional.", lang_code)

    try:
        ane_prompt = prompt_template.format(
            ano=selected_ano,
            unidade_tematica=selected_unidades_tematicas,
            objeto_conhecimento=selected_objeto_conhecimento,
            contexto=contexto
        )
    except KeyError as e:
        st.error(translate_text("Erro ao formatar o prompt", lang_code) + f": {e}. " + translate_text("variable not found", lang_code) + ". " + translate_text("check if all variables are defined correctly", lang_code))
        return
    except ValueError as ve:
        st.error(translate_text("Erro de formatação do prompt", lang_code) + f": {ve}")
        return

    system_prompt_ane = translate_text("""
    Como um assistente de professor, você deve criar avaliações de alta qualidade que ajudem a promover uma compreensão profunda do conteúdo. Suas respostas devem ser precisas, claras e alinhadas com o contexto fornecido. Utilize formatação Markdown para organizar as perguntas e respostas.
    """, lang_code)

    if st.sidebar.button(translate_text("Gerar atividades", lang_code)):
        with st.spinner(translate_text("Gerando atividades...", lang_code)):
            response = generate_llama3_response(ane_prompt, system_prompt_ane)
            if response:
                st.markdown(response)

if __name__ == "__main__":
    main()
