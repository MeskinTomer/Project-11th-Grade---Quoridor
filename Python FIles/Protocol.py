"""
Author: Tomer Meskin
Date: 12/05/2024
"""

import socket

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
ACK = 'acknowledgement'
ACK_VALID = 'valid'
ACK_INVALID = 'invalid'


def protocol_send(cmd, msg):
    """
    shapes and encodes the command and the message to be sent according to the protocol
    :param cmd: the command
    :type: string
    :param msg: the message
    :type: string
    :return: the final message
    :rtype: bytes
    """
    cmd_len = len(cmd)
    msg_len = len(msg)
    total_message = (str(cmd_len) + '!' + cmd + str(msg_len) + '!' + msg).encode()
    return total_message


def protocol_recv(my_socket):
    """
    receives the command and the message from the sending socket
    :param my_socket: the socket to be received from
    :type: socket
    :return: the command and the message
    :rtype: tuple
    """
    cur_char = ''
    cmd_len = ''
    msg_len = ''
    try:
        while cur_char != '!':
            cur_char = my_socket.recv(1).decode()
            cmd_len += cur_char
        cmd_len = cmd_len[:-1]

        cmd = my_socket.recv(int(cmd_len)).decode()

        cur_char = ''

        while cur_char != '!':
            cur_char = my_socket.recv(1).decode()
            msg_len += cur_char
        msg_len = msg_len[:-1]

        msg = my_socket.recv(int(msg_len)).decode()

        final_message = (cmd, msg)
    except socket.error:
        final_message = ('Error', '')
    return final_message


def shape_command(command, value):
    if command == ID or command == TURN or command == MOVE or command == WALL or command == ACK or command == NO_MOVE:
        ret_val = protocol_send(command, value)
    else:
        ret_val = 'error'
    return ret_val
