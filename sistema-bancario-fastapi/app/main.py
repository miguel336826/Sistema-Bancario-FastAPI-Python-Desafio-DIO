from fastapi import FastAPI
from app.usuarios.routes import router as auth_router
from app.transacoes.routes import router as transacoes_router

app = FastAPI(
    title="API Bancária Assíncrona",
    description="Desafio de gerenciamento de contas correntes, depósitos, saques e extratos com JWT.",
    version="1.0.0"
)

# incluindo os modulos de rotas
app.include_router(auth_router)
app.include_router(transacoes_router)

@app.get("/")
async def home():
    return {"mensagem": "Bem-vindo à API Bancária. Acesse /docs para a documentação."}