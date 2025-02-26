import streamlit as st
from helpdesk_farmacia.database import get_pending_users

def show(user_data):
    st.image('images/logo_shopfarma_sem_fundo.png', width=250)
    st.markdown(f"<h3 style='text-align: center;'>👤 Bem-vindo, {user_data['name']} ({user_data['role']})</h3>", unsafe_allow_html=True)

    # Verifica quantos cadastros estão pendentes
    pending_users = get_pending_users()
    num_pendentes = len(pending_users)

    # Layout dos cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)

    with col1:
        if user_data["role"] in ["COO", "Gestor Estoque"]:
            if st.button("🛒 Gestão de Estoque"):
                st.session_state["current_page"] = "estoque"
                st.experimental_rerun()

    with col2:
        if user_data["role"] in ["COO", "Assistente de RH"]:
            if st.button("👥 Gestão de Colaboradores"):
                st.session_state["current_page"] = "colaboradores"
                st.experimental_rerun()

    with col3:
        if st.button("🛠️ Helpdesk"):
            st.session_state["current_page"] = "helpdesk"
            st.experimental_rerun()

    with col4:
        if st.button("🔒 Logout"):
            st.session_state.clear()
            st.experimental_rerun()

    with col5:
        if user_data["role"] == "COO":
            if num_pendentes > 0:
                if st.button(f"✅ Aprovar Cadastros ({num_pendentes})"):
                    st.session_state["current_page"] = "aprovar_usuarios"
                    st.experimental_rerun()
            else:
                st.button("✅ Aprovar Cadastros (0)", disabled=True)

    with col6:
        if user_data["role"] == "COO":
            if st.button("✏️ Editar Usuários"):
                st.session_state["current_page"] = "editar_usuarios"
                st.experimental_rerun()
