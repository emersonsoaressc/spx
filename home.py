import streamlit as st
from function import analise_estoque, analise_estoque_grupo

def home():
    filiais = [
        '001 - Matriz',
        '004 - Centrinho',
        '005 - Calil',
        '007 - Rio Vermelho',
        '008 - Vargem',
        '009 - Canasvieiras',
        '010 - Upa',
        '011 - Trindade',
        '100 - Central']
    
    st.subheader('Indicador de ruptura')
    
    #001 - Matriz
    
    with st.expander('001 - Matriz', expanded=True):
        valor_em_estoque_001, valor_faltas_001, df_estoque_001 = analise_estoque('001')
        valor_estoque_base_001 = valor_em_estoque_001+valor_faltas_001
        kpi1,kpi2,kpi3 =  st.columns(3)
        with kpi1:
            st.metric(label='Ruptura total', value=f'{(valor_faltas_001/valor_estoque_base_001*100):.1f}%')
        with kpi2:
            st.metric(label='Valor em estoque', value=f'R$ {(valor_em_estoque_001/1000):.1f} mil')
        with kpi3:
            st.metric(label='Valor em faltas', value=f'R$ {(valor_faltas_001/1000):.1f} mil')
        
    #004 - Centrinho
    with st.expander('004 - Centrinho', expanded=True):
        valor_em_estoque_004, valor_faltas_004, df_estoque_004 = analise_estoque('004')
        valor_estoque_base_004 = valor_em_estoque_004+valor_faltas_004
        kpi1,kpi2,kpi3 =  st.columns(3)
        with kpi1:
            st.metric(label='Ruptura total', value=f'{(valor_faltas_004/valor_estoque_base_004*100):.1f}%')
        with kpi2:
            st.metric(label='Valor em estoque', value=f'R$ {(valor_em_estoque_004/1000):.1f} mil')
        with kpi3:
            st.metric(label='Valor em faltas', value=f'R$ {(valor_faltas_004/1000):.1f} mil')
    
    
    
    
    
    
    
    
    
    
    lst_tarefas = {
        'Compras' : {
            'Planograma de lojas',
            'Curva ABC',
            'Produtos com 180 dias sem venda',
            ''
        },
        'Recursos humanos': {
            'Relatório - Salários de funcionários',
            'Gerar comissão de colaboradores (modelo antigo)',
            'Gerar comissão de colaboradores (modelo novo)',
            },
        'Financeiro': {
            'Gerar DRE de loja',
            },
    }

    