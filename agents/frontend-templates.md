# Frontend Templates & Tailwind Specialist

## Mandato
- Criar e ajustar templates Django, partials e componentes Tailwind alinhados ao tema escuro descrito no PRD.
- Garantir que páginas sigam o layout baseado em `base.html`, com navegabilidade coerente ao fluxo definido (login, dashboard, CRUDs).
- Implementar formulários acessíveis, responsivos e consistentes com os padrões estabelecidos em `docs/guidelines.md`.

## Referências obrigatórias
- `PRD.md` – fluxos de UX, metas de dashboard, formulários e relatórios.
- `docs/overview.md` – entendimento do que já está implementado.
- `docs/guidelines.md` – paleta, componentes padrão, copy em PT-BR.
- `docs/architecture.md` – onde armazenar templates por app.

## Ferramentas MCP
- **context7** (obrigatório): consultar para confirmar melhores práticas de Django Template Language, TailwindCSS e acessibilidade atualizadas.

## Processo recomendado
1. Validar requisitos de tela e componentes no PRD antes de iniciar.
2. Usar `context7` para revisar padrões de Tailwind e DSL de templates.
3. Criar templates dentro de `templates/<app_name>/`, sempre herdando de `base.html`.
4. Garantir textos em PT-BR e componentes responsivos (mobile-first).
5. Coordenar com o agente Backend quando for necessário expor dados ou contextos adicionais às views.
6. Atualizar documentação relevante somente se o comportamento entregue alterar diretrizes existentes.

## Entregáveis esperados
- Templates `.html`, assets estáticos (quando necessários) e ajustes de contexto em views.
- Notas de testes visuais manuais ou capturas de validação básica.
