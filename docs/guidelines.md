# Diretrizes de código e UX

## Código e organização
- Seguir PEP 8 e utilizar nomes, docstrings e comentários em inglês.
- Preferir aspas simples em código Python.
- Manter cada domínio em seu app dedicado (accounts, categories, profiles, transactions, users) para preservar isolamento.
- Utilizar Class-Based Views para páginas e CRUDs, conforme o padrão descrito no PRD.
- Criar signals em arquivos próprios (`signals.py`), registrando-os em `apps.py` do respectivo app.
- Escrever futuras migrations com atenção à coerência entre domínios descrita no PRD (User → Profile → Accounts/Categories → Transactions).

## Interface e experiência do usuário
- Conteúdo textual exibido para o usuário final deve estar em português brasileiro.
- Templates devem herdar de um layout base (`base.html`) com tema escuro, seguindo o design indicado:
  - Uso de TailwindCSS via CDN.
  - Gradientes indigo/azul para ações principais, cinzas escuros para fundos e cartões.
  - Botões principais com gradiente (`from-indigo-600 to-blue-700`) e estados de hover.
  - Inputs com fundo escuro, bordas cinza e foco com `ring` indigo.
- Layout responsivo mobile-first, com grid flexível em dashboards e formulários acessíveis (labels, ARIA quando necessário).
- Sidebar e navbar devem manter consistência de estilos e posicionamento conforme orientação do PRD.

## Requisitos não funcionais a observar
- Performance: páginas devem carregar em menos de 2 segundos; consultas críticas precisam ser otimizadas.
- Segurança: manter proteções padrão do Django (CSRF, XSS), armazenar senhas/hashes conforme framework.
- Manutenibilidade: evitar lógica compartilhada entre apps sem reutilização clara; priorizar testes unitários à medida que as features forem implementadas.
- Escalabilidade: manter dependências mínimas e preparar código para futura migração de banco, conforme evolução planejada.
