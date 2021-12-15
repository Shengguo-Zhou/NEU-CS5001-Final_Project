'''
Shengguo Zhou
Final Project final version
CS 5001, Fall 2021

This is function that is used in the game

'''
import turtle


def draw_square(a_turtle, size):
    '''
        Function -- draw_square
            Draw a square of a given size.
        Parameters:
            a_turtle -- an instance of Turtle
            size -- the length of each side of the square
        Returns:
            Nothing. Draws a square in the graphics window.
    '''
    RIGHT_ANGLE = 90
    a_turtle.begin_fill()
    a_turtle.pendown()
    for i in range(4):
        a_turtle.forward(size)
        a_turtle.left(RIGHT_ANGLE)
    a_turtle.end_fill()
    a_turtle.penup()


def draw_empty_circle(a_turtle, size):
    '''
        Function -- draw_empty_circle
            Draw an empty circle of a given size.
        Parameters:
            a_turtle -- an instance of Turtle
            size -- the size of the empty circle
        Returns:
            Nothing. Draws an empty circle in the graphics window.
    '''
    a_turtle.pendown()
    a_turtle.circle(size)
    a_turtle.penup()


def draw_circle(a_turtle, size):
    '''
        Function -- draw_circle
            Draw a circle of a given size.
        Parameters:
            a_turtle -- an instance of Turtle
            size -- the radius of the circle
        Returns:
            Nothing. Draws a circle in the graphics window.
    '''
    a_turtle.begin_fill()
    a_turtle.pendown()
    a_turtle.circle(size)
    a_turtle.end_fill()
    a_turtle.penup()


def draw_winner(a_turtle, winner):
    '''
        Function -- draw_winner
            Draw a winner prompt.
        Parameters:
            a_turtle -- an instance of Turtle
            winner -- black winner or red winner
        Returns:
            Nothing. Draws the winner prompt.
    '''
    a_turtle.pendown()
    a_turtle.write("GAME OVER!\n {} WIN".format(winner),
                   font=("Comic Sans MS", 50, "bold"))
    a_turtle.penup()


def click_handler(x, y):
    '''
        Function -- click_handler
            Called when a click occurs.
        Parameters:
            x -- X coordinate of the click. Automatically provided by Turtle.
            y -- Y coordinate of the click. Automatically provided by Turtle.
        Returns:
            Does not and should not return. Click handlers are a special type
            of function automatically called by Turtle. You will not have
            access to anything returned by this function.
    '''
    print("Clicked at ", x, y)


def basic():
    '''
        Function -- basic
            Draw the basic board.
        Parameters:
            Nothing
        Returns:
            Nothing. Draws the board.
    '''
    NUM_SQUARES = 8
    SQUARE = 50
    SQUARE_COLORS = ("light gray", "white")
    board_size = NUM_SQUARES * SQUARE

    window_size = board_size + SQUARE  # The extra + SQUARE is the margin
    turtle.setup(window_size, window_size)
    turtle.screensize(board_size, board_size)
    turtle.bgcolor("white")  # The window's background color
    turtle.tracer(0, 0)  # makes the drawing appear immediately

    pen = turtle.Turtle()  # This variable does the drawing.
    pen.penup()  # This allows the pen to be moved.
    pen.hideturtle()  # This gets rid of the triangle cursor.
    pen.color("black", "white")

    corner = -board_size / 2 - 1
    pen.setposition(corner, corner)
    draw_square(pen, board_size)

    pen.color("black", SQUARE_COLORS[0])
    for col in range(NUM_SQUARES):
        for row in range(NUM_SQUARES):
            pen.setposition(corner + SQUARE * col, corner + SQUARE * row)
            if col % 2 != row % 2:
                draw_square(pen, SQUARE)
