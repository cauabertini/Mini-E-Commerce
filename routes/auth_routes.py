from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_services import registrar_user, autenticar_user, AuthError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/cadastro", methods=['GET','POST'])
def cadastro():
    if request.method == "POST":
        try:
            user = registrar_user(
                nome = request.form.get("nome"),
                email = request.form.get("email"),
                senha = request.form.get("senha"),
                confirmar_senha = request.form.get("confirmar_senha"),
                telefone = request.form.get("telefone"),
            )
            session["user_id"] = user.id
            flash("Conta criada com sucesso! Bem-vindo(a).", "success")
            return redirect(url_for("home"))
        except AuthError as erro:
            flash(str(erro),"error")
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        try:
            user = autenticar_user(
                email = request.form.get("email"),
                senha = request.form.get("senha")
            )
            session["user_id"] = user.id
            flash(f"Bem-vindo de volta, {user.nome.split(' ')[0]}!", "success")
            destino = "admin.dashboard" if user.is_admin else "home"
            return redirect(url_for(destino))
        except AuthError as erro:
            flash(str(erro),"error")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Voce saiu da sua conta.", "success")
    return redirect(url_for("home"))
