from enum import Enum
import random
from Resources import Resources
import pygame
import Player


class BoardPiece(Enum):
    EMPTY = 0
    NAUGHT = 1
    DRAUGHT = 2


class InvalidPlayersException(Exception):
    pass


class TicTacToeBoard:
    resources = Resources()

    def __init__(self, screen=None, size=3):
        self.__board = [[BoardPiece.EMPTY for x in range(size)] for y in range(size)]  # size X size board (NxN)
        self.__players = list()
        self.__turn = BoardPiece.EMPTY  # No turns may be taken until the 2 players have joined
        self.__screen = screen
        self.__size = size

    def init_board(self):
        self.__board = [[BoardPiece.EMPTY for x in range(self.__size)] for y in range(self.__size)]  # size X size board (NxN)

    @property
    def board(self):
        return self.__board

    @property
    def text_board(self):
        text_list = [['X' if piece is BoardPiece.DRAUGHT else 'O' if piece is BoardPiece.NAUGHT else '_' for piece in row] for row in self.__board]
        return '\r'.join([''.join(row) for row in text_list])

    def draw_board(self):
        cell_resource = TicTacToeBoard.resources.sprites.cell

        cell_x, cell_y = 0, 0

        if self.__screen:
            self.__screen.fill((255, 255, 255))  # Fill the screen white

        for row in self.__board:
            cell_x = 0
            for piece in row:
                piece_resource = TicTacToeBoard.resources.sprites.draught if piece is BoardPiece.DRAUGHT \
                    else TicTacToeBoard.resources.sprites.naught if piece is BoardPiece.NAUGHT else \
                    TicTacToeBoard.resources.sprites.empty

                if self.__screen:
                    self.__screen.blit(cell_resource, (cell_x, cell_y))  # Draw the cell
                    self.__screen.blit(piece_resource, (cell_x + 10, cell_y + 10))  # Draw the piece

                cell_x += cell_resource.get_size()[1]  # Increment the next cell draw column
            cell_y += cell_resource.get_size()[0]  # Increment the next cell draw row

        pygame.display.update()


    @property
    def turn(self):
        return self.__turn

    def new_player(self):
        if len(self.__players) is 1:
            if self.__players[0].piece is BoardPiece.NAUGHT:
                new_player = Player.Player(BoardPiece.DRAUGHT)
            else:
                new_player = Player.Player(BoardPiece.NAUGHT)

        elif len(self.__players) > 2:
            raise InvalidPlayersException("You can only have two players in a game of Tic Tac Toe.")

        else:
            new_player = Player.Player(random.choice([BoardPiece.NAUGHT, BoardPiece.DRAUGHT]))

        self.__players.append(new_player)

        turn = BoardPiece.EMPTY
        if len(self.__players) is 2:
            turn = self.choose_starting_turn()

        return new_player, turn

    def choose_starting_turn(self):
        if len(self.__players) == 2:
            self.__turn = random.choice([BoardPiece.NAUGHT, BoardPiece.DRAUGHT])
            return self.__turn
        else:
            raise InvalidPlayersException("There must be two players to play a game of Tic Tac Toe.")

    def is_valid_move(self, x, y, player):
        if self.__board[y][x] is BoardPiece.EMPTY:
            if player.piece == self.turn:
                return True
        return False

    def get_winning_areas(self):
        """Gets the areas that can be used to make a win (straight horizontals, diagonals, straight verticals)
        and throws them into a list of lists."""
        winning_spaces = list()
        for row in self.__board:
            winning_spaces.append(row)
        for column in zip(*self.__board):
            winning_spaces.append(column)

        winning_spaces.append([row[i] for i, row in enumerate(self.__board)])  # Get leading diagonal
        winning_spaces.append([row[::-1][i] for i, row in enumerate(self.__board)])  # Get other diagonal

        return winning_spaces

    def is_finished(self):
        winning_areas = self.get_winning_areas()  # Diagonals and straights
        for winning_area in winning_areas:
            # If the list is full of one element and isn't an empty space
            if winning_area[0] is not BoardPiece.EMPTY and winning_area.count(winning_area[0]) == len(winning_area):
                return True
        if len(self.get_empty_spaces()) is 0:
            return True

        return False

    def get_winner(self):
        winning_areas = self.get_winning_areas()
        for winning_area in winning_areas:
            # If the list is full of one element and isn't an empty space
            if winning_area[0] is not BoardPiece.EMPTY and winning_area.count(winning_area[0]) == len(winning_area):
                return winning_area[0]  # Return the piece type that won

        return BoardPiece.EMPTY  # Tie (or error)

    def player_make_move(self, x, y, player):
        if self.is_valid_move(x, y, player) and \
                self.is_finished() is False:
            self.__board[y][x] = player.piece
            self.__turn = BoardPiece.NAUGHT if player.piece is BoardPiece.DRAUGHT else BoardPiece.DRAUGHT
            self.draw_board()

    def get_empty_spaces(self):
        empty_spaces = []
        for y, row in enumerate(self.__board):
            for x, piece in enumerate(row):
                if piece == BoardPiece.EMPTY:
                    empty_spaces.append((x, y))
        return empty_spaces

    def player_move_random(self, player):
        empty_spaces = self.get_empty_spaces()
        if len(empty_spaces) > 0:
            coord = random.choice(self.get_empty_spaces())
            self.player_make_move(coord[0], coord[1], player)

    def reset_game(self):
        if self.__screen:
            self.__screen.fill((255, 255, 255))
        self.init_board()
        self.draw_board()

        self.__players.clear()

