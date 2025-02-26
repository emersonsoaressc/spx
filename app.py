import streamlit as st
from helpdesk_farmacia.auth import login, logout, check_session, approve_users
from compras.compras import layout_compras
from produto_individual import page_produto_individual
from home import home
from colaboradores import colab_individual
from helpdesk_farmacia.app_helpdesk import helpdesk_main

# Configuração da página
st.set_page_config(page_title="Shopfarma - Gestão", layout="wide")

# Verifica se o usuário está logado
user_data = check_session()

if user_data:
    # Exibir logo no topo
    st.image('images/logo_shopfarma_sem_fundo.png', width=200)  
    st.write(f"### 👤 Bem-vindo, {user_data['name']} ({user_data['role']})")
    st.button("🔒 Logout", on_click=logout)

    # Exibir cards clicáveis para selecionar a seção
    st.markdown("## 📌 Escolha uma seção:")

    col1, col2 = st.columns(2)  # Criando layout de 2 colunas

    with col1:
        home_button = st.button("🏠 Home")
        estoque_button = st.button("🛒 Gestão de Estoque")

    with col2:
        colaboradores_button = st.button("👥 Gestão de Colaboradores")
        helpdesk_button = st.button("🛠️ Helpdesk")

    # Controlando a navegação entre as seções
    if home_button:
        st.experimental_set_query_params(page="home")
    elif estoque_button:
        st.experimental_set_query_params(page="estoque")
    elif colaboradores_button:
        st.experimental_set_query_params(page="colaboradores")
    elif helpdesk_button:
        st.experimental_set_query_params(page="helpdesk")

    # Verifica a página atual e exibe o conteúdo correspondente
    query_params = st.experimental_get_query_params()
    current_page = query_params.get("page", ["home"])[0]

    if current_page == "home":
        home()
    elif current_page == "estoque":
        st.title("📦 Gestão de Estoque")
        opcao_estoque = st.selectbox("Selecione uma opção:", ["", "Produto Individual", "Sistema de Compras"])
        if opcao_estoque == "Produto Individual":
            page_produto_individual()
        elif opcao_estoque == "Sistema de Compras":
            layout_compras()
    elif current_page == "colaboradores":
        colab_individual()
    elif current_page == "helpdesk":
        helpdesk_main("Acompanhar Chamados")

else:
    # Tela de login caso o usuário não esteja logado
    st.image('images/logo_shopfarma_sem_fundo.png', width=200)
    st.title("🔑 Login")
    login()
    st.warning("Seu cadastro precisa ser aprovado pelo COO antes do acesso.")
