import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

def page_produto_individual()
    # Dicionário de filiais
    filiais_dict = {
        1: "Matriz", 4: "Centrinho", 5: "Calil", 7: "Rio Vermelho",
        8: "Vargem", 9: "Canasvieiras", 10: "Upa", 11: "Trindade", 12: "Palhoça"
    }

    # Conectar ao banco de dados SQLite
    def conectar_banco():
        conn = sqlite3.connect("vendas.db")
        return conn

    # Carregar dados do banco
    @st.cache_data
    def carregar_dados():
        conn = conectar_banco()
        query = "SELECT * FROM vendas"
        df = pd.read_sql(query, conn)
        conn.close()

        # ✅ Corrigir interpretação de datas
        df["data"] = pd.to_datetime(df["data"], format="%Y-%m-%d", errors="coerce")

        return df

    # Processar dados para métricas e visualização
    def calcular_metricas(df, produtos_selecionados, filiais_selecionadas):
        df_filtrado = df[df["produto"].isin(produtos_selecionados)]

        if filiais_selecionadas:
            df_filtrado = df_filtrado[df_filtrado["loja"].isin(filiais_selecionadas)]

        # Criar coluna de mês/ano corretamente
        df_filtrado["mes_ano"] = df_filtrado["data"].dt.strftime("%Y-%m")

        # Agrupar vendas por mês
        vendas_mensais = df_filtrado.groupby("mes_ano")["qtd_vendida"].sum().reset_index()

        # Agrupar preços médios por mês
        precos_mensais = df_filtrado.groupby("mes_ano")["preco_unit"].mean().reset_index()

        # Cálculo de métricas
        media_diaria = df_filtrado["qtd_vendida"].sum() / df_filtrado["data"].nunique()
        media_semanal = df_filtrado["qtd_vendida"].sum() / (df_filtrado["data"].nunique() / 7)
        media_mensal = df_filtrado.groupby("mes_ano")["qtd_vendida"].sum().mean()

        # Preço mínimo e máximo praticado
        preco_min = df_filtrado["preco_unit"].min()
        preco_max = df_filtrado["preco_unit"].max()

        return df_filtrado, vendas_mensais, precos_mensais, media_diaria, media_semanal, media_mensal, preco_min, preco_max

    # Criar gráfico de vendas mensais corrigido
    def criar_grafico_vendas(vendas_mensais):
        fig = go.Figure()

        # Barras para vendas mensais
        fig.add_trace(go.Bar(
            x=vendas_mensais["mes_ano"],
            y=vendas_mensais["qtd_vendida"],
            name="Vendas Mensais",
            marker_color="blue",
        ))

        # Linhas para médias móveis
        if len(vendas_mensais) >= 3:  # Só aplica média móvel se houver dados suficientes
            fig.add_trace(go.Scatter(
                x=vendas_mensais["mes_ano"],
                y=vendas_mensais["qtd_vendida"].rolling(window=3, min_periods=1).mean(),
                mode="lines",
                name="Média Móvel 3 Meses",
                line=dict(color="red", dash="dash"),
            ))

        fig.update_layout(
            title="📊 Vendas Mensais com Média Móvel",
            xaxis_title="Mês/Ano",
            yaxis_title="Quantidade Vendida",
            legend_title="Legenda",
            template="plotly_white"
        )

        return fig

    # Criar gráfico de preço médio mensal
    def criar_grafico_precos(precos_mensais):
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=precos_mensais["mes_ano"],
            y=precos_mensais["preco_unit"],
            mode="lines+markers",
            name="Preço Médio",
            line=dict(color="green", width=2),
        ))

        fig.update_layout(
            title="💰 Evolução do Preço Médio de Venda",
            xaxis_title="Mês/Ano",
            yaxis_title="Preço Médio (R$)",
            legend_title="Legenda",
            template="plotly_white"
        )

        return fig

    # Interface no Streamlit
    st.title("📊 Análise de Vendas por Produto")

    # Carregar dados
    df = carregar_dados()

    # Selecionar produtos
    produtos_disponiveis = df["produto"].unique().tolist()
    produtos_selecionados = st.multiselect("Selecione os produtos:", produtos_disponiveis)

    # Selecionar filiais
    filiais_selecionadas = st.multiselect("Selecione as filiais:", options=list(filiais_dict.keys()), format_func=lambda x: filiais_dict[x])

    # Gerar métricas e gráficos se houver seleção
    if produtos_selecionados:
        df_filtrado, vendas_mensais, precos_mensais, media_diaria, media_semanal, media_mensal, preco_min, preco_max = calcular_metricas(df, produtos_selecionados, filiais_selecionadas)

        # Exibir métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("📅 Média Diária de Vendas", f"{media_diaria:.2f} unid/dia")
        col2.metric("📆 Média Semanal de Vendas", f"{media_semanal:.2f} unid/semana")
        col3.metric("📅 Média Mensal de Vendas", f"{media_mensal:.2f} unid/mês")

        col4, col5 = st.columns(2)
        col4.metric("💰 Preço Mínimo", f"R$ {preco_min:.2f}")
        col5.metric("💰 Preço Máximo", f"R$ {preco_max:.2f}")

        # Exibir gráficos
        st.plotly_chart(criar_grafico_vendas(vendas_mensais), use_container_width=True)
        st.plotly_chart(criar_grafico_precos(precos_mensais), use_container_width=True)

        # Exibir DataFrame das vendas filtradas
        st.subheader("📜 Dados de Vendas Filtradas")
        st.dataframe(df_filtrado[["data", "num_venda", "codigo", "produto", "loja", "qtd_vendida", "preco_unit", "valor_total"]])

    else:
        st.warning("⚠️ Selecione pelo menos um produto para visualizar os dados.")
