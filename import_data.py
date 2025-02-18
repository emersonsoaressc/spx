import sqlite3
import pandas as pd


# Conectar ao banco de dados
def conectar_banco():
    return sqlite3.connect("vendas.db")


# Função para importar colaboradores
def importar_colaboradores():
    df_colaboradores = pd.read_excel('planilhas/vendas/vendedores/lista_colaboradores.xls', header=8,usecols=('B,C,E'))[0:-2]
    df_colaboradores = df_colaboradores.set_axis(['codigo','colaborador','admissao'], axis=1)
    df_colaboradores['cod_nome_colab'] = df_colaboradores['codigo'].astype(str) + ' - '+ df_colaboradores['colaborador']
    conn = conectar_banco()
    cursor = conn.cursor()

    for _, row in df_colaboradores.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO colaboradores (codigo, colaborador, cod_nome_colab)
            VALUES (?, ?, ?)
        """, (row["codigo"], row["colaborador"], row["cod_nome_colab"]))

    conn.commit()
    conn.close()
    print("📌 Colaboradores importados com sucesso!")


# Função para importar vendas gerais sem duplicação
def importar_vendas():
    df_relacao_vendas = pd.read_excel(
        'planilhas/vendas/vendedores/base_relacao_vendas/relacao_vendas.xls',
        header=10, usecols=('B,E,G,Q,U,AA,AB,AI,AL,AM,AP,AS')
    )

    df_relacao_vendas = df_relacao_vendas.set_axis(
        ['cod_venda', 'filial', 'forma_pagamento', 'data', 'hora', 'cupom', 'cliente',
         'vendedor', 'valor_bruto', '%desconto', 'valor_desconto', 'valor_liquido'], axis=1
    )[0:-3]

    df_relacao_vendas['vendedor'] = df_relacao_vendas['vendedor'].astype(int)
    df_relacao_vendas['cod_venda'] = df_relacao_vendas['cod_venda'].astype(str)
    df_relacao_vendas['cupom'] = df_relacao_vendas['cupom'].astype(str)

    # Converter 'data' e 'hora' para string antes de salvar no banco
    df_relacao_vendas['data'] = df_relacao_vendas['data'].astype(str)
    df_relacao_vendas['hora'] = df_relacao_vendas['hora'].astype(str)

    conn = conectar_banco()
    cursor = conn.cursor()

    # Carregar as vendas existentes para evitar duplicação
    cursor.execute("SELECT cod_venda FROM vendas_vendedores")
    vendas_existentes = set(row[0] for row in cursor.fetchall())

    novas_vendas = []

    for _, row in df_relacao_vendas.iterrows():
        if row["cod_venda"] not in vendas_existentes:
            novas_vendas.append((
                row["cod_venda"], row["filial"], row["forma_pagamento"], row["data"],
                row["hora"], row["cupom"], row["cliente"], row["vendedor"],
                row["valor_bruto"], row["%desconto"], row["valor_desconto"],
                row["valor_liquido"]
            ))

    if novas_vendas:
        cursor.executemany("""
            INSERT INTO vendas_vendedores (cod_venda, filial, forma_pagamento, data, hora, 
                                           cupom, cliente, vendedor, valor_bruto, desconto_percent, 
                                           valor_desconto, valor_liquido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, novas_vendas)

        conn.commit()
        print(f"📌 {len(novas_vendas)} novas vendas gerais foram adicionadas ao banco.")
    else:
        print("✅ Nenhuma nova venda geral foi adicionada. Todos os registros já existem.")

    conn.close()


# Função para processar os arquivos de vendas por grupo
def vendas_grupo(grupo):
    df = pd.read_excel(
        f'planilhas/vendas/vendedores/base_relacao_vendas/vendas_{grupo}.xls',
        header=10, usecols=('B,D,F,T,Z,AF,AM,BC')
    )

    df = df.set_axis(
        ['venda', 'filial', 'pagamento', 'data', 'hora', 'cupom', 'vendedor', 'valor_liquido'],
        axis=1
    )

    df['vendedor'] = df['vendedor'].shift(-1)
    df['valor_liquido'] = df['valor_liquido'].shift(-2)
    df.dropna(inplace=True)

    df['filial'] = df['filial'].astype(int)
    df['cupom'] = df['cupom'].astype(int)
    df['vendedor'] = df['vendedor'].astype(int)

    # Converter 'data' e 'hora' para string antes de salvar no banco
    df['data'] = df['data'].astype(str)
    df['hora'] = df['hora'].astype(str)

    return df


# Função para importar vendas dos grupos sem duplicação e contar corretamente as inserções
def importar_vendas_grupo(df_vendas_grupo, grupo_nome):
    conn = sqlite3.connect("vendas.db")
    cursor = conn.cursor()

    # Filtrar apenas novas vendas que ainda não estão no banco
    vendas_existentes = set(row[0] for row in cursor.execute(f"SELECT cod_venda FROM vendas_{grupo_nome}"))
    novas_vendas = [tuple(row) for _, row in df_vendas_grupo.iterrows() if row["venda"] not in vendas_existentes]

    if novas_vendas:
        cursor.executemany(f"""
            INSERT OR IGNORE INTO vendas_{grupo_nome} 
            (cod_venda, filial, forma_pagamento, data, hora, cupom, vendedor, valor_liquido)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, novas_vendas)
        conn.commit()

        # Verificar quantas inserções realmente ocorreram
        linhas_inseridas = conn.total_changes  # Conta mudanças reais no banco
        if linhas_inseridas > 0:
            print(f"📌 {linhas_inseridas} novas vendas do grupo {grupo_nome} foram adicionadas ao banco.")
        else:
            print(f"✅ Nenhuma nova venda do grupo {grupo_nome} foi adicionada. Todos os registros já existem.")
    else:
        print(f"✅ Nenhuma nova venda do grupo {grupo_nome} foi adicionada. Todos os registros já existem.")

    conn.close()


# Importar colaboradores
importar_colaboradores()
# Importar relação de vendas gerais
importar_vendas()

# Lista de grupos de vendas
grupos = ["genericos", "similares", "csr_gensim", "csr_referencia", "perfumaria"]

# Importar cada grupo de vendas para o banco de dados
for grupo in grupos:
    df_grupo = vendas_grupo(grupo)  # Processa o Excel
    importar_vendas_grupo(df_grupo, grupo)  # Insere no banco sem duplicar

print("🚀 Importação concluída com sucesso!")
