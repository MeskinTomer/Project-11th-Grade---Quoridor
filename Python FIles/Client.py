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


class Player:
    def __init__(self):
        self.x = 0
        self.y = 0

    def get_position(self):
        return self.x, self.y

    def move_up(self):
        self.y -= 80

    def move_down(self):
        self.y += 80

    def move_right(self):
        self.x += 80

    def move_left(self):
        self.x -= 80


class Block:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.player = 0
        self.up = 'clear'
        self.down = 'clear'
        self.right = 'clear'
        self.left = 'clear'

    def update_position(self, x, y):
        self.x = x
        self.y = y

    def update_player(self, player):
        self.player = player

    def update_wall(self, side):
        if side == 'up':
            self.up = 'blocked'
        elif side == 'down':
            self.down = 'blocked'
        elif side == 'right':
            self.right = 'blocked'
        elif side == 'left':
            self.left = 'blocked'

    def get_wall_status(self, side):
        ret = ''
        if side == 'up':
            ret = self.up
        elif side == 'down':
            ret = self.down
        elif side == 'right':
            ret = self.right
        elif side == 'left':
            ret = self.left
        return ret


def main():
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Quoridor")

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

    pygame.quit()


if __name__ == '__main__':
    main()
