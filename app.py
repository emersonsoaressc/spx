import streamlit as st
from compras.compras import layout_compras
from home import home
from estoque import layout_estoque


st.sidebar.image('images/logo_shopfarma_sem_fundo.png')

with st.sidebar.expander('Gestão de estoque avançada', expanded=True):
    gestao_lst = ['Home','Sistema de gestao']
    gestao_selectbox = st.selectbox('',gestao_lst)

if gestao_selectbox == 'Home':
    home()

if gestao_selectbox == 'Dashboard':
    layout_compras()
    
if gestao_selectbox == 'Sistema de compras':
    layout_estoque()