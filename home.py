import streamlit as st

def home():
    st.header('A fazer...')
    
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

    st.write(lst_tarefas)