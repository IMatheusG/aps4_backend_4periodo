from datetime import date, datetime, timedelta
from enum import Enum

from pydantic import BaseModel, Field

class Categoria(str, Enum):
    PALESTRA = "PALESTRA"
    WORKSHOP = "WORKSHOP"
    MINICURSO = "MINICURSO"
    SEMINARIO = "SEMINARIO"
    COMPETICAO = "COMPETICAO"
    
class EventoCreate(BaseModel):
    titulo: str = "WorkShop Mundo Senai"
    descricao: str = "Venha conhecer as estandes dos alunos com os melhores projetos do SENAI"
    data: str = (date.today() + timedelta(days=1)).isoformat()
    horario: str = datetime.now().strftime("%H:%M")
    local: str = "SENAI - Unidade CIC - Curitiba"
    capacidade: int = 100
    categoria: Categoria = Categoria.WORKSHOP.value

class EventoResponse(BaseModel):
    id: int = 0
    titulo: str = "WorkShop Mundo Senai"
    descricao: str = "Venha conhecer as estandes dos alunos com os melhores projetos do SENAI"
    data: str = (date.today() + timedelta(days=1)).isoformat()
    horario: str = datetime.now().strftime("%H:%M")
    local: str = "SENAI - Unidade CIC - Curitiba"
    capacidade: int = 100
    total_inscricoes: int = 0
    categoria: Categoria = Categoria.WORKSHOP.value

class EventoInscricaoResponse(BaseModel):
    id_inscricao: int = 1
    id_participante: int = 1
    data_inscricao: str = (date.today() + timedelta(days=1)).isoformat()
    participante_nome: str = "João da silva"
    participante_email: str = "joaosilva@gmail.com"
    participante_curso: str = "Mecânica"  
