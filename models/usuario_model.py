from pydantic import BaseModel
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base
    
class UsuarioModel(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, nullable=False)
    senha_hash = Column(String, nullable=False)
    perfil = Column(String, nullable=False) 