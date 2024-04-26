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


def decide_which_direction(mouse_pos, player_object: Player, are_adjacent: str) -> str:
    add_right, add_left, add_up, add_down = [0, 0, 0, 0]
    if are_adjacent != 'not adjacent':
        if are_adjacent == 'right':
            add_right += 80
        elif are_adjacent == 'left':
            add_left -= 80
        elif are_adjacent == 'down':
            add_down += 80
        elif are_adjacent == 'up':
            add_up -= 80
    x_difference = mouse_pos[0] - player_object.get_coordinates()[0]
    y_difference = mouse_pos[1] - player_object.get_coordinates()[1]
    ret_val = 'invalid'
    if x_difference in range(80 + add_right, 128 + add_right) and y_difference in range(0, 48):
        ret_val = 'right'
    elif x_difference in range(-80 + add_left, -32 + add_left) and y_difference in range(0, 48):
        ret_val = 'left'
    elif y_difference in range(80 + add_down, 128 + add_down) and x_difference in range(0, 48):
        ret_val = 'down'
    elif y_difference in range(-80 + add_up, -32 + add_up) and x_difference in range(0, 48):
        ret_val = 'up'
    return ret_val


def are_players_adjacent(player_blue_object: Player, player_red_object: Player, turn: int) -> str:
    side = 'not adjacent'
    blue_coordinates = player_blue_object.block
    red_coordinates = player_red_object.block
    if turn == 1:
        x_difference = blue_coordinates[1] - red_coordinates[1]
        y_difference = blue_coordinates[0] - red_coordinates[0]
    else:
        x_difference = red_coordinates[1] - blue_coordinates[1]
        y_difference = red_coordinates[0] - blue_coordinates[0]
    if x_difference == 1 and blue_coordinates[0] == red_coordinates[0]:
        side = 'left'
    elif x_difference == -1 and blue_coordinates[0] == red_coordinates[0]:
        side = 'right'
    elif y_difference == 1 and blue_coordinates[1] == red_coordinates[1]:
        side = 'up'
    elif y_difference == -1 and blue_coordinates[1] == red_coordinates[1]:
        side = 'down'
    return side


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
                are_adjacent = are_players_adjacent(player_blue_object, player_red_object, player_turn_id)
                side = decide_which_direction(mouse_pos, player_turn_object, are_adjacent)
                if side != 'invalid':
                    blocks_array[player_turn_object.block[0]][player_turn_object.block[1]].update_player(PLAYER_NONE)
                    if side == 'right':
                        player_turn_object.move_right()
                        if are_adjacent == 'right':
                            player_turn_object.move_right()
                    elif side == 'left':
                        player_turn_object.move_left()
                        if are_adjacent == 'left':
                            player_turn_object.move_left()
                    elif side == 'up':
                        player_turn_object.move_up()
                        if are_adjacent == 'up':
                            player_turn_object.move_up()
                    elif side == 'down':
                        player_turn_object.move_down()
                        if are_adjacent == 'down':
                            player_turn_object.move_down()
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
