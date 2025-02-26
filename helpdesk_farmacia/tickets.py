import streamlit as st
from shopfarma_app.database import create_ticket, get_user_tickets, update_ticket_status
from shopfarma_app.auth import check_session

def create_ticket_interface(user_data):
    """ Interface para abertura de novos chamados """
    st.subheader("🆕 Abrir Novo Chamado")

    with st.form("novo_chamado_form"):
        titulo = st.text_input("📌 Título do Chamado")
        descricao = st.text_area("📝 Descrição Detalhada")
        categoria = st.selectbox("📂 Categoria", ["Infraestrutura", "TI", "Equipamentos", "Outros"])
        urgencia = st.selectbox("⚠️ Nível de Urgência", ["Baixa", "Média", "Alta", "Crítica"])
        
        submit_button = st.form_submit_button("📩 Enviar Chamado")

        if submit_button and titulo and descricao:
            create_ticket(user_data["id"], titulo, descricao, categoria, urgencia)
            st.success("✅ Chamado criado com sucesso!")
            st.experimental_rerun()

def view_tickets_interface(user_data):
    """ Interface para exibir e atualizar chamados """
    st.subheader("📋 Meus Chamados")

    tickets = get_user_tickets(user_data["id"])

    if not tickets:
        st.info("🔹 Nenhum chamado encontrado.")
        return

    for ticket in tickets:
        with st.expander(f"🆔 {ticket['id']} - {ticket['titulo']} ({ticket['status']})", expanded=False):
            st.write(f"📅 **Data:** {ticket['data_abertura']}")
            st.write(f"📂 **Categoria:** {ticket['categoria']}")
            st.write(f"⚠️ **Urgência:** `{ticket['urgencia']}`")
            st.write(f"📝 **Descrição:** {ticket['descricao']}")
            
            # Apenas o CEO, COO e Assistente Financeiro podem mudar status
            if user_data["role"] in ["CEO", "COO", "Assistente Financeiro"]:
                novo_status = st.selectbox("🔄 Atualizar Status", ["Aberto", "Em Análise", "Aguardando Aprovação", "Em Execução", "Concluído"], index=["Aberto", "Em Análise", "Aguardando Aprovação", "Em Execução", "Concluído"].index(ticket['status']))
                
                if st.button(f"✅ Atualizar Status do Chamado {ticket['id']}"):
                    update_ticket_status(ticket["id"], novo_status)
                    st.success(f"✅ Chamado {ticket['id']} atualizado para `{novo_status}`!")
                    st.experimental_rerun()
