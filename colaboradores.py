import streamlit as st
from function import analise_estoque, analise_estoque_grupo

def dash_colab():
    st.header('Dashboard Geral')
    
    st.subheader('Colaboradores')
    kpi1,kpi2,kpi3 =  st.columns(3)
    with kpi1:
        st.metric(label='Colaboradores ativos', value=0, delta=0.1)
    with kpi2:
        st.metric(label='Venda por colaborador', value=0, delta=0.1)
    with kpi3:
        st.metric(label='Lucro Bruto por colaborador', value=0, delta=0.1)
    
    # melhores vendedores em faturamento
    st.subheader('Melhores Vendedores em faturamento')
    
    
    # melhores vendedores em lucratividade bruta
    st.subheader('Melhores Vendedores em lucratividade bruta')
    
    
    # melhores vendedores em ticket médio
    st.subheader('Melhores Vendedores em ticket médio')
    
    
    # melhores vendedores em itens por cupom
    st.subheader('Melhores Vendedores em ticket médio')