import streamlit as st
import sqlite3
from helpdesk_farmacia.database import create_user, get_user


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

def register_user():
    """ Tela de cadastro de novo usuário """
    st.subheader("📝 Cadastro")

    nome = st.text_input("Nome Completo")
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    cargo = st.selectbox("Cargo", ["Gestor", "CEO", "COO", "CFO", "Assistente Financeiro"])

    if st.button("Cadastrar"):
        if nome and email and senha:
            sucesso = create_user(nome, email, senha, cargo)
            if sucesso:
                st.success("✅ Usuário cadastrado com sucesso!")
            else:
                st.error("❌ Este e-mail já está cadastrado!")
        else:
            st.error("⚠️ Todos os campos são obrigatórios!")
