from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./eventos.db"

# para visualizar os comandos sql q são gerados
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False}) 

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# para pegar a conexão do banco em outros módulos
def get_db():
    db = SessionLocal()
    try:
        # retorna a referencia do banco de dados original
        yield db
    finally:
        # executa ao parar o servidor - no caso ele fecha o banco
        db.close()