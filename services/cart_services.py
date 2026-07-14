from flask import current_app
from models.cart import Cart
from models.product import Product

class CartError(Exception):
    pass

def adicionar_ao_carrinho(user_id, produto_id, quantidade):
    produto = Product.buscar_por_id(produto_id)
    if not produto:
        raise CartError("Produto não encontrado.")
    if produto["estoque"] is not None and produto["estoque"] <= 0:
        raise CartError("Este produto está esgotado.")
    quantidade = max(1, int(quantidade or 1))
    Cart.adicionar(user_id, produto_id, quantidade)

def atualizar_item(item_id, user_id, quantidade):
    item = Cart.buscar_item(item_id, user_id)
    if not item:
        raise CartError("Item não encontrado no carrinho.")
    Cart.atualizar_quantidades(item_id, user_id, int(quantidade))

def remover_item(item_id, user_id):
    Cart.remover(item_id, user_id)

def obter_resumo(user_id):
    itens = Cart.listar_itens(user_id)
    taxa_entrega = current_app.config.get("TAXA_ENTREGA", 0.0)
    frete_gratis = current_app.config.get("FRETE_GRATIS_ACIMA_DE")
    subtotal, entrega, total = Cart.calcular_totais(itens, taxa_entrega, frete_gratis)
    return itens, subtotal, entrega, total

