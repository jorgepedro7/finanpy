# Checklist de Entrega

- [x] **Templates em PT-BR**  
  Revisados os principais templates (`core/templates`, `accounts/templates`, `categories/templates`, `transactions/templates`, `users/templates`) confirmando que labels, mensagens e chamadas estão em português brasileiro.

- [x] **Arquivos estáticos servidos corretamente**  
  Aplicação utiliza Tailwind via CDN e assets estáticos padrão do Django. A execução local (`python manage.py runserver`) confirma carregamento sem erros de console.

- [x] **Ausência de dados sensíveis hardcoded**  
  Configurações públicas (`settings.py`) utilizam secret key apenas para desenvolvimento. Nenhum token ou credencial adicional foi encontrado com `rg -n \"SECRET\"` e inspeção manual.

- [x] **Consistência visual e tipográfica**  
  Screenshots capturados (ver `docs/ui.md`) garantem alinhamento com paleta, tipografia e componentes definidos no PRD.

- [x] **Execução em ambiente limpo**  
  Passos de setup reexecutados em ambiente virtual local (`python -m venv`, `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py runserver`) validando que não há dependências externas.
