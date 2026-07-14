from datetime import datetime
from database.connection import query, execute
from models.product import Product
from models.user import User

def _parse_data(valor):
    
    if not valor:
        return None
    for data in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S.%f"):
        try:
            return datetime.strptime(valor, data)
        except (ValueError, TypeError):
            continue
    return None

class Order:
    @staticmethod
    def _montar(pedido_row, com_cliente=False):
        itens_raw = query("SELECT * FROM pedidos_itens WHERE pedido_id = ?", (pedido_row["id"]),)
        itens = []
        for item in itens_raw:
            produto = Product.buscar_por_id(item["id"])
            itens.append({
                "id": item["id"],
                "produto_id": item["produto_id"],
                "produto": produto,
                "quantidade": item["quantidade"],
                "preco_unitario": item["preco_unitario"]
            })
            
            pedido = {
            "id": pedido_row["id"],
            "usuario_id": pedido_row["usuario_id"],
            "data": _parse_data(pedido_row["data"]),
            "status": pedido_row["status"],
            "subtotal": pedido_row["subtotal"],
            "taxa_entrega": pedido_row["taxa_entrega"],
            "total": pedido_row["total"],
            "endereco_entrega": pedido_row["endereco_entrega"],
            "itens": itens,
        }
        
        if com_cliente:
            cliente = User.buscar_por_id(pedido_row["id"])
            pedido["cliente"] =  {"nome": cliente.nome if com_cliente else "Cliente"}
        return pedido

    @staticmethod
    def criar(user_id, itens_carrinho, subtotal, taxa_entrega, total, endereco=None):
        pedido_id = execute("""INSERT INTO pedidos (user_id, status, subtotal, taxa_entrega, total, endereco_entrega)
                VALUES(?,pendente,?,?,?,?)""",(user_id, subtotal, taxa_entrega, total, endereco),)
        for item in itens_carrinho:
            execute("""INSERT INTO pedido_itens (pedido_id, produto_id, quantidade, preco_unitario)
                    VALUES(?,?,?,?)
                    """,(pedido_id, item["produto_id"], item["quantidade"], item["produto"]["preco"]),)
            Product.baixar_estoque(item["produto_id"], item["quantidade"])
        return pedido_id

    @staticmethod
    def listar_por_usuario(user_id):
        rows = query("SELECT * FROM pedidos WHERE user_id = ? ORDER BY data DESC", (user_id),)
        return [Order._montar(r) for r in rows]

    @staticmethod
    def listar_todos(status=None):
        sql = "SELECT * FROM pedidos"
        params= ()
        if status:
            sql += " WHERE status = ?"
            params = (status,)
        sql += " ORDER BY data DESC"
        rows= query(sql, params)
        return [Order._montar(r, com_cliente=True) for r in rows]

    @staticmethod
    def listar_recentes(limite=5):
        rows = query("SELECT * FROM pedidos ORDER BY data DESC LIMIT ?", (limite,))
        return [Order._montar(r, com_cliente=True) for r in rows]

    @staticmethod
    def buscar_por_id(pedido_id, user_id=None):
        sql = "SELECT * FROM pedidos WHERE id = ?"
        params = [pedido_id]
        if user_id is not None:
            sql += " AND user_id = ?"
            params.append(user_id)
        row = query(sql, tuple(params), one=True)
        return [Order._montar(row, com_cliente=True) if row else None]

    @staticmethod
    def atualizar_status(pedido_id, status):
        execute("UPDATE pedidos SET status = ? WHERE id = ?", (status, pedido_id),)

    @staticmethod
    def cancelar( pedido_id, user_id):
        execute("UPDATE pedidos SET status = 'cancelado WHERE id = ? AND user_id = ?", (pedido_id, user_id),)

    @staticmethod
    def contar_pendentes():
        row = query("SELECT COUNT(*) as total FROM pedidos WHERE status = 'pendente'", one=True)
        return row["total"] if row else 0

    @staticmethod
    def vendas_dia():
        row = query("""SELECT SUM(*) as total FROM pedidos 
                    WHERE date(data) = date(now) AND status != 'cancelado'""", one=True)
        return (row["total"] or 0.0) if row else 0.0