from flask import Blueprint, render_template, request, abort
from models.product import Product

products_bp = Blueprint("products", __name__)

@products_bp.route("/produtos")
def listar():
    categoria = request.args.get("categoria")
    busca = request.args.get("busca")
    produtos = Product.listar(categoria=categoria, busca=busca)
    return render_template("products/products.html", produtos=produtos)

@products_bp.route("/produtos/<int:produto_id>")
def detalhes(produto_id):
    produto = Product.buscar_por_id(produto_id)
    if not produto:
        abort(404)
    produtos_relacionados = Product.relacionados(produto["categoria"], produto_id)
    return render_template("products/products_details.html", produto=produto, produtos_relacionados=produtos_relacionados)