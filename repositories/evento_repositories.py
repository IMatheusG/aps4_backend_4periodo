from sqlalchemy import text
from sqlalchemy.orm import Session

from models.evento_model import EventoModel
from models.inscricao_model import InscricaoModel
from schemas.evento_schema import EventoResponse, EventoCreate, EventoInscricaoResponse

class EventoRepository: 
    # ----- Clientes -----
    # def salvar_cliente(db: Session, cliente: ClienteModel) -> ClienteModel:
    #     db.add(cliente)  # prepara o INSERT
    #     db.commit()  # executa de verdade no banco
    #     db.refresh(cliente)  # busca o id gerado pelo banco
    #     return cliente


    # def listar_clientes(db: Session) -> list[ClienteModel]:
    #     return db.query(ClienteModel).all()


    # def buscar_cliente(db: Session, cliente_id: int) -> ClienteModel | None:
    #     return db.query(ClienteModel).filter(ClienteModel.id == cliente_id).first()


    def salvar(self, db: Session, evento: EventoModel) -> EventoResponse:
        db.add(evento)
        db.commit()
        db.refresh(evento)
        return evento


    def listar(self, db: Session) -> list[EventoResponse]:
        query = text("""
            SELECT 
                e.*,
                COALESCE(COUNT(ei.id), 0) as total_inscricoes
            FROM eventos e 
            LEFT JOIN eventos_inscricoes ei on ei.id_evento = e.id            
            GROUP BY e.id
        """)
        return db.execute(query).mappings().all()
        # return db.query(EventoModel).all()

    def listar_inscricoes(self, db: Session, evento_id: int) -> list[EventoInscricaoResponse]:
        query = text("""
            SELECT
                ei.id as id_inscricao,
                ei.id_participante,
                ei.data_inscricao,
                p.nome as participante_nome,
                p.email as participante_email,
                p.curso as participante_curso
            FROM eventos_inscricoes ei            
            INNER JOIN participantes p on p.id = ei.id_participante
            WHERE ei.id_evento = :evento_id
            GROUP BY ei.id
        """)
        return db.execute(query, {"evento_id": evento_id}).mappings().all()
  

    def buscar_completo(self, db: Session, evento_id: int) -> EventoResponse | None:
        query = text("""
            SELECT 
                e.*,
                COALESCE(COUNT(ei.id), 0) as total_inscricoes
            FROM eventos e
            LEFT JOIN eventos_inscricoes ei on ei.id_evento = e.id
            WHERE e.id = :evento_id            
            GROUP BY e.id
        """)
        return db.execute(query, {"evento_id": evento_id}).mappings().first()
    
    def buscar(self, db: Session, evento_id: int) -> EventoModel | None:        
        return db.query(EventoModel).filter(EventoModel.id == evento_id).first()
 

    def atualizar(self, db: Session, evento_atualizado: EventoModel) -> EventoResponse:
        evento_bd = self.buscar(db, evento_atualizado.id)

        if not evento_bd:
            return None
        
        evento_bd.titulo = evento_atualizado.titulo
        evento_bd.descricao = evento_atualizado.descricao
        evento_bd.data = evento_atualizado.data
        evento_bd.horario = evento_atualizado.horario
        evento_bd.local = evento_atualizado.local
        evento_bd.capacidade = evento_atualizado.capacidade
        evento_bd.categoria = evento_atualizado.categoria

        db.commit()
        db.refresh(evento_bd)
        return self.buscar_completo(db, evento_bd.id)

    # def atualizar(self, evento_put):
    #     for i, evento in enumerate(self.eventos):   
    #         if evento.id == evento_put.id:
    #             self.eventos[i] = evento_put
    #             return evento_put
            
    #     return None
    
    def excluir(self, db: Session, evento_id):
        evento = self.buscar(db, evento_id)
        if not evento:
            return False

        # query = text("""
        #     DELETE FROM eventos_inscricoes WHERE id_evento = :evento_id
        # """)
        # db.execute(query, {"evento_id": evento.id: int})
        
        db.query(InscricaoModel).filter(InscricaoModel.id_evento == evento.id).delete()
        db.delete(evento)
        db.commit()
        return True