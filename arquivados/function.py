import pandas as pd 
import numpy as np
import streamlit as st
import plotly.graph_objects as go

def convertXLS(arquivo_xls):
    pass

@st.cache_data
def analise_estoque(filial):
    df_saldo_estoque = pd.read_excel(f'planilhas/estoque/saldo_estoque_{filial}.xlsx', header=11, usecols=('B,C,F,G,H,I,J,O,P,Q,S,U,X'))[0:-3]
    df_saldo_estoque = df_saldo_estoque.set_axis(['ean','produto','laboratorio','grupo','curva','estoque_minimo','demanda','estoque','preco_custo','preco_venda','lucro','preco_custo_total','preco_venda_total'], axis=1)
    df_saldo_estoque['grupo'] = df_saldo_estoque['grupo'].astype(int)
    df_saldo_estoque['preco_custo_total'] = df_saldo_estoque['preco_custo_total'].str.replace('.', '').str.replace(',', '.')
    df_saldo_estoque['preco_custo'] = df_saldo_estoque['preco_custo'].str.replace('.', '').str.replace(',', '.')
    df_saldo_estoque['estoque_minimo'] = pd.to_numeric(df_saldo_estoque['estoque_minimo'], errors='coerce')
    df_saldo_estoque['preco_custo_total'] = pd.to_numeric(df_saldo_estoque['preco_custo_total'], errors='coerce')
    df_saldo_estoque['preco_custo'] = pd.to_numeric(df_saldo_estoque['preco_custo'], errors='coerce')
    df_saldo_estoque['ean'] = df_saldo_estoque['ean'].fillna(0).astype(int)
    df_saldo_estoque['ean'] = df_saldo_estoque['ean'].astype(str)

    
    df_saldo_estoque_filtrado = df_saldo_estoque.query('estoque_minimo > 0')
    valor_em_estoque = df_saldo_estoque['preco_custo_total'].sum()
    df_faltas = df_saldo_estoque_filtrado.query('estoque == 0')
    df_faltas['valor_faltas'] = np.where((df_faltas['estoque_minimo'] - df_faltas['estoque']) < 0,0,((df_faltas['estoque_minimo'] - df_faltas['estoque'])*df_faltas['preco_custo']))
    valor_faltas = df_faltas['valor_faltas'].sum()
    
    return valor_em_estoque, valor_faltas, df_saldo_estoque

@st.cache_data
def analise_estoque_grupo(df_saldo_estoque_grupo, grupo):
    df = df_saldo_estoque_grupo.query(f'grupo == {grupo}')
    df_saldo_estoque_grupo_filtrado = df.query('estoque_minimo > 0')
    valor_em_estoque = df_saldo_estoque_grupo['preco_custo_total'].sum()
    df_faltas = df_saldo_estoque_grupo_filtrado
    df_faltas['valor_faltas'] = np.where((df_faltas['estoque_minimo'] - df_faltas['estoque']) < 0,0,((df_faltas['estoque_minimo'] - df_faltas['estoque'])*df_faltas['preco_custo']))
    df_faltas['ean'] = df_faltas['ean'].astype(str)
    valor_faltas = df_faltas['valor_faltas'].sum()
    
    df_excesso = df_saldo_estoque_grupo.query('estoque > 0')
    df_excesso['excesso'] = np.where(df_excesso['estoque']>df_excesso['demanda'],df_excesso['estoque']-df_excesso['demanda'],0)
    df_excesso = df_excesso.query('excesso > 0')
    df_excesso['ean'] = df_excesso['ean'].astype(str)
    return valor_em_estoque, valor_faltas, df_faltas, df_excesso

@st.cache_data
def consulta_estoque_central():
    df_estoque_central = pd.read_excel(f'planilhas/estoque/saldo_estoque_100.xls', header=11, usecols=('B,C,F,G,H,I,J,O,P,Q,S,U,X'))[0:-3]
    df_estoque_central = df_estoque_central.set_axis(['ean','produto','laboratorio','grupo','curva','estoque_minimo','demanda','estoque','preco_custo','preco_venda','lucro','preco_custo_total','preco_venda_total'], axis=1)
    df_estoque_central['grupo'] = df_estoque_central['grupo'].astype(int)
    df_estoque_central['estoque_minimo'] = pd.to_numeric(df_estoque_central['estoque_minimo'], errors='coerce')
    df_estoque_central['preco_custo_total'] = pd.to_numeric(df_estoque_central['preco_custo_total'], errors='coerce')
    df_estoque_central['ean'] = df_estoque_central['ean'].fillna(0).astype(int)
    df_estoque_central['ean'] = df_estoque_central['ean'].astype(str)
    df_estoque_central = df_estoque_central.query("estoque > 0")
    return df_estoque_central


@st.cache_data
def vendas_grupo(grupo):
    df = pd.read_excel(f'planilhas/vendas/vendedores/vendas_{grupo}.xls',header=10, usecols=('B,D,F,T,Z,AF,AM,BC') )
    df = df.set_axis(['venda','filial','pagamento','data','hora','cupom','vendedor','valor_liquido'], axis=1)
    df['vendedor'] = df['vendedor'].shift(-1)
    df['valor_liquido'] = df['valor_liquido'].shift(-2)
    df.dropna(inplace=True)
    df['filial'] = df['filial'].astype(int)
    df['cupom'] = df['cupom'].astype(int)
    df['vendedor'] = df['vendedor'].astype(int)
    return df


def graf_plotly(data_frame, titulo):
    fig = go.Figure()
    fig.update_layout(
    title= f'{titulo}', 

    xaxis=dict(
        rangeslider= dict(visible=True),
        type='date',
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(82, 82, 82)',
        ),
    ),
    yaxis=dict(
        
        showgrid=False,
        zeroline=True,
        showline=True,
        showticklabels=True,
    ),
    autosize=True,
    margin=dict(
        autoexpand=True,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=True,
    plot_bgcolor='white',
    legend= dict(
        font=dict(
            family='Arial',
            size=9)
    )
    )
    count = 0
    for i in data_frame.columns:
        if count < 2:
            count += 1
            lines = fig.add_trace(go.Scatter(x=data_frame.index, y=data_frame[f'{i}'], name= f"{i}", mode="markers+lines", visible=True))
        elif count == 2:
            count += 1
            lines = fig.add_trace(go.Scatter(x=data_frame.index, y=data_frame[f'{i}'], name= f"{i}", mode="lines", visible=True))
        elif count >2:
            count += 1
            lines = fig.add_trace(go.Scatter(x=data_frame.index, y=data_frame[f'{i}'], name= f"{i}", mode="lines", visible='legendonly'))
    return lines