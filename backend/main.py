from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from logica import exibir_produtos, atualizar_preco, atualizar_quantidade, inserir_produtos, deletar_produto, registrar_compra, abastecer_produto, exibir_clientes, inserir_clientes

# Conexao do app
app = FastAPI()

# Schemas
class ProdutoSchema(BaseModel):
    nome: str
    preco: float
    quantidade: int
    
class PrecoSchema(BaseModel):
    id:int
    preco: float
    
class QuantidadeSchema(BaseModel):
    id: int
    quantidade: int

class AtualizarSchema(BaseModel):
    nome: str
    quantidade_alterada: int

class CompraSchema(BaseModel):
    nome_cliente: str
    nome_produto: str
    quantidade_comprada: int = Field(..., gt=0, description="Quantidade deve ser maior que zero")
    email: str = "nao_informado@email.com"
    senha: str = "123456"
class ClienteSchema(BaseModel):
    nome: str
    email: str
    senha: str

# ROTAS

# POST / main/inserir_produtos_em_lote
@app.post("/main/inserir_produtos/lote")
def inserir_produtos_em_lote(dados: List[ProdutoSchema]):
    try:
        dados_formatados = [
            (dado.nome, dado.preco, dado.quantidade) for dado  in dados
        ]
        inserir_produtos(dados_formatados)
        return {"mensagem": f"{len(dados_formatados)} produtos inseridos com sucesso!"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir produtos: {exc}")

# POST / main/inserir_clientes_em_lote
@app.post("/main/inserir_clientes/lote")
def inserir_clientes_em_lote(dados: List[ClienteSchema]):
    try:
        dados_formatados = [
            (dado.nome, dado.email, dado.senha) for dado in dados
        ]
        inserir_clientes(dados_formatados)
        return {"mensagem": f"{len(dados_formatados)} clientes inseridos com sucesso!"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir clientes: {exc}")

# GET / estoque
@app.get("/main/estoque")
def exibir_estoque():
    return exibir_produtos()

# GET / clientes
@app.get("/main/clientes")
def exibir_dados_clientes():
    return exibir_clientes()

# PATCH / main/atualizar_preco/{id}
@app.patch("/main/atualizar_preco/{id}")
def atualizar_preco_por_id(dados: PrecoSchema):
    try:
        atualizar_preco(dados.id, dados.preco)
        return {"mensagem": "Preço atualizado com sucesso!"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail= f"Erro ao atualizar preço {exc}")

# PATCH / main/atualizar_quantidade/{id}
@app.patch("/main/atualizar_quantidade/{id}")
def atualizar_quantidade_por_id(dados: QuantidadeSchema):
    try:
        atualizar_quantidade(dados.id, dados.quantidade)
        return {"mensagem": "Quantidade atualizada com sucesso!"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar quantidade {exc}")
    
# PATCH / main/comprar_produto/{nome}
@app.patch("/main/comprar_produto/{nome}")
def comprar_produto_por_nome(dados: CompraSchema):
    try:
        registrar_compra(dados.nome_cliente, dados.nome_produto, dados.quantidade_comprada, dados.email, dados.senha)
        return {"mensagem": "Compra realizada com sucesso"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao comprar produto: {exc}")

# PATCH / main/abastecer_produto/{nome}
@app.patch("/main/abastecer_produto/{nome}")
def abastecer_produto_por_nome(dados: AtualizarSchema):
    try:
        abastecer_produto(dados.nome, dados.quantidade_alterada)
        return {"mensagem": "Abastecimento realizado com sucesso"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao abastecer produto: {exc}")
# DELETE / main/deletar_produto/{id}
@app.delete("/main/deletar_produto/{id}")
def deletar_produto_por_id(id: int):
    try:
        deletar_produto(id)
        return {"mensagem": f"Produto com id {id} deletado com sucesso!"}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro ao deletar produto: {exc}")

