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
LEFT = 1
SCROLL = 2
RIGHT = 3
PLAYER_BACKGROUND = (56, 228, 129)
COLS = 9
ROWS = 9

# Files Constants
FILE_PATH_CURRENT = os.path.dirname(__file__)
FILE_PATH_IMAGES_FOLDER = os.path.join(FILE_PATH_CURRENT, '..', 'Images')
FILE_PATH_BOARD = os.path.join(FILE_PATH_IMAGES_FOLDER, 'quoridor_board.png')
FILE_PATH_BLUE_PLAYER = os.path.join(FILE_PATH_IMAGES_FOLDER, 'player_blue.png')
FILE_PATH_RED_PLAYER = os.path.join(FILE_PATH_IMAGES_FOLDER, 'player_red.png')


class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def get_position(self) -> tuple:
        return self.x, self.y

    def move_up(self) -> None:
        self.y -= 80

    def move_down(self) -> None:
        self.y += 80

    def move_right(self) -> None:
        self.x += 80

    def move_left(self) -> None:
        self.x -= 80


class Block:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.player = 0
        self.up = 'clear'
        self.down = 'clear'
        self.right = 'clear'
        self.left = 'clear'

    def update_position(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_position(self) -> tuple:
        return self.x, self.y

    def update_player(self, player: int) -> None:
        self.player = player

    def update_wall(self, side: str) -> None:
        if side == 'up':
            self.up = 'blocked'
        elif side == 'down':
            self.down = 'blocked'
        elif side == 'right':
            self.right = 'blocked'
        elif side == 'left':
            self.left = 'blocked'

    def get_wall_status(self, side: str) -> str:
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
    # Booting up pygame and creating screen
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Quoridor")

    # Drawing board
    board = pygame.image.load(FILE_PATH_BOARD)
    screen.blit(board, (0, 0))

    # Drawing blue player
    player_blue_image = pygame.image.load(FILE_PATH_BLUE_PLAYER).convert()
    player_blue_image.set_colorkey(PLAYER_BACKGROUND)
    screen.blit(player_blue_image, [336, 656])

    # Drawing red player
    player_red_image = pygame.image.load(FILE_PATH_RED_PLAYER).convert()
    player_red_image.set_colorkey(PLAYER_BACKGROUND)
    screen.blit(player_red_image, [336, 16])
    pygame.display.flip()

    # Creating Player objects
    player_blue_object = Player(336, 656)
    player_red_object = Player(336, 16)

    # Creating 2D array for representation of board
    blocks_array = [[Block for _ in range(COLS)] for _ in range(ROWS)]
    x_block = 16
    y_block = 16

    # Setting coordinates for the Blocks in the board
    for i in range(ROWS):
        x_block = 16
        for j in range(COLS):
            blocks_array[i][j] = Block(x_block, y_block)
            x_block += 80
        y_block += 80

    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
        screen.blit(board, [0, 0])
        screen.blit(player_blue_image, list(player_blue_object.get_position()))
        screen.blit(player_red_image, list(player_red_object.get_position()))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
