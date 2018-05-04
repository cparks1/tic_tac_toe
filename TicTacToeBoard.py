from enum import Enum
import random


class BoardPiece(Enum):
    EMPTY = 0
    NAUGHT = 1
    DRAUGHT = 2


class InvalidPlayersException(Exception):
    pass


class TicTacToeBoard:
    def __init__(self, size=3):
        self.__board = [[BoardPiece.EMPTY for x in range(size)] for y in range(size)]  # size X size board (NxN)
        self.__players = list()
        self.__turn = BoardPiece.EMPTY  # No turns may be taken until the 2 players have joined

    def choose_starting_turn(self):
        if len(self.__players) == 2:
            self.__turn = random.randint(BoardPiece.NAUGHT, BoardPiece.DRAUGHT)
        else:
            raise InvalidPlayersException("There must be two players to play a game of Tic Tac Toe.")

    def is_valid_move(self, x, y, player, board_piece):
        if self.__board[x][y] is BoardPiece.EMPTY:
            if player.piece == board_piece:
                return True
        return False
