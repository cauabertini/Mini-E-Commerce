from database.connection import query, execute
from models.product import Product

class Cart:
    @staticmethod
    def listar_itens(user_id):
        linhas = query("SELECT * FROM carrinho_itens WHERE user_id = ?",(user_id,))
        itens = []
        for linha in linhas:
            produto = Product.buscar_por_id(linha["produto_id"])
            if not produto:
                continue
            itens.append({
                "id": linha["id"],
                "produto_id": linha["produto_id"],
                "quantidade": linha["quantidade"],
                "produto": produto
            })
        return itens
    
    @staticmethod
    def contar_itens(user_id):
        row = query("SELECT SUM(quantidade) as total FROM carrinho_itens WHERE user_id = ?", (user_id,), one=True,)
        return (row["total"] or 0) if row else 0
    
    @staticmethod
    def buscar_item(item_id, user_id):
        return query("SELECT * FROM carrinho_itens WHERE id = ? AND user_id = ?", (item_id, user_id,), one=True,)
    
    @staticmethod
    def adicionar(user_id, produto_id, quantidade):
        existente = query("SELECT * FROM carrinho_itens WHERE user_id = ? AND produto_id = ?", (user_id, produto_id,), one=True)
        if existente:
            nova_qntd = existente["quantidade"] + quantidade
            execute("UPDATE carrinho_itens SET quantidade = ? WHERE id = ?", (nova_qntd, existente["id"]),)
            
        else:
            execute("""INSERT INTO carrinho_itens (user_id, produto_id, quantidade)
                    VALUES(?, ?, ?)""", (user_id, produto_id, quantidade),)
            
    @staticmethod
    def remover(item_id, user_id):
        return execute("DELETE FROM carrinho_itens WHERE id = ? AND user_id = ?", (item_id, user_id),)
    
    @staticmethod
    def atualizar_quantidades(item_id, user_id, quantidade):
        if quantidade <= 0:
            Cart.remover(item_id, user_id)
            return execute("UPDATE carrinho_itens SET quantidade WHERE id = ? AND user_id = ?", (quantidade, item_id, user_id),)
        
    @staticmethod
    def limpar(user_id):
        return execute("DELETE FROM carrinho_itens WHERE user_id = ?", (user_id,),)
    
    @staticmethod
    def calcular_totais(itens, taxa_entrega=0.0, frete_gratis_acima_de=None):
        subtotal = sum(item["produto"]["preco"] * item["quantidade"] for item in itens)
        entrega = taxa_entrega
        if frete_gratis_acima_de is not None and subtotal >= frete_gratis_acima_de:
            entrega = 0.0
        total = subtotal + entrega
        return subtotal, entrega, total
