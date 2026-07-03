from werkzeug.security import generate_password_hash, check_password_hash
from database.connection import query, execute

class User:
    def __init__(self, row):
        self.id = row["id"]
        self.nome = row["nome"]
        self.email = row["email"]
        self.telefone = row["telefone"]
        self.senha_hash = row["senha_hash"]
        self.is_admin = bool(row["is_admin"])
        self.criado_em = row["criado_em"]
        
    @property
    def is_authenticated(self):
        return True
    
    def check_password(self, senha):
        return check_password_hash(self.senha_hash, senha)
    
    @staticmethod
    def criar(nome, email, senha, telefone=None, is_admin= False):
        senha_hash= generate_password_hash(senha)
        novo_id = execute("""INSERT INTO users (nome, email, senha_hash, telefone, is_admin) 
                          VALUES(?,?,?,?,?)""",
                          (nome, email, senha_hash, telefone, 1 if is_admin else 0))
        return User.buscar_por_id(novo_id)
    
    @staticmethod
    def buscar_por_id(user_id):
        row = query("SELECT * FROM users WHERE id=?", (user_id,), one=True)
        return User(row) if row else None
    
    @staticmethod
    def buscar_por_email(email):
    
        row = query("SELECT * FROM users WHERE email = ?", (email,), one=True)
        return User(row) if row else None
    
    @staticmethod
    def email_existe(email):
        return User.buscar_por_email(email) is not None
    
    class AnonymousUser:
        id = None
        nome = "Visitante"
        is_admin = False
        is_authenticated = False