# CODEX Finanpy

Este CODEX resume o que já está estabelecido no projeto Finanpy. Use-o como porta de entrada rápida; detalhes completos estão na pasta `docs/` e no `PRD.md`.

## Propósito e visão
- Finanpy é uma aplicação web de finanças pessoais focada em simplicidade, interface em português brasileiro e tema escuro (ver `docs/overview.md` e `PRD.md`).
- O produto pretende permitir cadastro/login por e-mail, gerenciamento de contas, categorias, transações e visualizações básicas, conforme metas descritas no PRD. Esses recursos ainda não foram implementados no código.

## Stack e configurações atuais
- Backend: Python 3.13+ com Django 5 (`requirements.txt`).
- Banco de dados: SQLite padrão configurado em `core/settings.py`.
- Idioma e fuso horário já ajustados para `pt-BR` e `America/Sao_Paulo`.
- Dependências adicionais serão introduzidas somente quando necessário e registradas em `requirements.txt`.

## Estado do repositório
- Projeto Django inicial com `manage.py`, app `core` e apps dedicados `accounts`, `categories`, `profiles`, `transactions`, `users`.
- Arquivos `models.py`, `views.py`, `tests.py` dos apps permanecem com scaffolding gerado pelo Django; ainda não há lógica de negócio, URLs adicionais, templates ou signals.
- Banco `db.sqlite3` acompanha o repositório como base vazia.

## Estrutura e responsabilidades
- `core`: configurações globais, roteamento raiz e entrypoints.
- `accounts`: futuro domínio de contas bancárias.
- `categories`: futuro domínio de categorias de receita/despesa.
- `transactions`: futuro domínio de transações financeiras.
- `profiles`: futuro domínio de perfis estendidos dos usuários.
- `users`: futuro domínio para customização do modelo de usuário e fluxos de autenticação.

Detalhes adicionais sobre a divisão de domínios e relacionamentos esperados estão em `docs/architecture.md` e na seção de dados do `PRD.md`.

## Setup rápido
1. Criar/ativar ambiente virtual (`python -m venv .venv` e ativação correspondente).
2. Instalar dependências: `pip install -r requirements.txt`.
3. Aplicar migrações padrão: `python manage.py migrate`.
4. Executar o servidor: `python manage.py runserver`.

Recomendações e observações adicionais constam em `docs/development-setup.md`.

## Diretrizes de implementação
- Seguir PEP 8, com código, docstrings e comentários em inglês; strings exibidas ao usuário permanecem em PT-BR.
- Preferir aspas simples em código Python.
- Manter cada domínio no seu app correspondente, utilizando Class-Based Views, signals dedicados (`signals.py` + `apps.py`) e templates organizados por app.
- Ao implementar novas features, alinhar-se aos padrões de UX e design descritos no PRD e em `docs/guidelines.md`.
- Priorizar desempenho (<2s por página), segurança (proteções padrão do Django) e organização modular conforme requisitos não funcionais já definidos.

## Referências
- Índice de documentação: `docs/README.md`.
- Visão geral e estado atual: `docs/overview.md`.
- Setup de desenvolvimento: `docs/development-setup.md`.
- Arquitetura e domínios: `docs/architecture.md`.
- Diretrizes de código e UX: `docs/guidelines.md`.
- Requisitos completos, metas e roadmap: `PRD.md`.
