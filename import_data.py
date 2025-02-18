import sqlite3
import pandas as pd

# Função para inserir os colaboradores no banco
def importar_colaboradores(df_colaboradores):
    conn = sqlite3.connect("vendas.db")
    cursor = conn.cursor()

    for _, row in df_colaboradores.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO colaboradores (codigo, colaborador, admissao, cod_nome_colab)
            VALUES (?, ?, ?, ?)
        """, (row["codigo"], row["colaborador"], row["admissao"], row["cod_nome_colab"]))
    
    conn.commit()
    conn.close()
    print("Colaboradores importados com sucesso!")

# Função para inserir as vendas no banco
def importar_vendas(df_vendas):
    conn = sqlite3.connect("vendas.db")
    cursor = conn.cursor()

    for _, row in df_vendas.iterrows():
        cursor.execute("""
            INSERT INTO vendas_vendedores (cod_venda, filial, forma_pagamento, data, hora, cupom, cliente, vendedor, valor_bruto, desconto_percent, valor_desconto, valor_liquido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["cod_venda"], row["filial"], row["forma_pagamento"], row["data"], row["hora"],
            row["cupom"], row["cliente"], row["vendedor"], row["valor_bruto"],
            row["%desconto"], row["valor_desconto"], row["valor_liquido"]
        ))

    conn.commit()
    conn.close()
    print("Vendas importadas com sucesso!")

# Exemplo de uso
if __name__ == "__main__":
    # Carregar os arquivos Excel e converter para DataFrames
    df_colaboradores = pd.read_excel("planilhas/vendas/vendedores/lista_colaboradores.xls", header=8, usecols=("B,C,E"))[0:-2]
    df_colaboradores = df_colaboradores.set_axis(["codigo", "colaborador", "admissao"], axis=1)
    df_colaboradores["cod_nome_colab"] = df_colaboradores["codigo"].astype(str) + " - " + df_colaboradores["colaborador"]

    df_relacao_vendas = pd.read_excel("planilhas/vendas/vendedores/relacao_vendas.xls", header=10, usecols=("B,E,G,Q,U,AA,AB,AI,AL,AM,AP,AS"))
    df_relacao_vendas = df_relacao_vendas.set_axis(["cod_venda", "filial", "forma_pagamento", "data", "hora", "cupom", "cliente", "vendedor", "valor_bruto", "%desconto", "valor_desconto", "valor_liquido"], axis=1)[0:-3]

    df_relacao_vendas["vendedor"] = df_relacao_vendas["vendedor"].astype(int)
    df_relacao_vendas["cod_venda"] = df_relacao_vendas["cod_venda"].astype(str)
    df_relacao_vendas["cupom"] = df_relacao_vendas["cupom"].astype(str)

    # Importar dados para o banco de dados
    importar_colaboradores(df_colaboradores)
    importar_vendas(df_relacao_vendas)
