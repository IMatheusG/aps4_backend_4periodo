from datetime import date
from pydantic import BaseModel
 
class InscricaoCreate(BaseModel):
    id_participante: int = 1
    id_evento: int = 1
    data_inscricao: str = (date.today()).isoformat()
    
 
class InscricaoResponse(BaseModel):
    id: int = 1
    id_participante: int = 1
    id_evento: int = 1
    data_inscricao: str = (date.today()).isoformat()
