import streamlit as st
from compras.compras import layout_compras
from home import home


st.sidebar.image('images/logo_shopfarma_sem_fundo.png')

with st.sidebar.expander('Gestão de estoque avançada', expanded=True):
    gestao_lst = ['Home','Sistema de compras']
    gestao_selectbox = st.selectbox('',gestao_lst)

if gestao_selectbox == 'Home':
    home()

if gestao_selectbox == 'Dashboard':
    pass
    
if gestao_selectbox == 'Sistema de compras':
    layout_compras()