from sqlalchemy.orm import Session
from models.inscricao_model import InscricaoModel
from schemas.inscricao_schema import InscricaoResponse

class InscricaoRepository:
    def salvar(self, db: Session, inscricao: InscricaoModel) -> InscricaoModel:        
        db.add(inscricao)
        db.commit()
        db.refresh(inscricao)
        return inscricao 

    def buscar_por_id(self, db: Session, evento_id, participante_id):
        return db.query(InscricaoModel).filter(InscricaoModel.id_participante == participante_id, InscricaoModel.id_evento == evento_id).first()
 