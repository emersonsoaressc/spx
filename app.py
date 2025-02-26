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
    st.image('images/logo_shopfarma_sem_fundo.png', width=250)  
    st.markdown(f"<h3 style='text-align: center;'>👤 Bem-vindo, {user_data['name']} ({user_data['role']})</h3>", unsafe_allow_html=True)

    # Criar sessão de navegação
    if "current_page" not in st.session_state:
        st.session_state.current_page = "helpdesk"  # Padrão: Helpdesk

    # Estilo dos botões como cards
    button_style = """
        <style>
            .stButton>button {
                width: 100%;
                height: 100px;
                font-size: 20px;
                font-weight: bold;
                border-radius: 12px;
                background-color: #f8f9fa;
                color: #333;
                border: 2px solid #ddd;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .stButton>button:hover {
                transform: scale(1.05);
                box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            }
        </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)

    # Criando os botões clicáveis (disfarçados de cards)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if user_data["role"] == "COO":
            if st.button("🛒 Gestão de Estoque"):
                st.session_state.current_page = "estoque"

    with col2:
        if user_data["role"] == "COO":
            if st.button("👥 Gestão de Colaboradores"):
                st.session_state.current_page = "colaboradores"

    with col3:
        if st.button("🛠️ Helpdesk"):
            st.session_state.current_page = "helpdesk"

    with col4:
        if st.button("🔒 Logout"):
            logout()

    # Exibe o conteúdo da página atual
    if st.session_state.current_page == "estoque":
        st.title("📦 Gestão de Estoque")
        opcao_estoque = st.selectbox("Selecione uma opção:", ["", "Produto Individual", "Sistema de Compras"])
        if opcao_estoque == "Produto Individual":
            page_produto_individual()
        elif opcao_estoque == "Sistema de Compras":
            layout_compras()
    elif st.session_state.current_page == "colaboradores":
        colab_individual()
    elif st.session_state.current_page == "helpdesk":
        helpdesk_main("Acompanhar Chamados")

else:
    # Tela de login caso o usuário não esteja logado
    st.image('images/logo_shopfarma_sem_fundo.png', width=250)
    st.title("🔑 Login")
    login()
    st.warning("Seu cadastro precisa ser aprovado pelo COO antes do acesso.")
