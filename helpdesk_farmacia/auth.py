import streamlit as st
import sqlite3
from helpdesk_farmacia.database import create_user, get_user, get_pending_users, approve_user

# Simples sistema de sessão
def check_session():
    """ Verifica se o usuário está logado """
    if "user" in st.session_state:
        return st.session_state["user"]
    return None

def login():
    """ Tela de login do sistema """
    st.subheader("🔑 Login")

    email = st.text_input("📧 E-mail")
    senha = st.text_input("🔒 Senha", type="password")

    if st.button("Entrar"):
        user = get_user(email, senha)
        if user:
            if user[5] == 0:  # Verifica se está aprovado (0 = pendente, 1 = aprovado)
                st.error("⚠️ Seu cadastro ainda não foi aprovado pelo COO.")
                return
            st.session_state["user"] = {
                "id": user[0],
                "name": user[1],
                "email": user[2],
                "role": user[4]
            }
            st.success(f"✅ Bem-vindo, {user[1]}!")
            st.experimental_rerun()
        else:
            st.error("❌ E-mail ou senha incorretos!")

def logout():
    """ Desloga o usuário """
    st.session_state.pop("user", None)
    st.experimental_rerun()

def approve_users():
    """ COO aprova usuários pendentes """
    st.subheader("👤 Aprovar Usuários Pendentes")

    pending_users = get_pending_users()
    
    if not pending_users:
        st.info("🔹 Nenhum usuário pendente.")
        return
    
    for user in pending_users:
        col1, col2 = st.columns([3,1])
        col1.write(f"📌 {user[1]} ({user[2]}) - Cargo: {user[4]}")
        if col2.button(f"✅ Aprovar {user[1]}", key=user[0]):
            approve_user(user[0])
            st.success(f"✅ Usuário {user[1]} aprovado!")
            st.experimental_rerun()
