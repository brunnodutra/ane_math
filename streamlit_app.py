import streamlit as st
import replicate
import os

st.set_page_config(page_title="Nova Escola - Gerador de Avaliações de Matemática")

def generate_llama3_response(prompt_input, system_prompt_ane):
    output = replicate.run("meta/meta-llama-3-70b-instruct", 
                           input={ "prompt": prompt_input,
                                  "temperature": 0.1, "top_p": 1,
                                  "debug": False,
                                  "system_prompt": system_prompt_ane + "You are a helpful, respectful and honest assistant focused on creating high-quality math assessments. Always provide accurate and pedagogically sound questions. Ensure that your responses are safe and unbiased.\\\\n\\\\nIf a question does not make sense or is not factually coherent, explain why instead of providing incorrect information. If you don't know the answer to a question, please don't share false information.",
                                  "max_new_tokens": 500,
                                  "min_new_tokens": 100,
                                  "prompt_template": "[INST] <<SYS>>\\\\n{system_prompt}\\\\n<</SYS>>\\\\n\\\\n{prompt} [/INST]",
                                  "repetition_penalty": 1.15
                                  })      
    full_response = ''
    for item in output:
        full_response += item
                  
    return full_response

def main():
    replicate_api = st.secrets['REPLICATE_API_TOKEN']
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    
    custom_css = """
      <style>
          /* Style for the sidebar header */
          .sidebar-header {
              background-color: #E32458; /* Red background color */
              color: white; /* White text color */
              padding: 20px; /* Add padding */
              text-align: center; /* Center the text */
          }
          .sidebar .sidebar-content {
              padding: 20px; /* Add padding to the sidebar content */
          }
      </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    st.sidebar.markdown("<h1 class='sidebar-header'>Gerador de Avaliações</h1>", unsafe_allow_html=True)
    
    st.sidebar.markdown("## Selecione as opções para gerar a avaliação")
    
    options_ano = ['6° ano', '7° ano', '8° ano', '9° ano']
    unidades_tematicas = {
        '6° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
        '7° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
        '8° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
        '9° ano': ['Números e operações', 'Álgebra', 'Geometria', 'Grandezas e medidas', 'Probabilidade e estatística'],
    }

    link_planos_aula = {
        '6° ano': ['https://novaescola.org.br/planos-de-aula/fundamental/6ano'],
        '7° ano': ['https://novaescola.org.br/planos-de-aula/fundamental/7ano'],
        '8° ano': ['https://novaescola.org.br/planos-de-aula/fundamental/8ano'],
        '9° ano': ['https://novaescola.org.br/planos-de-aula/fundamental/9ano'],
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
    selected_link_planos_aula = link_planos_aula[selected_ano]
    index_objeto_conhecimento = f"{selected_ano}-{selected_unidades_tematicas}"
    selected_objeto_conhecimento = st.sidebar.selectbox("Objetos de conhecimento", objetos_conhecimento[index_objeto_conhecimento])
    
    ane_prompt = f'Gerar 10 questões de múltipla escolha para o {selected_ano} com a Unidade temática {selected_unidades_tematicas} e objeto de conhecimento {selected_objeto_conhecimento}. Gerar toda a resposta em português BR.'

    system_prompt_ane = f"Como um assistente do professor de escola pública brasileira, gera uma atividade com 10 questões de múltipla escolha e indique a alternativa correta. As questões devem ser para o {selected_ano} do ensino fundamental sobre a unidade temática {selected_unidades_tematicas} com o objeto de conhecimento {selected_objeto_conhecimento}. Use como base de conhecimento os planos de aula de matemática da Nova Escola e indique no final da resposta ao menos 3 planos de aula do tema, se possível com link para o site da Nova Escola: {selected_link_planos_aula}"

    if st.sidebar.button('Gerar atividades'):
        with st.spinner("Gerando atividades..."):
            response = generate_llama3_response(ane_prompt, system_prompt_ane)
            st.text(response)

if __name__ == "__main__":
    main()
