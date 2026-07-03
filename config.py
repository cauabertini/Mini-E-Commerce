import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY não definida no .env")
    
    DATABASE = os.path.join(BASE_DIR, "database", "mercado.db")

    TAXA_ENTREGA = 6.90

    FRETE_GRATIS_ACIMA_DE = 80.00
    