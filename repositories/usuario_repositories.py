from models.usuario_model import UsuarioModel
from models.inscricao_model import InscricaoModel
from schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from sqlalchemy.orm import Session

class UsuarioRepository:
    def salvar(self, db: Session, usuario: UsuarioModel) -> UsuarioModel:
        db.add(usuario)
        db.commit()
        db.refresh(usuario)
        return usuario 

    
    def listar(self, db: Session) -> list[UsuarioModel]:
        return db.query(UsuarioModel).all() 

    def buscar_por_id(self, db: Session, usuario_id: int = 0) -> UsuarioModel:
        return db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
            
    def buscar_por_email(self, db: Session, usuario_email: str) -> UsuarioModel:
        return db.query(UsuarioModel).filter(UsuarioModel.email == usuario_email).first()
            
    def duplicidade_por_email(self, db: Session, usuario_email: str, usuario_id: int = 0) -> bool:
        if usuario_id != 0:
            return (
                db.query(UsuarioModel).filter(UsuarioModel.email == usuario_email, UsuarioModel.id != usuario_id).first()
                is not None
            )
        else:
            return (
                db.query(UsuarioModel).filter(UsuarioModel.email == usuario_email).first()
                is not None
            )
            

    def atualizar(self, db: Session, usuario_update: UsuarioModel) -> UsuarioModel:
        usuario_bd = self.buscar_por_id(db, usuario_update.id)

        if not usuario_bd:
            return None
        
        usuario_bd.nome = usuario_update.nome
        usuario_bd.email = usuario_update.email
        usuario_bd.senha_hash = usuario_update.senha_hash
  
        db.commit()
        db.refresh(usuario_bd)
        return usuario_bd
              
    
    def excluir(self, db: Session, usuario_id: int):
        usuario = self.buscar_por_id(db, usuario_id)
        if not usuario:
            return False

        # db.query(InscricaoModel).filter(InscricaoModel.id_participante == usuario.id).delete()
        db.delete(usuario)
        db.commit()
        return True
