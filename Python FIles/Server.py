"""
Author: Tomer Meskin
Date: 12/5/2024
"""

# Imports
import socket
import pygame
import os
import datetime
from Player import Player
from Block import Block
from Wall import Wall
from GameFunctions import *
from Protocol import *

# Socket Constants
QUEUE_SIZE = 1
IP = '0.0.0.0'
PORT = 1779
SOCKET_TIMEOUT = 90

# Game Constants
PLAYER_NONE = 0
PLAYER_BLUE = 1
PLAYER_RED = 2
COLS = 9
ROWS = 9

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
NO_MOVE = 'no move'
BLANK = ''
WIN = 'win'
DISCONNECT = 'disconnect'
ACK = 'acknowledgement'
ACK_VALID = 'valid'
ACK_INVALID = 'invalid'


def invert_movement(direction: str):
    if direction == MOVE_UP:
        ret_val = MOVE_DOWN
    elif direction == MOVE_DOWN:
        ret_val = MOVE_UP
    elif direction == MOVE_RIGHT:
        ret_val = MOVE_LEFT
    elif direction == MOVE_LEFT:
        ret_val = MOVE_RIGHT
    else:
        ret_val = 'invalid'
    return ret_val


def invert_wall_cords(wall_pos, side):
    x_wall = int(wall_pos.split(' ')[0])
    y_wall = int(wall_pos.split(' ')[1])
    print('x: ' + str(x_wall) + ' y: ' + str(y_wall))
    if side == 'horizontal':
        ret_val = (592 - x_wall, 688 - y_wall)
    elif side == 'vertical':
        ret_val = (688 - x_wall, 592 - y_wall)
    else:
        ret_val = ()
    return ret_val


