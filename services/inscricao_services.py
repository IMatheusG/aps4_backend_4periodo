from sqlalchemy.orm import Session
from models.inscricao_model import InscricaoModel
from schemas.inscricao_schema import InscricaoCreate, InscricaoResponse
from excecao import Excecao

class InscricaoService:    
    def __init__(self, repository, evento_repository, participante_repository):
        self.repository = repository
        self.evento_repository = evento_repository
        self.participante_repository = participante_repository    

    def criar(self, db: Session, inscricao: InscricaoCreate) -> InscricaoResponse:
        evento = self.evento_repository.buscar_completo(db, inscricao.id_evento)        
        if evento is None or not evento:
            raise Excecao("O evento não existe!", 404)
        
        participante = self.participante_repository.buscar_por_id(db, inscricao.id_participante)
        if participante is None or not participante:
            raise Excecao("O participante não existe!", 404)
        
        ja_existe = self.repository.buscar_por_id(db, inscricao.id_evento, inscricao.id_participante)
        if ja_existe is not None:
            raise Excecao("A inscrição já existe!", 409)
        if evento.total_inscricoes == evento.capacidade:
            raise Excecao("O evento já está lotado!")

        # fazer o total_inscritos direto no banco

        # for i, evento_bd in enumerate(self.evento_repository.eventos):           
        #     if evento_bd.id == evento.id:
        #         self.evento_repository.eventos[i].total_inscritos += 1
        inscricao = InscricaoModel(**inscricao.model_dump())
        return self.repository.salvar(db, inscricao)
 
    def consultar(self, db, evento_id, participante_id):
        inscricao = self.repository.buscar_por_id(db, evento_id, participante_id)
        if inscricao is None or not inscricao:
            raise Excecao("Inscrição não encontrada!", 404)
        return inscricao
 