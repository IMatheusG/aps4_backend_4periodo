from pydantic import BaseModel
 
class ParticipanteCreate(BaseModel):
    nome: str = "João da Silva"
    email: str = "joaosilva@gmail.com"
    curso: str = "Mecânica"

class ParticipanteResponse(BaseModel):
    id: int = 0
    nome: str = "João da Silva"
    email: str = "joaosilva@gmail.com"
    curso: str = "Mecânica"
    