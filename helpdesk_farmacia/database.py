import sqlite3
from datetime import datetime

DB_NAME = "helpdesk.db"

def connect_db():
    """ Conecta ao banco de dados SQLite """
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    """ Cria as tabelas do banco de dados se não existirem """
    conn = connect_db()
    cursor = conn.cursor()

    # Criar tabela de usuários com campos "loja" e "whatsapp"
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            cargo TEXT NOT NULL,
            loja TEXT DEFAULT NULL,
            whatsapp TEXT NOT NULL,
            aprovado INTEGER DEFAULT 0  -- 0 = pendente, 1 = aprovado
        )
    """)

    # Criar tabela de chamados
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chamados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            categoria TEXT NOT NULL,
            urgencia TEXT NOT NULL DEFAULT 'Média',
            status TEXT NOT NULL DEFAULT 'Aberto',
            data_abertura TEXT NOT NULL,
            usuario_id INTEGER,
            FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
        )
    """)

    # Criar usuário padrão (COO) se não existir
    cursor.execute("SELECT COUNT(*) FROM usuarios WHERE cargo = 'COO'")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha, cargo, loja, whatsapp, aprovado)
            VALUES ('Admin COO', 'admin@shopfarma.com', 'admin123', 'COO', NULL, '+55 48 99999-9999', 1)
        """)
        conn.commit()
        print("✅ Usuário padrão (COO) criado com sucesso!")

    conn.commit()
    conn.close()

def create_user(nome, email, senha, cargo, loja, whatsapp):
    """ Cadastra um novo usuário como pendente, associado a uma loja se necessário """
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha, cargo, loja, whatsapp, aprovado) VALUES (?, ?, ?, ?, ?, ?, 0)", 
                       (nome, email, senha, cargo, loja, whatsapp))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(email, senha):
    """ Retorna um usuário pelo email e senha, verificando se foi aprovado """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, cargo, loja, whatsapp FROM usuarios WHERE email = ? AND senha = ? AND aprovado = 1", (email, senha))
    user = cursor.fetchone()  # Retorna uma tupla
    
    conn.close()
    
    if user:
        return {
            "id": user[0],
            "name": user[1],
            "email": user[2],
            "role": user[3],
            "loja": user[4],
            "whatsapp": user[5]
        }
    return None  # Retorna None caso o usuário não seja encontrado ou não esteja aprovado

def get_pending_users():
    """ Retorna usuários que ainda não foram aprovados pelo COO """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, cargo, loja, whatsapp FROM usuarios WHERE aprovado = 0")
    users = cursor.fetchall()
    conn.close()

    # Converte os usuários para dicionários
    return [{"id": u[0], "name": u[1], "email": u[2], "role": u[3], "loja": u[4], "whatsapp": u[5]} for u in users]


def approve_user(user_id):
    """ Aprova um usuário pendente """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET aprovado = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def get_all_users():
    """ Retorna todos os usuários cadastrados """
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, cargo, loja, whatsapp, aprovado FROM usuarios")
    users = cursor.fetchall()
    conn.close()
    return users

def create_ticket(usuario_id, titulo, descricao, categoria, urgencia="Média"):
    """ Cria um novo chamado no sistema """
    conn = connect_db()
    cursor = conn.cursor()

    data_abertura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO chamados (titulo, descricao, categoria, urgencia, status, data_abertura, usuario_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (titulo, descricao, categoria, urgencia, "Aberto", data_abertura, usuario_id))

    conn.commit()
    conn.close()

def get_user_tickets(usuario_id):
    """ Retorna os chamados de um usuário """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chamados WHERE usuario_id = ?", (usuario_id,))
    tickets = cursor.fetchall()
    conn.close()

    return [{"id": t[0], "titulo": t[1], "descricao": t[2], "categoria": t[3], "urgencia": t[4], "status": t[5], "data_abertura": t[6]} for t in tickets]

def update_ticket_status(ticket_id, new_status):
    """ Atualiza o status de um chamado """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("UPDATE chamados SET status = ? WHERE id = ?", (new_status, ticket_id))
    conn.commit()
    conn.close()
