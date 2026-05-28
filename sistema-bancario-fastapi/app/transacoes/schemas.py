from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import datetime

class TransacaoCriar(BaseModel):
    tipo: Literal["deposito", "saque"]
    valor: float = Field(..., description="O valor deve ser maior que zero")

    # Validação do Pydantic para impedir valores negativos ou zerados
    @field_validator("valor")
    def validar_valor_positivo(cls, v):
        if v <= 0:
            raise ValueError("O valor da operação deve ser maior que zero.")
        return v

class TransacaoResponse(BaseModel):
    tipo: str
    valor: float
    data: datetime

class ExtratoResponse(BaseModel):
    saldo_atual: float
    transacoes: list[TransacaoResponse]