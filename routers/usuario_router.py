from fastapi import APIRouter, HTTPException, Depends

from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioCreate, UsuarioResponse, UsuarioAdminCreate, UsuarioAdminResponse, LoginRequest, TokenResponse
from services.usuario_services import UsuarioService
from database import get_db
from excecao import Excecao
from repositories.usuario_repositories import UsuarioRepository
from sqlalchemy.orm import Session
from auth import exigir_login, get_usuario_atual

usuario_repository = UsuarioRepository()
usuario_service = UsuarioService(usuario_repository)

router = APIRouter()

def get_usuario_service():
    return usuario_service
 

@router.post("/usuarios", 
             response_model=UsuarioResponse,
             summary="[ADMIN] Criar Usuários",
             )
def criar_usuario(
    usuario: UsuarioCreate, 
    service: UsuarioService = Depends(get_usuario_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    try:
        return service.criar(db, usuario)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))

@router.post("/administradores", 
             response_model=UsuarioAdminResponse,
             summary="[ADMIN] Criar Administradores",
             )
def criar_administrador(
    admin: UsuarioAdminCreate, 
    service: UsuarioService = Depends(get_usuario_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    try:
        return service.criar_adm(db, admin)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))

@router.put("/usuarios/{usuario_id}", 
            response_model=UsuarioResponse,
            summary="[ADMIN] Atualizar Usuários / Administradores",
            )
def atualizar_usuario(
    usuario_id: int, 
    usuario: UsuarioCreate, 
    service: UsuarioService = Depends(get_usuario_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    # usuario = UsuarioCreate(id=usuario_id, **usuario.model_dump())
    usuario = UsuarioResponse(**usuario.model_dump())
    usuario.id = usuario_id
    
    try:
        return service.atualizar(db, usuario)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    
@router.delete("/usuarios/{usuario_id}",
               summary="[ADMIN] Excluir Usuários / Administradores",
               )
def excluir_usuario(
    usuario_id: int, 
    service: UsuarioService = Depends(get_usuario_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    try:
        return service.excluir(db, usuario_id)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    

# @router.get("/usuarios")
@router.get("/usuarios", 
            response_model=list[UsuarioResponse], 
            summary="[ADMIN] Listar Usuários / Administradores",
            )
def listar_usuarios(
    service: UsuarioService = Depends(get_usuario_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    try:
        return service.listar(db)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    

@router.get("/usuarios/{usuario_id}", 
            response_model=UsuarioResponse,
            summary="[ADMIN] Buscar Usuário / Administrador",
            )
def buscar_usuario(
    usuario_id: int, 
    service: UsuarioService = Depends(get_usuario_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    try:
        return service.consultar(db, usuario_id)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))


@router.post("/auth/login",
             response_model=TokenResponse,
             summary="[ALL] Logar como Usuário / Administrador",
             )
def login(
    dados: LoginRequest, 
    service: UsuarioService = Depends(get_usuario_service), 
    db: Session = Depends(get_db)
    ):
    try:
        token = service.autenticar(db, dados)
        return TokenResponse(access_token=token)
    except Excecao as e:
        raise HTTPException(e.status_code, e.mensagem)
    
@router.post("/auth/me", 
             response_model=UsuarioResponse,
             summary="[ADMIN / USUÁRIO] Visualizar cadastro do Usuário / Administrador logado",
             )
def ver_perfil(
    usuario_logado: UsuarioModel = Depends(exigir_login()),
    dados_usuario: UsuarioModel = Depends(get_usuario_atual)
    ):
    try:
        return dados_usuario
    except Excecao as e:
        raise HTTPException(e.status_code, e.mensagem)
