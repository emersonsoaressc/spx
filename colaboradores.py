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
    df_colaboradores = pd.read_excel('planilhas/vendas/vendedores/lista_colaboradores.xls', header=8,usecols=('B,C,E'))[0:-5]
    df_colaboradores = df_colaboradores.set_axis(['codigo','colaborador','admissao'], axis=1)
    df_colaboradores['cod_nome_colab'] = df_colaboradores['codigo'].astype(str) + ' - '+ df_colaboradores['colaborador']

    df_relacao_vendas = pd.read_excel('planilhas/vendas/vendedores/relacao_vendas.xls', header=10, usecols=('B,E,G,Q,U,AA,AB,AI,AL,AM,AP,AS'))
    df_relacao_vendas = df_relacao_vendas.set_axis(['cod_venda','filial','forma_pagamento','data','hora','cupom','cliente','vendedor','valor_bruto','%desconto','valor_desconto','valor_liquido'], axis=1)[0:-3]
    df_relacao_vendas['vendedor'] = df_relacao_vendas['vendedor'].astype(int)
    df_relacao_vendas['cod_venda'] = df_relacao_vendas['cod_venda'].astype(str)
    df_relacao_vendas['cupom'] = df_relacao_vendas['cupom'].astype(str)
    lst_vendedor = df_colaboradores['cod_nome_colab'].unique()
    seletor_colab = st.multiselect('Selecione o vendedor',lst_vendedor)
    st.write(seletor_colab)
    
    lista_codigos_vendedores = []
    
    for i in seletor_colab:
        codigo = i.split('-')[0].strip()
        lista_codigos_vendedores.append(codigo)
        st.write(codigo)
    
    # inserir tratamento de erros

    df_vendedor = df_relacao_vendas.query('vendedor in @lista_codigos_vendedores')
    dt1,dt2 =  st.columns(2)
    with dt1:
        data_inicial = st.date_input('Data inicial')
    with dt2:
        data_final = st.date_input('Data final')
    df_vendedor = df_vendedor.query('data >= @data_inicial')
    df_vendedor = df_vendedor.query('data <= @data_final')

    #KPI's
    venda_liquida = round(float(df_vendedor['valor_liquido'].sum()),2)
    clientes_atendidos = int(df_vendedor['cupom'].count())
    tkm = round(venda_liquida/clientes_atendidos,2)
    valor_desconto = -df_vendedor['valor_desconto'].sum()
    venda_bruta = venda_liquida + valor_desconto
    desconto_percent = round(valor_desconto/venda_bruta*100,2)
    
    cupons_nao_identificados = df_vendedor['cliente'].isna().sum()
    cupons_identificados = df_vendedor['cliente'].count()
    cupons_identificados_percent = round(cupons_identificados/(cupons_identificados+cupons_nao_identificados)*100,2)
    
    kpi1,kpi2,kpi3 =  st.columns(3)
    with kpi1:
        st.metric(label='Venda liquida', value=f'R$ {venda_liquida}')
        st.metric(label='% desconto concedido', value=f'{desconto_percent}%')
        st.metric(label='Vendas Genéricos/Similares', value=0)
    with kpi2:
        st.metric(label='Clientes atendidos', value=clientes_atendidos)
        st.metric(label='% cupons com clientes cadastrados', value=f'{cupons_identificados_percent}%')
        st.metric(label='Vendas Perfumaria', value=0)
    with kpi3:
        st.metric(label='Ticket médio', value=f'R$ {tkm}')
        st.metric(label='Itens por cupom', value=0)
        st.metric(label='Vendas CSR', value=0)

    st.write(df_vendedor)
    

    st.warning('No momento não temos dados para este colaborador')
    