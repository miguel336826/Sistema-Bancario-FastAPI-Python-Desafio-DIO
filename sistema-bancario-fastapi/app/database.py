import asyncio

# db em memoria
DB_USUARIOS = {}  # {username: {username, senha_criptografada, saldo}}
DB_TRANSACOES = {} # {username: [lista_de_transacoes]}

async def buscar_usuario(username: str):
    await asyncio.sleep(0.1)  # Simula I/O de banco de dados
    return DB_USUARIOS.get(username)

async def salvar_usuario(usuario_dict: dict):
    await asyncio.sleep(0.1)
    username = usuario_dict["username"]
    DB_USUARIOS[username] = usuario_dict
    DB_TRANSACOES[username] = []

async def buscar_transacoes(username: str):
    await asyncio.sleep(0.1)
    return DB_TRANSACOES.get(username, [])

async def adicionar_transacao(username: str, transacao: dict):
    await asyncio.sleep(0.1)
    DB_TRANSACOES[username].append(transacao)
    #atualiza o saldo do usuario
    if transacao["tipo"] == "deposito":
        DB_USUARIOS[username]["saldo"] += transacao["valor"]
    elif transacao["tipo"] == "saque":
        DB_USUARIOS[username]["saldo"] -= transacao["valor"]