def add_wall_without_graphics(wall_pos, wall_list, blocks_array, side):
    if side == 'horizontal':
        x_cord = wall_pos[0] // 80 * 80 + 16
        y_cord = (wall_pos[1] - 16) // 80 * 80 + 64

        no_other_wall = True
        for wall in wall_list:
            if wall.get_coordinates() == (x_cord, y_cord):
                no_other_wall = False
            elif wall.get_coordinates() == (x_cord + 48, y_cord - 48):
                no_other_wall = False
            elif wall.get_coordinates() == (x_cord - 80, y_cord):
                no_other_wall = False
            elif wall.get_coordinates() == (x_cord + 80, y_cord):
                no_other_wall = False

        if no_other_wall:
            wall = Wall(x_cord, y_cord, side)
            wall_list.append(wall)

            blocks_array[(y_cord - 16) // 80][x_cord // 80].update_wall('down')
            blocks_array[(y_cord - 16) // 80][(x_cord // 80) + 1].update_wall('down')

            blocks_array[((y_cord - 16) // 80) + 1][x_cord // 80].update_wall('up')
            blocks_array[((y_cord - 16) // 80) + 1][(x_cord // 80) + 1].update_wall('up')
    if side == 'vertical':
        y_cord = wall_pos[1] // 80 * 80 + 16
        x_cord = (wall_pos[0] - 16) // 80 * 80 + 64

        no_other_wall = True
        for wall in wall_list:
            if wall.get_coordinates() == (x_cord, y_cord):
                no_other_wall = False
            elif wall.get_coordinates() == (x_cord - 48, y_cord + 48):
                no_other_wall = False
            elif wall.get_coordinates() == (x_cord, y_cord - 80):
                no_other_wall = False
            elif wall.get_coordinates() == (x_cord, y_cord + 80):
                no_other_wall = False

        if no_other_wall:
            wall = Wall(x_cord, y_cord, side)
            wall_list.append(wall)

            blocks_array[y_cord // 80][(x_cord - 16) // 80].update_wall('right')
            blocks_array[y_cord // 80 + 1][(x_cord - 16) // 80].update_wall('right')

            blocks_array[y_cord // 80][((x_cord - 16) // 80) + 1].update_wall('left')
            blocks_array[(y_cord // 80) + 1][((x_cord - 16) // 80) + 1].update_wall('left')
    return blocks_array


def main():
    # Creating Player objects
    player_blue_object = Player(336, 656, [8, 4])
    player_red_object = Player(336, 16, [0, 4])

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

    # Setting up server and clients sockets
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(QUEUE_SIZE)
        server_socket.settimeout(SOCKET_TIMEOUT)
        print("Listening for connections on port %d" % PORT)

        client_socket1, client_address1 = server_socket.accept()
        client_socket2, client_address2 = server_socket.accept()

        client_socket1.settimeout(SOCKET_TIMEOUT)
        client_socket2.settimeout(SOCKET_TIMEOUT)

        client_socket1.send(shape_command(ID, ID_ONE))
        response = protocol_recv(client_socket1)
        print('ID 1: ' + response[0] + response[1])
        if response[0] == ACK and response[1] == ACK_VALID:
            pass
        else:
            print('Error with Ack after ID - client 1')

        client_socket2.send(shape_command(ID, ID_TWO))
        response = protocol_recv(client_socket2)
        print('ID 2: ' + response[0] + response[1])
        if response[0] == ACK and response[1] == ACK_VALID:
            pass
        else:
            print('Error with Ack after ID - client 2')

        # Setting client 2 - not your turn
        client_socket2.send(shape_command(TURN, NOT_YOUR_TURN))
        response = protocol_recv(client_socket2)
        print('Not Your Turn: ' + response[0] + response[1])
        if response[0] == ACK and response[1] == ACK_VALID:
            pass
        else:
            print('Error with Ack after TURN - client 2')

        # response = protocol_recv(client_socket1)
        # print(response)
        # if response[0] == ACK and response[1] == ACK_VALID:
        #     client_socket1.send(shape_command(WALL, '268 398'))
        # response = protocol_recv(client_socket1)
        # print(response)
        # if response[0] == ACK and response[1] == ACK_VALID:
        #     client_socket1.send(shape_command(TURN, YOUR_TURN))

        # Setting the first player to go
        player_turn_id = PLAYER_BLUE
        player_turn_object = player_blue_object
        current_socket = client_socket1

        # Setting update variable
        update = ()

        # Setting Scoreboard
        score = [0, 0]

        finish = False
        try:
            while not finish:
                # Sending updates
                if update:
                    update_data = update[1]
                    if update[0] == MOVE:
                        update_data = invert_movement(update[1])
                    elif update[0] == WALL:
                        side_update = is_trying_to_place_wall((int(update[1].split(' ')[0]), int(update[1].split(' ')[1])))
                        update_data = invert_wall_cords(update[1], side_update)
                        update_data = str(update_data[0]) + ' ' + str(update_data[1])
                    current_socket.send(shape_command(update[0], update_data))
                    response = protocol_recv(current_socket)
                    print('Update: ' + response[0] + response[1])
                    if response[0] == ACK and response[1] == ACK_VALID:
                        pass
                    else:
                        print('Error with Ack after UPDATE')

                # Sending 'Your Turn'
                current_socket.send(shape_command(TURN, YOUR_TURN))

                response = protocol_recv(current_socket)
                print('Turn: ' + response[0] + response[1])
                if response[0] == ACK and response[1] == ACK_VALID:
                    pass
                else:
                    print('Error with Ack after TURN')

                # Making requested turn
                data = protocol_recv(current_socket)
                if data:
                    print(data)
                    if data[0] == MOVE:
                        direction = data[1]
                        if player_turn_id == PLAYER_RED:
                            direction = invert_movement(direction)
                        mouse_pos = calculate_new_mouse_pos(player_turn_object, player_blue_object, player_red_object, player_turn_id, direction)
                        print(mouse_pos)
                        side = player_movement_function(mouse_pos, blocks_array, player_turn_id, player_turn_object, player_blue_object, player_red_object)
                        if side != 'invalid':
                            current_socket.send(shape_command(ACK, ACK_VALID))
                            update = (data[0], data[1])
                            if player_turn_id == PLAYER_BLUE:
                                player_turn_object = player_red_object
                                current_socket = client_socket2
                                player_turn_id = PLAYER_RED
                            else:
                                player_turn_object = player_blue_object
                                current_socket = client_socket1
                                player_turn_id = PLAYER_BLUE
                        else:
                            current_socket.send(shape_command(ACK, ACK_INVALID))
                    elif data[0] == WALL:
                        wall_pos = (int(data[1].split(' ')[0]), int(data[1].split(' ')[1]))
                        side = is_trying_to_place_wall(wall_pos)
                        if player_turn_id == PLAYER_RED:
                            wall_pos = invert_wall_cords(data[1], side)
                        add_wall_without_graphics(wall_pos, wall_list, blocks_array, side)
                        if side != 'invalid':
                            current_socket.send(shape_command(ACK, ACK_VALID))
                            update = (data[0], data[1])
                            if player_turn_id == PLAYER_BLUE:
                                player_turn_object = player_red_object
                                current_socket = client_socket2
                                player_turn_id = PLAYER_RED
                            else:
                                player_turn_object = player_blue_object
                                current_socket = client_socket1
                                player_turn_id = PLAYER_BLUE
                        else:
                            current_socket.send(shape_command(ACK, ACK_INVALID))
                    elif data[0] == NO_MOVE:
                        current_socket.send(shape_command(ACK, ACK_VALID))
                        update = (data[0], data[1])
                        if player_turn_id == PLAYER_BLUE:
                            player_turn_object = player_red_object
                            current_socket = client_socket2
                            player_turn_id = PLAYER_RED
                        else:
                            player_turn_object = player_blue_object
                            current_socket = client_socket1
                            player_turn_id = PLAYER_BLUE
                    elif data[0] == DISCONNECT:
                        print('Disconnected')
                        if player_turn_id == PLAYER_BLUE:
                            player_turn_object = player_red_object
                            current_socket = client_socket2
                            player_turn_id = PLAYER_RED
                        else:
                            player_turn_object = player_blue_object
                            current_socket = client_socket1
                            player_turn_id = PLAYER_BLUE

                        current_socket.send(shape_command(WIN, BLANK))
                        finish = True

                # Check if someone won the game
                winner = check_win(player_blue_object, player_red_object)
                if winner != 'None':
                    if winner == 'blue':
                        score[0] += 1
                    else:
                        score[1] += 1

                    for i in range(ROWS):
                        for j in range(COLS):
                            blocks_array[i][j].restart_block()

                    player_blue_object.restart('blue')
                    player_red_object.restart('red')

                    blocks_array[player_blue_object.block[0]][player_blue_object.block[1]].update_player(PLAYER_BLUE)
                    blocks_array[player_red_object.block[0]][player_red_object.block[1]].update_player(PLAYER_RED)

                    wall_list.clear()
        except socket.timeout:
            print('Timeout')
            if player_turn_id == PLAYER_BLUE:
                player_turn_object = player_red_object
                current_socket = client_socket2
                player_turn_id = PLAYER_RED
            else:
                player_turn_object = player_blue_object
                current_socket = client_socket1
                player_turn_id = PLAYER_BLUE

            current_socket.send(shape_command(WIN, BLANK))
            finish = True
    except socket.error as err:
        print('received socket exception - ' + str(err))
        if err.errno == 10053:
            if player_turn_id == PLAYER_BLUE:
                player_turn_object = player_red_object
                current_socket = client_socket2
                player_turn_id = PLAYER_RED
            else:
                player_turn_object = player_blue_object
                current_socket = client_socket1
                player_turn_id = PLAYER_BLUE

            current_socket.send(shape_command(WIN, BLANK))
            finish = True
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()
