import numpy as np

import settings
from errors import InvalidMoveError
from mixins import GameSavingMixin, GameUnlockingMixin


class TicTacToeGame(GameSavingMixin, GameUnlockingMixin):
    def __init__(self):
        self.board = np.full(
            (settings.BATTLEFIELD_WITH, settings.BATTLEFIELD_HEIGHT),
            settings.EMPTY_SPACE_HOLDER
        )
        self.current_player = settings.AVAILABLE_PLAYERS[0]

    def stop(self) -> None:
        """
        Stops an active game by clearing a battleground
        :return:
        """
        self.unlock()
        self.board[:] = settings.EMPTY_SPACE_HOLDER

    def __validate_input(self, row: int, col: int) -> None:
        """
        Provides validation of given coordinates
        :param row:
        :param col:
        :return:
        """
        if not (0 <= row < settings.BATTLEFIELD_WITH and 0 <= col < settings.BATTLEFIELD_HEIGHT
                and self.board[row, col] == settings.EMPTY_SPACE_HOLDER):
            raise InvalidMoveError("Invalid move. Try again.")

    def play(self, row: int, col: int) -> str:
        """
        Music can't stop
        TL;DR: This method is not ideal, so if you see a ways of improving it feel free to give me some insights.
        :param row:
        :param col:
        :return: str
        """
        self.__validate_input(row, col)
        # Filling chosen sell with current player
        self.board[row, col] = self.current_player
        if self.check_win():
            # Saving information about participants
            self.lock_participants(self.current_player)
            self.save_state(board=self.board)
            self.stop()
            return f"Player {self.current_player} wins!"
        elif self.check_draw():
            # Kinda rare case, so I believe that this shouldn't be saved. Nobody wanna keep such nasty situations =/
            self.stop()
            return "It's a draw!"
        self.switch_player()
        return "Move successful"

    def check_win(self) -> bool:
        """
        Checks if it was the winning move
        :return: bool
        """
        pattern = self.board == self.current_player
        # Checking horizontal and vertical wins
        out = pattern.all(0).any() | pattern.all(1).any()
        # Checking diagonal wins
        out |= np.diag(pattern).all() | np.diag(pattern[:, ::-1]).all()
        return out

    def check_draw(self) -> bool:
        """
        Covers case when player has no way to play anymore
        :return: bool
        """
        return settings.EMPTY_SPACE_HOLDER not in self.board

    def get_board(self) -> np.array:
        return self.board

    def switch_player(self) -> None:
        """
        Changes an active player
        :return:
        """
        self.current_player = settings.AVAILABLE_PLAYERS[0] \
            if self.current_player == settings.AVAILABLE_PLAYERS[1] else settings.AVAILABLE_PLAYERS[1]
