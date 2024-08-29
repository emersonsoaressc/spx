import streamlit as st
from function import analise_estoque, analise_estoque_grupo

def dash_colab():
    st.header('Dashboard Geral')
    
    st.subheader('Colaboradores')
    kpi1,kpi2,kpi3 =  st.columns(3)
    with kpi1:
        st.metric(label='Colaboradores ativos', value=f'')
    with kpi2:
        st.metric(label='Venda por colaborador', value=f'')
    with kpi3:
        st.metric(label='Lucro Bruto por colaborador', value=f'')