"""
Author: Tomer Meskin
Date: 24/04/2024
"""

# Imports
import pygame
import os

# Pygame Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720
REFRESH_RATE = 60
PLAYER_BACKGROUND = (56, 228, 129)

# Files Constants
FILE_PATH_CURRENT = os.path.dirname(__file__)
FILE_PATH_IMAGES_FOLDER = os.path.join(FILE_PATH_CURRENT, '..', 'Images')
FILE_PATH_BOARD = os.path.join(FILE_PATH_IMAGES_FOLDER, 'quoridor_board.png')
FILE_PATH_BLUE_PLAYER = os.path.join(FILE_PATH_IMAGES_FOLDER, 'player_blue.png')
FILE_PATH_RED_PLAYER = os.path.join(FILE_PATH_IMAGES_FOLDER, 'player_red.png')


def main():
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Quoridor")

    clock = pygame.time.Clock()

    board = pygame.image.load(FILE_PATH_BOARD)
    screen.blit(board, (0, 0))

    player_blue = pygame.image.load(FILE_PATH_BLUE_PLAYER).convert()
    player_blue.set_colorkey(PLAYER_BACKGROUND)
    screen.blit(player_blue, [336, 656])

    player_red = pygame.image.load(FILE_PATH_RED_PLAYER).convert()
    player_red.set_colorkey(PLAYER_BACKGROUND)
    screen.blit(player_red, [336, 16])
    pygame.display.flip()

    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        pygame.display.flip()
        clock.tick(REFRESH_RATE)

    pygame.quit()


if __name__ == '__main__':
    main()
