from pydantic import BaseModel

class Item(BaseModel):
    nome: str
    preco: float
    em_estoque: bool = True