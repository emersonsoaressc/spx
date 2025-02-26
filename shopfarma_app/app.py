import streamlit as st
from auth import check_session, logout
from pages import login, dashboard, helpdesk, estoque, colaboradores, aprovar_usuarios, editar_usuarios

st.set_page_config(page_title="Shopfarma - Gestão", layout="wide")

# Verifica se o usuário está logado
user_data = check_session()

if not user_data:
    login.show()
else:
    page = st.session_state.get("current_page", "dashboard")

    if page == "dashboard":
        dashboard.show(user_data)
    elif page == "helpdesk":
        helpdesk.show()
    elif page == "estoque":
        estoque.show()
    elif page == "colaboradores":
        colaboradores.show()
    elif page == "aprovar_usuarios":
        aprovar_usuarios.show()
    elif page == "editar_usuarios":
        editar_usuarios.show()
