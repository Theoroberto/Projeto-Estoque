import sqlite3
from pathlib import Path
from typing import List, Tuple, Dict

ROOT_PATH = Path(__file__).parent.parent
DATABASE_PATH = ROOT_PATH / "database"

# Criação da tabela
def conectar():
    return sqlite3.connect(DATABASE_PATH / "estoque.db")

def criar_tabela():
    conexao = conectar()
    try:
        
        with conexao:
            cursor = conexao.cursor()
            
            cursor.execute("""CREATE TABLE IF NOT EXISTS estoque(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL UNIQUE,
                preco FLOAT NOT NULL,
                quantidade POSITIVE INTEGER NOT NULL
                )""")
    except Exception as exc:
        raise exc

# Create
def inserir_produtos(data: List[Tuple]) -> None:
    conexao = conectar()
    try:
        
        with conexao:
            cursor = conexao.cursor()
            
            cursor.executemany("INSERT INTO estoque (nome, preco, quantidade) VALUES (?, ?, ?)", data)
    except Exception as exc:
        raise exc
    finally:
        conexao.close()

# Read
def exibir_produtos() -> List[Dict]:
    conexao = conectar()
    try:
        with conexao:
            cursor = conexao.cursor()
            
            cursor.execute("SELECT id, nome, preco, quantidade FROM estoque ORDER BY nome")
            linhas = cursor.fetchall()
            
            estoque = []
            for linha in linhas:
                estoque.append(
                    {
                        "id": linha[0],
                        "nome": linha[1],
                        "preco": linha[2],
                        "quantidade": linha[3]
                    }
                )
            return estoque
        
    except Exception as exc:
        raise exc

# Update
def atualizar_preco(id: int, preco: float):
    conexao = conectar()
    try:
        with conexao:
            cursor = conexao.cursor()
            
            cursor.execute("UPDATE estoque SET preco = ? WHERE id = ?", (preco, id))
    except Exception as exc:
        raise exc
        
def atualizar_quantidade(id: int, quantidade: int):
    conexao = conectar()
    try:
        with conexao:
            cursor = conexao.cursor()

            cursor.execute("UPDATE estoque SET quantidade = ? WHERE id = ?", (quantidade, id))
    except Exception as exc:
        raise exc

# Função de compra
def comprar_produto(nome: str, quantidade_comprada: int):
    conexao = conectar()
    try:
        with conexao:
            cursor = conexao.cursor()
            
            # Obtendo id e guardando em variável
            cursor.execute("SELECT id FROM estoque WHERE nome = ?", (nome,))
            produto = cursor.fetchone()
            
            # Verificando se o prodtuo está no estoque
            if not produto:
                raise ValueError("Produto não encontrado")
            
            # Correção 2: Usando id do produto para atualizar quantidade
            id_produto = produto[0]
            cursor.execute("SELECT quantidade FROM estoque WHERE nome = ?", (nome,))
            quantidade_anterior = cursor.fetchone()[0]

            # Verificando se quantidade é suficiente
            if quantidade_anterior < quantidade_comprada:
                raise ValueError("Quantidade insuficiente em estoque")

            # Atualizando quantidade
            quantidade_nova = quantidade_anterior - quantidade_comprada
            cursor.execute("UPDATE estoque SET quantidade = ? WHERE id = ?", (quantidade_nova, id_produto))
    except Exception as exc:
        raise exc

# Função de abastecimento
def abastecer_produto(nome: str, quantidade_abastecida: int):
    conexao = conectar()
    with conexao:
        cursor = conexao.cursor()
        
        # Obtendo id e guardando em variável
        cursor.execute("SELECT id FROM estoque WHERE nome = ?", (nome,))
        produto = cursor.fetchone()
        
        # Verificando se o produto está no estoque
        if not produto:
            raise ValueError("Produto não encontrado")
        
        # Obtendo quantidade anterior usando o id
        id_produto = produto[0]
        cursor.execute("SELECT quantidade FROM estoque WHERE id = ?", (id_produto,))
        quantidade_anterior = cursor.fetchone()[0]
        
        # Atualizando quantidade
        quantidade_nova = quantidade_anterior + quantidade_abastecida
        cursor.execute("UPDATE estoque SET quantidade = ? WHERE id = ?", (quantidade_nova, id_produto))

# Delete
def deletar_produto(id: int):
    conexao = conectar()
    try:
        with conexao:
            cursor = conexao.cursor()

            cursor.execute("DELETE FROM estoque WHERE id = ?", (id,))
    except Exception as exc:
        raise exc
