from datetime import datetime, date
from sqlalchemy.orm import Session
from models.evento_model import EventoModel
from schemas.evento_schema import EventoCreate, EventoResponse, EventoInscricaoResponse
from excecao import Excecao

class EventoService:
    def __init__(self,repository):
        self.repository = repository
    
    def criar(self,db, evento: EventoCreate) -> EventoModel:
        evento = EventoModel(**evento.model_dump())

        try:
            data_evento = datetime.strptime(evento.data, "%Y-%m-%d").date()
        except Excecao:
            raise Excecao("Formato de data inválido! Use YYYY-MM-DD.")
        if data_evento <= date.today():
            raise Excecao("A data do evento precisa ser uma data futura!")
        
        if evento.titulo == '':
            raise Excecao("O título não pode ser vazio!")
        if evento.data == '':
            raise Excecao("A data não pode ser vazia!")
        if evento.horario == '':
            raise Excecao("O horário não pode ser vazio!")
        if evento.local == '':
            raise Excecao("O local não pode ser vazio!")
        if evento.capacidade <= 0:
            raise Excecao("A capacidade não pode ser igual ou menor que zero!")
        
        return self.repository.salvar(db,evento)

    def listar(self, db: Session) -> list[EventoResponse]:
        eventos = self.repository.listar(db)
        if not eventos:
            raise Excecao("Sem eventos cadastrados!", 404)

        return eventos
    
    def listar_inscricoes(self, db: Session, evento_id: int) -> list[EventoInscricaoResponse]:
        inscricoes = self.repository.listar_inscricoes(db, evento_id)
        if not inscricoes:
            raise Excecao("Este evento ainda não tem inscrições!")

        return inscricoes

    def consultar(self, db: Session, evento_id) -> EventoResponse | None:
        evento = self.repository.buscar_completo(db, evento_id)
        if evento is None or not evento:
            raise Excecao("Evento não encontrado", 404)
        return evento

    def atualizar(self, db: Session, evento: EventoModel) -> EventoResponse:
        try:
            data_evento = datetime.strptime(evento.data, "%Y-%m-%d").date()
        except Excecao:
            raise Excecao("Formato de data inválido! Use YYYY-MM-DD.")
        if data_evento <= date.today():
            raise Excecao("A data do evento precisa ser uma data futura!")
    
        if evento.titulo == '':
            raise Excecao("O título não pode ser vazio!")
        if evento.data == '':
            raise Excecao("A data não pode ser vazia!")
        if evento.horario == '':
            raise Excecao("O horário não pode ser vazio!")
        if evento.local == '':
            raise Excecao("O local não pode ser vazio!")
        if evento.capacidade <= 0:
            raise Excecao("A capacidade não pode ser igual ou menor que zero!")
        
        evento = self.repository.atualizar(db, evento) 
        if evento is None or not evento:
            raise Excecao("Evento não encontrado!", 404)
        return evento
    
    def excluir(self, db: Session, evento_id): 
        result = self.repository.excluir(db, evento_id)
        if result == False:
            raise Excecao("Evento não encontrado!", 404)
        return "Excluído com sucesso!"

