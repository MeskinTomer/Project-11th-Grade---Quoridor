"""
Author: Tomer Meskin
Date: 24/04/2024
"""

# Imports
import pygame
import os
from Player import Player
from Wall import Wall


# Pygame Constants
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720
REFRESH_RATE = 60
LEFT = 1
SCROLL = 2
RIGHT = 3
BACKGROUND_COLOR = (56, 228, 129)

# Files Constants
FILE_PATH_CURRENT = os.path.dirname(__file__)
FILE_PATH_IMAGES_FOLDER = os.path.join(FILE_PATH_CURRENT, '..', 'Images')
FILE_PATH_BOARD = os.path.join(FILE_PATH_IMAGES_FOLDER, 'quoridor_board.png')
FILE_PATH_BLUE_PLAYER = os.path.join(FILE_PATH_IMAGES_FOLDER, 'player_blue.png')
FILE_PATH_RED_PLAYER = os.path.join(FILE_PATH_IMAGES_FOLDER, 'player_red.png')
FILE_PATH_WALL_HORIZONTAL = os.path.join(FILE_PATH_IMAGES_FOLDER, 'wall_horizontal.png')
FILE_PATH_WALL_VERTICAL = os.path.join(FILE_PATH_IMAGES_FOLDER, 'wall_vertical.png')

# Game Constants
PLAYER_NONE = 0
PLAYER_BLUE = 1
PLAYER_RED = 2
COLS = 9
ROWS = 9


def decide_which_direction(mouse_pos: tuple, player_object: Player, are_adjacent: str, block_array: list) -> str:
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
        if block_array[player_object.block[0]][player_object.block[1] + 1].left == 'clear':
            if add_right != 0:
                if block_array[player_object.block[0]][player_object.block[1] + 1 + add_right // 80].left == 'clear':
                    ret_val = 'right'
            else:
                ret_val = 'right'
    elif x_difference in range(-80 + add_left, -32 + add_left) and y_difference in range(0, 48):
        if block_array[player_object.block[0]][player_object.block[1] - 1].right == 'clear':
            if add_left != 0:
                if block_array[player_object.block[0]][player_object.block[1] - 1 + add_left // 80].right == 'clear':
                    ret_val = 'left'
            else:
                ret_val = 'left'
    elif y_difference in range(80 + add_down, 128 + add_down) and x_difference in range(0, 48):
        if block_array[player_object.block[0] + 1][player_object.block[1]].up == 'clear':
            if add_down != 0:
                if block_array[player_object.block[0] + 1 + add_down // 80][player_object.block[1]].up == 'clear':
                    ret_val = 'down'
            else:
                ret_val = 'down'
    elif y_difference in range(-80 + add_up, -32 + add_up) and x_difference in range(0, 48):
        if block_array[player_object.block[0] - 1][player_object.block[1]].down == 'clear':
            if add_up != 0:
                if block_array[player_object.block[0] - 1 + add_up // 80][player_object.block[1]].down == 'clear':
                    ret_val = 'up'
            else:
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


def is_trying_to_place_wall(mouse_pos: tuple) -> str:
    ret_val = 'invalid'

    # Checking if trying to place horizontal wall
    trying_to_place_horizontal_1 = False
    trying_to_place_horizontal_2 = False
    x_mouse = mouse_pos[0]
    y_mouse = mouse_pos[1]
    x_cord = 16
    y_cord = 64
    for i in range(8):
        if x_cord <= x_mouse < x_cord + 48:
            trying_to_place_horizontal_1 = True
        x_cord += 80
    for j in range(8):
        if y_cord <= y_mouse < y_cord + 32:
            trying_to_place_horizontal_2 = True
        y_cord += 80

    if trying_to_place_horizontal_1 == trying_to_place_horizontal_2 == True:
        ret_val = 'horizontal'

    # Checking if trying to place vertical wall
    trying_to_place_vertical_1 = False
    trying_to_place_vertical_2 = False
    x_cord = 64
    y_cord = 16
    for i in range(8):
        if x_cord <= x_mouse < x_cord + 32:
            trying_to_place_vertical_1 = True
        x_cord += 80
    for j in range(8):
        if y_cord <= y_mouse < y_cord + 48:
            trying_to_place_vertical_2 = True
        y_cord += 80
    if trying_to_place_vertical_1 == trying_to_place_vertical_2 == True:
        ret_val = 'vertical'

    return ret_val


def add_wall_to_list(wall_list: list, side: str, mouse_pos: tuple, blocks_array: list, screen: pygame.display) -> list:
    if side == 'horizontal':
        x_cord = mouse_pos[0] // 80 * 80 + 16
        y_cord = (mouse_pos[1] - 16) // 80 * 80 + 64

        no_other_wall = True
        for i in range(128):
            for j in range(32):
                if screen.get_at((x_cord + i, y_cord + j))[:3] != (67, 33, 57):
                    no_other_wall = False
        if no_other_wall:
            wall = Wall(x_cord, y_cord, side)
            wall_list.append(wall)

            blocks_array[(y_cord - 16) // 80][x_cord // 80].update_wall('down')
            blocks_array[(y_cord - 16) // 80][(x_cord // 80) + 1].update_wall('down')

            blocks_array[((y_cord - 16) // 80) + 1][x_cord // 80].update_wall('up')
            blocks_array[((y_cord - 16) // 80) + 1][(x_cord // 80) + 1].update_wall('up')
    if side == 'vertical':
        y_cord = mouse_pos[1] // 80 * 80 + 16
        x_cord = (mouse_pos[0] - 16) // 80 * 80 + 64

        no_other_wall = True
        for i in range(32):
            for j in range(128):
                if screen.get_at((x_cord + i, y_cord + j))[:3] != (67, 33, 57):
                    no_other_wall = False

        if no_other_wall:
            wall = Wall(x_cord, y_cord, side)
            wall_list.append(wall)

            blocks_array[y_cord // 80][(x_cord - 16) // 80].update_wall('right')
            blocks_array[y_cord // 80 + 1][(x_cord - 16) // 80].update_wall('right')

            blocks_array[y_cord // 80][((x_cord - 16) // 80) + 1].update_wall('left')
            blocks_array[(y_cord // 80) + 1][((x_cord - 16) // 80) + 1].update_wall('left')
    return blocks_array


def check_win(player_blue_object: Player, player_red_object: Player) -> str:
    winner = ''
    if player_blue_object.y == 16:
        winner = 'blue'
    elif player_red_object.y == 656:
        winner = 'red'
    else:
        winner = 'None'
    return winner
