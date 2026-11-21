from fastapi import APIRouter, HTTPException, Depends

from schemas.participante_schema import ParticipanteCreate, ParticipanteResponse
from services.participante_services import ParticipanteService
from database import get_db
from excecao import Excecao
from repositories.participante_repositories import ParticipanteRepository
from sqlalchemy.orm import Session
from auth import exigir_login
from models.usuario_model import UsuarioModel

participante_repository = ParticipanteRepository()
participante_service = ParticipanteService(participante_repository)

router = APIRouter()

def get_participante_service():
    return participante_service


@router.post("/participantes", 
             response_model=ParticipanteResponse,
             summary="[ADMIN] Cadastrar Participante",
             )
def criar_participante(
    participante: ParticipanteCreate,
    service: ParticipanteService = Depends(get_participante_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    try:
        return service.criar(db, participante)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))

@router.put("/participantes/{participante_id}",
            response_model=ParticipanteResponse,
            summary="[ADMIN] Atualizar Participante",
            )
def atualizar_participante(
    participante_id: int, 
    participante: ParticipanteCreate, 
    service: ParticipanteService = Depends(get_participante_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    # participante = ParticipanteCreate(id=participante_id, **participante.model_dump())
    participante = ParticipanteResponse(**participante.model_dump())
    participante.id = participante_id
    
    try:
        return service.atualizar(db, participante)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    
@router.delete("/participantes/{participante_id}",
               summary="[ADMIN] Excluir Participante",
               )
def excluir_participante(
    participante_id: int, 
    service: ParticipanteService = Depends(get_participante_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    try:
        return service.excluir(db, participante_id)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    

# @router.get("/participantes")
@router.get("/participantes", 
            response_model=list[ParticipanteResponse],
            summary="[ADMIN / USUÁRIO] Visualizar Participantes",
            )
def listar_participantes(
    service: ParticipanteService = Depends(get_participante_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login()),
    db: Session = Depends(get_db)
    ):
    try:
        return service.listar(db)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    

@router.get("/participantes/{participante_id}",
             response_model=ParticipanteResponse,
             summary="[ADMIN / USUÁRIO] Buscar Participante",
             )
def buscar_participante(
    participante_id: int, 
    service: ParticipanteService = Depends(get_participante_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login()),
    db: Session = Depends(get_db)
    ):
    try:
        return service.consultar(db, participante_id)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))

