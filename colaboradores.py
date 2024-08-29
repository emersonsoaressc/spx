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
    df_relacao_vendas = pd.read_excel('planilhas/vendas/vendedores/relacao_vendas.xls', header=10, usecols=('B,E,G,Q,U,AA,AB,AI,AL,AM,AP,AS'))
    df_relacao_vendas = df_relacao_vendas.set_axis(['cod_venda','filial','forma_pagamento','data','hora','cupom','cliente','vendedor','valor_bruto','%desconto','valor_desconto','valor_liquido'], axis=1)[0:-3]
    df_relacao_vendas['vendedor'] = df_relacao_vendas['vendedor'].astype(int)
    lst_vendedor = ['6 - Emerson Soares', '11 - Shandrica Soares']
    cod_vendedor = int((st.selectbox('Selecione o vendedor',lst_vendedor)).split('-')[0].strip())
    
    df_vendedor = df_relacao_vendas.query('vendedor == @cod_vendedor')
    
    #KPI's
    venda_total = float(df_vendedor['valor_liquido'].sum())
    clientes_atendidos = int(df_vendedor['cupom'].count())
    tkm = venda_total/clientes_atendidos
    
    kpi1,kpi2,kpi3 =  st.columns(3)
    with kpi1:
        st.metric(label='Venda Total', value=f'R${venda_total}')
        st.metric(label='% desconto concedido', value=0)
        st.metric(label='Vendas Genéricos/Similares', value=0)
    with kpi2:
        st.metric(label='Clientes atendidos', value=clientes_atendidos)
        st.metric(label='% cupons com clientes cadastrados', value=0)
        st.metric(label='Vendas Perfumaria', value=0)
    with kpi3:
        st.metric(label='Ticket médio', value=tkm)
        st.metric(label='Itens por cupom', value=0)
        st.metric(label='Vendas CSR', value=0)

    st.write(df_vendedor)
    