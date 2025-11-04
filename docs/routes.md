# Rotas e APIs do Finanpy

Este documento descreve as rotas principais expostas pela aplicação. Todas as views seguem o padrão Django com templates renderizados no servidor; quando necessário, formulários enviam dados via POST (`application/x-www-form-urlencoded`). Para integração programática, os exemplos de payloads abaixo usam JSON apenas como referência de campos.

## Autenticação e Página Pública

| Rota | Métodos | Autenticação | Descrição |
| --- | --- | --- | --- |
| `/` | GET | Não | Landing page pública com CTA para login/cadastro. |
| `/login/` | GET, POST | Não (redireciona autenticados) | Formulário de login via e-mail e senha. |
| `/signup/` | GET, POST | Não (redireciona autenticados) | Cadastro de novo usuário. |
| `/logout/` | POST/GET | Sim | Finaliza sessão e retorna à home. |

### Exemplo de payload (login)
```json
{
  "username": "usuario@example.com",
  "password": "SenhaSegura123!"
}
```

### Exemplo de payload (signup)
```json
{
  "email": "novo@finanpy.dev",
  "password1": "SenhaForte!123",
  "password2": "SenhaForte!123"
}
```

## Áreas Autenticadas

| Rota | Métodos | Autenticação | Descrição |
| --- | --- | --- | --- |
| `/dashboard/` | GET | Sim | Visão geral com saldo, totais mensais e transações recentes. |
| `/reports/` | GET | Sim | Relatórios com filtros `data_inicio` e `data_fim`. |
| `/accounts/` | GET | Sim | Lista de contas do usuário com saldo corrente. |
| `/accounts/nova/` | GET, POST | Sim | Cadastro de conta bancária. |
| `/accounts/<id>/editar/` | GET, POST | Sim (somente dono) | Edição de conta existente. |
| `/accounts/<id>/remover/` | GET, POST | Sim (somente dono) | Confirma e remove conta. |
| `/categories/` | GET | Sim | Lista as categorias do usuário. |
| `/categories/nova/` | GET, POST | Sim | Cadastro de categoria (receita ou despesa). |
| `/categories/<id>/editar/` | GET, POST | Sim | Edição de categoria. |
| `/categories/<id>/remover/` | GET, POST | Sim | Remove categoria. |
| `/transactions/` | GET | Sim | Lista de transações com filtros `month` e `year`. |
| `/transactions/nova/` | GET, POST | Sim | Cadastro de transação (receita/despesa). |
| `/transactions/<id>/editar/` | GET, POST | Sim | Edição de transação existente. |
| `/transactions/<id>/remover/` | GET, POST | Sim | Remove transação. |

### Filtros e parâmetros
- `/transactions/?month=2&year=2025`
- `/reports/?data_inicio=2025-01-01&data_fim=2025-01-31`

### Exemplo de payload (criar conta)
```json
{
  "name": "Conta Investimentos",
  "initial_balance": "3500.00",
  "type": "savings"
}
```

### Exemplo de payload (criar transação)
```json
{
  "transaction_date": "2025-01-15",
  "type": "expense",
  "account": 4,
  "category": 9,
  "amount": "220.00",
  "description": "Mercado semanal"
}
```

### Resposta típica após envio bem-sucedido
As views utilizam o padrão Django `HttpResponseRedirect` para retornar o usuário ao índice correspondente (ex.: `/accounts/`). No caso de erros de validação, a página é re-renderizada com mensagens em PT-BR.
