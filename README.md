# Game Shop API
## Descrição do Projeto:
Projeto MVP desenvolvido para a sprint de Desenvolvimento Back-end Avançado do curso de pós-graduação em Desenvolvimento Full Stack da PUC Rio.

A **Game Shop API** é uma API RESTful desenvolvida em Python com Flask, que permite gerenciar uma loja fictícia de jogos, com funcionalidades para listar o catálogo de games disponíveis, adicionar, editar e excluir jogos no catálogo da loja, e acessar uma área de admin para importar novos jogos da API externa RAWG com armazenamento dos dados em um banco de dados SQLite. A documentação interativa está disponível via Swagger, facilitando o uso e teste das rotas.

### Instruções de Instalação:
1. **Clone o repositório**
   ```bash
   git clone https://github.com/prisfalcao/game-shop-api

2. Navegue até o diretório do projeto:
   ```bash
   cd game-shop-api

3. É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
4. Instale as dependências com o comando:
   ```bash 
   pip install -r requirements.txt

### Executando o projeto localmente:
1. Inicie o servidor Flask com o comando:
   ```bash 
   flask run --host 0.0.0.0 --port 5000

2. Acesse a documentação Swagger:  
   
    No navegador acesse:  
    http://127.0.0.1:5000/openapi
   
    Rotas Disponíveis:
    * POST /admin-import-games - importa uma lista de jogos da RAWG API, adiciona preço e estoque aleatórios e salva no banco de dados local;
    * GET  /games - Retorna a lista de jogos existentes no banco de dados local; 
    * POST /game - Adiciona um novo jogo ao banco de dados local;
    * PUT  /game - Edita detalhes de estoque e preço de um jogo existente no banco de dados local, através do seu ID;
    * DELETE	/game	- Remove um jogo pelo ID.

    As rotas de POST, PUT e DELETE requerem um token de admin para serem executadas. O token é: admin-secret-token

### Executando o projeto via Docker:
1. No terminal do projeto digite os seguintes comandos:
   ```bash
   docker build -t game-shop-api .
   docker run -p 5000:5000 game-shop-api

### Contribuindo: 
Contribuições são bem-vindas! Para relatar bugs ou sugerir melhorias, por favor, abra uma issue no repositório.

------------------------------------------------
# Game Shop API
## Project Description:
MVP project developed for the Sprint of Advanced Back-end Development of the Full Stack Development postgraduate course at PUC Rio.

The **Game Shop API** is a RESTful API developed in Python with Flask that allows users to manage a fictitious game store. It offers functionalities to list a catalog of available games, add, update and delete games in the catalog, and access an admin area to import new games from the external API RAWG, with data storage in an SQLite database. Interactive documentation is available via Swagger, making it easy to use and test the routes.

### Installation Instructions:

1. **Clone the repository**
    ```bash
   git clone https://github.com/prisfalcao/game-shop-api  

2. Navigate to the project directory:
   ```bash
   cd game-shop-api

3. It is highly recommended to use virtual environments, such as [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
4. Install dependencies with the following command:
   ```bash 
   pip install -r requirements.txt

### Running the project locally:
1. Start the Flask server with the command:
   ```bash 
   flask run --host 0.0.0.0 --port 5000

2. Access the Swagger documentation: 
    In your browser, go to:  
    http://127.0.0.1:5000/openapi
   
    Available Routes:
    * POST /admin-import-games - imports a list of games from the RAWG API, adds random price and stock values and saves them to the local database;  
    * GET  /games - Returns the list of existing games in the local database;
    * POST /game - Adds a new game to the local database;
    * PUT  /game - Edits the stock and price details of an existing game in the local database, using its ID;
    * DELETE /game - Removes a game by ID

    The routes for POST, PUT and DELETE will require an admin token, it is: admin-secret-token

### Running the project on Docker:
1. On your terminal run the following commands:
   ```bash
   docker build -t game-shop-api .
   docker run -p 5000:5000 game-shop-api

### Contributing:
Contributions are welcome! To report bugs or suggest improvements, please open an issue in the repository.
