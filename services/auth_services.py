from models.user import User
import re

class AuthError(Exception):
    pass

def registrar_user(nome, email, senha, confirmar_senha, telefone):
    nome = (nome or "").strip()
    email = (email or "").strip().lower()
    
    if not nome or not email:
        raise AuthError("Preencha os campos obrigatórios.")
    if len(senha) < 6:
        raise AuthError("A senha precisa ter pelo menos 6 caracteres.")
    if not re.search(r"[A-Z]", senha):
        raise AuthError("A senha deve conter pelo menos uma letra maiúscula.")
    if not re.search(r"[a-z]", senha):
        raise AuthError("A senha deve conter pelo menos uma letra minúscula.")
    if not re.search(r"\d", senha):
        raise AuthError("A senha deve conter pelo menos um número.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
        raise AuthError("A senha deve conter pelo menos um caractere especial.")
    if senha != confirmar_senha:
        raise AuthError("As senhas não se coincidem.")
    if User.email_existe(email):
        raise AuthError("O email já está cadastrado.")
    return User.criar(nome=nome, email=email, senha=senha, telefone=telefone)

def autenticar_user(email, senha):
    email = (email or "").strip().lower()
    user = User.buscar_por_email(email)
    if not user or not user.check_password(senha):
        raise AuthError("Email ou senha inválidos.")
    return user