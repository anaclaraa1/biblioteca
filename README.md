# Biblioteca

Projeto da matéria **Banco de Dados**

## Como executar

1. **Clone o repositório**

    ```git
    git clone https://github.com/anaclaraa1/biblioteca.git
    ```

2. **Instale todas as dependências**

    ```ps
    pip install -r requirements.txt
    ```

3. **Crie uma conexão em um banco de dados `MySQL`. Use o schema [`database/schema.sql`](database/schema.sql)**

4. **Crie um arquivo `.env` na raiz do projeto e adicione**

    ```.env
    SECRET_KEY="<CHAVE SECRETA>"
    DATABASE_URI="mysql+mysqlconnector://root<SENHA?>@localhost<PORTA>/db_biblioteca_2m"
    ```

5. **Execute a aplicação**

    ```ps
    flask run --debug
    ```

> [!TIP]
> Use ambiente virtual 😉

Se tudo ocorrer bem, a aplicação está rodando em [`http://localhost:5000`](http://localhost:5000)
