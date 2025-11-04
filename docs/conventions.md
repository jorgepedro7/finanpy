# Convenções de Código e Estilo

## Nomenclatura
- **Classes**: `PascalCase` (ex.: `DashboardView`, `AccountForm`).
- **Funções e variáveis**: `snake_case`.
- **Constantes**: `UPPER_CASE`.
- **Choices**: utilize `TextChoices` ou tuplas nomeadas (`CategoryType`).

## Strings e Internacionalização
- Código em inglês; strings exibidas ao usuário em PT-BR.
- Prefira aspas simples em Python (`'Texto'`).

## Importações
- Siga a ordem: padrão da biblioteca → terceiros → internos.
- Utilize linhas em branco entre blocos e evite imports não utilizados.

## Views e Padrões Django
- Prefira **Class-Based Views** (`ListView`, `CreateView`, etc.) com mixins como `LoginRequiredMixin`.
- Delegue validações a `forms.py` quando a lógica envolver formulário.
- Use `select_related`/`prefetch_related` em consultas intensivas (ex.: `TransactionListView`).

## Estrutura Modular
- Cada domínio permanece no próprio app (`accounts`, `categories`, `transactions`, `profiles`, `users`).
- Signals ficam em `signals.py`, importadas em `apps.py`.
- Templates são armazenados em `templates/<app_name>/`.
- Mantenha contextos complexos em métodos utilitários (`get_context_data`).

## Testes
- Utilize `django.test.TestCase`.
- Prefira `setUpTestData` para dados estáticos por classe.
- Mensagens e validações importantes devem ter asserts específicos.

## Convenções de Git e PRs
- Branches: `feature/...`, `fix/...`, `docs/...`.
- Mensagens de commit no infinitivo em inglês (ex.: `add transaction filters`).
- Pull requests devem incluir descrição, checklist de testes e prints quando relevante.
