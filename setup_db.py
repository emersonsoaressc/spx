import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("vendas.db")
cursor = conn.cursor()

# Criar tabela de colaboradores
cursor.execute("""
CREATE TABLE IF NOT EXISTS colaboradores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo INTEGER UNIQUE NOT NULL,
    colaborador TEXT NOT NULL,
    admissao DATE NOT NULL,
    cod_nome_colab TEXT NOT NULL
);
""")

# Criar tabela de vendas por vendedor
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas_vendedores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cod_venda TEXT NOT NULL,
    filial TEXT NOT NULL,
    forma_pagamento TEXT,
    data DATE NOT NULL,
    hora TEXT,
    cupom TEXT,
    cliente TEXT,
    vendedor INTEGER NOT NULL,
    valor_bruto REAL NOT NULL,
    desconto_percent REAL,
    valor_desconto REAL,
    valor_liquido REAL NOT NULL,
    FOREIGN KEY (vendedor) REFERENCES colaboradores(codigo)
);
""")

# Criar índices para melhorar performance nas consultas
cursor.execute("CREATE INDEX IF NOT EXISTS idx_vendas_vendedores_data ON vendas_vendedores(data);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_colaboradores_codigo ON colaboradores(codigo);")

# Confirmar mudanças e fechar conexão
conn.commit()
conn.close()

print("Tabelas criadas/atualizadas com sucesso!")
