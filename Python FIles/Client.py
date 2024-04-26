"""
Author: Tomer Meskin
Date: 24/04/2024
"""

# Imports
import pygame
import os
from Player import Player
from Block import Block

# Pygame Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720
REFRESH_RATE = 60
LEFT = 1
SCROLL = 2
RIGHT = 3
PLAYER_BACKGROUND = (56, 228, 129)

# Files Constants
FILE_PATH_CURRENT = os.path.dirname(__file__)
FILE_PATH_IMAGES_FOLDER = os.path.join(FILE_PATH_CURRENT, '..', 'Images')
FILE_PATH_BOARD = os.path.join(FILE_PATH_IMAGES_FOLDER, 'quoridor_board.png')
FILE_PATH_BLUE_PLAYER = os.path.join(FILE_PATH_IMAGES_FOLDER, 'player_blue.png')
FILE_PATH_RED_PLAYER = os.path.join(FILE_PATH_IMAGES_FOLDER, 'player_red.png')

# Game Constants
PLAYER_NONE = 0
PLAYER_BLUE = 1
PLAYER_RED = 2
COLS = 9
ROWS = 9

def decide_which_direction(mouse_pos, player_object: Player) -> str:
    x_difference = mouse_pos[0] - player_object.get_coordinates()[0]
    y_difference = mouse_pos[1] - player_object.get_coordinates()[1]
    ret_val = 'invalid'
    if x_difference in range(80, 128) and y_difference in range(0, 48):
        ret_val = 'right'
    if x_difference in range(-80, -32) and y_difference in range(0, 48):
        ret_val = 'left'
    if y_difference in range(80, 128) and x_difference in range(0, 48):
        ret_val = 'down'
    if y_difference in range(-80, -32) and x_difference in range(0, 48):
        ret_val = 'up'
    return ret_val


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
    player_blue_object = Player(336, 656, [8, 4])
    player_red_object = Player(336, 16, [0, 4])

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

    # Inputting starting point of player in the block array
    blocks_array[player_blue_object.block[0]][player_blue_object.block[1]].update_player(PLAYER_BLUE)
    blocks_array[player_red_object.block[0]][player_blue_object.block[1]].update_player(PLAYER_RED)

    # Setting the first player to go
    player_turn_object = player_blue_object
    player_turn_id = PLAYER_BLUE

    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                mouse_pos = pygame.mouse.get_pos()
                side = decide_which_direction(mouse_pos, player_turn_object)
                if side != 'invalid':
                    blocks_array[player_turn_object.block[0]][player_turn_object.block[1]].update_player(PLAYER_NONE)
                if side == 'right':
                    player_turn_object.move_right()
                elif side == 'left':
                    player_turn_object.move_left()
                elif side == 'up':
                    player_turn_object.move_up()
                elif side == 'down':
                    player_turn_object.move_down()
                if side != 'invalid':
                    blocks_array[player_turn_object.block[0]][player_turn_object.block[1]].update_player(player_turn_id)
                    if player_turn_id == PLAYER_BLUE:
                        player_turn_object = player_red_object
                        player_turn_id = PLAYER_RED
                    else:
                        player_turn_object = player_blue_object
                        player_turn_id = PLAYER_BLUE

        screen.blit(board, [0, 0])
        screen.blit(player_blue_image, list(player_blue_object.get_coordinates()))
        screen.blit(player_red_image, list(player_red_object.get_coordinates()))
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
