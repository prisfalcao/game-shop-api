class GameNotFoundError(Exception):
    """Exception thrown when a game id is not found in the database."""

    def __init__(self, message="Game not found. Please check the game_id inserted and try again.", status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class NoGamesFoundError(Exception):
    """Exception thrown when there are no games in the database."""

    def __init__(self, message="There are no games in the store catalog yet, please add a new game.", status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class GameAlreadyExistsError(Exception):
    """Exception thrown when a game with the same name already exists in the database."""

    def __init__(self, message="A game with the same name already exists in the store catalog.", status_code=409):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class DatabaseError(Exception):
    """Generic exception thrown for database errors."""

    def __init__(self, message="Database operation failed", status_code=500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
