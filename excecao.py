class Excecao(Exception):
    def __init__(self, mensagem: str, status_code: int = 400):
        self.mensagem = mensagem
        self.status_code = status_code
        super().__init__(mensagem)