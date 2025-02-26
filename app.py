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
    st.image('images/logo_shopfarma_sem_fundo.png', width=250)
    st.title("🔑 Login")

    # Login
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        user = get_user(email, senha)
        if user:
            st.session_state["user"] = user
            st.experimental_rerun()
        else:
            st.error("⚠️ Usuário não encontrado ou ainda não aprovado pelo COO.")

    # Botão para novo cadastro
    if st.button("Novo Cadastro"):
        st.session_state.current_page = "cadastro"

    # Página de cadastro
    if "current_page" in st.session_state and st.session_state.current_page == "cadastro":
        st.subheader("📋 Novo Cadastro")

        nome = st.text_input("Nome Completo")
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")

        cargo = st.selectbox("Selecione seu Cargo", [
            "Gestor", "CEO", "CFO", "Assistente Financeiro", "Assistente de RH", "Assistente de Estoque"
        ])

        loja = st.selectbox("Selecione sua Loja", ["Loja 1", "Loja 2", "Loja 3", "Loja 4"]) if cargo == "Gestor" else None

        if st.button("Registrar"):
            if nome and email and senha and cargo:
                if create_user(nome, email, senha, cargo, loja):
                    st.success(f"✅ Cadastro enviado! Aguarde aprovação do COO.")
                    st.session_state.current_page = "login"
                else:
                    st.error("⚠️ Este e-mail já está em uso.")
            else:
                st.warning("⚠️ Preencha todos os campos antes de cadastrar.")
