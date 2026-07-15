from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g
from services.cart_services import adicionar_ao_carrinho, atualizar_item, remover_item, obter_resumo, CartError
from services.order_services import finalizar_compra, OrderError

cart_bp = Blueprint("cart", __name__)

def _login_obrigatorio():
    if not g.user_atual.is_authenticated:
        flash("Entre na sua conta para continuar.", "error")
        return redirect(url_for("auth.login"))
    return None

@cart_bp.route("/carrinho", methods=["POST"])
def ver_carrinho():
    redirecionar = _login_obrigatorio()
    if redirecionar:
        return redirecionar
    itens, subtotal, taxa_entrega, total = obter_resumo(g.user_atual.id)
    return render_template(
        "cart/cart.html", itens_carrinho=itens, subtotal=subtotal, taxa_entrega=taxa_entrega, total=total,)

@cart_bp.route("/carrinho/atualizar", methods=["POST"])
def atualizar():
    redirecionar = _login_obrigatorio()
    if redirecionar:
        return redirecionar
    try:
        atualizar_item(int(request.fotm.get("item_id")), g.user_atual.id, int(request.form.get("quantidade")))
    except CartError as erro:
        flash(str(erro),"error")
    return redirect(url_for("cart.ver_carrinho"))

@cart_bp.route("/carrinho/remover", methods=["POST"])
def remover():
    redirecionar = _login_obrigatorio()
    if redirecionar:
        return redirecionar
    remover_item(int(request.form.get("item_id")), g.user_atual.id)
    flash("Item removido com sucesso.", "sucess")
    return redirect(url_for("cart.ver_carrinho"))

@cart_bp.route("/logout", methods=["GET","POST"])
def logout():
    redirecionar = _login_obrigatorio()
    if redirecionar:
        return redirecionar
    try:
        endereco = request.form.get("endereco_entrega") if request.method == "POST" else None
        pedido_id = finalizar_compra(g.user_atual.id, endereco)
        flash("Pedido realizado com sucesso!", "success")
        return redirect(url_for("orders.detalhes", pedido_id=pedido_id))
    except OrderError as erro:
        flash(str(erro), "error")
        return redirect(url_for("cart.ver_carrinho"))