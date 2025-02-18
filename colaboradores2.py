import streamlit as st
import pandas as pd
import sqlite3
from function import graf_plotly

# Função para conectar ao banco de dados
def conectar_banco():
    return sqlite3.connect("vendas.db")

# Função para carregar os colaboradores do banco de dados
def carregar_colaboradores():
    conn = conectar_banco()
    df = pd.read_sql("SELECT codigo, colaborador, cod_nome_colab FROM colaboradores", conn)
    conn.close()
    return df

# Função para carregar as vendas gerais
def carregar_vendas():
    conn = conectar_banco()
    df = pd.read_sql("SELECT * FROM vendas_vendedores", conn)
    conn.close()
    return df

# Função para carregar vendas por grupo
def carregar_vendas_grupo(grupo):
    conn = conectar_banco()
    df = pd.read_sql(f"SELECT * FROM vendas_{grupo}", conn)
    conn.close()
    return df

# Função para criar a interface principal do Dashboard
def dash_colab():
    st.header('Dashboard Geral')

    # Carregar dados do banco
    df_colaboradores = carregar_colaboradores()
    df_vendas = carregar_vendas()

    # KPIs gerais
    total_colaboradores = len(df_colaboradores)
    venda_total = round(df_vendas['valor_liquido'].sum(), 2)
    lucro_bruto = round(df_vendas['valor_bruto'].sum() - df_vendas['valor_desconto'].sum(), 2)

    kpi1, kpi2, kpi3 = st.columns(3)
    with kpi1:
        st.metric(label='Colaboradores ativos', value=total_colaboradores)
    with kpi2:
        st.metric(label='Venda total', value=f'R$ {venda_total}')
    with kpi3:
        st.metric(label='Lucro Bruto total', value=f'R$ {lucro_bruto}')

    # Melhores vendedores por categorias
    st.subheader('Melhores Vendedores')

    with st.expander('Melhores Vendedores em faturamento', expanded=False):
        top_faturamento = df_vendas.groupby('vendedor')['valor_liquido'].sum().sort_values(ascending=False).head(10)
        st.write(top_faturamento)

    with st.expander('Melhores Vendedores em lucratividade bruta', expanded=False):
        top_lucratividade = df_vendas.groupby('vendedor').apply(lambda x: x['valor_bruto'].sum() - x['valor_desconto'].sum()).sort_values(ascending=False).head(10)
        st.write(top_lucratividade)

    with st.expander('Melhores Vendedores em ticket médio', expanded=False):
        df_vendas['ticket_medio'] = df_vendas['valor_liquido'] / df_vendas['cupom'].astype(float)
        top_tkm = df_vendas.groupby('vendedor')['ticket_medio'].mean().sort_values(ascending=False).head(10)
        st.write(top_tkm)

    with st.expander('Melhores Vendedores em itens por cupom', expanded=False):
        df_vendas['itens_por_cupom'] = df_vendas['cupom'].astype(float)
        top_ipc = df_vendas.groupby('vendedor')['itens_por_cupom'].mean().sort_values(ascending=False).head(10)
        st.write(top_ipc)

# Função para análise individual do colaborador
def colab_individual():
    st.header('Análise Individual do Vendedor')

    # Carregar os dados
    df_colaboradores = carregar_colaboradores()
    df_vendas = carregar_vendas()
    df_vendas_genericos = carregar_vendas_grupo('genericos')
    df_vendas_similares = carregar_vendas_grupo('similares')
    df_vendas_perfumaria = carregar_vendas_grupo('perfumaria')
    df_vendas_csr_referencia = carregar_vendas_grupo('csr_referencia')
    df_vendas_csr_gensim = carregar_vendas_grupo('csr_gensim')

    # Seleção do vendedor
    lst_vendedor = df_colaboradores['cod_nome_colab'].unique()
    seletor_colab = st.multiselect('Selecione o vendedor', lst_vendedor)

    lista_codigos_vendedores = [int(i.split('-')[0].strip()) for i in seletor_colab]

    # Seleção de período
    dt1, dt2 = st.columns(2)
    with dt1:
        data_inicial = st.date_input('Data inicial')
    with dt2:
        data_final = st.date_input('Data final')
    
    # Converter a coluna 'data' para datetime antes de filtrar
    df_vendas['data'] = pd.to_datetime(df_vendas['data'])

    # Filtrar vendas pelo vendedor e período
    df_vendedor = df_vendas.query("vendedor in @lista_codigos_vendedores and data >= @data_inicial and data <= @data_final")

    # KPIs individuais
    try:
        venda_liquida = round(df_vendedor['valor_liquido'].sum(), 2)
        clientes_atendidos = df_vendedor['cupom'].count()
        tkm = round(venda_liquida / clientes_atendidos, 2) if clientes_atendidos > 0 else 0
        valor_desconto = -df_vendedor['valor_desconto'].sum()
        venda_bruta = venda_liquida + valor_desconto
        desconto_percent = round(valor_desconto / venda_bruta * 100, 2) if venda_bruta > 0 else 0
        vendas_genericos_similares = round(df_vendas_genericos['valor_liquido'].sum() + df_vendas_similares['valor_liquido'].sum(), 2)
        vendas_perfumaria = round(df_vendas_perfumaria['valor_liquido'].sum(), 2)
        vendas_csr = round(df_vendas_csr_referencia['valor_liquido'].sum() + df_vendas_csr_gensim['valor_liquido'].sum(), 2)

        kpi1, kpi2, kpi3 = st.columns(3)
        with kpi1:
            st.metric(label='Venda líquida', value=f'R$ {venda_liquida}')
            st.metric(label='% desconto concedido', value=f'{desconto_percent}%')
            st.metric(label='Vendas Genéricos/Similares', value=f'R$ {vendas_genericos_similares}')
        with kpi2:
            st.metric(label='Clientes atendidos', value=clientes_atendidos)
            st.metric(label='Vendas Perfumaria', value=f'R$ {vendas_perfumaria}')
        with kpi3:
            st.metric(label='Ticket médio', value=f'R$ {tkm}')
            st.metric(label='Vendas CSR', value=f'R$ {vendas_csr}')

        # Evolução do Ticket Médio
        st.subheader('Evolução do Ticket Médio')
        tkm_checkbox = st.checkbox('Exibir gráfico de evolução de TKM')
        if tkm_checkbox:
            df_evol_tkm = df_vendedor.groupby('data')[['valor_liquido']].sum() / df_vendedor.groupby('data')[['cupom']].count()
            df_evol_tkm['media_7d'] = df_evol_tkm['valor_liquido'].ewm(span=7, min_periods=7).mean()
            df_evol_tkm['media_30d'] = df_evol_tkm['valor_liquido'].ewm(span=30, min_periods=30).mean()
            st.write(graf_plotly(df_evol_tkm, 'Evolução do Ticket Médio'))

    except Exception as e:
        st.warning(f'Erro ao calcular KPIs: {e}')

colab_individual()