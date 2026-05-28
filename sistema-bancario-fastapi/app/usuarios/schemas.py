from pydantic import BaseModel, Field

class UsuarioCriar(BaseModel):
    username: str = Field(..., description="Nome de usuário único")
    senha: str = Field(..., min_length=6, description="Senha com no mínimo 6 caracteres")

class UsuarioResponse(BaseModel):
    username: str
    saldo: float

class Token(BaseModel):
    access_token: str
    token_type: str