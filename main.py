import pygame
from TicTacToeBoard import TicTacToeBoard, BoardPiece


def main():
    board_size = 3
    game_board_size = (board_size*50, board_size*50)

    pygame.init()  # Initialize the pygame module

    screen = pygame.display.set_mode(game_board_size)  # Create a surface on screen large enough to hold all pieces
    screen.fill((255, 255, 255))  # Fill the screen white
    pygame.display.set_caption('Tic Tac Toe')

    clock = pygame.time.Clock()

    board = TicTacToeBoard(screen, size=board_size)
    #board = TicTacToeBoard(size=board_size)

    running = True  # Variable used to control the main loop
    game_count = 0  # Counts the number of games played
    while running:  # Main loop
        for event in pygame.event.get():  # Event handling (Gets all events from the event queue)
            if event.type == pygame.QUIT:  # Quitting? Run tear down, break run loop.
                running = False  # Kill the run loop

        players = [board.new_player(), board.new_player()]
        while board.is_finished() is False:  # Play until a win or full
            for player, _ in players:
                if board.turn == player.piece:
                    board.player_move_random(player)
                    clock.tick(4)

        game_count += 1
        winner = board.get_winner()
        if winner is BoardPiece.EMPTY:
            print("Game %d: Tie!" % game_count)
        else:
            board.draw_win()
            print("Game %d: %s won!" % (game_count, "DRAUGHT" if winner is BoardPiece.DRAUGHT else "NAUGHT"))

        pygame.display.update()
        clock.tick(3)
        board.reset_game()


if __name__ == "__main__":
    main()
