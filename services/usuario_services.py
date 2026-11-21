from models.usuario_model import UsuarioModel
from schemas.usuario_schema import UsuarioCreate, UsuarioResponse
from sqlalchemy.orm import Session
from excecao import Excecao
from auth import gerar_hash_senha
from schemas.usuario_schema import UsuarioAdminCreate, LoginRequest
from auth import criar_token, verificar_senha

class UsuarioService:
    def __init__(self,repository):
        self.repository = repository
    
    def criar(self, db: Session, usuario_post: UsuarioCreate) -> UsuarioModel:
        usuario = UsuarioModel(
            nome = usuario_post.nome,
            email = usuario_post.email,
            senha_hash = usuario_post.senha_hash,
            perfil = "USUARIO"
        )

        if usuario.nome == '':
            raise Excecao("O nome não pode ser vazio!")
        if usuario.email == '':
            raise Excecao("O email não pode ser vazio!")
        if usuario.senha_hash == '':
            raise Excecao("A senha não pode ser vazia!")
        if len(usuario.senha_hash) < 3:
            raise Excecao("A senha não pode ter menos que 3 caracteres!")

        duplicidade = self.repository.duplicidade_por_email(db, usuario.email)
        if duplicidade:
            raise Excecao("Este e-mail já está sendo utilizado por outro usuário!", 409)

        usuario.senha_hash = gerar_hash_senha(usuario.senha_hash)           
        return self.repository.salvar(db, usuario)
    
    def criar_adm(self, db: Session, adm_post: UsuarioAdminCreate) -> UsuarioModel:
        usuario = UsuarioModel(
            nome = adm_post.nome,
            email = adm_post.email,
            senha_hash = adm_post.senha_hash,
            perfil = "ADMIN"
        )

        if usuario.nome == '':
            raise Excecao("O nome não pode ser vazio!")
        if usuario.email == '':
            raise Excecao("O email não pode ser vazio!")
        if usuario.senha_hash == '':
            raise Excecao("A senha não pode ser vazia!")
        if len(usuario.senha_hash) < 3:
            raise Excecao("A senha não pode ter menos que 3 caracteres!")

        duplicidade = self.repository.duplicidade_por_email(db, usuario.email)
        if duplicidade:
            raise Excecao("Este e-mail já está sendo utilizado por outro usuário!", 409)

        usuario.senha_hash = gerar_hash_senha(usuario.senha_hash)           
        return self.repository.salvar(db, usuario)
    
    def consultar(self, db: Session, usuario_id: int):
        usuario = self.repository.buscar_por_id(db, usuario_id)
        if usuario is None or not usuario:
            raise Excecao("Usuário não encontrado", 404)
        return usuario
    
    def listar(self, db: Session):
        result = self.repository.listar(db)
        if len(result) == 0:
            raise Excecao("Sem Usuários cadastrados!")
        return result

    def atualizar(self, db: Session, usuario: UsuarioResponse) -> UsuarioResponse:        
        usuario = UsuarioModel(**usuario.model_dump())

        if usuario.nome == '':
            raise Excecao("O nome não pode ser vazio!")
        if usuario.email == '':
            raise Excecao("O email não pode ser vazio!")
 
        duplicidade = self.repository.duplicidade_por_email(db, usuario.email, usuario.id)
        if duplicidade:
            raise Excecao("Este e-mail já está sendo utilizado por outro usuario!", 409)

        usuario.senha_hash = gerar_hash_senha(usuario.senha_hash)           
        
        usuario = self.repository.atualizar(db, usuario) 
        if usuario is None or not usuario:
            raise Excecao("Usuario não encontrado!", 404)
        return usuario
    
    def excluir(self, db: Session ,usuario_id): 
        usuario = self.repository.buscar_por_id(db, usuario_id)
        if (usuario.id == 11 and usuario.perfil == "ADMIN"):
            raise Excecao("Este Adminsitrador não pode ser excluído!", 400)

        result = self.repository.excluir(db, usuario_id)
        if result is None or not result:
            raise Excecao("Usuario não encontrado!", 404)
        return "Excluído com sucesso!"

        
    def autenticar(self, db: Session, dados: LoginRequest) -> str:
        usuario = self.repository.buscar_por_email(db, dados.email)

        if (usuario is None or not verificar_senha(dados.senha, usuario.senha_hash)):
            raise Excecao("E-mail ou senha inválidos!", 401)

        return criar_token(usuario.id, usuario.email, usuario.perfil)
