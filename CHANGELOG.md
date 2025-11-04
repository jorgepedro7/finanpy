# Changelog

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

## [v0.1.0] - 2025-11-04
### Documentação e Entrega Final (Sprint 7)
- Adicionado `README.md` completo com visão geral, setup e mermaid diagram.
- Criados guias em `docs/` para rotas, modelos, convenções e interface (com screenshots).
- Introduzido `CHANGELOG.md` e checklist final de entrega.

### Docker e Testes (Sprint Final)
- Adicionados `Dockerfile` e `docker-compose.yml`.
- Configurado volume nomeado para persistir `db.sqlite3`.
- Criada suíte de testes unitários com cobertura >90% utilizando `coverage`.

### Relatórios e Polimento (Sprint 6)
- Implementados relatórios com filtros por data e agregações por categoria/conta.
- Adicionadas mensagens flash e responsividade nos templates.
- Revisão geral de UX e documentação de pendências futuras.

### Transações (Sprint 5)
- Criado modelo `Transaction` com signals para atualizar saldo das contas.
- Implementado CRUD completo com filtros mensais.
- Dashboard passou a exibir as 10 últimas transações.

### Categorias (Sprint 4)
- Implementado modelo `Category` com cores Tailwind e CRUD dedicado.
- Links e estatísticas de categorias integrados ao dashboard.

### Contas Bancárias (Sprint 3)
- Implementado modelo `Account` com saldo atual e sinal de recalculo.
- Criado CRUD de contas com mensagens em PT-BR.
- Dashboard exibe saldo consolidado e detalhes por conta.

### Perfis e Dashboard Básico (Sprint 2)
- Adicionada criação automática de `Profile` via signal.
- Dashboard inicial com placeholders, sidebar e atalhos.

### Setup e Autenticação (Sprint 1)
- Projeto Django configurado com idioma pt-BR e fuso America/Sao_Paulo.
- Customização do modelo `User` para e-mail como credencial.
- Views/templates de login, cadastro, logout e home pública em tema escuro.

[v0.1.0]: https://github.com/finanpy/finanpy/releases/tag/v0.1.0
