from fastapi import APIRouter, HTTPException, Depends
from models.evento_model import EventoModel
from services.evento_services import EventoService
from sqlalchemy.orm import Session
from database import get_db
from schemas.evento_schema import EventoCreate, EventoResponse, EventoInscricaoResponse
from excecao import Excecao
from repositories.evento_repositories import EventoRepository
from services.evento_services import EventoService
from auth import exigir_login
from models.usuario_model import UsuarioModel

router = APIRouter()

evento_repository = EventoRepository()
evento_service = EventoService(evento_repository)

def get_evento_service():
    return evento_service

@router.post("/eventos", 
             response_model=EventoResponse,
             summary="[ADMIN] Cadastrar Evento",
             )
def criar_evento(
    evento: EventoCreate, 
    service: EventoService = Depends(get_evento_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    try:
        return service.criar(db,evento)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))

@router.get("/eventos/{evento_id}", 
            response_model=EventoResponse,
            summary="[ADMIN / USUÁRIO] Buscar Evento",
            )
def buscar_evento(
    evento_id: int, 
    service: EventoService = Depends(get_evento_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login()),
    db: Session = Depends(get_db)):
    try:
        return service.consultar(db, evento_id)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))

    
@router.get("/eventos/{evento_id}/inscricoes", 
            response_model=list[EventoInscricaoResponse],
            summary="[ADMIN / USUÁRIO] Buscar Inscrições",
            )
def buscar_inscricoes_evento(
    evento_id: int, 
    service: EventoService = Depends(get_evento_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login()),
    db: Session = Depends(get_db)):
    try:
        return service.listar_inscricoes(db, evento_id)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    
@router.put("/eventos/{evento_id}", 
            response_model=EventoResponse,
            summary="[ADMIN] Atualizar Evento",
            )
def atualizar_evento(
    evento_id: int, 
    evento: EventoCreate, 
    service: EventoService = Depends(get_evento_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    evento = EventoModel(**evento.model_dump())
    evento.id = evento_id
    try:
        return service.atualizar(db, evento)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    
@router.delete("/eventos/{evento_id}",
               summary="[ADMIN] Excluir Evento",
               )
def excluir_evento(
    evento_id: int, 
    service: EventoService = Depends(get_evento_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN")),
    db: Session = Depends(get_db)
    ):
    try:
        return service.excluir(db, evento_id)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    

@router.get("/eventos", 
            response_model=list[EventoResponse],
            summary="[ADMIN / USUÁRIO] Listar Eventos",
            )
def listar_eventos(
    db: Session = Depends(get_db), 
    service: EventoService = Depends(get_evento_service),
    usuario_logado: UsuarioModel = Depends(exigir_login()),
    ):
    try:
        return service.listar(db)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    