from fastapi import APIRouter, HTTPException, Depends

from models.inscricao_model import InscricaoModel
from services.inscricao_services import InscricaoService
from schemas.inscricao_schema import InscricaoCreate, InscricaoResponse
from sqlalchemy.orm import Session
from database import get_db
from excecao import Excecao
from repositories.evento_repositories import EventoRepository
from repositories.participante_repositories import ParticipanteRepository
from repositories.inscricao_repositories import InscricaoRepository
from services.inscricao_services import InscricaoService
from auth import exigir_login
from models.usuario_model import UsuarioModel


evento_repository = EventoRepository()
participante_repository = ParticipanteRepository()
inscricao_repository = InscricaoRepository()

inscricao_service = InscricaoService(
    repository=inscricao_repository,
    evento_repository=evento_repository,
    participante_repository=participante_repository
)

def get_inscricao_service():
    return inscricao_service

router = APIRouter()
 
@router.post("/inscricoes", 
             response_model=InscricaoResponse,
             summary="[ADMIN / USUÁRIO] Cadastrar Inscrição",
             )
def criar_inscricao(
    inscricao: InscricaoCreate, 
    service: InscricaoService = Depends(get_inscricao_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login()),
    db: Session = Depends(get_db)
    ):    
    try:
        return service.criar(db, inscricao)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem)) 


@router.get("/inscricoes/{evento_id}/{participante_id}", 
            response_model=InscricaoResponse,
            summary="[ADMIN / USUÁRIO] Buscar Inscrição",
            )
def buscar_inscricao(
    evento_id: int, 
    participante_id: int, 
    service: InscricaoService = Depends(get_inscricao_service), 
    usuario_logado: UsuarioModel = Depends(exigir_login()),
    db: Session = Depends(get_db)):
    try:
        return service.consultar(db, evento_id, participante_id)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem)) 

