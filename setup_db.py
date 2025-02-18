import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("vendas.db")
cursor = conn.cursor()

# Criar tabela de colaboradores
cursor.execute("""
CREATE TABLE IF NOT EXISTS colaboradores (
    codigo TEXT PRIMARY KEY UNIQUE NOT NULL,
    colaborador TEXT NOT NULL,
    cod_nome_colab TEXT NOT NULL
);
""")

# Criar tabela de vendas gerais por vendedor
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas_vendedores (
    cod_venda TEXT PRIMARY KEY,  -- Definir como chave primária para evitar duplicação
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

# Criar tabelas separadas para cada grupo de vendas
grupos_vendas = ["genericos", "similares", "csr_gensim", "csr_referencia", "perfumaria"]

for grupo in grupos_vendas:
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS vendas_{grupo} (
        cod_venda TEXT PRIMARY KEY,  -- Definir como chave primária
        filial TEXT NOT NULL,
        forma_pagamento TEXT,
        data DATE NOT NULL,
        hora TEXT,
        cupom TEXT,
        vendedor INTEGER NOT NULL,
        valor_liquido REAL NOT NULL,
        FOREIGN KEY (vendedor) REFERENCES colaboradores(codigo)
    );
    """)

    # Criar índices para otimizar consultas
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_vendas_{grupo}_data ON vendas_{grupo}(data);")

# Criar índices gerais
cursor.execute("CREATE INDEX IF NOT EXISTS idx_vendas_vendedores_data ON vendas_vendedores(data);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_colaboradores_codigo ON colaboradores(codigo);")

# Confirmar mudanças e fechar conexão
conn.commit()
conn.close()

print("🔧 Tabelas criadas/atualizadas com sucesso!")
