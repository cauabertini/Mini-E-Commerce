from flask import Blueprint, render_template, request, redirect, url_for, flash, g, abort
from models.product import Product
from models.order import Order
from services.order_services import atualizar_status_pedido, OrderError

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.before_request
def exigir_admin():
    if not g.user_atual.is_authenticated:
        flash("Entre na sua conta para acessar o painel.", "error")
        return redirect(url_for("auth.login"))
    if not g.user_atual.is_admin:
        abort(403)

@admin_bp.route("/dashboard")
def dashboard():
    estatisticas = {
        "vendas_hoje": Order.vendas_de_hoje(),
        "variacao_vendas": 0,
        "pedidos_pendentes": Order.contar_pendentes(),
        "total_produtos": Product.contar_total(),
        "estoque_baixo": Product.contar_estoque_baixo(),
    }
    pedidos_recentes = Order.listar_recentes(5)
    return render_template("admin/dashboard.html", estatisticas=estatisticas, pedidos_recentes=pedidos_recentes)

@admin_bp.route("/produtos")
def produtos():
    lista = Product.listar()
    return render_template("admin/products.html", produtos=lista)

@admin_bp.route("/produtos/novo", methods=["GET", "POST"])
def novos_produtos():
    if request.method == "POST":
        dados = _dados_produto_do_form()
        Product.criar(dados)
        flash("Produto criado com sucesso.", "sucess")
        return redirect(url_for("admin.produtos"))
    return render_template("products/add_product.html", produto=None)

@admin_bp.route("/produtos/<int:produto_id>/editar", methods=["GET", "POST"])
def editar_produto(produto_id):
    produto = Product.buscar_por_id(produto_id)
    if not produto:
        abort(404)
    if request.method == "POST":
        dados = _dados_produto_do_form()
        Product.atualizar(produto, dados)
        flash("Produto atualizado com sucesso", "sucess")
        return redirect(url_for("admin.produtos"))
    return render_template("products/add_product.html", produto=produto)

@admin_bp.route("/produtos/<int:produto_id>/excluir", methods=["POST"])
def excluir(produto_id):
    Product.excluir(produto_id)
    flash("Produto excluido com sucesso.", "sucess")
    return redirect(url_for("admin.produtos"))

@admin_bp.route("/pedidos")
def pedidos():
    status = request.form.get("status") or None
    lista = Order.listar_todos(status=status)
    return render_template("admin/orders.html", pedidos=lista)

@admin_bp.route("/pedidos/<int:pedido_id>/status", methods=["POST"])
def status(pedido_id):
    try:
        Order.atualizar_status(pedido_id, request.form.get("status"))
        flash("Status do pedido atualizado com sucesso.", "sucess")
    except OrderError as erro:
        flash(str(erro), "error")
    return redirect(url_for("admin.pedidos"))

def _dados_produto_do_form():
    return {
        "nome": request.form.get("nome"),
        "categoria": request.form.get("categoria"),
        "preco": float(request.form.get("preco", 0) or 0),
        "preco_antigo": float(request.form["preco_antigo"]) if request.form.get("preco_antigo") else None,
        "estoque": int(request.form.get("estoque", 0) or 0),
        "peso": request.form.get("peso"),
        "imagem": request.form.get("imagem"),
        "descricao": request.form.get("descricao"),
        "descricao_curta": request.form.get("descricao_curta"),
        "destaque": bool(request.form.get("destaque")),
        "desconto": int(request.form["desconto"]) if request.form.get("desconto") else None,
    }