"""
Author: Tomer Meskin
Date: 24/04/2024
"""

# Imports
import socket
import pygame
import os
import time
from Player import Player
from Block import Block
from Wall import Wall
from datetime import datetime
from GameFunctions import *

# Socket Constants
QUEUE_SIZE = 1
IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 90

# Game Constants
PLAYER_NONE = 0
PLAYER_BLUE = 1
PLAYER_RED = 2
COLS = 9
ROWS = 9

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
        print("Listening for connections on port %d" % PORT)

        client_socket1, client_address1 = server_socket.accept()
        client_socket2, client_address2 = server_socket.accept()
        finish = False
        while not finish:


    except socket.error as err:
        print('received socket exception - ' + str(err))
    finally:
        server_socket.close()


if __name__ == '__main__':
    main()