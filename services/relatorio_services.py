from sqlalchemy.orm import Session
from schemas.relatorio_schema import RelatorioOcupacaoResponse, RelatorioEventosCategoriasResponse, RelatorioParticipantesCursosResponse
from excecao import Excecao

class RelatorioService:
    def __init__(self, relatorio_repository, evento_repository, participante_repository, inscricao_repository):  
        self.relatorio_repository = relatorio_repository
        self.evento_repository = evento_repository
        self.participante_repository = participante_repository      
        self.inscricao_repository = inscricao_repository


    def listar_relatorio_evento_ocupacao(self, db: Session) -> list[RelatorioOcupacaoResponse]:
        relatorio = self.relatorio_repository.relatorio_ocupacao(db)
        if not relatorio:
            raise Excecao("Sem dados suficientes para gerar o relatório!", 404)
        return relatorio
    
    def listar_relatorio_evento_categoria(self, db: Session) -> list[RelatorioEventosCategoriasResponse]:
        relatorio = self.relatorio_repository.relatorio_categorias(db)
        if not relatorio:
            raise Excecao("Sem dados suficientes para gerar o relatório!", 404)

        return relatorio

    def listar_relatorio_evento_curso(self, db: Session) -> RelatorioParticipantesCursosResponse:
        relatorio = self.relatorio_repository.relatorio_cursos(db)
        if not relatorio:
            raise Excecao("Sem dados suficientes para gerar o relatório!", 404)
        return relatorio
 
