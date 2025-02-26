import streamlit as st
from database import create_user, get_user, get_pending_users, approve_user
from helpdesk_farmacia.auth import check_session, logout

# Configuração da página
st.set_page_config(page_title="Shopfarma - Gestão", layout="wide")

# Verifica se o usuário já está logado
user_data = check_session()

if user_data:
    st.image('images/logo_shopfarma_sem_fundo.png', width=250)
    st.markdown(f"<h3 style='text-align: center;'>👤 Bem-vindo, {user_data['name']} ({user_data['role']})</h3>", unsafe_allow_html=True)

    # Layout dos cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if user_data["role"] in ["COO", "Gestor Estoque"]:
            if st.button("🛒 Gestão de Estoque"):
                st.session_state.current_page = "estoque"

    with col2:
        if user_data["role"] in ["COO", "Assistente de RH"]:
            if st.button("👥 Gestão de Colaboradores"):
                st.session_state.current_page = "colaboradores"

    with col3:
        if st.button("🛠️ Helpdesk"):
            st.session_state.current_page = "helpdesk"

    with col4:
        if st.button("🔒 Logout"):
            logout()

    # Controle de navegação
    if "current_page" not in st.session_state:
        st.session_state.current_page = "helpdesk"

    if st.session_state.current_page == "estoque":
        st.title("📦 Gestão de Estoque")
    elif st.session_state.current_page == "colaboradores":
        st.title("👥 Gestão de Colaboradores")
    elif st.session_state.current_page == "helpdesk":
        st.title("🛠️ Helpdesk")

else:
    # Verifica se o usuário quer se cadastrar
    if "show_register" not in st.session_state:
        st.session_state.show_register = False

    st.image('images/logo_shopfarma_sem_fundo.png', width=250)

    if not st.session_state.show_register:
        st.title("🔑 Login")

        email_login = st.text_input("E-mail para Login")
        senha_login = st.text_input("Senha para Login", type="password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Entrar"):
                user = get_user(email_login, senha_login)
                if user:
                    st.session_state["user"] = user
                    st.experimental_rerun()
                else:
                    st.error("⚠️ Usuário não encontrado ou ainda não aprovado pelo COO.")
        with col2:
            if st.button("Cadastre-se"):
                st.session_state.show_register = True
                st.experimental_rerun()

    else:
        st.title("📋 Novo Cadastro")

        nome = st.text_input("Nome Completo")
        email_cadastro = st.text_input("E-mail para Cadastro")
        senha_cadastro = st.text_input("Senha para Cadastro", type="password")

        cargo = st.selectbox("Selecione seu Cargo", [
            "Gestor", "CEO", "CFO", "Assistente Financeiro", "Assistente de RH", "Assistente de Estoque"
        ])

        loja = st.selectbox("Selecione sua Loja", ["Loja 1", "Loja 2", "Loja 3", "Loja 4"]) if cargo == "Gestor" else None

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Registrar"):
                if nome and email_cadastro and senha_cadastro and cargo:
                    if create_user(nome, email_cadastro, senha_cadastro, cargo, loja):
                        st.success(f"✅ Cadastro enviado! Aguarde aprovação do COO.")
                        st.session_state.show_register = False
                        st.experimental_rerun()
                    else:
                        st.error("⚠️ Este e-mail já está em uso.")
                else:
                    st.warning("⚠️ Preencha todos os campos antes de cadastrar.")

        with col2:
            if st.button("Voltar ao Login"):
                st.session_state.show_register = False
                st.experimental_rerun()
