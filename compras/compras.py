import streamlit as st
from function import analise_estoque, analise_estoque_grupo


def layout_compras():
    filial = st.selectbox('Escolha a filial:', ['001 - Matriz','004 - Centrinho','005 - Calil','007 - Rio Vermelho','008 - Vargem','009 - Canasvieiras','010 - Upa','011 - Trindade','100 - Central'])
    cod_filial = filial[0:3]
    
    valor_em_estoque, valor_faltas, df_estoque = analise_estoque(cod_filial)
    
    valor_estoque_base = valor_em_estoque+valor_faltas

    st.subheader('Indicador de ruptura')
    kpi1,kpi2,kpi3 =  st.columns(3)
    with kpi1:
        st.metric(label='Ruptura total', value=f'{(valor_faltas/valor_estoque_base*100):.1f}%')
    with kpi2:
        st.metric(label='Valor em estoque', value=f'R$ {(valor_em_estoque/1000):.1f} mil')
    with kpi3:
        st.metric(label='Valor em faltas', value=f'R$ {(valor_faltas/1000):.1f} mil')
    
    with st.expander('Comprar Produtos', expanded=False):
        
        grupo_produtos = st.selectbox('Selecione o grupo de produtos e aguarde a geração da análise de ruptura',['Genéricos e Similares (por princípio ativo)','3000 - Éticos','8000 - Perfumaria', '9000 - Correlatos', '10000 - Conveniência'])
        st.write(grupo_produtos)
        
        kpi1,kpi2,kpi3 =  st.columns(3)
        

        if grupo_produtos == '3000 - Éticos':
            estoque_grupo, faltas_grupo, df_faltas_grupo, df_excesso_grupo = analise_estoque_grupo(df_estoque, grupo='3000')
            estoque_base_grupo = estoque_grupo+faltas_grupo
            
        elif grupo_produtos == '8000 - Perfumaria':
            estoque_grupo, faltas_grupo, df_faltas_grupo, df_excesso_grupo = analise_estoque_grupo(df_estoque, grupo='8000')
            estoque_base_grupo = estoque_grupo+faltas_grupo

        elif grupo_produtos == '9000 - Correlatos':
            estoque_grupo, faltas_grupo, df_faltas_grupo, df_excesso_grupo = analise_estoque_grupo(df_estoque, grupo='9000')
            estoque_base_grupo = estoque_grupo+faltas_grupo

        elif grupo_produtos == '10000 - Conveniência':
            estoque_grupo, faltas_grupo, df_faltas_grupo, df_excesso_grupo = analise_estoque_grupo(df_estoque, grupo='10000')
            estoque_base_grupo = estoque_grupo+faltas_grupo
            
        elif grupo_produtos == 'Genéricos e Similares (por princípio ativo)':
            estoque_grupo, faltas_grupo, df_faltas_grupo, df_excesso_grupo = analise_estoque_grupo(df_estoque, grupo='2000')
            estoque_base_grupo = estoque_grupo+faltas_grupo

            st.warning('Ainda estamos trabalhando nisso! Aguarde!')
            
        else:
            estoque_grupo = 1
            faltas_grupo = 1
            df_faltas_grupo = 1
            df_excesso_grupo = 1
            estoque_base_grupo = 1
            
        
        with kpi1:
            st.metric(label='Ruptura do grupo', value=f'{(faltas_grupo/estoque_base_grupo*100):.1f}%')
        with kpi2:
            st.metric(label='R$ estoque do grupo', value=f'R$ {(estoque_grupo/1000):.1f} mil')
        with kpi3:
            st.metric(label='R$ faltas do grupo', value=f'R$ {(faltas_grupo/1000):.1f} mil')
            
        if cod_filial == '001':
            df_faltas_grupo['cnpj'] = '31179778000214'
        if cod_filial == '004':
            df_faltas_grupo['cnpj'] = '31179778000303'
        if cod_filial == '005':
            df_faltas_grupo['cnpj'] = '31179778000486'
        if cod_filial == '007':
            df_faltas_grupo['cnpj'] = '51816219000285'
        if cod_filial == '008':
            df_faltas_grupo['cnpj'] = '51816219000102'
        if cod_filial == '009':
            df_faltas_grupo['cnpj'] = '31179778000567'
        if cod_filial == '010':
            df_faltas_grupo['cnpj'] = '31179778000133'
        if cod_filial == '011':
            df_faltas_grupo['cnpj'] = '31179778000648'
            
        #ver dataframe de faltas
        ver_df_faltas_grupo = st.checkbox('Ver dataframe')
        if ver_df_faltas_grupo:
            st.write(df_faltas_grupo)
            
        #filtros avançados
        df_faltas_smartped = df_faltas_grupo
        
        #comprar por filtros avançados (laboratórios)
        filtro_avançado = st.selectbox('Selecione o filtro avançado', [
            'Nenhum filtro avançado',
            'Comprar por laboratório',
            'Comprar por descrição',
            ])
        if filtro_avançado == 'Comprar por laboratório':
            lst_labs = st.multiselect('laboratorios',df_faltas_smartped['laboratorio'].unique())
            df_faltas_smartped = df_faltas_smartped.query("laboratorio in @lst_labs")
        
        if filtro_avançado == 'Comprar por descrição':
            txt_descricao = st.text_input('qual descrição quer filtrar?',)
            df_faltas_smartped = df_faltas_smartped.query("produto.str.contains('@txt_descricao')")
            
        #comprar por curva
        curvas = st.multiselect('Selecione as curvas',['A / Q','B / Q','C / Q','D / Q'])
        if curvas != None:
            df_faltas_smartped = df_faltas_smartped.query("curva in @curvas")
        
        #comprar somente zerados
        somente_zerados = st.checkbox('somente zerados')
        if somente_zerados:
            df_faltas_smartped = df_faltas_smartped.query("estoque == 0")
        
        #retirar envelopes
        retirar_envelopes = st.checkbox('retirar envelopes')
        if retirar_envelopes:
            df_faltas_smartped = df_faltas_smartped.query("produto.str.contains('ENV') == False")
            
        tipo_compras = st.selectbox('Selecione o tipo da compra:',['Estoque mínimo','Demanda'],)
        
        #compras por estoque mínimo
        if tipo_compras == 'Estoque mínimo':
            df_faltas_smartped['comprar'] = df_faltas_smartped['estoque_minimo'] - df_faltas_smartped['estoque']
            df_faltas_smartped = df_faltas_smartped.query("comprar > 0")
        #compras por Demanda
        if tipo_compras == 'Demanda':
            df_faltas_smartped['comprar'] = df_faltas_smartped['demanda'] - df_faltas_smartped['estoque']
            df_faltas_smartped = df_faltas_smartped.query("comprar > 0")
                
                
        df_faltas_smartped = df_faltas_smartped[['cnpj','produto','laboratorio','ean','comprar','preco_custo','curva']]
        st.write(df_faltas_smartped)
        
        df_pedido = df_faltas_smartped
        df_pedido['custo_total'] = df_pedido['comprar'] * df_pedido['preco_custo']
        valor_pedido = df_pedido['custo_total'].sum()
        st.warning(f'O valor estimado para esse pedido é de R$ {valor_pedido:.2f}')
        