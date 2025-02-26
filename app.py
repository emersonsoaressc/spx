import streamlit as st
from helpdesk_farmacia.auth import login, logout, check_session, approve_users
from compras.compras import layout_compras
from produto_individual import page_produto_individual
from home import home
from colaboradores import colab_individual
from helpdesk_farmacia.app_helpdesk import helpdesk_main

from helpdesk_farmacia.database import init_db

# Inicializa o banco de dados (caso ainda não exista)
init_db()

# Configuração da página
st.set_page_config(page_title="Shopfarma - Gestão", layout="wide")

# Verifica se o usuário está logado
user_data = check_session()

if user_data:
    # Se logado, mostra o menu e dashboard
    st.sidebar.image('images/logo_shopfarma_sem_fundo.png', use_column_width=True)  # 🔹 Corrigindo o logo!
    st.sidebar.markdown(f"### 👤 Bem-vindo, {user_data['name']} ({user_data['role']})")
    st.sidebar.button("🔒 Logout", on_click=logout)

    # Se for COO, exibe opção para aprovar usuários
    if user_data["role"] == "COO":
        with st.sidebar.expander("⚡ Aprovar Usuários"):
            approve_users()

    # Criando menu principal
    menu_principal = st.sidebar.radio(
        "📌 Escolha uma seção:", 
        ["🏠 Home", "🛒 Gestão de Estoque", "👥 Gestão de Colaboradores", "🛠️ Helpdesk"]
    )

    st.sidebar.markdown("---")  # Linha divisória

    # Exibição do conteúdo conforme a opção escolhida
    if menu_principal == "🏠 Home":
        st.title("📌 Painel Shopfarma")
        st.write("Gerencie colaboradores, estoque e chamados de manutenção.")

        col1, col2, col3 = st.columns(3)
        col1.metric(label="💰 Vendas Mensais", value="R$ 120.000", delta="+5%")
        col2.metric(label="📦 Produtos em Estoque", value="8.500", delta="-2%")
        col3.metric(label="📋 Chamados Pendentes", value="12", delta="+3")

    elif menu_principal == "🛒 Gestão de Estoque":
        st.title("📦 Gestão de Estoque")
        opcao_estoque = st.sidebar.selectbox("Selecione uma opção:", ["", "Produto Individual", "Sistema de Compras"])

        if opcao_estoque == "Produto Individual":
            page_produto_individual()
        elif opcao_estoque == "Sistema de Compras":
            layout_compras()

    elif menu_principal == "👥 Gestão de Colaboradores":
        st.title("👥 Gestão de Colaboradores")
        opcao_colab = st.sidebar.selectbox("Selecione uma opção:", ["", "Dashboard Geral", "Avaliação Individual"])

        if opcao_colab == "Dashboard Geral":
            st.write("Aqui ficará o dashboard de colaboradores.")
        elif opcao_colab == "Avaliação Individual":
            colab_individual()

    elif menu_principal == "🛠️ Helpdesk":
        st.title("🛠️ Helpdesk - Suporte e Manutenção")
        opcao_helpdesk = st.sidebar.selectbox("Selecione uma opção:", ["", "Acompanhar Chamados", "Abrir Novo Chamado"])

        if opcao_helpdesk in ["Acompanhar Chamados", "Abrir Novo Chamado"]:
            helpdesk_main(opcao_helpdesk)

else:
    # Se não estiver logado, mostra apenas o login
    st.sidebar.image('images/logo_shopfarma_sem_fundo.png', use_column_width=True)  # 🔹 Corrigindo o logo na tela de login
    st.sidebar.title("🔑 Login")
    login()
    st.sidebar.markdown("---")
    st.sidebar.subheader("Cadastro restrito")
    st.sidebar.write("O COO precisa aprovar seu cadastro antes de você acessar o sistema.")
