from sqlalchemy.orm import Session
from sqlalchemy import Float, func, cast, distinct
 
from models.evento_model import EventoModel
from models.inscricao_model import InscricaoModel
from models.participante_model import ParticipanteModel
from schemas.relatorio_schema import RelatorioOcupacaoResponse, RelatorioEventosCategoriasResponse, RelatorioParticipantesCursosResponse

class RelatorioRepository:   
 
    def relatorio_ocupacao(self, db: Session) -> list[RelatorioOcupacaoResponse]:
        # query = text("""
        #     SELECT 
        #         e.id as evento_id,
        #         e.titulo,
        #         e.capacidade,
        #         COALESCE(COUNT(ei.id),0) as total_inscricoes,
        #         (e.capacidade - e.total_inscricoes) as vagas_disponiveis,
        #         (total_inscricoes / e.capacidade) as percentual_ocupacao
        #     FROM eventos e 
        #     LEFT JOIN eventos_inscricoes ei on ei.id_evento = e.id            
        #     GROUP BY e.id
        # """)
        # return db.execute(query).mappings().all()
        total_inscricoes = func.count(InscricaoModel.id)

        resultados = (
            db.query(
                EventoModel.id.label("evento_id"),
                EventoModel.titulo,
                EventoModel.capacidade,
                total_inscricoes.label("total_inscricoes"),
                (EventoModel.capacidade - total_inscricoes).label("vagas_disponiveis"),
                func.round(
                    (cast(total_inscricoes, Float) * 100.0) / EventoModel.capacidade, 2
                ).label("percentual_ocupacao"),
            )
            .outerjoin(InscricaoModel, InscricaoModel.id_evento == EventoModel.id)
            .group_by(EventoModel.id)
            .all()
        )

        return [row._asdict() for row in resultados]
 
    def relatorio_categorias(self, db: Session) -> list[RelatorioEventosCategoriasResponse]:
        # query = text("""
        #      SELECT 
        #         e.categoria,
        #         COUNT(e.id) as total_eventos,
        #         SUM(e.capacidade) as capacidade_total,
        #         COALESCE(SUM(sub.qtd_inscricoes), 0) AS total_inscricoes
        #     FROM eventos e 
        #     LEFT JOIN (
        #         SELECT 
        #             id_evento, 
        #             COUNT(id) AS qtd_inscricoes
        #         FROM eventos_inscricoes
        #         GROUP BY id_evento
        #     ) sub ON sub.id_evento = e.id
        #     GROUP BY e.categoria
        # """)        
        sub_inscricoes = (
            db.query(
                InscricaoModel.id_evento.label("id_evento"),
                func.count(InscricaoModel.id).label("qtd_inscricoes"),
            )
            .group_by(InscricaoModel.id_evento)
            .subquery()
        )

        resultados = (
            db.query(
                EventoModel.categoria,
                func.count(EventoModel.id).label("total_eventos"),
                func.coalesce(func.sum(EventoModel.capacidade), 0).label("capacidade_total"),
                func.coalesce(func.sum(sub_inscricoes.c.qtd_inscricoes), 0).label("total_inscricoes"),
            )
            .outerjoin(sub_inscricoes, sub_inscricoes.c.id_evento == EventoModel.id)
            .group_by(EventoModel.categoria)
            .all()
        )

        return [row._asdict() for row in resultados]
 
 
    def relatorio_cursos(self, db: Session) -> list[RelatorioParticipantesCursosResponse]:
        # query = text("""
        #     SELECT
        #         p.curso,
        #         COUNT(p.id) as total_participantes,
        #         COUNT(i.id) as total_inscricoes                
        #     FROM participantes p
        #     LEFT JOIN inscricoes i on i.id_participante = p.id
        #     GROUP BY p.curso
        # """)

        resultados = (
            db.query(
                ParticipanteModel.curso,
                func.count(distinct(ParticipanteModel.id)).label("total_participantes"),
                func.count(InscricaoModel.id).label("total_inscricoes")
            )
            .outerjoin(InscricaoModel, InscricaoModel.id_participante == ParticipanteModel.id)
            .group_by(ParticipanteModel.curso)
            .all()
        )

        return [row._asdict() for row in resultados]
 
 