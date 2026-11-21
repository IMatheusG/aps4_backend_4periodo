from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nome: str = "João da Silva"
    email: str = "joaosilva@gmail.com"
    senha_hash: str = "senha_super_secreta_123456_01"

class UsuarioResponse(BaseModel):
    id: int = 0
    nome: str = "João da Silva"
    senha_hash: str = "senha_secreta"
    email: str = "joaosilva@gmail.com"
    perfil: str = "USUARIO"


class UsuarioAdminCreate(BaseModel):
    nome: str = "João Admin"
    email: str = "joaoadm@gmail.com"
    senha_hash: str = "senha_super_secreta_123456_02"
 
class UsuarioAdminResponse(BaseModel):
    id: int = 0
    nome: str = "João da Silva"
    senha_hash: str = "senha_secreta"
    email: str = "joaosilva@gmail.com"
    perfil: str = "ADMIN"
 
class LoginRequest(BaseModel):
    email: str = "usuariosecreto"
    senha: str = "senha_super_secreta_321"

class TokenResponse(BaseModel):
    access_token: str = "token_secreto_123"
    token_type: str = "bearer"
