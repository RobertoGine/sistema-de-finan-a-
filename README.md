# Sistema Finanças (Django)
Projeto exemplo de gerenciamento financeiro mensal com:
- Django 5.2.8
- SQLite3
- Autenticação (registro/login/logout)
- CRUD de transações (receita/despesa)
- Relatório mensal e exportação para PDF (xhtml2pdf)
- Templates com Bootstrap

## Como rodar localmente
1. Crie e ative um virtualenv (recomendo Python 3.10+)
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # mac/linux
   .venv\Scripts\activate   # windows
   ```
2. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Aplique migrações:
   ```bash
   python manage.py migrate
   ```
4. Crie um superuser (opcional):
   ```bash
   python manage.py createsuperuser
   ```
5. Rode o servidor:
   ```bash
   python manage.py runserver
   ```
6. Acesse `http://127.0.0.1:8000/` e registre uma conta ou faça login.

## Notas
- PDF usa `xhtml2pdf` (simples de instalar). Para PDFs com CSS avançado, recomendo `WeasyPrint`.
- Este projeto é um ponto de partida: sinta-se livre para pedir que eu adicione filtros por categoria, export CSV, gráficos ou API REST.
