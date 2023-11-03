from functools import wraps

from main import game_locker


def is_game_ready(f):
    """
    Decorator for restricting access to the game in case of missing players.
    :param f:
    :return:
    """
    @wraps(f)
    def inner(*args, **kwargs):
        if game_locker.is_locked():
            return f(*args, **kwargs)
        else:
            return {'error': "Register as a player and ask your fella to register as well to play with you!"}, 400

    return inner


