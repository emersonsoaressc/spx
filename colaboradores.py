import streamlit as st
import pandas as pd
from function import analise_estoque, analise_estoque_grupo, vendas_grupo, graf_plotly

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
    lista_codigos_vendedores = []
    
    df_vendas_genericos = vendas_grupo('genericos')
    df_vendas_similares = vendas_grupo('similares')
    df_vendas_perfumaria = vendas_grupo('perfumaria')
    df_vendas_csr_referencia = vendas_grupo('csr_referencia')
    df_vendas_csr_gensim = vendas_grupo('csr_gensim')
    
    for i in seletor_colab:
        codigo = i.split('-')[0].strip()
        lista_codigos_vendedores.append(int(codigo))
    dt1,dt2 =  st.columns(2)
    with dt1:
        data_inicial = st.date_input('Data inicial')
    with dt2:
        data_final = st.date_input('Data final')
    
    st.subheader('Estatísticas do(s) vendedor(es) para o período:')
    #utilizando os filtros da página
    df_vendedor = df_relacao_vendas.query('vendedor in @lista_codigos_vendedores')
    df_vendas_genericos = df_vendas_genericos.query('vendedor in @lista_codigos_vendedores')
    df_vendas_similares = df_vendas_similares.query('vendedor in @lista_codigos_vendedores')
    df_vendas_perfumaria = df_vendas_perfumaria.query('vendedor in @lista_codigos_vendedores')
    df_vendas_csr_referencia = df_vendas_csr_referencia.query('vendedor in @lista_codigos_vendedores')
    df_vendas_csr_gensim = df_vendas_csr_gensim.query('vendedor in @lista_codigos_vendedores')
    
    df_vendedor = df_vendedor.query('data >= @data_inicial')
    df_vendedor = df_vendedor.query('data <= @data_final')
    
    df_vendas_genericos = df_vendas_genericos.query('data >= @data_inicial')
    df_vendas_genericos = df_vendas_genericos.query('data <= @data_final')
    
    df_vendas_similares = df_vendas_similares.query('data >= @data_inicial')
    df_vendas_similares = df_vendas_similares.query('data <= @data_final')
    
    df_vendas_perfumaria = df_vendas_perfumaria.query('data >= @data_inicial')
    df_vendas_perfumaria = df_vendas_perfumaria.query('data <= @data_final')
    
    df_vendas_csr_referencia = df_vendas_csr_referencia.query('data >= @data_inicial')
    df_vendas_csr_referencia = df_vendas_csr_referencia.query('data <= @data_final')
    
    df_vendas_csr_gensim = df_vendas_csr_gensim.query('data >= @data_inicial')
    df_vendas_csr_gensim = df_vendas_csr_gensim.query('data <= @data_final')
    
    
    # inserindo tratamento de erros para visualização dos KPI's
    try:
        #KPI's
        venda_liquida = round(float(df_vendedor['valor_liquido'].sum()),2)
        clientes_atendidos = int(df_vendedor['cupom'].count())
        tkm = round(venda_liquida/clientes_atendidos,2)
        valor_desconto = -df_vendedor['valor_desconto'].sum()
        venda_bruta = venda_liquida + valor_desconto
        desconto_percent = round(valor_desconto/venda_bruta*100,2)
        vendas_genericos_similares = round(df_vendas_genericos['valor_liquido'].sum() + df_vendas_similares['valor_liquido'].sum(),2)
        vendas_perfumaria = round(df_vendas_perfumaria['valor_liquido'].sum(),2)
        vendas_csr = round(df_vendas_csr_referencia['valor_liquido'].sum() + df_vendas_csr_gensim['valor_liquido'].sum(),2)
        
        cupons_nao_identificados = df_vendedor['cliente'].isna().sum()
        cupons_identificados = df_vendedor['cliente'].count()
        cupons_identificados_percent = round(cupons_identificados/(cupons_identificados+cupons_nao_identificados)*100,2)
        
        
        kpi1,kpi2,kpi3 =  st.columns(3)
        with kpi1:
            st.metric(label='Venda liquida', value=f'R$ {venda_liquida}')
            st.metric(label='% desconto concedido', value=f'{desconto_percent}%')
            st.metric(label='Vendas Genéricos/Similares', value=f'R$ {vendas_genericos_similares}')
        with kpi2:
            st.metric(label='Clientes atendidos', value=clientes_atendidos)
            st.metric(label='% cupons com clientes cadastrados', value=f'{cupons_identificados_percent}%')
            st.metric(label='Vendas Perfumaria', value=f'R$ {vendas_perfumaria}')
        with kpi3:
            st.metric(label='Ticket médio', value=f'R$ {tkm}')
            st.metric(label='Itens por cupom', value=0)
            st.metric(label='Vendas CSR', value=f'R$ {vendas_csr}')
    except:
        st.warning('No momento não temos dados para este colaborador')
    
    #visualização dos gráficos de evolução dos KPI's ao longo do tempo
    st.subheader('Evolução do ticket médio:')

    df_evol_tkm = df_vendedor.groupby('data')
    df_evol_tkm = df_evol_tkm[['valor_liquido']].sum() / df_evol_tkm[['valor_liquido']].count()
    df_evol_tkm['media_7d'] = df_evol_tkm['valor_liquido'].ewm(span=7, min_periods=7).mean()
    df_evol_tkm['media_30d'] = df_evol_tkm['valor_liquido'].ewm(span=30, min_periods=30).mean()
    st.write(graf_plotly(df_evol_tkm, 'Evolução do Ticket Médio'))
    
    st.subheader('Evolução das metas:')
    
    # META ZERO = Vender acima de 25 mil reais
    meta_zero = 25000
    meta_zero_value = 0
    meta1 = 0
    
    col_meta_1,col_meta_2,col_meta_3 =  st.columns(3)
    with col_meta_1:
        st.metric(label='Meta ZERO - R$ 25.000,00', value=f'R$ {venda_liquida}')
        st.metric(label='Meta 1', value=f'{desconto_percent}%')
        st.metric(label='Meta 2', value=f'R$ {vendas_genericos_similares}')
    with col_meta_2:
        st.metric(label='Meta 3', value=clientes_atendidos)
        st.metric(label='Meta 4', value=f'{cupons_identificados_percent}%')
        st.metric(label='Meta 5', value=f'R$ {vendas_perfumaria}')
    with col_meta_3:
        st.metric(label='Meta 6', value=f'R$ {tkm}')
        st.metric(label='Meta 7', value=0)
        st.metric(label='meta 8', value=f'R$ {vendas_csr}')