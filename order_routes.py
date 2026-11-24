from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao, verificar_token
from sqlalchemy.orm import Session
from schemas import PedidoSchema
from models import Pedido, Usuario

order_router = APIRouter(prefix="/order", tags=["order"], dependencies = [Depends(verificar_token)])

@order_router.get("/") # decorator
async def order():
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação.
    """
    return {"mensagem": "Você acessou a rota de pedidos!"}

@order_router.post("/create_order")
async def create_order(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):
    novo_pedido = Pedido(usuario=pedido_schema.id_usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso. ID do pedido: {novo_pedido.id}"}

@order_router.post("/order/cancel/{id_pedido}")
async def cancel_order(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=401, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    pedido.status = "CANCELADO"
    session.commit()
    return {
        "mensagem": f"Pedido numero {pedido.id} cancelado com sucesso",
        "pedido": pedido
    }