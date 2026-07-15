from flask import Blueprint, render_template, redirect, url_for, session, flash, g, abort
from models.order import Order
from services.order_services import cancelar_compra, OrderError

orders_bp = Blueprint("orders", __name__)

def _login_obrigatorio():
    if not g.user_atual.is_authenticated:
        flash("Entre na sua conta para continuar.", "error")
        return redirect(url_for("auth.login"))
    return None

@orders_bp.route("/pedidos")
def listar():
    redirecionar = _login_obrigatorio()
    if redirecionar:
        return redirecionar
    pedidos = Order.listar_por_usuario(g.user_atual.id)
    return render_template("orders/orders.html", pedidos=pedidos)

@orders_bp.route("/pedidos/<int:pedido_id>")
def detalhes(pedido_id):
    redirecionar = _login_obrigatorio()
    if redirecionar:
        return redirecionar
    pedido = Order.buscar_por_id(pedido_id, g.user_atual.id)
    if not pedido:
        abort(404)
    return render_template("orders/orders_details.html", pedido=pedido)

@orders_bp.route("/pedidos/<int:pedido_id>/cancelar", methods=["POST"])
def cancelar(pedido_id):
    redirecionar = _login_obrigatorio()
    if redirecionar:
        return redirecionar
    try:
        cancelar_compra(pedido_id, g.user_atual.id)
        flash("Pedido cancelado.", "success")
    except OrderError as erro:
        flash(str(erro), "error")
    return redirect(url_for("orders.detalhes", pedido_id=pedido_id))