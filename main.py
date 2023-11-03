import logging

from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

from game import TicTacToeGame
from models import DB, Player, Game
from lockers import GameLocker

app = Flask(__name__)

# SWAGGER initialization
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "TicTacToe App"
    })

app.register_blueprint(swaggerui_blueprint)

game = TicTacToeGame()
game_locker = GameLocker()


from views import *

if __name__ == "__main__":
    # LOGGING FOR DB QUERIES
    logger = logging.getLogger('peewee')
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.DEBUG)

    DB.connect()
    DB.create_tables([Player, Game])

    app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)
