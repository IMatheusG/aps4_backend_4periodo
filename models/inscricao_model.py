from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class InscricaoModel(Base):
    __tablename__ = "eventos_inscricoes"

    id = Column(Integer, primary_key=True, index=True)
    id_participante = Column(Integer, ForeignKey("participantes.id"), nullable=False)
    id_evento = Column(Integer, ForeignKey("eventos.id") ,nullable=False)  
    data_inscricao = Column(String, nullable=False)

 