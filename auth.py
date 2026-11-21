from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from excecao import Excecao

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "senha_super_secreta_123456")
ALGORITH = os.getenv("ALGORITH", "HS256")
EXPIRACAO_TOKEN_MINUTOS = int(os.getenv("EXPIRACAO_TOKEN_MINUTOS", 60))

from database import get_db
from models.usuario_model import UsuarioModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()

# 1. Hash de senha
def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return pwd_context.verify(senha,hash_senha)

# 2. Token JWT
def criar_token(id: int, email: str, perfil: str) -> str:
    payload = {
        "id": id,
        "email": email,
        "perfil": perfil,
        "exp": datetime.now(timezone.utc) + timedelta(minutes=EXPIRACAO_TOKEN_MINUTOS)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITH)

def decodificar_token(token: str) -> str:
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITH])
        return payload["email"] #devolvendo oo email do usuário
    except jwt.ExpiredSignatureError:
        raise Excecao("Token expirado", 401)
    except jwt.InvalidTokenError:
        raise Excecao("Token inválido", 401)

# 3. Dependêcias de acesso

def get_usuario_atual(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)) -> UsuarioModel:
    email = decodificar_token(credentials.credentials)

    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == email).first()
    if usuario is None:
        raise Excecao("Usuário do token não existe mais", 401)
    
    return usuario

# def exigir_admin(usuario: UsuarioModel = Depends(get_usuario_atual)) -> UsuarioModel:
#     if usuario.perfil != "ADMIN":
#         raise Excecao("Apenas usuários administradores podem realizar essa ação", 401)
#     return usuario

# def exigir_usuario(usuario: UsuarioModel = Depends(get_usuario_atual)) -> UsuarioModel:
#     if usuario.perfil != "USUARIO":
#         raise Excecao("Apenas usuários podem realizar essa ação", 401)
#     return usuario

def exigir_login(nivel_permissao: str = "USUARIO") -> UsuarioModel:
    def verificar_permissao(usuario: UsuarioModel = Depends(get_usuario_atual)) -> UsuarioModel:
        if usuario.perfil == "USUARIO" and nivel_permissao == "ADMIN":
            raise Excecao("Apenas usuários administradores podem realizar essa ação", 403)
        
        return usuario
    
    return verificar_permissao
