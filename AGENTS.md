# Repository Guidelines

## Project Structure & Module Organization
- `core/` contém configurações, URLs raiz e entrypoints Django; apps de domínio vivem em `accounts/`, `categories/`, `profiles/`, `transactions/` e `users/`.
- Templates, static assets e forms devem residir dentro do app correspondente (`templates/<app_name>/`, `static/<app_name>/`), mantendo isolamento descrito em `docs/architecture.md`.
- Documentação de suporte está em `docs/`, enquanto agentes especializados e seus mandatos estão em `agents/`.
- O banco local `db.sqlite3` acompanha o repositório e deve ser tratado como ambiente de desenvolvimento.

## Build, Test, and Development Commands
- Criar ambiente: `python -m venv .venv && source .venv/bin/activate` (Linux/macOS) ou `.venv\Scripts\activate` (Windows).
- Instalar dependências: `pip install -r requirements.txt`.
- Sincronizar schema base: `python manage.py migrate`.
- Servidor local: `python manage.py runserver`.
- Testes Django (quando existirem): `python manage.py test <app_name>`; testes E2E via Playwright devem ser executados pelos cenários definidos pelo agente QA.

## Coding Style & Naming Conventions
- Siga PEP 8, use quatro espaços e prefira aspas simples em Python. Comentários e docstrings em inglês; textos exibidos ao usuário em PT-BR.
- Views devem ser Class-Based quando possível; signals ficam em `signals.py` importados via `apps.py`.
- Nomeie migrations e arquivos com foco no domínio (`accounts/migrations/0002_add_type_field.py`), alinhando-se ao roadmap do PRD.

## Testing Guidelines
- Framework padrão: `django.test.TestCase` para unidade/integrado; recorrer a Playwright para fluxos end-to-end e verificação visual.
- Objetivo de cobertura definido no PRD: ≥70% para autenticação e CRUD ao final do MVP.
- Use fixtures mínimas e dados consistentes com o modelo ER descrito no PRD. Nomeie métodos de teste como `test_<feature>_<scenario>()`.

## Commit & Pull Request Guidelines
- O histórico atual é inicial; adote mensagens no imperativo curto (`Add account model signal`) e inclua contexto do PRD ou issue.
- PRs devem conter descrição objetiva, checklist de validação (migrações, testes manuais), e evidências visuais para mudanças de UI.
- Relacione PRs aos agentes ou documentos envolvidos (ex.: “Covered pela diretriz em `agents/frontend-templates.md`”) sempre que aplicável.

## Agent Workflow
- Consulte `agents/README.md` para escolher o agente apropriado antes de iniciar uma tarefa. Cada agente usa MCP servers específicos (context7 para implementação, playwright para QA) e deve ser citado nas entregas quando acionado.
