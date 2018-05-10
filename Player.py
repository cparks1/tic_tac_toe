class Player:
    def __init__(self, piece):
        self.__piece = piece

    @property
    def piece(self):
        return self.__piece

    def play(self, x, y, board):
        if board.turn == self.piece:  # We can make a play
            board.player_make_move(x, y, self)

    def play_random(self, board):
        if board.turn == self.piece:  # We can make a play
            board.player_move_random(self)
