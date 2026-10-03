
import streamlit as st
import pandas as pd

from banco import (
    conectar,
    criar_tabela,
    inserir_registro,
    listar_registros,
    excluir_registro
)


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Churrasfy - Análise de Compras",
    page_icon="🥩",
    layout="wide"
)


# ============================================================
# CONEXÃO COM O BANCO
# ============================================================

@st.cache_resource
def obter_conexao():
    """
    Mantém a conexão com o banco utilizando
    o cache de recursos do Streamlit.
    """
    return conectar()


# Inicializa a conexão
conexao = obter_conexao()

# Cria a tabela caso ela ainda não exista
criar_tabela()


# ============================================================
# TÍTULO
# ============================================================

st.title("🥩 Churrasfy")
st.subheader("Sistema de Cadastro e Análise de Compras para Churrasco")

st.write(
    "Cadastre os produtos comprados para seus churrascos "
    "e acompanhe os gastos através de indicadores e gráficos."
)


# ============================================================
# FORMULÁRIO DE CADASTRO
# ============================================================

st.header("➕ Cadastro de Compra")

with st.form("formulario_cadastro"):

    col1, col2 = st.columns(2)

    with col1:

        produto = st.text_input(
            "Produto *",
            placeholder="Ex: Picanha"
        )

        categoria = st.selectbox(
            "Categoria *",
            [
                "Carnes",
                "Bebidas",
                "Pães",
                "Carvão",
                "Outros"
            ]
        )

        estabelecimento = st.text_input(
            "Estabelecimento *",
            placeholder="Ex: Atacadão"
        )

    with col2:

        quantidade = st.number_input(
            "Quantidade *",
            min_value=1,
            step=1
        )

        valor = st.number_input(
            "Valor total da compra *",
            min_value=0.01,
            step=10.00,
            format="%.2f"
        )

        data_compra = st.date_input(
            "Data da compra *"
        )

    enviar = st.form_submit_button(
        "💾 Cadastrar compra"
    )


# ============================================================
# VALIDAÇÃO E INSERÇÃO
# ============================================================

if enviar:

    if produto.strip() == "":
        st.error("Informe o nome do produto.")

    elif estabelecimento.strip() == "":
        st.error("Informe o estabelecimento.")

    elif quantidade <= 0:
        st.error("A quantidade deve ser maior que zero.")

    elif valor <= 0:
        st.error("O valor deve ser maior que zero.")

    else:

        inserir_registro(
            produto,
            categoria,
            estabelecimento,
            quantidade,
            valor,
            str(data_compra)
        )

        st.success("Compra cadastrada com sucesso!")

        st.rerun()


# ============================================================
# LEITURA DOS DADOS
# ============================================================

df = listar_registros()


# ============================================================
# VERIFICA SE EXISTEM DADOS
# ============================================================

if df.empty:

    st.info(
        "Ainda não existem compras cadastradas. "
        "Utilize o formulário acima para cadastrar a primeira compra."
    )

else:

    # ========================================================
    # FILTROS
    # ========================================================

    st.header("🔎 Filtros")

    col1, col2 = st.columns(2)

    with col1:

        categorias = ["Todas"] + sorted(
            df["categoria"].unique().tolist()
        )

        filtro_categoria = st.selectbox(
            "Filtrar por categoria",
            categorias
        )

    with col2:

        valor_maximo = float(df["valor"].max())

        filtro_valor = st.slider(
            "Valor máximo da compra",
            min_value=0.0,
            max_value=valor_maximo,
            value=valor_maximo,
            step=10.0
        )


    # ========================================================
    # APLICAÇÃO DOS FILTROS
    # ========================================================

    df_filtrado = df.copy()

    if filtro_categoria != "Todas":

        df_filtrado = df_filtrado[
            df_filtrado["categoria"] == filtro_categoria
        ]

    df_filtrado = df_filtrado[
        df_filtrado["valor"] <= filtro_valor
    ]


    # ========================================================
    # MÉTRICAS
    # ========================================================

    st.header("📈 Indicadores")

    total_gasto = df_filtrado["valor"].sum()

    media_compra = df_filtrado["valor"].mean()

    quantidade_compras = len(df_filtrado)

    quantidade_itens = df_filtrado["quantidade"].sum()


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Total gasto",
            f"R$ {total_gasto:,.2f}"
        )

    with col2:
        st.metric(
            "📊 Média por compra",
            f"R$ {media_compra:,.2f}"
        )

    with col3:
        st.metric(
            "🛒 Nº de compras",
            quantidade_compras
        )

    with col4:
        st.metric(
            "📦 Itens comprados",
            quantidade_itens
        )


    # ========================================================
    # TABELA
    # ========================================================

    st.header("📋 Compras cadastradas")

    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True
    )


    # ========================================================
    # GRÁFICO 1
    # TOTAL GASTO POR CATEGORIA
    # ========================================================

    st.header("📊 Análises")

    gastos_categoria = (
        df_filtrado
        .groupby("categoria")["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("💰 Total gasto por categoria")

    st.bar_chart(gastos_categoria)


    # ========================================================
    # GRÁFICO 2
    # TOTAL GASTO POR ESTABELECIMENTO
    # ========================================================

    gastos_estabelecimento = (
        df_filtrado
        .groupby("estabelecimento")["valor"]
        .sum()
        .sort_values(ascending=False)
    )

    st.subheader("🏪 Total gasto por estabelecimento")

    st.bar_chart(gastos_estabelecimento)


    # ========================================================
    # EXCLUSÃO
    # ========================================================

    st.header("🗑️ Excluir compra")

    ids_disponiveis = df["id"].tolist()

    id_excluir = st.selectbox(
        "Selecione o ID da compra que deseja excluir",
        ids_disponiveis
    )

    if st.button("🗑️ Excluir compra"):

        excluir_registro(id_excluir)

        st.success(
            f"Compra de ID {id_excluir} excluída com sucesso!"
        )

        st.rerun()

