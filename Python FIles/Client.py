"""
Author: Tomer Meskin
Date: 24/04/2024
"""

# Imports
import pygame
import socket
import os
import time
from Player import Player
from Block import Block
from Wall import Wall
from datetime import datetime
import select
from GameFunctions import *
from Protocol import *


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

# Socket Constants
IP = '127.0.0.1'
PORT = 1779

# Commands
ID = 'identification'
ID_ONE = 'player one'
ID_TWO = 'player two'
TURN = 'turn'
YOUR_TURN = 'your turn'
NOT_YOUR_TURN = 'not your turn'
MOVE = 'move'
MOVE_RIGHT = 'right'
MOVE_LEFT = 'left'
MOVE_UP = 'up'
MOVE_DOWN = 'down'
WALL = 'wall'
ACK = 'acknowledgement'
ACK_VALID = 'valid'
ACK_INVALID = 'invalid'


def main():
    # Booting up pygame and creating screen
    pygame.init()
    size = (WINDOW_WIDTH, WINDOW_HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Quoridor")
    clock = pygame.time.Clock()

    # Drawing board
    board = pygame.image.load(FILE_PATH_BOARD)
    screen.blit(board, (0, 0))

    # Drawing blue player
    player_blue_image = pygame.image.load(FILE_PATH_BLUE_PLAYER).convert()
    player_blue_image.set_colorkey(BACKGROUND_COLOR)
    screen.blit(player_blue_image, [336, 656])

    # Drawing red player
    player_red_image = pygame.image.load(FILE_PATH_RED_PLAYER).convert()
    player_red_image.set_colorkey(BACKGROUND_COLOR)
    screen.blit(player_red_image, [336, 16])

    pygame.display.flip()

    # Creating Player objects
    player_blue_object = Player(336, 656, [8, 4])
    player_red_object = Player(336, 16, [0, 4])

    # Loading wall images
    wall_horizontal_image = pygame.image.load(FILE_PATH_WALL_HORIZONTAL).convert()
    wall_horizontal_image.set_colorkey(BACKGROUND_COLOR)

    wall_vertical_image = pygame.image.load(FILE_PATH_WALL_VERTICAL).convert()
    wall_vertical_image.set_colorkey(BACKGROUND_COLOR)

    # Creating Wall list
    wall_list = []

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
    blocks_array[player_red_object.block[0]][player_red_object.block[1]].update_player(PLAYER_RED)

    # Setting the first player to go
    player_turn_object = player_blue_object
    player_turn_id = PLAYER_BLUE

    # Setting text box for timer
    font = pygame.font.Font('freesansbold.ttf', 55)
    text = font.render('01:00', True, (0, 255, 0), (0, 0, 128))
    text_object = text.get_rect()
    text_object.center = (800, 150)

    # Setting timer
    start_time = datetime.now().time()
    print(start_time.second)

    # Setting turn variable
    turn = False

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, PORT))
    except socket.error as err:
        print(err)

    # Setting ID
    data = protocol_recv(my_socket)
    if data[0] == ID:
        if data[1] == ID_ONE:
            my_socket.send(shape_command(ACK, ACK_VALID))
        else:
            my_socket.send(shape_command(ACK, ACK_VALID))

    # Setting turns
    data = protocol_recv(my_socket)
    if data[0] == TURN:
        if data[1] == YOUR_TURN:
            turn = True
            my_socket.send(shape_command(ACK, ACK_VALID))
        else:
            turn = False
            my_socket.send(shape_command(ACK, ACK_VALID))

    inputs = [my_socket]
    outputs = []

    finish = False
    while not finish:
        if turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    finish = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT and turn:
                    mouse_pos = pygame.mouse.get_pos()
                    side = player_movement_function(mouse_pos, blocks_array, player_turn_id, player_turn_object, player_blue_object, player_red_object)
                    if side != 'invalid':
                        turn = False
                        if player_turn_id == PLAYER_BLUE:
                            player_turn_object = player_red_object
                            player_turn_id = PLAYER_RED
                        else:
                            player_turn_object = player_blue_object
                            player_turn_id = PLAYER_BLUE
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT and turn:
                    mouse_pos = pygame.mouse.get_pos()
                    side = wall_addition_function(mouse_pos, wall_list, blocks_array, screen)
                    if side != 'invalid':
                        turn = False
                        if player_turn_id == PLAYER_BLUE:
                            player_turn_object = player_red_object
                            player_turn_id = PLAYER_RED
                        else:
                            player_turn_object = player_blue_object
                            player_turn_id = PLAYER_BLUE
        else:
            readable, writable, exceptional = select.select(inputs, outputs, inputs, 0.1)

            for s in readable:
                if s is my_socket:
                    data = protocol_recv(s)
                    if data:
                        print(data)
                        if data[0] == TURN:
                            if data[1] == YOUR_TURN:
                                turn = True
                                player_turn_object = player_blue_object
                                player_turn_id = PLAYER_BLUE
                                my_socket.send(shape_command(ACK, ACK_VALID))
                            elif data[1] == NOT_YOUR_TURN:
                                turn = False
                                player_turn_object = player_red_object
                                player_turn_id = PLAYER_RED
                                my_socket.send(shape_command(ACK, ACK_VALID))
                        elif data[0] == MOVE:
                            mouse_pos = calculate_new_mouse_pos(player_red_object, data[1])
                            side = player_movement_function(mouse_pos, blocks_array, player_turn_id, player_turn_object, player_blue_object, player_red_object)
                            if side != 'invalid':
                                my_socket.send(shape_command(ACK, ACK_VALID))
                        elif data[0] == WALL:
                            wall_pos = (int(data[1].split(' ')[0]), int(data[1].split(' ')[1]))
                            side = wall_addition_function(wall_pos, wall_list, blocks_array, screen)
                            if side != 'invalid':
                                my_socket.send(shape_command(ACK, ACK_VALID))

                    else:
                        print('closed')
                        finish = True

        screen.blit(board, [0, 0])
        screen.blit(player_blue_image, list(player_blue_object.get_coordinates()))
        screen.blit(player_red_image, list(player_red_object.get_coordinates()))
        screen.blit(text, text_object)
        for wall_object in wall_list:
            if wall_object.side == 'horizontal':
                screen.blit(wall_horizontal_image, list(wall_object.get_coordinates()))
            else:
                screen.blit(wall_vertical_image, list(wall_object.get_coordinates()))
        pygame.display.flip()
        clock.tick(REFRESH_RATE)

        # Check if someone won the game
        winner = check_win(player_blue_object, player_red_object)
        if winner != 'None':
            time.sleep(5)

            for i in range(ROWS):
                for j in range(COLS):
                    blocks_array[i][j].restart_block()

            player_blue_object.restart('blue')
            player_red_object.restart('red')

            blocks_array[player_blue_object.block[0]][player_blue_object.block[1]].update_player(PLAYER_BLUE)
            blocks_array[player_red_object.block[0]][player_red_object.block[1]].update_player(PLAYER_RED)

            wall_list.clear()

    pygame.quit()


if __name__ == '__main__':
    main()
