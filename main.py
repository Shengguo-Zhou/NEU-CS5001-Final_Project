'''
Shengguo Zhou
Final Project final version
CS 5001, Fall 2021

This is the main function

This game can not only realize a piece can have multiple times to eat,
but also can eat multiple pieces in one time (which is a function that
is not required).

'''

import turtle
from GameState import GameState
from game_function import basic

NUM_SQUARES = 8  # The number of squares on each row.
SQUARE = 50  # The size of each square in the checkerboard.
SQUARE_COLORS = ("light gray", "white")
CIRCLE_COLORS = ("black", "dark red")


def main():
    basic()  # Draw the chessboard
    game_state = GameState()
    game_state.draw()
    turtle.done()  # Stops the window from closing.


if __name__ == "__main__":
    main()
