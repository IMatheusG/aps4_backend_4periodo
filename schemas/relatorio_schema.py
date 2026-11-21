from pydantic import BaseModel 
  
class RelatorioOcupacaoResponse(BaseModel):
    evento_id: int = 0
    titulo: str = "WorkShop Mundo Senai"
    total_inscricoes: int = 0
    vagas_disponiveis: int = 0
    percentual_ocupacao: float = 0


class RelatorioEventosCategoriasResponse(BaseModel):
    categoria: str = "Palestra"
    total_eventos: int = 0
    capacidade_total: int = 0
    total_inscricoes: int = 0

class RelatorioParticipantesCursosResponse(BaseModel):
    curso: str = "Mecânica"
    total_participantes: int = 0
    total_inscricoes: int = 0