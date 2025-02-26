import streamlit as st
from arquivados.function import analise_estoque, analise_estoque_grupo

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
            
    #005 - Calil
    with st.expander('005 - Calil', expanded=True):
        valor_em_estoque_005, valor_faltas_005, df_estoque_005 = analise_estoque('005')
        valor_estoque_base_005 = valor_em_estoque_005+valor_faltas_005
        kpi1,kpi2,kpi3 =  st.columns(3)
        with kpi1:
            st.metric(label='Ruptura total', value=f'{(valor_faltas_005/valor_estoque_base_005*100):.1f}%')
        with kpi2:
            st.metric(label='Valor em estoque', value=f'R$ {(valor_em_estoque_005/1000):.1f} mil')
        with kpi3:
            st.metric(label='Valor em faltas', value=f'R$ {(valor_faltas_005/1000):.1f} mil')

    #007 - Rio Vermelho
    with st.expander('007 - Rio Vermelho', expanded=True):
        valor_em_estoque_007, valor_faltas_007, df_estoque_007 = analise_estoque('007')
        valor_estoque_base_007 = valor_em_estoque_007+valor_faltas_007
        kpi1,kpi2,kpi3 =  st.columns(3)
        with kpi1:
            st.metric(label='Ruptura total', value=f'{(valor_faltas_007/valor_estoque_base_007*100):.1f}%')
        with kpi2:
            st.metric(label='Valor em estoque', value=f'R$ {(valor_em_estoque_007/1000):.1f} mil')
        with kpi3:
            st.metric(label='Valor em faltas', value=f'R$ {(valor_faltas_007/1000):.1f} mil')
            
    #008 - Vargem
    with st.expander('008 - Vargem', expanded=True):
        valor_em_estoque_008, valor_faltas_008, df_estoque_008 = analise_estoque('008')
        valor_estoque_base_008 = valor_em_estoque_008+valor_faltas_008
        kpi1,kpi2,kpi3 =  st.columns(3)
        with kpi1:
            st.metric(label='Ruptura total', value=f'{(valor_faltas_008/valor_estoque_base_008*100):.1f}%')
        with kpi2:
            st.metric(label='Valor em estoque', value=f'R$ {(valor_em_estoque_008/1000):.1f} mil')
        with kpi3:
            st.metric(label='Valor em faltas', value=f'R$ {(valor_faltas_008/1000):.1f} mil')

    #009 - Canasvieiras
    with st.expander('009 - Canasvieiras', expanded=True):
        valor_em_estoque_009, valor_faltas_009, df_estoque_009 = analise_estoque('009')
        valor_estoque_base_009 = valor_em_estoque_009+valor_faltas_009
        kpi1,kpi2,kpi3 =  st.columns(3)
        with kpi1:
            st.metric(label='Ruptura total', value=f'{(valor_faltas_009/valor_estoque_base_009*100):.1f}%')
        with kpi2:
            st.metric(label='Valor em estoque', value=f'R$ {(valor_em_estoque_009/1000):.1f} mil')
        with kpi3:
            st.metric(label='Valor em faltas', value=f'R$ {(valor_faltas_009/1000):.1f} mil')
            
    #010 - Upa Norte
    with st.expander('010 - Upa Norte', expanded=True):
        valor_em_estoque_010, valor_faltas_010, df_estoque_010 = analise_estoque('010')
        valor_estoque_base_010 = valor_em_estoque_010+valor_faltas_010
        kpi1,kpi2,kpi3 =  st.columns(3)
        with kpi1:
            st.metric(label='Ruptura total', value=f'{(valor_faltas_010/valor_estoque_base_010*100):.1f}%')
        with kpi2:
            st.metric(label='Valor em estoque', value=f'R$ {(valor_em_estoque_010/1000):.1f} mil')
        with kpi3:
            st.metric(label='Valor em faltas', value=f'R$ {(valor_faltas_010/1000):.1f} mil')
            
    #011 - Trindade
    with st.expander('011 - Trindade', expanded=True):
        valor_em_estoque_011, valor_faltas_011, df_estoque_011 = analise_estoque('011')
        valor_estoque_base_011 = valor_em_estoque_011+valor_faltas_011
        kpi1,kpi2,kpi3 =  st.columns(3)
        with kpi1:
            st.metric(label='Ruptura total', value=f'{(valor_faltas_011/valor_estoque_base_011*100):.1f}%')
        with kpi2:
            st.metric(label='Valor em estoque', value=f'R$ {(valor_em_estoque_011/1000):.1f} mil')
        with kpi3:
            st.metric(label='Valor em faltas', value=f'R$ {(valor_faltas_011/1000):.1f} mil')
    
    
    
    
    
    
    
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

    