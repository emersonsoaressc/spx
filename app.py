import streamlit as st
from compras.compras import layout_compras
from home import home
from colaboradores import dash_colab

st.sidebar.image('images/logo_shopfarma_sem_fundo.png')

with st.sidebar.expander('Gestão de colaboradores',expanded=True):
    lst_gestao_colab = ['Dashboard Geral','Avaliação Individual']
    gestao_colab = st.selectbox('',lst_gestao_colab)
    
if gestao_colab == 'Dashboard Geral':
    dash_colab()

with st.sidebar.expander('Gestão de estoque avançada', expanded=False):
    lst_gestao_estoque = ['','Home','Sistema de compras']
    gestao_estoque_selectbox = st.selectbox('',lst_gestao_estoque)

if gestao_estoque_selectbox == 'Home':
    home()

if gestao_estoque_selectbox == 'Dashboard':
    pass
    
if gestao_estoque_selectbox == 'Sistema de compras':
    layout_compras()