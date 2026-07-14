from flask import current_app
from models.cart import Cart
from models.order import Order
class OrderError(Exception):
    pass

def finalizar_compra(user_id, endereco_entrega=None):
    itens = Cart.listar_itens(user_id)
    if not itens:
        raise OrderError("Seu carrinho está vazio.")
    for item in itens:
        if item["produto"]["estoque"] is not None and item["quantidade"] > item["produto"]["estoque"]:
            raise OrderError(f"Estoque insuficiente para {item['produto']['nome']}.")
    taxa_entrega = current_app.config.get("TAXA_ENTREGA", 0.0)
    frete_gratis = current_app.config.get("FRETE_GRATIS_ACIMA_DE")
    subtotal, entrega, total = Cart.calcular_totais(itens, taxa_entrega, frete_gratis) 
    pedido_id = Order.criar(user_id, itens, subtotal, entrega, total, endereco_entrega)
    Cart.limpar(user_id)
    return pedido_id

def cancelar_compra(pedido_id, user_id):
    pedido = Order.buscar_por_id(pedido_id, user_id)
    if not pedido:
        raise OrderError("Pedido não encontrado.")
    if pedido["status"] in ("entregue", "cancelado"):
        raise OrderError("Este pedido não pode mais ser cancelado.")
    Order.cancelar(pedido_id, user_id)

def atualizar_status_pedido(pedido_id, status):
    status_validos =  {"pendente", "preparando", "enviado", "entregue", "cancelado"}
    if status not in status_validos:
        raise OrderError("Status inválido.")
    Order.atualizar_status(pedido_id, status)