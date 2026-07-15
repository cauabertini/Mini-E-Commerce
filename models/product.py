from database.connection import query, execute

class Product:
    def __init__(self, row):
        self.nome = row["nome"]
        self.categoria = row["categoria"]
        self.preco = row["preco"]
        self.preco_antigo = row["preco_antigo"]
        self.estoque = row["estoque"]
        self.peso = row["peso"]
        self.imagem = row["imagem"]
        self.descricao = row["descricao"]
        self.descicao_curta = row["descricao_curta"]
        self.destaque = row["destaque"]
        self.criado_em = row["criado_em"]
    
    @staticmethod
    def listar(categoria=None, busca=None):
        sql="SELECT * FROM produtos WHERE 1=1"
        params=[]
        if categoria:
            sql += " AND categoria = ?"
            params.append(categoria)
        if busca:
            sql+= " AND nome LIKE ?"
            params.append(f"%{busca}%")
        sql += " ORDER BY nome ASC"
        return query(sql, tuple(params))

    @staticmethod
    def destaques(limite=8):
        return query("SELECT * FROM produtos WHERE destaque = 1 ORDER BY id DESC LIMIT ?",(limite,),)
    
    @staticmethod
    def buscar_por_id(produto_id):
        return query("SELECT * FROM produtos WHERE id =?",(produto_id,), one=True)
    
    @staticmethod
    def relacionados(categoria, excluir_id, limite=4):
        return query("""SELECT * FROM produtos
                     WHERE categoria = ? AND id != ?
                     ORDER BY RANDOM() LIMIT ?""",
                     (categoria, excluir_id, limite,))
    
    @staticmethod
    def criar(dados):
        return execute("""INSERT INTO produtos
            (nome, categoria, preco, preco_antigo, estoque, peso,
            imagem, descricao, descricao_curta, destaque, desconto)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
            (dados["nome"], dados["categoria"], dados["preco"],
            dados.get("preco_antigo"), dados.get("estoque"), dados.get("peso"),
            dados.get("imagem"), dados.get("descricao"), dados.get("descricao_curta"),
            1 if dados.get("destaque") else 0, dados.get("desconto"),),)
        
    @staticmethod
    def atualizar(produto_id, dados):
        return execute("""UPDATE produtos SET nome = ?, categoria = ?, preco = ?,
            preco_antigo = ?, estoque = ?, peso = ?, imagem = ?, descricao = ?,
            descricao_curta = ?, destaque = ?, desconto = ? WHERE id = ?""",
            (dados["nome"], dados["categoria"], dados["preco"],
            dados.get("preco_antigo"), dados["estoque"], dados.get("peso"),
            dados.get("imagem"), dados.get("descricao"), dados.get("descricao_curta"),
            1 if dados.get("destaque") else 0, dados.get("desconto"), produto_id,),)
    
    @staticmethod
    def excluir(produto_id):
        return execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    
    @staticmethod
    def baixar_estoque(produto_id, quantidade):
        return execute("UPDATE produtos SET estoque = estoque - ? WHERE id = ?",(quantidade, produto_id),)
    
    @staticmethod
    def contar_abaixo_estoque(limite=5):
        row = query("SELECT COUNT(*) as total FROM produtos WHERE estoque < ?",(limite,), one=True)
        return row["total"] if row else 0
    
    @staticmethod
    def contar_total():
        row = query("SELECT COUNT(*) as total FROM produtos", one=True)
        return row["total"] if row else 0