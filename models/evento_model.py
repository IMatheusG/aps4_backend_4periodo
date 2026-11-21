from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
    
class EventoModel(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    data = Column(String, nullable=False)
    horario = Column(String, nullable=False)
    local = Column(String, nullable=False)
    capacidade = Column(Integer, nullable=False)
    categoria = Column(String, nullable=False)

# class EventoCriar(BaseModel):
#     titulo = Column(String, nullable=False)
#     descricao = Column(String, nullable=False)
#     data = Column(String, nullable=False)
#     horario = Column(String, nullable=False)
#     local = Column(String, nullable=False)
#     capacidade = Column(Integer, nullable=False)
#     categoria = Column(String, nullable=False)
  
# class Evento(EventoCriar):
#     id = Column(Integer, primary_key=True, index=True)
 