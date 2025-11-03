# Visão geral

## Contexto do produto
- Finanpy é um sistema web para gestão financeira pessoal baseado em Django 5, descrito no PRD do projeto.
- O objetivo é oferecer uma experiência simples em português brasileiro, com interface responsiva e tema escuro.
- O PRD define o uso de TailwindCSS via CDN, autenticação nativa do Django com login por e-mail e módulos isolados para cada domínio (contas, categorias, transações, perfis).

## Estado atual do repositório
- Estrutura Django centralizada em apps especializados para usuários, perfis, contas, categorias, transações e core (dashboard, relatórios, páginas públicas).
- Autenticação customizada com login por e-mail, templates Tailwind completos (home pública, login/signup, dashboard, contas, categorias, transações e relatórios).
- Migrações dedicadas implementam `Profile`, `Account` (com saldo atual), `Category` e `Transaction`, com signals para criação automática de perfis e atualização de saldos das contas.
- Views baseadas em classe oferecem CRUD completo para contas, categorias e transações, com mensagens de sucesso em PT-BR, filtros por data e indicadores resumidos.
- Dashboard apresenta saldo consolidado, KPIs mensais, últimas transações, visão das contas e destaques de categorias; página de relatórios fornece filtros por data e tabelas agregadas por conta/categoria.
- Admin do Django exibe modelos customizados com inlines para transações dentro de contas e categorias.

## Como o PRD deve ser lido
- O PRD (`PRD.md`) descreve metas e requisitos planejados, inclusive itens ainda não desenvolvidos.
- Use-o como referência para entender o escopo proposto, mantendo o foco no que já está presente neste repositório ao comunicar progresso ou criar novas tarefas.

## Pendências priorizadas para as próximas sprints
- Containerização com Docker (Dockerfile e docker-compose para empacotar a aplicação e o banco SQLite).
- Testes automatizados (unitários e de integração) cobrindo autenticação e fluxos CRUD principais.
- Integração de gráficos interativos (Chart.js) nos dashboards e relatórios, substituindo os placeholders atuais.
