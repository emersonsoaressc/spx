import streamlit as st
from compras.compras import layout_compras
from produto_individual import page_produto_individual
from home import home
from colaboradores import colab_individual
from helpdesk_farmacia.app_helpdesk import helpdesk_main

# Configuração da página
st.set_page_config(page_title="Shopfarma - Gestão", layout="wide")

# Sidebar - Logo e Menu
st.sidebar.image('images/logo_shopfarma_sem_fundo.png', use_column_width=True)
st.sidebar.markdown("### 📊 Painel de Gestão")

# Criando um menu principal com botões estilizados
menu_principal = st.sidebar.radio(
    "Escolha uma seção:", 
    ["🏠 Home", "🛒 Gestão de Estoque", "👥 Gestão de Colaboradores", "🛠️ Helpdesk"],
)

st.sidebar.markdown("---")

# Exibição do conteúdo conforme a opção escolhida
if menu_principal == "🏠 Home":
    st.title("📌 Bem-vindo ao Painel Shopfarma")
    st.write("Aqui você pode gerenciar colaboradores, estoque e chamados de manutenção.")

    # Criando métricas importantes (caso aplicável)
    col1, col2, col3 = st.columns(3)
    col1.metric(label="💰 Vendas Mensais", value="R$ 120.000", delta="+5%")
    col2.metric(label="📦 Produtos em Estoque", value="8.500", delta="-2%")
    col3.metric(label="📋 Chamados Pendentes", value="12", delta="+3")

elif menu_principal == "🛒 Gestão de Estoque":
    st.title("📦 Gestão de Estoque Avançada")
    opcao_estoque = st.selectbox("Selecione uma opção:", ["", "Produto Individual", "Sistema de Compras"])

    if opcao_estoque == "Produto Individual":
        page_produto_individual()
    elif opcao_estoque == "Sistema de Compras":
        layout_compras()

elif menu_principal == "👥 Gestão de Colaboradores":
    st.title("👥 Gestão de Colaboradores")
    opcao_colab = st.selectbox("Selecione uma opção:", ["", "Dashboard Geral", "Avaliação Individual"])

    if opcao_colab == "Dashboard Geral":
        st.write("Aqui ficará o dashboard de colaboradores.")
    elif opcao_colab == "Avaliação Individual":
        colab_individual()

elif menu_principal == "🛠️ Helpdesk":
    st.title("🛠️ Helpdesk - Suporte e Manutenção")
    helpdesk_option = st.selectbox("Selecione uma opção:", ["", "Acompanhar Chamados", "Abrir Novo Chamado"])

    if helpdesk_option in ["Acompanhar Chamados", "Abrir Novo Chamado"]:
        helpdesk_main(helpdesk_option)
