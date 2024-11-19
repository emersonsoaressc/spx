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
        
        df_ipc_bonificados = pd.read_excel('planilhas/vendas/vendedores/ipc.xls')
        df_ipc_bonificados = df_ipc_bonificados.query("codigo in @lista_codigos_vendedores")
        ipc = df_ipc_bonificados['ipc'].mean()
        bonificados_5reais = round(df_ipc_bonificados['bonificados_5reais'].sum() * 5,2)
        bonificados_10reais = round(df_ipc_bonificados['bonificados_10reais'].sum() * 10,2)
        perfumaria_comissionada = round(df_ipc_bonificados['perfumaria_comissionada'].sum(),2)
        
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
            st.metric(label='Itens por cupom', value=ipc)
            st.metric(label='Vendas CSR', value=f'R$ {vendas_csr}')
    except:
        st.warning('No momento não temos dados para este colaborador')
    
    #visualização dos gráficos de evolução dos KPI's ao longo do tempo
    st.subheader('Evolução do ticket médio:')
    tkm_checkbox = st.checkbox('Exibir grafico de evolução de TKM')
    df_evol_tkm = df_vendedor.groupby('data')
    df_evol_tkm = df_evol_tkm[['valor_liquido']].sum() / df_evol_tkm[['valor_liquido']].count()
    df_evol_tkm['media_7d'] = df_evol_tkm['valor_liquido'].ewm(span=7, min_periods=7).mean()
    df_evol_tkm['media_30d'] = df_evol_tkm['valor_liquido'].ewm(span=30, min_periods=30).mean()
    if tkm_checkbox:
        st.write(graf_plotly(df_evol_tkm, 'Evolução do Ticket Médio'))
    
    st.subheader('Evolução das metas e comissões:')
    
    # meta ZERO
    if venda_liquida > 25000:
        meta_zero = round(vendas_genericos_similares*0.02,2)
        meta_zero_icon = f'R$ {meta_zero} ✅'
    else:
        meta_zero = 0
        meta_zero_icon = f'❌'
        
        
    # meta_1
    if (meta_zero>0) and (tkm > 50) and (ipc>0):
        meta_1 = round(100.00,2)
        meta_1_icon = f'R$ {meta_1} ✅'
    else:
        meta_1 = 0
        meta_1_icon = f'❌'
        
    # meta_2
    
    if (meta_zero>0):
        meta_2 = round(perfumaria_comissionada*0.02,2)
        meta_2_icon = f'R$ {meta_2} ✅'
    else:
        meta_2 = 0
        meta_2_icon = f'❌'
        
    # meta_3
    if (meta_zero>0) and (ipc >= 2.0):
        meta_3 = round(100.00,2)
        meta_3_icon = f'R$ {meta_3} ✅'
    else:
        meta_3 = 0
        meta_3_icon = f'❌'
        
    # meta_4
    if (meta_zero>0) and (vendas_perfumaria >= 10000):
        meta_4 = round(100.00,2)
        meta_4_icon = f'R$ {meta_4} ✅'
    else:
        meta_4 = 0
        meta_4_icon = f'❌'
        
    # meta_5
    if (meta_zero>0) and (venda_liquida > 35000):
        meta_5 = round(vendas_genericos_similares*0.01,2)
        meta_5_icon = f'R$ {meta_5} ✅'
    else:
        meta_5 = 0
        meta_5_icon = f'❌'

    # meta_6
    if (meta_zero>0) and (venda_liquida > 50000):
        meta_6 = round(vendas_genericos_similares*0.02,2)
        meta_6_icon = f'R$ {meta_6} ✅'
    else:
        meta_6 = 0
        meta_6_icon = f'❌'
        

    if bonificados_5reais > 0:
        bon_5reais_icon = f'R$ {bonificados_5reais} ✅'
    else:
        bon_5reais_icon = f'❌'
        
    if bonificados_10reais > 0:
        bon_10reais_icon = f'R$ {bonificados_10reais} ✅'
    else:
        bon_10reais_icon = f'❌'

        
    
    
    # metas de Agosto/2024
    if (data_inicial.month > 1 and lista_codigos_vendedores[0] != 10): 
        col_meta_1,col_meta_2,col_meta_3 =  st.columns(3)
        with col_meta_1:
            st.metric(label='Meta ZERO - R$ 25.000,00', value=f'{meta_zero_icon}', help=f'Essa meta ativa as outras metas, se não atingir a meta ZERO, não tem direito as outras metas!')
            st.metric(label='Meta 3 - IPC', value= f'{meta_3_icon}', help=f'Itens por cliente acima de 2.00. O seu IPC foi de {ipc}')
            st.metric(label='Meta 6 - 50k', value= f'{meta_6_icon}', help=f'Venda total acima de 50.000,00 . Você vendeu {venda_liquida}')
            
            
        with col_meta_2:
            st.metric(label='Meta 1 - TKM', value= f'{meta_1_icon}', help=f'Ticket médio acima de 50,00. O seu TKM foi de {tkm}')
            st.metric(label='Meta 4 - Perfumaria', value= f'{meta_4_icon}', help=f'Venda de Perfumaria acima de 10.000,00. Você vendeu {vendas_perfumaria}')
            st.metric(label='Bonificados 5 reais', value=f'{bon_5reais_icon}')
            
        with col_meta_3:
            st.metric(label='Meta 2 - Comissão 2% em perfumaria comissionada', value= f'{meta_2_icon}', help=f'Você vendeu R$ {perfumaria_comissionada} em perfumaria comissionada (Dermos, perfumes e maquiagens)')
            st.metric(label='Meta 5 - 35k', value= f'{meta_5_icon}', help=f'Venda total acima de 35.000,00 . Você vendeu {venda_liquida}')
            st.metric(label='Bonificados 10 reais', value=f'{bon_10reais_icon}')
        
        
        if meta_zero > 0:
            meta_total = round(meta_zero+meta_1+meta_2+meta_3+meta_4+meta_5+meta_6+bonificados_10reais+bonificados_5reais,2)
            st.success(f'Sua Comissão referente as vendas do mês {data_inicial.month} é de R$ {meta_total}')
        else:
            meta_total = round(bonificados_10reais+bonificados_5reais,2)
            st.error(f'Infelizmente você não atingiu a META ZERO no mês {data_inicial.month}. Sua comissão é de {meta_total}')
    
    else:
        password = st.text_input('', max_chars=6)
        if password == '100000':
            comissao_otavio =  vendas_genericos_similares*0.05 + df_vendas_csr_gensim['valor_liquido'].sum()*0.05
            st.success(f'Sua Comissão referente as vendas do mês {data_inicial.month} é de R$ {round(comissao_otavio)}')
        

        

        
    # metas a partir de setembro/2024        
