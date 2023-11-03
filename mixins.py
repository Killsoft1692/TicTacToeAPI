from datetime import datetime

from models import Game, Player
from settings import AVAILABLE_PLAYERS


class GameSavingMixin:
    """
    Mixin for saving game stats
    """

    winner = None
    looser = None

    def save_state(self, **kwargs) -> None:
        kwargs.update({'winner': self.winner, 'looser': self.looser, 'stopped_at': datetime.now()})
        Game.create(**kwargs)

    def lock_participants(self, player_symbol: str) -> None:
        self.winner = Player.resolve_player_from_symbol(player_symbol)
        # Getting looser by looking at the next player's symbol
        self.looser = Player.resolve_player_from_symbol(
            list(filter(lambda x: x != player_symbol, AVAILABLE_PLAYERS))[0]
        )


class GameUnlockingMixin:
    """
    Mixin to unlock a game session
    """

    @staticmethod
    def unlock() -> None:
        from main import game_locker
        game_locker.unlock()

