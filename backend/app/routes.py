from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from validate_docbr import CPF
from app.services.initituicaoService import BancoA
from app.models.UserModel import CadastroData, LoginData, ValorData, ChavePixData, TransferenciaData
import app.services.userService as user_services
from app.database.Conection import get_db
#import requisicoes

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/")
async def index():
    return {"message": "API is up and running"}

@router.post("/cadastro")
async def cadastro(data: CadastroData, db=Depends(get_db)):
    return user_services.cadastrar_usuario(data, db)

@router.post("/login")
async def login(data: LoginData, db=Depends(get_db)):
    return user_services.login_usuario(data, db)

""""
@router.post("/cadastro")
async def cadastro(data: CadastroData, banco_a: BancoA = Depends()):
    cpf_v = CPF()
    if cpf_v.validate(data.cpf):
        response = banco_a.cadastrar_usuario(
            data.nome, data.cpf, data.data_nascimento, data.login, data.senha, data.tel
        )
        if response['status'] == 'success':
            return {"message": "User registered successfully"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Registration failed")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid CPF")

@router.post("/login")
async def login(data: LoginData, banco_a: BancoA = Depends()):
    response = banco_a.login_usuario(data.login, data.senha)
    if response['status'] == 'success':
        return {"message": "Login successful", "user_id": response['user'][0]}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=response['message'])

@router.get("/dashboard")
async def dashboard(user_id: str = Depends(oauth2_scheme), banco_a: BancoA = Depends()):
    user = banco_a.get_user_by_id(user_id)
    saldo = userService.get_saldo(banco_a.conn, user_id)
    return {"user": user, "saldo": saldo}

@router.post("/depositar")
async def depositar(data: ValorData, user_id: str = Depends(oauth2_scheme), banco_a: BancoA = Depends()):
    response = banco_a.depositar(user_id, data.valor)
    return {"message": "Deposit successful"}

@router.post("/retirar")
async def retirar(data: ValorData, user_id: str = Depends(oauth2_scheme), banco_a: BancoA = Depends()):
    response = banco_a.retirar(user_id, data.valor)
    return {"message": "Withdrawal successful"}

@router.post("/definir_chave_pix")
async def definir_chave_pix(data: ChavePixData, user_id: str = Depends(oauth2_scheme), banco_a: BancoA = Depends()):
    response = banco_a.definir_chave_pix(user_id, data.chave_pix)
    return {"message": "Pix key defined successfully"}

@router.post("/transferir")
async def transferir(data: TransferenciaData, user_id: str = Depends(oauth2_scheme), banco_a: BancoA = Depends()):
    response = banco_a.transferir(user_id, data.chave_pix_destino, data.valor)
    return {"message": "Transfer successful"}

@router.get("/logout")
async def logout():
    return {"message": "Logout successful"}

#@router.post("/loginCore")
#async def loginCore():
    #response = requisicoes.requisicao_core()
    #return response


"""