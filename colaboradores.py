import streamlit as st
import pandas as pd
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
    cod_vendedor = (st.selectbox('Selecione o vendedor',lst_vendedor)).split('-')[0].strip()
    st.write(cod_vendedor)
    
    df_relacao_vendas = pd.read_excel('planilhas/vendas/vendedores/relacao_vendas.xls', header=10, usecols=('B,E,G,Q,U,AA,AB,AI,AL,AM,AP,AS'))
    df_relacao_vendas = df_relacao_vendas.set_axis(['cod_venda','filial','forma_pagamento','data','hora','cupom','cliente','vendedor','valor_bruto','%desconto','valor_desconto','valor_liquido'], axis=1)
    st.write(df_relacao_vendas)