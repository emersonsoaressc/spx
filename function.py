import pandas as pd 
import numpy as np
import streamlit as st

def convertXLS(arquivo_xls):
    pass

@st.cache
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

    
    df_saldo_estoque_filtrado = df_saldo_estoque.query('estoque_minimo > 0')
    valor_em_estoque = df_saldo_estoque['preco_custo_total'].sum()
    df_faltas = df_saldo_estoque_filtrado.query('estoque == 0')
    df_faltas['valor_faltas'] = np.where((df_faltas['estoque_minimo'] - df_faltas['estoque']) < 0,0,((df_faltas['estoque_minimo'] - df_faltas['estoque'])*df_faltas['preco_custo']))
    valor_faltas = df_faltas['valor_faltas'].sum()
    
    return valor_em_estoque, valor_faltas, df_saldo_estoque


@st.cache
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