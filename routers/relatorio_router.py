from fastapi import APIRouter, HTTPException, Depends
from services.relatorio_services import RelatorioService
from sqlalchemy.orm import Session
from database import get_db
from schemas.relatorio_schema import RelatorioEventosCategoriasResponse, RelatorioOcupacaoResponse, RelatorioParticipantesCursosResponse
from excecao import Excecao
from repositories.evento_repositories import EventoRepository
from repositories.participante_repositories import ParticipanteRepository
from repositories.inscricao_repositories import InscricaoRepository
from repositories.relatorio_repositories import RelatorioRepository
from services.relatorio_services import RelatorioService

from auth import exigir_login
from models.usuario_model import UsuarioModel

evento_repository = EventoRepository()
participante_repository = ParticipanteRepository()
inscricao_repository = InscricaoRepository()
relatorio_repository = RelatorioRepository()

router = APIRouter()
 
relatorio_service = RelatorioService(    
    relatorio_repository=relatorio_repository,
    evento_repository=evento_repository,
    participante_repository=participante_repository,
    inscricao_repository=inscricao_repository
)
 
def get_relatorio_service():
    return relatorio_service

@router.get("/relatorios/eventos/ocupacao", 
            response_model=list[RelatorioOcupacaoResponse],
            summary="[ADMIN] Visualizar Relatório de Ocupação",
            )
def listar_relatorio_evento_ocupacao(
    db: Session = Depends(get_db), 
    service: RelatorioService = Depends(get_relatorio_service),
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN"))
    ):
    try:
        return service.listar_relatorio_evento_ocupacao(db)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))

 
@router.get("/relatorios/eventos/categorias", 
            response_model=list[RelatorioEventosCategoriasResponse],
            summary="[ADMIN] Visualizar Relatório por Categoria",
            )
def listar_relatorio_evento_categoria(
    db: Session = Depends(get_db), 
    service: RelatorioService = Depends(get_relatorio_service),
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN"))
    ):
    try:
        return service.listar_relatorio_evento_categoria(db)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    
  
@router.get("/relatorios/participantes/cursos", 
            response_model=list[RelatorioParticipantesCursosResponse],
            summary="[ADMIN] Visualizar Relatório por Curso",
            )
def listar_relatorio_evento_cursos(
    db: Session = Depends(get_db), 
    service: RelatorioService = Depends(get_relatorio_service),
    usuario_logado: UsuarioModel = Depends(exigir_login("ADMIN"))
    ):
    try:
        return service.listar_relatorio_evento_curso(db)
    except Excecao as e:
        raise HTTPException(e.status_code, str(e.mensagem))
    