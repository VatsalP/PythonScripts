import os
import sys
import random

from copy import deepcopy
from time import sleep

def random_state(width, height):
    """ Get a random board to start with
    """
    return_val = [
        [1 if random.random() > 0.5 else 0 for _ in range(0, width)] for _ in range(0, height)]
    return return_val

def render(to_render):
    """
    Takes board as parameter
    and creates a formatted string of the board and returns it
    """
    width = len(to_render[0]) + 2
    format_string = ""
    top_line = bottom_line = "".join(["_" for _ in range(0, width)]) + "\n"
    format_string = top_line + format_string
    for i in to_render:
        format_string += "|" + "".join(["\u25CF" if x == 1 else " " for x in i]) + "|\n"
    format_string = format_string + bottom_line
    return format_string

def cells_alive(j, i, board):
    """Checks how many cells near the cell[j][i] are and returns the value
    y coordinates before x cause of the list(board)
    """
    to_check = (
        [j-1, i-1], [j-1, i], [j-1, i+1],
        [j, i-1], [j, i+1],
        [j+1, i-1], [j+1, i], [j+1, i+1]
    )
    alive_counter = 0
    for cord in to_check:
        try:
            if board[cord[0]][cord[1]]:
                alive_counter += 1
        except IndexError:
            if cord[0] == len(board):
                cord[0] = 0
            if cord[1] == len(board[0]):
                cord[1] = 0
            if board[cord[0]][cord[1]]:
                alive_counter += 1
    return alive_counter

def update_state(board):
    """ Returns next state of board based on the current one
    """
    old_board = deepcopy(board) # to use current state to determine next state
    for i in range(0, len(old_board[0])): # width
        for j in range(0, len(old_board)): # height
            alive = True if old_board[j][i] else False
            nieghbours_alive = cells_alive(j, i, old_board)
            if alive:
                if nieghbours_alive < 2 or nieghbours_alive > 3:
                    board[j][i] = 0
            else: # its dead
                if nieghbours_alive == 3:
                    board[j][i] = 1
    return board


if __name__ == "__main__":
    if "Win" in sys.platform:
        clear = "cls"
    else:
        clear = "clear"
    board_state = random_state(int(sys.argv[1]), int(sys.argv[2]))
    os.system(clear)
    print(render(board_state))
    sleep(1)
    while True:
        try:
            os.system(clear)
            board_state = update_state(board_state)
            print(render(board_state))
            sleep(1)
        except KeyboardInterrupt:
            print("gg\n10 secs and we quit")
            sleep(10)
            exit(0)
