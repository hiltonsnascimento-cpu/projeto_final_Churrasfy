import sqlite3
import pandas as pd

# ============================================================
# CONFIGURAÇÃO DO BANCO
# ============================================================

NOME_BANCO = "churrasfy.db"
# ============================================================
# CONEXÃO COM O BANCO
# ============================================================
def conectar():
    """
    Cria e retorna uma conexão com o banco SQLite.
    """

    conexao = sqlite3.connect(NOME_BANCO)

    return conexao

# ============================================================
# CRIAÇÃO DA TABELA
# ============================================================
def criar_tabela():
    """
    Cria a tabela de compras caso ela ainda não exista.
    """

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            categoria TEXT NOT NULL,
            estabelecimento TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            valor REAL NOT NULL,
            data_compra TEXT NOT NULL
        )
    """)

    conexao.commit()

    conexao.close()

# ============================================================
# INSERIR NOVA COMPRA
# ============================================================

def inserir_registro(
    produto,
    categoria,
    estabelecimento,
    quantidade,
    valor,
    data_compra
):
    """
    Insere uma nova compra no banco.
    """
    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute("""
        INSERT INTO compras
        (
            produto,
            categoria,
            estabelecimento,
            quantidade,
            valor,
            data_compra
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        produto,
        categoria,
        estabelecimento,
        quantidade,
        valor,
        data_compra
    ))

    conexao.commit()

    conexao.close()

# ============================================================
# LISTAR TODOS OS REGISTROS
# ============================================================
def listar_registros():
    """
    Retorna todas as compras cadastradas
    em um DataFrame do Pandas.
    """
    conexao = conectar()

    df = pd.read_sql_query(
        """
        SELECT
            id,
            produto,
            categoria,
            estabelecimento,
            quantidade,
            valor,
            data_compra
        FROM compras
        ORDER BY id DESC
        """,
        conexao
    )

    conexao.close()

    return df

# ============================================================
# EXCLUIR REGISTRO PELO ID
# ============================================================
def excluir_registro(id_compra):
    """
    Exclui uma compra pelo ID.
    """

    conexao = conectar()

    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM compras WHERE id = ?",
        (id_compra,)
    )

    conexao.commit()

    conexao.close()