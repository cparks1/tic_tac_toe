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

    def draw_win(self):
        """
        Draws a line through the winning pieces.
        :return: None
        """
        win_area = self.get_win_area()
        if win_area and self.__screen:  # If there is a winner and there is a screen to draw to
            rows = [x[0] for x in win_area]
            cols = [x[1] for x in win_area]

            cell_sz = TicTacToeBoard.resources.sprites.cell_sz  # Cell size should always be square

            if rows == cols == [x for x in range(self.__size)]:  # Diagonal (top left to bottom right)
                pygame.draw.line(self.__screen, TicTacToeBoard.resources.colors.Red, [0, 0], [self.__size*cell_sz, self.__size*cell_sz], 2)
            elif rows == [x for x in range(self.__size)] and cols == [x for x in range(self.__size)[::-1]]:  # Diagonal (bottom left to top right)
                pygame.draw.line(self.__screen, TicTacToeBoard.resources.colors.Red, [0, self.__size * cell_sz], [self.__size * cell_sz, 0], 2)
            elif rows.count(rows[0]) == len(win_area):  # Rows are all the same, horizontal win
                row_screen_coord = rows[0] * cell_sz + cell_sz/2
                pygame.draw.line(self.__screen, TicTacToeBoard.resources.colors.Red, [0, row_screen_coord], [self.__size * cell_sz, row_screen_coord], 2)
            elif cols.count(cols[0]) == len(win_area):  # Columns are all the same, vertical win
                col_screen_coord = cols[0] * cell_sz + cell_sz/2
                pygame.draw.line(self.__screen, TicTacToeBoard.resources.colors.Red, [col_screen_coord, 0], [col_screen_coord, self.__size * cell_sz], 2)

    @property
    def turn(self):
        """
        Returns a BoardPiece enum corresponding to whose turn it is.
        :return: BoardPiece that is currently allowed to make a move.
        """
        return self.__turn

    def new_player(self):
        """
        Creates a new player in the game.
        :return: The player object.
        """
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
        """
        Randomly chooses which player gets to move first.
        :return:
        """
        if len(self.__players) == 2:
            self.__turn = random.choice([BoardPiece.NAUGHT, BoardPiece.DRAUGHT])
            return self.__turn
        else:
            raise InvalidPlayersException("There must be two players to play a game of Tic Tac Toe.")

    def is_valid_move(self, x, y, player):
        """
        Determines if the chosen move by the given player is valid.
        :param x:
        :param y:
        :param player:
        :return: None
        """
        if self.__board[y][x] is BoardPiece.EMPTY:
            if player.piece == self.turn:
                return True
        return False

    def get_winning_areas(self):
        """
        Gets the areas that can be used to make a win (straight horizontals, diagonals, straight verticals)
        and throws them into a list of lists.
        """
        winning_spaces = list()
        for row in self.__board:
            winning_spaces.append(row)
        for column in zip(*self.__board):
            winning_spaces.append(column)

        winning_spaces.append([row[i] for i, row in enumerate(self.__board)])  # Get leading diagonal
        winning_spaces.append([row[::-1][i] for i, row in enumerate(self.__board)])  # Get other diagonal

        return winning_spaces

    def get_win_area(self):
        """
        Gets the area that contains the winning moves.
        :return: List of coordinates (and piece) for each winning piece.
        """
        winning_spaces = list()

        # Get horizontals
        for row_i, row in enumerate(self.__board):
            coords = list()
            for col_i, piece in enumerate(row):
                coords.append((row_i, col_i, piece))
            winning_spaces.append(coords)

        # Get verticals
        for col_i, col in enumerate(zip(*self.__board)):
            coords = list()
            for row_i, piece in enumerate(col):
                coords.append((row_i, col_i, piece))
            winning_spaces.append(coords)

        winning_spaces.append([(i, i, row[i]) for i, row in enumerate(self.__board)])  # Get leading diagonal

        winning_spaces.append([(i, len(row)-1-i, row[::-1][i]) for i, row in enumerate(self.__board)])  # Get other diagonal

        for win_area in winning_spaces:
            if win_area[0][2] is not BoardPiece.EMPTY and [x[2] for x in win_area].count(win_area[0][2]) == len(win_area):
                return win_area

        return None

    def is_finished(self):
        """
        Determines if the game is finished.
        :return: True if the game is finished, False otherwise.
        """
        winning_areas = self.get_winning_areas()  # Diagonals and straights
        for winning_area in winning_areas:
            # If the list is full of one element and isn't an empty space
            if winning_area[0] is not BoardPiece.EMPTY and winning_area.count(winning_area[0]) == len(winning_area):
                return True
        if len(self.get_empty_spaces()) is 0:
            return True

        return False

    def get_winner(self):
        """
        Determines which piece type won the game.
        :return: BoardPiece enum
        """
        winning_areas = self.get_winning_areas()
        for winning_area in winning_areas:
            # If the list is full of one element and isn't an empty space
            if winning_area[0] is not BoardPiece.EMPTY and winning_area.count(winning_area[0]) == len(winning_area):
                return winning_area[0]  # Return the piece type that won

        return BoardPiece.EMPTY  # Tie (or error)

    def player_make_move(self, x, y, player):
        """
        If the move is valid, places a piece by the given player.
        :param x:
        :param y:
        :param player:
        :return: None
        """
        if self.is_valid_move(x, y, player) and \
                self.is_finished() is False:
            self.__board[y][x] = player.piece
            self.__turn = BoardPiece.NAUGHT if player.piece is BoardPiece.DRAUGHT else BoardPiece.DRAUGHT
            self.draw_board()

    def get_empty_spaces(self):
        """
        Gets the coordinates of all empty spaces on the board and returns them in a list.
        :return: List of empty board space coordinates.
        """
        empty_spaces = []
        for y, row in enumerate(self.__board):
            for x, piece in enumerate(row):
                if piece == BoardPiece.EMPTY:
                    empty_spaces.append((x, y))
        return empty_spaces

    def player_move_random(self, player):
        """
        Causes the player to make a move randomly.
        :param player:
        :return: None
        """
        empty_spaces = self.get_empty_spaces()
        if len(empty_spaces) > 0:
            coord = random.choice(self.get_empty_spaces())
            self.player_make_move(coord[0], coord[1], player)

    def reset_game(self):
        """
        Resets the game by wiping the board and clearing the player list.
        :return:
        """
        if self.__screen:
            self.__screen.fill((255, 255, 255))
        self.init_board()
        self.draw_board()

        self.__players.clear()

