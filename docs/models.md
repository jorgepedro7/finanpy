# Modelos e Relacionamentos

## User (`users.User`)
- **Base**: `AbstractUser` sem campo `username`.
- **Campos principais**:
  - `email` (`EmailField`, único) – usado como `USERNAME_FIELD`.
  - Campos padrão do Django (`password`, `is_active`, etc.).
- **Manager**: `UserManager` com validação de e-mail obrigatório.
- **Relacionamentos**: um usuário possui `Profile`, `Account`, `Category` e `Transaction`.

## Profile (`profiles.Profile`)
- `user` (`OneToOneField` → `User`, `on_delete=CASCADE`, `related_name='profile'`).
- `full_name` (`CharField`, opcional).
- `photo` (`ImageField`, opcional, `upload_to='profiles/photos/'`).
- `created_at` / `updated_at` (`DateTimeField`).
- **Signal**: `post_save` em `profiles/signals.py` cria automaticamente um `Profile` ao salvar um novo `User`.

## Account (`accounts.Account`)
- `user` (`ForeignKey` → `User`, `on_delete=CASCADE`, `related_name='accounts'`).
- `name` (`CharField`).
- `initial_balance` (`DecimalField`, default 0.00).
- `current_balance` (`DecimalField`, recalculado automaticamente).
- `type` (`CharField` com choices `checking`, `savings`, `credit`).
- `created_at` / `updated_at`.
- **Signals**:
  - `accounts/signals.py` recalcula saldo em `post_save`/`post_delete` de `Transaction`.
  - `pre_save` guarda conta anterior para tratar transferências entre contas.

## Category (`categories.Category`)
- `user` (`ForeignKey` → `User`, `on_delete=CASCADE`, `related_name='categories'`).
- `name` (`CharField`).
- `type` (`CharField` com choices `income`, `expense`).
- `color` (`CharField`, classes Tailwind pré-definidas).
- `created_at` / `updated_at`.
- **Uso**: classifica transações por natureza (receita/despesa).

## Transaction (`transactions.Transaction`)
- `user` (`ForeignKey` → `User`, `on_delete=CASCADE`, `related_name='transactions'`).
- `account` (`ForeignKey` → `Account`, `on_delete=CASCADE`, `related_name='transactions'`).
- `category` (`ForeignKey` → `Category`, `on_delete=SET_NULL`, opcional).
- `amount` (`DecimalField`).
- `description` (`CharField`, opcional).
- `transaction_date` (`DateField`).
- `type` (`CharField`, choices `income`, `expense`).
- `created_at` / `updated_at`.
- **Signals**: integrados com `accounts.signals` para atualizar `current_balance` após qualquer alteração.

## Fluxo de criação (resumo)
1. Usuário cadastra conta → `Account.save()` garante `current_balance` inicial.
2. Usuário registra transação → signals recalculam saldo da conta (e da antiga conta em caso de edição).
3. Relatórios (`core.views.ReportsView`) usam agregações (`Sum`, `Coalesce`) para produzir totais por categoria/conta.
