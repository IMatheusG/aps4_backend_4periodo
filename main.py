import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from rich.console import Console
from database import Base, engine
from routers import evento_router, participante_router, inscricao_router, relatorio_router, usuario_router
from excecao import Excecao

console = Console()
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API de Eventos v4 - Banco de dados + Autenticação")

# código do gemini pra filtrar os erros
@app.middleware("http")
async def capturar_erros_limpos(request: Request, call_next):
    try:
        return await call_next(request)
    except Excecao as e:
        return JSONResponse(
            status_code=e.status_code,
            content={"detail": e.mensagem}
        )
    except Exception as exc:
        # Filtra o rastro para manter APENAS arquivos fora da venv/Python
        frames = traceback.extract_tb(exc.__traceback__)
        meus_arquivos = [
            f'  Arquivo "{f.filename}", linha {f.lineno}, em {f.name}\n    -> {f.line}'
            for f in frames
            if "venv" not in f.filename.lower() and "python3" not in f.filename.lower()
        ]

        console.print(f"\n[bold red]❌ {type(exc).__name__}:[/bold red] {exc}")
        if meus_arquivos:
            console.print("[yellow]Onde ocorreu no seu código:[/yellow]")
            console.print("\n".join(meus_arquivos))
        console.print()

        return JSONResponse(
            status_code=500,
            content={"detail": f"{type(exc).__name__}: {exc}"},
        )


app.include_router(evento_router.router)
app.include_router(participante_router.router)
app.include_router(inscricao_router.router)
app.include_router(relatorio_router.router)
app.include_router(usuario_router.router)


@app.get("/")
def raiz():
    return {"mensagem": "API de Eventos v4 - Banco de dados + Autenticação"}