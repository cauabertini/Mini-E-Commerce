# 🛒 Pastorão — Mini Mercado

Aplicação web de e-commerce para um mini mercado de bairro, desenvolvida com **Flask** e **SQLite**. Permite que clientes naveguem por produtos, adicionem ao carrinho e finalizem pedidos, enquanto administradores gerenciam o estoque e acompanham os pedidos pelo painel.

---

## Funcionalidades

- Cadastro e login de usuários com senha em hash (`werkzeug.security`)
- Catálogo de produtos com filtro por categoria e busca
- Carrinho de compras persistente por usuário
- Checkout com cálculo automático de frete (grátis acima de R$ 80,00)
- Histórico de pedidos com status em tempo real
- Painel administrativo para gerenciar produtos e pedidos
- Seed automático de produtos e usuário admin na primeira execução

---

## Tecnologias

- Python 3 + Flask
- SQLite (sem ORM — queries SQL puras)
- Werkzeug (hash de senhas)
- Jinja2 (templates)
- python-dotenv (variáveis de ambiente)

---

## Estrutura

```
├── app.py
├── config.py
├── .env                  # não versionado
├── database/
│   ├── connection.py
│   └── schema.sql
├── models/
│   ├── user.py
│   ├── product.py
│   ├── cart.py
│   └── order.py
├── services/
│   ├── auth_services.py
│   ├── cart_services.py
│   └── order_services.py
├── routes/
│   ├── auth_routes.py
│   ├── products_routes.py
│   ├── cart_routes.py
│   ├── order_routes.py
│   └── admin_routes.py
├── templates/
└── static/
```

---

## Como rodar

**1. Clone o repositório**
```bash
git clone https://github.com/cauabertini/pastorao-mini-mercado.git
cd pastorao-mini-mercado
```

**2. Crie o ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

**3. Instale as dependências**
```bash
pip install -r requirements.txt
```

**4. Configure o `.env`**
```bash
cp .env.example .env
```
Edite o `.env` e defina uma `SECRET_KEY` segura:
```
SECRET_KEY=sua-chave-aqui
```
Gere uma chave segura com:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**5. Rode a aplicação**
```bash
python app.py
```
O banco de dados e os produtos de exemplo são criados automaticamente na primeira execução.

Acesse em: `http://localhost:5000`

---

## Projeto Pessoal

Desenvolvido como projeto de e-commerce full-stack para desenvolvimento pessoal
