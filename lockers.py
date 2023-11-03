from errors import GameLockedError


class GameLocker:
    """
    Helper for locking the game
    """
    players = []

    def lock_player(self, player: str) -> None:
        """
        Locks current player
        :param player:
        :return:
        """
        if self.is_locked():
            raise GameLockedError('Players already selected. Game is locked!')
        self.players.append(player)

    def is_locked(self) -> bool:
        """
        Checks if game is locked
        :return: bool
        """
        return len(self.players) == 2

    def unlock(self) -> None:
        """
        Removes lock
        :return:
        """
        self.players = []
