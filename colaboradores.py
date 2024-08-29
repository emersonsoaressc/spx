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
    with st.expander('Melhores Vendedores em faturamento', expanded=False):
        st.write('')
    
    
    # melhores vendedores em lucratividade bruta
    with st.expander('Melhores Vendedores em lucratividade bruta', expanded=False):
        st.write('')
    
    
    # melhores vendedores em ticket médio
    with st.expander('Melhores Vendedores em ticket médio', expanded=False):
        st.write('')
    
    
    # melhores vendedores em itens por cupom
    with st.expander('Melhores Vendedores em itens por cupom', expanded=False):
        st.write('')
        
        
def colab_individual():
    lst_vendedor = ['6 - Emerson Soares', '11 - Shandrica Soares']
    st.selectbox('Selecione o vendedor',lst_vendedor)