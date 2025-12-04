# Sistema Finanças (Django)

Sistema web completo desenvolvido para **gestão financeira pessoal do
dia a dia**, permitindo registrar receitas e despesas, acompanhar
relatórios mensais e exportar informações para PDF.\
Ideal como exemplo prático de aplicação Django com autenticação, CRUD e
relatórios.

## Funcionalidades

-   ✔️ Cadastro de usuário (registro/login/logout)\
-   ✔️ CRUD completo de transações (receitas e despesas)\
-   ✔️ Relatório financeiro mensal\
-   ✔️ Exportação de relatório para PDF (`xhtml2pdf`)\
-   ✔️ Interface simples utilizando Bootstrap\
-   ✔️ Banco de dados SQLite3\
-   ✔️ Compatível com Django **5.2.8**

## Como rodar localmente

1.  Crie e ative um ambiente virtual (Python 3.10+):

    ``` bash
    python -m venv .venv
    source .venv/bin/activate   # mac/linux
    .venv\Scripts\activate      # windows
    ```

2.  Instale as dependências:

    ``` bash
    pip install -r requirements.txt
    ```

3.  Aplique as migrações:

    ``` bash
    python manage.py migrate
    ```

4.  (Opcional) Crie um superusuário:

    ``` bash
    python manage.py createsuperuser
    ```

5.  Execute o servidor de desenvolvimento:

    ``` bash
    python manage.py runserver
    ```

6.  Acesse no navegador:

        http://127.0.0.1:8000/

## Observações

-   A geração de PDF utiliza **xhtml2pdf**, ideal para PDFs simples.\
-   O projeto foi estruturado como um exemplo real para quem estuda
    Django e precisa de um sistema completo e funcional.
