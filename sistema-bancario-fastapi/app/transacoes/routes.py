from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import obter_usuario_atual
from app.transacoes.schemas import TransacaoCriar, ExtratoResponse
from app.database import adicionar_transacao, buscar_transacoes, buscar_usuario
from datetime import datetime

router = APIRouter(prefix="/conta", tags=["Operações Bancárias"])

@router.post("/transacao", status_code=status.HTTP_201_CREATED)
async def realizar_transacao(
    transacao: TransacaoCriar, 
    usuario_atual: dict = Depends(obter_usuario_atual)
):
    username = usuario_atual["username"]
    
    #validacao de saldo para saques
    if transacao.tipo == "saque" and usuario_atual["saldo"] < transacao.valor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Saldo insuficiente para realizar o saque."
        )
    
    nova_transacao = {
        "tipo": transacao.tipo,
        "valor": transacao.valor,
        "data": datetime.utcnow()
    }
    
    await adicionar_transacao(username, nova_transacao)
    return {"mensagem": f"{transacao.tipo.capitalize()} realizado com sucesso!"}

@router.get("/extrato", response_model=ExtratoResponse)
async def exibir_extrato(usuario_atual: dict = Depends(obter_usuario_atual)):
    username = usuario_atual["username"]
    
    # busca o estado mais atualizado do usuario para o saldo
    usuario_atualizado = await buscar_usuario(username)
    transacoes = await buscar_transacoes(username)
    
    return {
        "saldo_atual": usuario_atualizado["saldo"],
        "transacoes": transacoes
    }