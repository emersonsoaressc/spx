import sqlite3
from datetime import datetime

# Nome do banco de dados
DB_NAME = "helpdesk.db"

def connect_db():
    """ Conecta ao banco de dados SQLite """
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def init_db():
    """ Cria as tabelas do banco de dados se não existirem """
    conn = connect_db()
    cursor = conn.cursor()

    # Tabela de usuários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            cargo TEXT NOT NULL
        )
    """)

    # Tabela de chamados
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

    conn.commit()
    conn.close()

def create_user(nome, email, senha, cargo):
    """ Cadastra um novo usuário no sistema """
    conn = connect_db()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nome, email, senha, cargo) VALUES (?, ?, ?, ?)",
                       (nome, email, senha, cargo))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_user(email, senha):
    """ Retorna um usuário pelo email e senha """
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    user = cursor.fetchone()
    conn.close()

    return user

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
