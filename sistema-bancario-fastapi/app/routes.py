from fastapi import APIRouter
from app.schemas import Item

router = APIRouter()

@router.get("/itens")
def listar_itens():
    return {"mensagem": "Lista de itens"}

@router.post("/itens")
def criar_item(item: Item):
    return {"mensagem": "Item recebido com sucesso!", "dados": item}