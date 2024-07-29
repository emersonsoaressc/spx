import streamlit as st
from compras import layout_compras
from home import home
from estoque import layout_estoque


st.sidebar.image('images/logo_shopfarma_sem_fundo.png')

with st.sidebar.expander('Sistema de Compras', expanded=True):
    compras_lst = ['Home','Dashboard','Análise de estoque']
    compras_selectbox = st.selectbox('',compras_lst)

if compras_selectbox == 'Home':
    home()

if compras_selectbox == 'Dashboard':
    layout_compras()
    
if compras_selectbox == 'Análise de estoque':
    layout_estoque()