# Arquitetura e domínios

## Estrutura principal
- `core`: configurações do projeto, roteamento raiz e entrypoints (`asgi.py`, `wsgi.py`, `urls.py`).
- `accounts`: app destinado ao gerenciamento de contas bancárias de usuários.
- `categories`: app destinado ao catálogo de categorias de receita/despesa.
- `transactions`: app destinado ao registro de transações financeiras vinculadas a contas e categorias.
- `profiles`: app destinado a informações adicionais do usuário (perfil estendido).
- `users`: app destinado à customização do modelo de usuário (login por e-mail) e fluxos de autenticação.

Todos os apps acima estão criados, mas atualmente contêm apenas os arquivos padrão gerados pelo Django (`models.py`, `views.py`, `tests.py` sem implementação). Ao desenvolver novas funcionalidades, concentre cada domínio em seu respectivo app para manter a separação definida no PRD.

## Padrões derivado do PRD
- **Modelos e signals**: implementar modelos em `models.py` e signals relacionados em `signals.py`, importados via `apps.py`.
- **Class-Based Views**: priorizar CBVs para CRUDs e páginas, usando mixins do Django quando necessário.
- **Templates**: armazenar templates específicos de um app dentro da pasta `templates/<app_name>/`.
- **Internacionalização**: interface em português brasileiro; mensagens para usuários devem seguir PT-BR.
- **Autenticação**: personalização do `User` (login por e-mail) deve residir em `users/models.py`, mantendo o Django Auth como base.

## Fluxo de dados esperado
O PRD define relacionamentos entre domínios (usuário possui contas, categorias e transações; perfis estendem usuários). Esse desenho servirá de referência para as futuras migrações e integrações entre apps.
