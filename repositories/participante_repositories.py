from models.participante_model import ParticipanteModel
from models.inscricao_model import InscricaoModel
from schemas.participante_schema import ParticipanteCreate, ParticipanteResponse
from sqlalchemy.orm import Session

class ParticipanteRepository:
    def salvar(self, db: Session, participante: ParticipanteModel) -> ParticipanteModel:
        db.add(participante)
        db.commit()
        db.refresh(participante)
        return participante

    def listar(self, db: Session) -> list[ParticipanteModel]:
        return db.query(ParticipanteModel).all() 


    def buscar_por_id(self, db: Session, participante_id) -> ParticipanteModel | None:
        return db.query(ParticipanteModel).filter(ParticipanteModel.id == participante_id).first()
    
    def buscar_por_email(self, db: Session, participante_email: str, participante_id: int = 0) -> bool:
        if participante_id != 0:
            return (
                db.query(ParticipanteModel).filter(ParticipanteModel.email == participante_email, ParticipanteModel.id != participante_id).first()
                is not None
            )
        else:
            return (
                db.query(ParticipanteModel).filter(ParticipanteModel.email == participante_email).first()
                is not None
            )
            

    def atualizar(self, db: Session, participante_update: ParticipanteModel) -> ParticipanteModel:
        participante_bd = self.buscar_por_id(db, participante_update.id)

        if not participante_bd:
            return None
        
        participante_bd.nome = participante_update.nome
        participante_bd.email = participante_update.email
        participante_bd.curso = participante_update.curso
 
        db.commit()
        db.refresh(participante_bd)
        return participante_bd
              
    
    def excluir(self, db: Session, participante_id: int):
        participante = self.buscar_por_id(db, participante_id)
        if not participante:
            return False

        db.query(InscricaoModel).filter(InscricaoModel.id_participante == participante.id).delete()
        db.delete(participante)
        db.commit()
        return True
