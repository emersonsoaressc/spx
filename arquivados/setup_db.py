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

# Criar tabela de vendas gerais por vendedor com CHAVE PRIMÁRIA COMPOSTA (cod_venda + filial)
cursor.execute("""
CREATE TABLE IF NOT EXISTS vendas_vendedores (
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
    PRIMARY KEY (cod_venda, filial),  -- Evita duplicação entre lojas
    FOREIGN KEY (vendedor) REFERENCES colaboradores(codigo)
);
""")

# Criar tabelas separadas para cada grupo de vendas com CHAVE PRIMÁRIA COMPOSTA
grupos_vendas = ["genericos", "similares", "csr_gensim", "csr_referencia", "perfumaria"]

for grupo in grupos_vendas:
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS vendas_{grupo} (
        cod_venda TEXT NOT NULL,
        filial TEXT NOT NULL,
        forma_pagamento TEXT,
        data DATE NOT NULL,
        hora TEXT,
        cupom TEXT,
        vendedor INTEGER NOT NULL,
        valor_liquido REAL NOT NULL,
        PRIMARY KEY (cod_venda, filial),  -- Chave composta evita duplicação entre lojas
        FOREIGN KEY (vendedor) REFERENCES colaboradores(codigo)
    );
    """)

    # Criar índices para otimizar consultas
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_vendas_{grupo}_data ON vendas_{grupo}(data);")

# Criar índices gerais para acelerar buscas
cursor.execute("CREATE INDEX IF NOT EXISTS idx_vendas_vendedores_data ON vendas_vendedores(data);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_vendas_vendedores_filial ON vendas_vendedores(filial);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_vendas_vendedores_cupom ON vendas_vendedores(cupom);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_colaboradores_codigo ON colaboradores(codigo);")

# Confirmar mudanças e fechar conexão
conn.commit()
conn.close()

print("🔧 Banco de dados recriado com sucesso!")
