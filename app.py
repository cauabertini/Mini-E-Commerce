#python -m venv venv ou python3 -m venv venv
#source -m venv venv
#pip install flask
from flask import Flask, render_template, g, session
from config import Config
from database.connection import init_db
from models.user import User, AnonymousUser
from models.product import Product
from models.cart import Cart
from routes.auth_routes import auth_bp
from routes.products_routes import products_bp
from routes.cart_routes import cart_bp
from routes.order_routes import orders_bp
from routes.admin_routes import admin_bp

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)
    app.register_blueprint(auth_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(admin_bp)

    @app.before_request
    def carregar_usuario_atual():
        user_id = session.get("user_id")
        g.user_atual = User.buscar_por_id(user_id) if user_id else AnonymousUser()

    @app.context_processor
    def injetar_contexto_global():
        cart_count = 0
        if g.user_atual.is_authenticated:
            cart_count = Cart.contar_itens(g.user_atual.id)
        return {"Usuario Atual": g.user_atual, "Cart Count": cart_count}

    @app.route("/")
    def home():
        produtos_destaque = Product.destaques(8)
        return render_template("index.html", produtos_destaque=produtos_destaque)

    with app.app_context():
        init_db()
        
        if not User.email_existe("admin@pastorao.com"):
            User.criar(nome="admin", email="admin@pastorao.com", senha="#Admin123", is_admin=True)
        _seed_produtos_demo()

    return app

def _seed_produtos_demo():
    if Product.contar_total() > 0:
        return
    produtos_demo = [
        dict(nome="Banana prata (kg)", categoria="hortifruti", preco=6.49, estoque=40,
             peso="1kg", descricao_curta="Doce e fresquinha.", destaque=True, desconto=10),
        dict(nome="Pão francês (unidade)", categoria="padaria", preco=0.99, estoque=120,
             peso="unidade", descricao_curta="Assado toda manhã.", destaque=True),
        dict(nome="Picanha bovina (kg)", categoria="acougue", preco=59.90, estoque=15,
             peso="1kg", descricao_curta="Maturada, no ponto certo."),
        dict(nome="Suco de laranja 1L", categoria="bebidas", preco=8.50, estoque=30,
             peso="1L", descricao_curta="Natural, sem conservantes.", destaque=True),
        dict(nome="Detergente neutro 500ml", categoria="limpeza", preco=2.99, estoque=4,
             peso="500ml", descricao_curta="Rende bastante."),
        dict(nome="Arroz tipo 1 (5kg)", categoria="mercearia", preco=24.90, estoque=25,
             peso="5kg", descricao_curta="Graos selecionados.", destaque=True),
    ]
    for dados in produtos_demo:
        Product.criar(dados)

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)