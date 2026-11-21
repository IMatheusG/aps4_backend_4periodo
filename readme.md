# API de Eventos v4 - Banco de dados + Autenticação

# Divergências em relação as rotas:
1. A rota de inscrição no evento foi utilizada como /inscricoes/{evento_id}/{participante_id}
2. A rota /eventos/{evento_id}/inscricoes não retorna todos os dados do evento pq fica redundante, deixamos apenas com os dados das inscrições e dos participantes.

# Observações:
1. Acabamos instalando uma biblioteca chamda rich do python q o gemini recomendou, pq tava insuportável ler 50 linhas de mensagem de erro pra cada 1 problema no código. 
Ela basicamente só oculta os erros que não pertencem ao código, e sim a biblioteca que está sendo utilizada, assim mostra direto o erro no seu código. aí pegamos um código adaptado do gemini no main.app pra mostrar apenas nossos erros.
Outro ponto é que no localhost/docs antes retornava status code 500 com internal server error, graças a este código agora ele retorna direto o erro q deu no código.

2. Para não ficar detalhando e aprofundando muito as rotas de usuários, deixamos o ADM como o único tipo de usuário que pode fazer o CRUD dos usuários da API.

3. Todas as rotas relacionadas a Usuário e ADMIN ficou dentro do service de usuário, senão teria q criar uma extra específica pra adm e eu estava com preguiça de ficar detalhando muito...

4. Você pode acabar encontrando uns comentários perdidos de códigos no meio do código funcional, pode ignorar eles, pois foram usados para uns testes antes de chegar na versão final, se bem que a maioria foi retirado.

5. A mesma função q valida duplicidade de e-mail foi adaptada para quando receber um parametro id a mais validar e-mails desconsiderando o daquele id específico q seria do usuário atual q tá sendo atualizado.

6. A senha do usuário é exibida em hash na hora da listagem só pra mostrar q tá sendo salva corretamente


# SIM, pedi pro gemini gerar o resto do read.me abaixo, pq oq considero relevante tá acima e no vídeo, o resto você já sabe.


API RESTful desenvolvida em **Python** com **FastAPI** e **SQLAlchemy** para o gerenciamento completo de eventos, participantes, inscrições e relatórios analíticos. O sistema conta com arquitetura em camadas, persistência em banco de dados SQLite (`eventos.db`) e autenticação via **JWT (JSON Web Token)** com controle de permissões por perfil (`USUARIO` e `ADMIN`).

---

## 📋 Índice

- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Perfis e Permissões](#-perfis-e-permissões)
- [Principais Rotas](#-principais-rotas)
- [Como Cadastrar Usuários e Obter Tokens](#-como-cadastrar-usuários-e-obter-tokens)
- [Exemplos de Utilização da API](#-exemplos-de-utilização-da-api)
- [Roteiro para Reproduzir os Testes](#-roteiro-para-reproduzir-os-testes)

---

## 🗂️ Estrutura do Projeto

O projeto segue o padrão de **Arquitetura em Camadas**, separando responsabilidades de roteamento, regras de negócio, acesso a dados, validação e segurança:

```text
aps4/
├── main.py                              # Ponto de entrada da aplicação FastAPI, rotas e tratamento global de exceções
├── auth.py                              # Geração/verificação de hash de senhas (bcrypt), tokens JWT e validação de permissões
├── database.py                          # Configuração da engine do SQLAlchemy, sessão e base declarativa
├── excecao.py                           # Classe de exceção customizada para erros de regra de negócio e status HTTP
├── eventos.db                           # Banco de dados SQLite gerado automaticamente na inicialização
├── requirements.txt                     # Dependências do projeto
├── .env                                 # Variáveis de ambiente (chave secreta, algoritmo e tempo de expiração)
│
├── models/                              # Modelos ORM (mapeamento das tabelas do banco de dados)
│   ├── evento_model.py
│   ├── inscricao_model.py
│   ├── participante_model.py
│   └── usuario_model.py
│
├── schemas/                             # Schemas Pydantic (validação de entrada e serialização de saída)
│   ├── evento_schema.py
│   ├── inscricao_schema.py
│   ├── participante_schema.py
│   ├── relatorio_schema.py
│   └── usuario_schema.py
│
├── repositories/                        # Camada de acesso a dados (consultas SQL/ORM no banco)
│   ├── evento_repositories.py
│   ├── inscricao_repositories.py
│   ├── participante_repositories.py
│   ├── relatorio_repositories.py
│   └── usuario_repositories.py
│
├── services/                            # Camada de regras de negócio e validações de domínio
│   ├── evento_services.py
│   ├── inscricao_services.py
│   ├── participante_services.py
│   ├── relatorio_services.py
│   └── usuario_services.py
│
└── routers/                             # Endpoints HTTP organizados por domínio
    ├── evento_router.py
    ├── inscricao_router.py
    ├── participante_router.py
    ├── relatorio_router.py
    └── usuario_router.py
```

---

## 🛡️ Perfis e Permissões

O controle de acesso é realizado pela dependência de autenticação em `auth.py`, verificando o atributo `perfil` do usuário autenticado:

| Perfil | Descrição | Permissões na API |
| :--- | :--- | :--- |
| **`USUARIO`** | Usuário padrão do sistema | • Consultar perfil próprio (`/usuarios/auth/me`)<br>• Listar e buscar eventos e participantes<br>• Realizar e consultar inscrições em eventos |
| **`ADMIN`** | Administrador do sistema | • Todas as permissões do perfil `USUARIO`<br>• Criar, atualizar e excluir eventos<br>• Gerenciar participantes e inscrições administrativas<br>• Acessar relatórios gerenciais de ocupação, categorias e cursos |

Caso um usuário com perfil `USUARIO` tente acessar uma rota restrita a `ADMIN`, a API bloqueia a requisição retornando **`403 Forbidden`** (ou `401 Unauthorized` caso o token esteja ausente, inválido ou expirado).

---

## 🛣️ Principais Rotas

### Autenticação e Usuários (`routers/usuario_router.py`)
| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `POST` | `/usuarios` | Público | Cadastra um novo usuário (`USUARIO` ou `ADMIN`) com senha criptografada |
| `POST` | `/usuarios/login` *(ou `/login`)* | Público | Autentica e-mail e senha e retorna o token JWT (`Bearer`) |
| `GET` / `POST` | `/usuarios/auth/me` | Logado | Retorna os dados do usuário autenticado no token atual |

### Eventos (`routers/evento_router.py`)
| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `GET` | `/eventos` | Logado | Lista todos os eventos cadastrados |
| `GET` | `/eventos/{evento_id}` | Logado | Busca os detalhes de um evento específico |
| `GET` | `/eventos/{evento_id}/inscricoes` | Logado | Lista todos os participantes inscritos em um evento |
| `POST` | `/eventos` | `ADMIN` | Cria um novo evento |
| `PUT` | `/eventos/{evento_id}` | `ADMIN` | Atualiza os dados de um evento |
| `DELETE` | `/eventos/{evento_id}` | `ADMIN` | Exclui um evento e suas inscrições vinculadas |

### Participantes (`routers/participante_router.py`)
| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `GET` | `/participantes` | Logado | Lista todos os participantes |
| `GET` | `/participantes/{participante_id}` | Logado | Busca um participante por ID |
| `POST` | `/participantes` | Logado / `ADMIN` | Cadastra um novo participante |
| `PUT` | `/participantes/{participante_id}` | `ADMIN` | Atualiza os dados de um participante |
| `DELETE` | `/participantes/{participante_id}` | `ADMIN` | Remove um participante |

### Inscrições (`routers/inscricao_router.py`)
| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `GET` | `/inscricoes` | Logado | Lista todas as inscrições realizadas |
| `POST` | `/inscricoes` | Logado | Inscreve um participante em um evento (valida capacidade e duplicidade) |
| `DELETE` | `/inscricoes/{inscricao_id}` | Logado / `ADMIN` | Cancela uma inscrição |

### Relatórios (`routers/relatorio_router.py`)
| Método | Rota | Acesso | Descrição |
| :--- | :--- | :--- | :--- |
| `GET` | `/relatorios/eventos/ocupacao` | `ADMIN` | Exibe total de inscritos, vagas disponíveis e percentual de ocupação por evento |
| `GET` | `/relatorios/eventos/categorias` | `ADMIN` | Agrupa total de eventos, capacidade total e inscrições por categoria |
| `GET` | `/relatorios/participantes/cursos` | `ADMIN` | Consolida total de participantes e inscrições agrupados por curso |

---

## 🔑 Como Cadastrar Usuários e Obter Tokens

### Passo 1: Cadastrar um usuário
Envie uma requisição `POST` para a rota de cadastro de usuários informando nome, e-mail, senha e perfil (`"ADMIN"` ou `"USUARIO"`):

```json
{
  "nome": "Administrador Sistema",
  "email": "admin@email.com",
  "senha": "123456",
  "perfil": "ADMIN"
}
```

### Passo 2: Realizar login e obter o Token JWT
Envie uma requisição `POST` para a rota de login com as credenciais cadastradas:

```json
{
  "email": "admin@email.com",
  "senha": "123456"
}
```

A API responderá com o token de acesso:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Passo 3: Autenticar no Swagger UI (`/docs`)
1. Clique no botão **`Authorize`** (cadeado no topo direito da página `/docs`).
2. Cole apenas o valor do `access_token` no campo indicado e clique em **Authorize**.
3. Todas as requisições seguintes enviarão automaticamente o cabeçalho `Authorization: Bearer <token>`.

---

## 💻 Exemplos de Utilização da API

### 1. Cadastrar um usuário comum e um administrador (`cURL`)
```bash
curl -X POST "http://127.0.0.1:8000/usuarios" \
  -H "Content-Type: application/json" \
  -d '{"nome": "João Silva", "email": "joao@email.com", "senha": "123456", "perfil": "USUARIO"}'
```

### 2. Criar um evento (Requer token de `ADMIN`)
```bash
curl -X POST "http://127.0.0.1:8000/eventos" \
  -H "Authorization: Bearer SEU_TOKEN_ADMIN" \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Semana de Tecnologia",
    "descricao": "Palestras e workshops de back-end",
    "categoria": "Tecnologia",
    "data": "2026-12-10",
    "capacidade": 50
  }'
```

### 3. Inscrever um participante em um evento
```bash
curl -X POST "http://127.0.0.1:8000/inscricoes" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "id_evento": 1,
    "id_participante": 1
  }'
```

### 4. Consultar relatório de ocupação (Requer token de `ADMIN`)
```bash
curl -X GET "http://127.0.0.1:8000/relatorios/eventos/ocupacao" \
  -H "Authorization: Bearer SEU_TOKEN_ADMIN"
```

---

## 🧪 Roteiro para Reproduzir os Testes

Para validar todos os fluxos de autenticação, autorização e regras de negócio via **Swagger UI** (`http://127.0.0.1:8000/docs`):

1. **Criação de Contas:**
   - Cadastre um usuário com `"perfil": "ADMIN"` e outro com `"perfil": "USUARIO"`.
   - Tente cadastrar novamente com o mesmo e-mail para confirmar o bloqueio de duplicidade (`400 Bad Request`).
2. **Teste de Permissão (`USUARIO` vs `ADMIN`):**
   - Faça login com o usuário de perfil **`USUARIO`**, copie o token e autentique no botão **Authorize**.
   - Tente criar (`POST /eventos`) ou excluir (`DELETE /eventos/{id}`) um evento. A API deve bloquear a ação com erro **`403 Forbidden`**.
3. **Fluxo Administrativo (`ADMIN`):**
   - Faça login com o usuário **`ADMIN`** e atualize o token no botão **Authorize**.
   - Crie dois eventos (ex.: categorias `"Tecnologia"` e `"Gestão"`).
   - Cadastre dois participantes em cursos diferentes (ex.: `"Engenharia de Software"` e `"Mecânica"`).
4. **Inscrições e Regras de Negócio:**
   - Realize inscrições vinculando os participantes aos eventos (`POST /inscricoes`).
   - Tente inscrever o mesmo participante duas vezes no mesmo evento (deve retornar erro `400`).
   - Tente inscrever em um evento com capacidade esgotada ou inexistente (deve retornar `400` ou `404`).
5. **Conferência de Relatórios:**
   - Execute as rotas de `/relatorios/...` e verifique se os totais de inscritos, vagas disponíveis, porcentagens de ocupação e agrupamentos por categoria e curso refletem os dados inseridos.
6. **Expiração de Token:**
   - Aguarde o tempo definido em `EXPIRACAO_TOKEN_MINUTOS` no `.env` e refaça uma requisição protegida para validar a rejeição automática do token expirado (`401 Unauthorized`).