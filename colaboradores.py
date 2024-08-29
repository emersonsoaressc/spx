import streamlit as st
from function import analise_estoque, analise_estoque_grupo

def dash_colab():
    st.header('Dashboard Geral')
    
    st.subheader('Indicadores de Faturamento')
    kpi1,kpi2,kpi3 =  st.columns(3)
    with kpi1:
        st.metric(label='Faturamento Atual', value=f'')
    with kpi2:
        st.metric(label='Faturamento ', value=f'')
    with kpi3:
        st.metric(label='Faturamento', value=f'')