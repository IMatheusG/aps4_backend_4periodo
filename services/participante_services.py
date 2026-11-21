from models.participante_model import ParticipanteModel
from schemas.participante_schema import ParticipanteCreate, ParticipanteResponse
from sqlalchemy.orm import Session
from excecao import Excecao

class ParticipanteService:
    def __init__(self,repository):
        self.repository = repository
    
    def criar(self, db: Session, participante: ParticipanteCreate) -> ParticipanteModel:
        participante = ParticipanteModel(**participante.model_dump())

        if participante.nome == '':
            raise Excecao("O nome não pode ser vazio!")
        if participante.email == '':
            raise Excecao("O email não pode ser vazio!")
        if participante.curso == '':
            raise Excecao("O curso não pode ser vazio!")

        duplicidade = self.repository.buscar_por_email(db, participante.email)
        if duplicidade:
            raise Excecao("Este e-mail já está sendo utilizado por outro participante!", 409)
        
        return self.repository.salvar(db, participante)

    def listar(self, db: Session):
        result = self.repository.listar(db)
        if len(result) == 0:
            raise Excecao("Sem participantes cadastrados!")
        return result

    def consultar(self, db: Session, participante_id: int):
        participante = self.repository.buscar_por_id(db, participante_id)
        if participante is None or not participante:
            raise Excecao("Participante não encontrado", 404)
        return participante

    def atualizar(self, db: Session, participante: ParticipanteResponse) -> ParticipanteResponse:        
        participante = ParticipanteModel(**participante.model_dump())

        if participante.nome == '':
            raise Excecao("O nome não pode ser vazio!")
        if participante.email == '':
            raise Excecao("O email não pode ser vazio!")
        if participante.curso == '':
            raise Excecao("O curso não pode ser vazio!")

        duplicidade = self.repository.buscar_por_email(db, participante.email, participante.id)
        if duplicidade:
            raise Excecao("Este e-mail já está sendo utilizado por outro participante!", 409)

        
        participante = self.repository.atualizar(db, participante) 
        if participante is None or not participante:
            raise Excecao("Participante não encontrado!", 404)
        return participante
    
    def excluir(self, db: Session ,participante_id): 
        result = self.repository.excluir(db, participante_id)
        if result is None or not result:
            raise Excecao("Participante não encontrado!", 404)
        return "Excluído com sucesso!"