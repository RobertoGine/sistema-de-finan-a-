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

---

## 🧑‍💻 Autor

**Roberto Giné**  
🎯 Projeto desenvolvido para fins de **gestão financeira pessoal** e portfólio.

---
Licença de Uso Livre para Fins Não Comerciais
Copyright (c) 2025 Roberto Giné

É concedida permissão para qualquer pessoa usar, estudar, copiar e modificar
este software para fins pessoais, educacionais ou de pesquisa, desde que
sejam mantidos os avisos de copyright acima.

É estritamente proibido:

1. Utilizar este software ou qualquer parte dele para fins comerciais,
   incluindo venda, prestação de serviços, licenciamento ou qualquer tipo
   de atividade que gere lucro;

2. Criar versões modificadas deste software com a intenção de venda ou
   distribuição comercial;

3. Distribuir este software sem manter esta licença e os créditos
   originais.

Qualquer uso comercial somente poderá ser realizado mediante autorização
escrita do autor, Roberto Giné.

O software é fornecido "no estado em que se encontra", sem garantias de
qualquer tipo. O autor não se responsabiliza por danos decorrentes do uso
deste software.
