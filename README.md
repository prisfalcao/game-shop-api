# Game Collection API

## Descrição do Projeto:

Projeto MVP desenvolvido para o curso de pós-graduação em Desenvolvimento Full Stack da PUC Rio.

A **Game Collection API** é uma API RESTful desenvolvida em Python com Flask, que permite gerenciar uma coleção de jogos, oferecendo funcionalidades para listar, adicionar e excluir jogos, com armazenamento dos dados em um banco de dados SQLite. A documentação interativa está disponível via Swagger, facilitando o uso e teste das rotas.

### Instruções de Instalação:

1. **Clone o repositório**
   ```bash
   git clone https://github.com/prisfalcao/Game-Collectors-Api

2. Navegue até o diretório do projeto:
   ```bash
   cd Game-Collectors-Api

3. É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
4. Instale as dependências com o comando:
   ```bash 
   pip install -r requirements.txt no terminal.

### Executando o projeto:

1. Inicie o servidor Flask com o comando:
   ```bash 
   flask run --host 0.0.0.0 --port 5000

2. Acesse a documentação Swagger:  
   
    No navegador acesse:  
    http://127.0.0.1:5000/openapi
   
    Rotas Disponíveis:  
    * GET	/games - Retorna a lista de jogos  
    * POST	/game	- Adiciona um novo jogo  
    * DELETE	/game	- Remove um jogo pelo ID  

### Contribuindo: 
Contribuições são bem-vindas! Para relatar bugs, sugerir melhorias ou enviar pull requests, por favor, abra uma issue no repositório.

------------------------------------------------
# Game Collection API
## Project Description:
MVP project developed for the Full Stack Development postgraduate course at PUC Rio.

The **Game Collection API** is a RESTful API developed in Python with Flask that allows users to manage a game collection. It offers functionality to list, add, and delete games, with data storage in an SQLite database. Interactive documentation is available via Swagger, making it easy to use and test the routes.

### Installation Instructions:

1. **Clone the repository**
    ```bash
   git clone https://github.com/prisfalcao/Game-Collectors-Api  

2. Navigate to the project directory:
   ```bash
   cd Game-Collectors-Api

3. It is highly recommended to use virtual environments, such as [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).
4. Install dependencies with the following command:
   ```bash 
   pip install -r requirements.txt no terminal.

### Running the Project:
1. Start the Flask server with the command:
   ```bash 
   flask run --host 0.0.0.0 --port 5000

2. Access the Swagger documentation: 
   
    In your browser, go to:  
    http://127.0.0.1:5000/openapi
   
    Available Routes:  
    * GET	/games - Returns the list of games 
    * POST	/game - Adds a new game  
    * DELETE	/game	- Removes a game by ID 

### Contributing:
Contributions are welcome! To report bugs, suggest improvements, or submit pull requests, please open an issue in the repository.
