import streamlit as st
from helpdesk_farmacia.database import get_user_tickets, create_ticket, update_ticket_status
from auth import check_session

def helpdesk_main(option):
    """Função principal do módulo Helpdesk"""
    
    # Verifica se o usuário está logado
    user_data = check_session()

    if not user_data:
        st.error("⚠️ Você precisa estar logado para acessar o Helpdesk.")
        return

    st.title("🛠️ Helpdesk - Suporte e Manutenção")

    if option == "Acompanhar Chamados":
        show_tickets(user_data)

    elif option == "Abrir Novo Chamado":
        open_ticket(user_data)

def show_tickets(user_data):
    """Exibe os chamados do usuário logado"""
    st.subheader("📋 Meus Chamados")

    tickets = get_user_tickets(user_data["id"])

    if not tickets:
        st.info("🔹 Nenhum chamado encontrado.")
        return

    for ticket in tickets:
        st.write(f"🆔 **ID:** {ticket['id']}")
        st.write(f"📌 **Título:** {ticket['titulo']}")
        st.write(f"📅 **Data:** {ticket['data_abertura']}")
        st.write(f"📌 **Status:** `{ticket['status']}`")
        st.write("---")

def open_ticket(user_data):
    """Formulário para abrir novo chamado"""
    st.subheader("🆕 Abrir Novo Chamado")

    with st.form("novo_chamado_form"):
        titulo = st.text_input("Título do chamado")
        descricao = st.text_area("Descreva o problema")
        categoria = st.selectbox("Categoria", ["Infraestrutura", "TI", "Equipamentos", "Outros"])
        submit_button = st.form_submit_button("📩 Enviar Chamado")

        if submit_button and titulo and descricao:
            create_new_ticket(user_data["id"], titulo, descricao, categoria)
            st.success("✅ Chamado aberto com sucesso!")

