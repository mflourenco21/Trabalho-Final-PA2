'''
DESENVOLVIDO COM AJUDA DO CHATGPT 4.0

'''


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import json

# Configuração da página =================================================================================================================================
st.image(os.path.join(os.getcwd(), "static", "Logo.png"))
st.title("Estatísticas do Jogo")
st.subheader("Aqui podes consultar todos os teus movimentos do jogo")
st.subheader("e alterar os valores dos acontecimentos.")
st.divider()


# JSON DE DADOS DO JOGO====================================================================================================================================
with open("dados_jogo.json", "r", encoding="UTF-8") as file:
    data1 = json.load(file)

st.subheader("Dados do Jogo")
st.write("Abaixo estão os dados do jogo em formato JSON.")
st.write(data1)
st.write("Abaixo estão os dados do jogo em tabela.")
st.dataframe(data1)
st.divider()


# JSON DE ACONTECIMENTOS ==================================================================================================================================
with open("acontecimentos.json", "r", encoding="UTF-8") as file:
    data = json.load(file)

st.subheader("Acontecimentos do Jogo")
st.write("Abaixo estão os acontecimentos do jogo em formato JSON.")

# Função para converter JSON em DataFrame
def json_to_dataframe(data):
    rows = []
    for categoria, eventos in data.items():
        for evento, detalhes in eventos.items():
            rows.append({
                'Categoria': categoria,
                'Evento': evento,
                'Valor': detalhes['valor'],
                'Despesa': detalhes['despesa'],
                'Mensagem': detalhes['mensagem']
            })
    return pd.DataFrame(rows)

# Função para converter DataFrame em JSON
def dataframe_to_json(df):
    data = {}
    for _, row in df.iterrows():
        if row['Categoria'] not in data:
            data[row['Categoria']] = {}
        data[row['Categoria']][row['Evento']] = {
            'valor': row['Valor'],
            'despesa': row['Despesa'],
            'mensagem': row['Mensagem']
        }
    return data

# Função principal
def main():
    if data:
        # Converter para DataFrame
        df = json_to_dataframe(data)

        st.subheader("Dados Atuais")
        st.dataframe(df)

        st.subheader("Editar Dados")

        # Editor de dados interativo
        edited_df = st.data_editor(
            df,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Categoria": st.column_config.TextColumn(
                    "Categoria", width="medium", required=True
                ),
                "Evento": st.column_config.TextColumn(
                    "Evento", width="medium", required=True
                ),
                "Valor": st.column_config.NumberColumn(
                    "Valor (€)", width="small", required=True
                ),
                "Despesa": st.column_config.TextColumn(
                    "Descrição da Despesa", width="large", required=True
                ),
                "Mensagem": st.column_config.TextColumn(
                    "Mensagem Completa", width="large", required=True
                )
            }
        )

    # Botão para salvar os dados editados no JSON
    if st.button("Salvar alterações"):
        novo_json = dataframe_to_json(edited_df)
        with open("acontecimentos.json", "w", encoding="UTF-8") as f:
            json.dump(novo_json, f, ensure_ascii=False, indent=4)
        st.success("Dados salvos com sucesso!")

# Executar a função principal
if __name__ == "__main__":
    main()
