# class ParticipanteCriar(BaseModel):
#     nome: str = 'Indefinido'
#     email: EmailStr
#     curso: str = 'Indefinido'

from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
    
class ParticipanteModel(Base):
    __tablename__ = "participantes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    curso = Column(String, nullable=False)