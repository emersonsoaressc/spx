import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("vendas.db")
cursor = conn.cursor()

# Função para corrigir valores numéricos no banco
def corrigir_valores(tabela):
    print(f"🔄 Corrigindo valores na tabela {tabela}...")

    # Selecionar os valores errados
    cursor.execute(f"SELECT cod_venda, valor_liquido FROM {tabela}")
    registros = cursor.fetchall()

    # Processar e corrigir os valores
    for cod_venda, valor in registros:
        if isinstance(valor, str):  # Se estiver no formato de string, converter
            valor_corrigido = float(valor.replace(",", "."))
            cursor.execute(f"UPDATE {tabela} SET valor_liquido = ? WHERE cod_venda = ?", (valor_corrigido, cod_venda))

    conn.commit()
    print(f"✅ Valores corrigidos na tabela {tabela}")

# Lista das tabelas a serem corrigidas
tabelas = ["vendas_vendedores", "vendas_genericos", "vendas_similares", "vendas_csr_gensim", "vendas_csr_referencia", "vendas_perfumaria"]

# Aplicar a correção em todas as tabelas
for tabela in tabelas:
    corrigir_valores(tabela)

# Fechar conexão
conn.close()
print("🚀 Correção concluída com sucesso!")
