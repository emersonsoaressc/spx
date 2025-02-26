import streamlit as st
from helpdesk_farmacia.database import create_user, get_user

def show():
    if "show_register" not in st.session_state:
        st.session_state.show_register = False

    st.image('images/logo_shopfarma_sem_fundo.png', width=250)

    if not st.session_state.show_register:
        st.title("🔑 Login")

        email_login = st.text_input("E-mail para Login")
        senha_login = st.text_input("Senha para Login", type="password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Cadastre-se"):
                st.session_state.show_register = True
                st.experimental_rerun()
        with col2:
            if st.button("Entrar"):
                user = get_user(email_login, senha_login)
                if user:
                    st.session_state["user"] = user
                    st.session_state["current_page"] = "dashboard"
                    st.experimental_rerun()
                else:
                    st.error("⚠️ Usuário não encontrado ou ainda não aprovado pelo COO.")
    else:
        st.title("📋 Novo Cadastro")

        nome = st.text_input("Nome Completo")
        email_cadastro = st.text_input("E-mail para Cadastro")
        senha_cadastro = st.text_input("Senha para Cadastro", type="password")
        whatsapp = st.text_input("Número do WhatsApp", placeholder="Ex: +5548999999999")

        cargo = st.selectbox("Selecione seu Cargo", [
            "Proprietário (CEO – Chief Executive Officer)",
            "Diretor de Operações (COO – Chief Operating Officer)",
            "Diretor Comercial (CCO – Chief Commercial Officer)",
            "Diretor Financeiro (CFO – Chief Financial Officer)",
            "Diretor de Compras",
            "Diretor de Auditoria e Compliance (CAO – Chief Audit Officer)",
            "Líder de Loja",
            "Assistente Financeiro",
            "Assistente de RH",
            "Assistente de Estoque e Suprimentos",
            "Fiscal de Auditoria e Compliance",
            "Analista de Marketing",
        ])

        loja = st.selectbox("Selecione sua Loja", [
            "001 - Matriz",
            "004 - Centrinho",
            "005 - Calil",
            "007 - Rio vermelho",
            "008 - Vargem Grande",
            "009 - Canasvieiras",
            "010 - UPA Norte",
            "011 - Trindade",
            "012 - Palhoça"
        ]) if cargo == "Líder de Loja" else None

        if st.button("Registrar"):
            if nome and email_cadastro and senha_cadastro and whatsapp and cargo:
                if create_user(nome, email_cadastro, senha_cadastro, cargo, loja, whatsapp):
                    st.success("✅ Cadastro enviado! Aguarde aprovação do COO.")
                    st.session_state.show_register = False
                    st.experimental_rerun()
                else:
                    st.error("⚠️ Este e-mail já está em uso.")
            else:
                st.warning("⚠️ Preencha todos os campos antes de cadastrar.")

        if st.button("Voltar ao Login"):
            st.session_state.show_register = False
            st.experimental_rerun()
