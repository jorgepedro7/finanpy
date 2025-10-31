# Setup de desenvolvimento

## Pré-requisitos
- Python 3.13+ (conforme definido no PRD).
- Pip atualizado (`python -m pip install --upgrade pip`).
- Ambiente virtual recomendado (`venv` ou equivalente).

## Passo a passo sugerido
1. Criar e ativar um ambiente virtual:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows PowerShell
   ```
2. Instalar dependências listadas em `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
3. Garantir que o banco SQLite local existe (o arquivo `db.sqlite3` já está versionado como base vazia).
4. Executar migrações padrão do Django (ainda não há migrações próprias dos apps):
   ```bash
   python manage.py migrate
   ```
5. Rodar o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Convenções adicionais
- Ative o ambiente virtual sempre que for trabalhar no projeto.
- Utilize `python manage.py makemigrations <app>` apenas após implementar modelos conforme o PRD.
- Commits não devem incluir diretórios de ambientes virtuais (`venv/`, `.venv/`) ou arquivos temporários.
