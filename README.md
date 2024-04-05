# Project-11th-Grade---Quoridor
My final project for 11th grade, Cyber - The game Quoridor.
Written in Python, using Socket communication.
The game will consist of 2 players, racing to reach the ooposite side of the board. The player can either move once, or place a wall during thier turn. A wall can't be placed, if it's position entirly blocks the way of a player to reach the other side.

# Planning
Server - 
No threads/select
Sends Timer starts messages
Responssible for switching turns
Has a timeout of 1.5 minuts for a player's turn to resign

User -
Has Select meskanism for user input and Pygame screen
Starts own timer of it's/other's turn. - 1 minute timer.
Has a PathFinding meskanism for checking viability of wall placement.
Has a User Input meskanism

Both -
Have the board as a 2D array which consists each cell as an Object.
Each Object has the following attributes:
* Value - PLayer 1/2, Empty...
* Top - Blocked/Not
* Bottom - Blocked/Not
* Right - Blocked/Not
* Left - Blocked/Not
Have a Protocol for communication
Have a GUI using Pygame


