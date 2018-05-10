import pygame
from TicTacToeBoard import TicTacToeBoard


def main():
    board_size = 3
    game_board_size = (board_size*32, board_size*32)

    pygame.init()  # Initialize the pygame module

    screen = pygame.display.set_mode(game_board_size)  # Create a surface on screen large enough to hold all pieces
    screen.fill((255, 255, 255))  # Fill the screen white
    pygame.display.set_caption('Tic Tac Toe')

    clock = pygame.time.Clock()

    board = TicTacToeBoard(screen, size=board_size)

    running = True  # Variable used to control the main loop
    while running:  # Main loop
        for event in pygame.event.get():  # Event handling (Gets all events from the event queue)
            if event.type == pygame.QUIT:  # Quitting? Run tear down, break run loop.
                running = False  # Kill the run loop

        players = [board.new_player(), board.new_player()]
        while board.is_finished() is False:  # Play until a win or full
            for player, _ in players:
                if board.turn == player.piece:
                    board.player_move_random(player)


        pygame.display.update()
        clock.tick(2)
        board.reset_game()


if __name__ == "__main__":
    main()
