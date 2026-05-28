from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.usuarios.schemas import UsuarioCriar, UsuarioResponse, Token
from app.database import buscar_usuario, salvar_usuario
from app.auth import criptografar_senha, verificar_senha, criar_token_acesso

router = APIRouter(prefix="/auth", tags=["Autenticação"])

@router.post("/cadastro", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def cadastrar(usuario: UsuarioCriar):
    usuario_existente = await buscar_usuario(usuario.username)
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Usuário já cadastrado")
    
    novo_usuario = {
        "username": usuario.username,
        "senha": criptografar_senha(usuario.senha),
        "saldo": 0.0  # Conta começa com saldo zero
    }
    await salvar_usuario(novo_usuario)
    return novo_usuario

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    usuario = await buscar_usuario(form_data.username)
    
    # PRINTS DE DEPURAÇÃO (Aparecerão no seu terminal)
    print(f"--> Tentando login com Usuário: {form_data.username}")
    print(f"--> Usuário encontrado no banco? {usuario is not None}")
    
    if usuario:
        senha_valida = verificar_senha(form_data.password, usuario["senha"])
        print(f"--> A senha digitada está correta? {senha_valida}")

    if not usuario or not verificar_senha(form_data.password, usuario["senha"]):
        raise HTTPException(status_code=400, detail="Usuário ou senha incorretos")
    
    token_acesso = criar_token_acesso(dados={"sub": usuario["username"]})
    return {"access_token": token_acesso, "token_type": "bearer"}