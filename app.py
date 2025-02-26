import streamlit as st
from auth import login, logout, check_session, approve_users
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
    
    # Botão de logout no topo
    st.markdown("<div style='text-align: right;'>", unsafe_allow_html=True)
    if st.button("🔒 Logout"):
        logout()
    st.markdown("</div>", unsafe_allow_html=True)

    # Exibir cards estilizados para selecionar a seção
    st.markdown("## 📌 Escolha uma seção:")

    # Definição do estilo dos cards usando CSS inline
    card_style = """
        <style>
            .card {
                background-color: #f8f9fa;
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                transition: transform 0.2s, box-shadow 0.2s;
                cursor: pointer;
                font-size: 20px;
                font-weight: bold;
                color: #333;
                border: 2px solid #ddd;
            }
            .card:hover {
                transform: scale(1.05);
                box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
            }
            .icon {
                font-size: 50px;
                display: block;
            }
        </style>
    """

    st.markdown(card_style, unsafe_allow_html=True)

    # Criando os cards clicáveis
    col1, col2 = st.columns(2)

    with col1:
        home_card = st.markdown("<div class='card' id='home'>🏠<br>Home</div>", unsafe_allow_html=True)
        estoque_card = st.markdown("<div class='card' id='estoque'>🛒<br>Gestão de Estoque</div>", unsafe_allow_html=True)

    with col2:
        colaboradores_card = st.markdown("<div class='card' id='colaboradores'>👥<br>Gestão de Colaboradores</div>", unsafe_allow_html=True)
        helpdesk_card = st.markdown("<div class='card' id='helpdesk'>🛠️<br>Helpdesk</div>", unsafe_allow_html=True)

    # Captura do clique nos cards
    query_params = st.experimental_get_query_params()
    current_page = query_params.get("page", ["home"])[0]

    if st.button("🏠 Home"):
        st.experimental_set_query_params(page="home")
    elif st.button("🛒 Gestão de Estoque"):
        st.experimental_set_query_params(page="estoque")
    elif st.button("👥 Gestão de Colaboradores"):
        st.experimental_set_query_params(page="colaboradores")
    elif st.button("🛠️ Helpdesk"):
        st.experimental_set_query_params(page="helpdesk")

    # Exibe o conteúdo da página atual
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
    st.image('images/logo_shopfarma_sem_fundo.png', width=250)
    st.title("🔑 Login")
    login()
    st.warning("Seu cadastro precisa ser aprovado pelo COO antes do acesso.")
