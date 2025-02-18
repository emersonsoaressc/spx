import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("vendas.db")
cursor = conn.cursor()

# Lista de tabelas a serem limpas
tabelas = [
    "vendas_csr_gensim",
    "vendas_csr_referencia",
    "vendas_genericos",
    "vendas_perfumaria",
    "vendas_similares",
    "vendas_vendedores"
]

# Excluir todos os dados das tabelas
for tabela in tabelas:
    cursor.execute(f"DELETE FROM {tabela}")
    print(f"Dados da tabela {tabela} excluídos com sucesso!")

# Confirmar a exclusão
conn.commit()
conn.close()

print("Todas as tabelas foram limpas com sucesso!")
