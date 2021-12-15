'''
Shengguo Zhou
Final Project final version
CS 5001, Fall 2021

This is a GameState class

P.S.
This game can not only realize a function that a piece can have multiple
times to eat, but also they can eat multiple pieces in one time if they
are in the right position.
(which is a function that is not required)
'''

import turtle
import math
import random
from game_function import draw_circle, draw_empty_circle, draw_winner


class GameState:
    '''
        Class -- GameState
            Represents the state of the game.
        Attributes:
            squares -- The state of chessboard.
            king_state -- The state of whether a piece is a king.
            screen -- Turtle to draw the UI screen.
            onclick --  pass the click point into the function.
            curr_pos -- The postion that you are cliking.
            cell_to_move -- The place you are going to move.
            move_to_place -- The place that you can move.
            place_movable -- The place where you can move.
            has_eaten -- Check whether there is piece on board can be eaten.
            turn -- Start with the black piece.
        Methods:
            cell_conversion -- Convert the piece you click into cell number.
            click_handler --  Move the piece by clicking.
            check_change_turn -- If there is multiple eat,
                                and the turn won't be changed.
            check_double_eat -- Have a check whether there is double eat.
            computer -- The computer AI, it will auto move the red piece.
            eat_list -- If a piece can be eaten,
                        it will be added into the list.
            check_check_eat_list -- Return true if the piece can be eaten.
            check_eat_list -- Check whether the piece can eat other.
            check_win -- Have a check whether one has won.
            check_append_place_movable -- Put the movable position
                                          into the list.
            draw_win -- Draw the winning prompt if one side has won.
            draw -- Draw the piece when the piece is moved.
            check_eating_number -- Check how many pieces left on board.
            check_may_be_eat_list -- Add the pieces may be eaten into the list.
            check_empty_or_selfcolor -- Check whether the clicking
                                        piece is valid.
            draw_king_circle -- Draw the white circle on piece
                                if one piece becomes a king.
            update_new_king -- Update a piece into a king when it is qualified.
            boundary_check -- Check whether the clicking piece is
                                in the boundary.
            append_place_movable -- Append movable piece into a list.
            clear_state -- Clear the king-state,
                            if the piece is no longer a king.
            change_turn -- Change the default piece color.
            exchange_king_state -- Exchange the king state if it is moved.
            boundary -- Check whether the non-king-move is in the boundary.
            cur_same_color -- Check the four pieces around the central
                                non-king piece are all the same or not.
            check_to_eat -- Check the four pieces around the central
                            non-king piece can be eaten or not.
            clear -- Clear the piece, if the piece is eaten.
    '''
    # initiate the game state
    BLACK = "black"
    RED = "dark red"
    EMPTY = "light gray"  # when the square is empty, we can use a gray circle.
    NUM_SQUARES = 8  # The number of squares on each row.
    SQUARE = 50  # The size of each square in the checkerboard.
    SQUARE_COLORS = ("light gray", "white")
    CIRCLE_COLORS = ("black", "dark red")
    DIFFERENCE = 4
    board_size = NUM_SQUARES * SQUARE
    LOWER_LIMIT = 0
    UPPER_LIMIT = 8
    TOTAL_NUMBER = 12
    is_able_to_eat = False
    four_place_list = [[1, 1], [1, -1], [-1, 1], [-1, -1]]

    def __init__(self):
        self.squares = [[self.EMPTY, self.BLACK, self.EMPTY, self.BLACK,
                        self.EMPTY, self.BLACK, self.EMPTY, self.BLACK],

                        [self.BLACK, self.EMPTY, self.BLACK, self.EMPTY,
                        self.BLACK, self.EMPTY, self.BLACK, self.EMPTY],

                        [self.EMPTY, self.BLACK, self.EMPTY, self.BLACK,
                        self.EMPTY, self.BLACK, self.EMPTY, self.BLACK],

                        [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY,
                        self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],

                        [self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY,
                        self.EMPTY, self.EMPTY, self.EMPTY, self.EMPTY],

                        [self.RED, self.EMPTY, self.RED, self.EMPTY, self.RED,
                        self.EMPTY, self.RED, self.EMPTY],

                        [self.EMPTY, self.RED, self.EMPTY, self.RED,
                        self.EMPTY, self.RED, self.EMPTY, self.RED],

                        [self.RED, self.EMPTY, self.RED, self.EMPTY, self.RED,
                        self.EMPTY, self.RED, self.EMPTY]]

        self.king_state = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

        self.screen = turtle.Screen()
        self.screen.onclick(self.click_handler)
        self.curr_pos = []
        self.cell_to_move = []
        self.move_to_place = []
        self.place_movable = []
        self.pen = turtle.Turtle()
        self.has_eaten = False
        self.turn = self.BLACK  # start with the black piece

    def cell_conversion(self, a, b):
        '''
        Function -- cell_conversion
            Convert the point into cell number.
        Parameters:
            a -- the coordinate x
            b -- the coordinate y
        Returns:
            a list that contains the row and column of the cell.
        '''
        col = math.floor(a / self.SQUARE) + self.DIFFERENCE
        row = math.floor(b / self.SQUARE) + self.DIFFERENCE
        cell_list = [row, col]
        return cell_list

    def click_handler(self, x, y):
        '''
        Function -- click_handler
            Record the previous clicking coordinate and the next clicking one.
            And then move the piece by clicking.
        Parameters:
            x -- the coordinate x
            y -- the coordinate y
        Returns:
            The piece's previous and next position. And move the piece.
        '''
        # The most important function
        if(len(self.curr_pos) == 0):
            self.curr_pos = self.cell_conversion(x, y)
            print("You are clicking [", self.curr_pos[0],
                  ",", self.curr_pos[1], "]")
            if(not self.boundary_check()):
                print("1. Out of chessboard boundary")
                self.curr_pos = []
            elif(not self.check_empty_or_selfcolor()):
                print("2. Please click another color of piece\
 or click a piece")
                self.curr_pos = []
            elif(not self.check_cur_same_color()):
                print("3. This piece can‘t be moved,\
 please choose another piece.")
                self.curr_pos = []
            else:
                self.place_movable = self.append_place_movable()
                # add place to move for a certain piece
                if(len(self.place_movable) == 0):
                    print("This piece has no place to move,\
 please choose another piece")
                    self.curr_pos = []
                self.eat_list()
                if(self.turn == self.RED):
                    if(len(red_eat_list) != 0):
                        if([self.curr_pos[0], self.curr_pos[1]]
                                not in red_eat_list):
                            print("There is a piece that can eat other,\
 please move that piece")
                            self.curr_pos = []
                if(self.turn == self.BLACK):
                    if(len(black_eat_list) != 0):
                        if([self.curr_pos[0], self.curr_pos[1]]
                                not in black_eat_list):
                            print("There is a piece can eat other,\
 please move that piece")
                            self.curr_pos = []
        else:
            self.cell_to_move = self.cell_conversion(x, y)
            if(not self.second_click_boundary_check()):
                print("4.out of chessboard boundary")
            elif(not self.second_click_empty_check()):
                print("5.the place you move is not empty")
            elif(not self.non_king_move_check()):
                print("6.please choose another place to move")
            elif([self.cell_to_move[0], self.cell_to_move[1]]
                 not in self.place_movable):
                print("7.You can not move to this place")
            else:
                old_color = self.squares[self.curr_pos[0]][self.curr_pos[1]]
                self.squares[self.curr_pos[0]][self.curr_pos[1]] = self.EMPTY
                self.squares[self.cell_to_move[0]][self.cell_to_move[1]]\
                    = old_color
                self.exchange_king_state()  # exchange king state
                self.update_new_king()  # update new king
                self.clear(self.curr_pos, self.cell_to_move)
                self.clear_state(self.curr_pos, self.cell_to_move)
                self.has_eaten = False
                if(abs(self.cell_to_move[0] - self.curr_pos[0]) > 1):
                    self.has_eaten = True
                self.check_eating_number()
                self.check_win()
                self.draw()
                self.draw_king_circle()
                self.draw_win()
                self.curr_pos = []
                self.move_to_place = []
                self.place_movable = []
                self.check_change_turn()
                print("Next color of piece is", self.turn)
                while(self.turn == self.RED):
                    self.computer()
                    # If you don't want a computer, just annotated it.

    def check_change_turn(self):
        '''
        Function -- check_change_turn
            If there is multiple eat, and the turn won't be changed.
        Parameters:
            Nothing.
        Returns:
            Nothing.
        '''
        if(self.turn == self.BLACK):
            if(not self.has_eaten):
                self.change_turn()
            else:
                if(not self.check_double_eat()):
                    # check multiple eat
                    self.change_turn()
                else:
                    print("Multiple eat")
        elif(self.turn == self.RED):
            if(not self.has_eaten):
                self.change_turn()
            else:
                if(not self.check_double_eat()):
                    # check multiple eat
                    self.change_turn()
                else:
                    print("Multiple eat")

    def check_double_eat(self):
        '''
        Function -- check_double_eat
            Have a check whether there is multiple eat.
        Parameters:
            Nothing.
        Returns:
            Return true if there exists double eat, otherwise,
            return false.
        '''
        position = self.cell_to_move
        self.eat_list()
        if(self.squares[position[0]][position[1]] == self.RED):
            if([position[0], position[1]] in red_eat_list):
                return True
            else:
                return False
        if(self.squares[position[0]][position[1]] == self.BLACK):
            if([position[0], position[1]] in black_eat_list):
                return True
            else:
                return False

    def computer(self):
        '''
        Function -- computer
           It is the computer AI, it will move the red piece
           after you moving the black piece.
        Parameters:
            Nothing.
        Returns:
            Nothing.
        '''
        whole_list = []
        self.eat_list()  # get a red_eat_list
        if(len(red_eat_list) != 0):
            whole_list = red_eat_list
        else:  # no eat piece, add the non-eat ones
            for i in range(self.NUM_SQUARES):
                for j in range(self.NUM_SQUARES):
                    position = [i, j]
                    if(not self.check_append_place_movable(position)):  # 237
                        if(self.squares[position[0]][position[1]] == self.RED):
                            whole_list.append(position)
        print("Whole moving list is:", whole_list)
        choice1 = random.choice(whole_list)
        self.curr_pos = choice1
        old_color = self.squares[self.curr_pos[0]][self.curr_pos[1]]
        self.squares[self.curr_pos[0]][self.curr_pos[1]] = self.EMPTY

        self.place_movable = self.append_place_movable()

        choice2 = random.choice(self.place_movable)
        self.cell_to_move = choice2

        self.squares[self.cell_to_move[0]][self.cell_to_move[1]] = old_color
        self.exchange_king_state()  # exchange king state
        self.update_new_king()  # update new king
        self.clear(self.curr_pos, self.cell_to_move)
        self.clear_state(self.curr_pos, self.cell_to_move)
        self.has_eaten = False
        if(abs(self.cell_to_move[0] - self.curr_pos[0]) > 1):
            self.has_eaten = True
        self.check_eating_number()
        self.check_win()
        self.draw()
        self.draw_king_circle()
        self.draw_win()
        self.curr_pos = []
        self.move_to_place = []
        self.place_movable = []
        if(self.turn == self.RED):
            if(not self.has_eaten):
                self.change_turn()
            else:
                if(not self.check_double_eat()):  # check连吃
                    self.change_turn()
                else:
                    print("Multiple eat")
        # self.change_turn()
        print("Next color of piece is", self.turn)

    def eat_list(self):
        '''
        Function -- eat_list
            Get a red_eat_list, and a black_eat_list,
            if the red piece can be eaten,
            it will be added to the red_eat_list, black is the same.
        Parameters:
            Nothing
        Returns:
            The global variable will record
            the red_eat_list and the black_eat_list.
        '''
        global red_eat_list, black_eat_list
        red_eat_list = []
        black_eat_list = []
        for i in range(self.NUM_SQUARES):
            for j in range(self.NUM_SQUARES):
                if(self.squares[i][j] == self.BLACK):
                    if(self.check_eat_list([i, j])):
                        if([i, j] not in black_eat_list):
                            black_eat_list.append([i, j])
                if(self.squares[i][j] == self.RED):
                    if(self.check_eat_list([i, j])):
                        if([i, j] not in red_eat_list):
                            red_eat_list.append([i, j])

    def check_check_eat_list(self, i, position):
        '''
        Function -- check_check_eat_list
            It is a recursion function.
            return true if the piece can be eaten.
        Parameters:
            i -- The current position.
            position -- The postion need to move.
        Returns:
            Return true if the piece can be eaten.
        '''
        now_x = position[0]
        now_y = position[1]
        deltax = i[0] - now_x
        deltay = i[1] - now_y
        nextx = i[0] + deltax
        nexty = i[1] + deltay
        next_pos = [nextx, nexty]
        now_pos = [i[0], i[1]]

        if(self.boundary(nextx) and self.boundary(nexty)):
            if(self.squares[next_pos[0]][next_pos[1]] == self.EMPTY):
                return True
            elif(self.squares[next_pos[0]][next_pos[1]] == self.turn):
                return False
            else:
                return self.check_check_eat_list(next_pos, now_pos)
        else:  # out of boundary
            return False

    def check_eat_list(self, position):
        '''
        Function -- check_eat_list
            Check whether the piece can eat other.
        Parameters:
            position -- The positon need to move.
        Returns:
            Return true if the piece can eat other.
        '''
        global check_empty_place
        check_empty_place = []
        self.move_to_place = []
        placex = position[0]
        placey = position[1]

        if(self.squares[placex][placey] == self.BLACK):
            opp = self.RED
        if(self.squares[placex][placey] == self.RED):
            opp = self.BLACK

        if(self.king_state[placex][placey] == 1):
            move_place = self.four_place_list
        else:
            if(self.squares[placex][placey] == self.RED):
                move_place = [[-1, 1], [-1, -1]]
            elif(self.squares[placex][placey] == self.BLACK):
                move_place = [[1, 1], [1, -1]]

        for i in move_place:
            x = placex + i[0]
            y = placey + i[1]
            if(not self.boundary(x) or not self.boundary(y)):
                continue
            else:
                check_empty_place.append([x, y])
        may_be_can_eat = False
        may_be_can_eat_list = []

        for i in check_empty_place:
            if(self.squares[i[0]][i[1]] == opp):
                may_be_can_eat = True
                may_be_can_eat_list.append(i)

        if(may_be_can_eat):
            for i in may_be_can_eat_list:
                if(self.check_check_eat_list(i, position)):
                    return True
        else:
            return False

    def check_win(self):
        '''
        Function -- check_win
            Have a check whether one has won.
        Parameters:
            Nothing
        Returns:
            Return true one side has won.
        '''
        global red_win, black_win
        red_win = False
        black_win = False
        red_nowhere_tomove = 0
        black_nowhere_tomove = 0
        for i in range(self.NUM_SQUARES):
            for j in range(self.NUM_SQUARES):
                position = [i, j]
                if(self.squares[i][j] == self.RED):
                    if(self.check_append_place_movable(position)):  # 237
                        red_nowhere_tomove += 1
                if(self.squares[i][j] == self.BLACK):
                    if(self.check_append_place_movable(position)):  # 237
                        black_nowhere_tomove += 1
        print("Number of red pieces that are nowhere to move:",
              red_nowhere_tomove)
        print("Number of black pieces that are nowhere to move:",
              black_nowhere_tomove)
        if(black_nowhere_tomove == black):
            red_win = True
            print("Red win.")
        elif(red_nowhere_tomove == red):
            black_win = True
            print("Black win.")
        elif(red == 0):
            black_win = True
        elif(black == 0):
            red_win = True

    def check_append_place_movable(self, position):
        '''
        Function -- check_append_place_movable
            Put the movable position into the list.
        Parameters:
            position -- The positon need to move.
        Returns:
            Return true the list is empty, otherwise, return false.
        '''
        global check_empty_place
        check_empty_place = []
        self.move_to_place = []
        placex = position[0]
        placey = position[1]
        move_place = []

        if(self.squares[placex][placey] == self.BLACK):
            opp = self.RED
        if(self.squares[placex][placey] == self.RED):
            opp = self.BLACK
        if(self.king_state[placex][placey] == 1):
            move_place = self.four_place_list
        else:
            if(self.squares[placex][placey] == self.RED):
                move_place = [[-1, 1], [-1, -1]]
            elif(self.squares[placex][placey] == self.BLACK):
                move_place = [[1, 1], [1, -1]]
        for i in move_place:
            x = placex + i[0]
            y = placey + i[1]
            if(not self.boundary(x) or not self.boundary(y)):
                continue
            else:
                check_empty_place.append([x, y])
        may_be_can_eat = False
        may_be_can_eat_list = []

        for i in check_empty_place:
            if(self.squares[i[0]][i[1]] == opp):
                may_be_can_eat = True
                may_be_can_eat_list.append(i)

        if(may_be_can_eat):
            for i in may_be_can_eat_list:
                if(self.check_may_be_eat_list(i, position)):
                    self.move_to_place.append(really_can_move_place)
                    # attention: append which position

        if(len(self.move_to_place) == 0):
            # all of them are empty
            for i in check_empty_place:
                if(self.king_state[position[0]][position[1]] == 1):
                    if(self.squares[i[0]][i[1]] == self.EMPTY):
                        if(i not in self.move_to_place):
                            self.move_to_place.append(i)
                else:
                    if(self.squares[placex][placey] == self.BLACK):
                        # if(i[0] - position[0]) > 0:
                        if(self.squares[i[0]][i[1]] == self.EMPTY):
                            if(i not in self.move_to_place):
                                self.move_to_place.append(i)
                    if(self.squares[placex][placey] == self.RED):
                        # if(i[0] - position[0]) < 0:
                        if(self.squares[i[0]][i[1]] == self.EMPTY):
                            if(i not in self.move_to_place):
                                self.move_to_place.append(i)
        # print("append_place_movable function: ", self.move_to_place)
        if(len(self.move_to_place) == 0):
            return True
        else:
            return False

    def draw_win(self):
        '''
        Function -- draw_win
            Draw the winning prompt if one side has won.
        Parameters:
            Nothing
        Returns:
            Nothing.
        '''
        if(red_win):
            winner = "RED"
            color = "red"
            self.pen.setposition(-150, -60)
            self.pen.color(color)
            draw_winner(self.pen, winner)
        elif(black_win):
            winner = "BLACK"
            color = "black"
            self.pen.setposition(-150, -60)
            self.pen.color(color)
            draw_winner(self.pen, winner)
        else:
            pass

    def check_eating_number(self):
        '''
        Function -- check_eating_number
            Check how many pieces that are left on board.
        Parameters:
            Nothing
        Returns:
            Nothing.
        '''
        global red, black
        red = 0
        black = 0
        for i in range(self.NUM_SQUARES):
            for j in range(self.NUM_SQUARES):
                if(self.squares[i][j] == self.BLACK):
                    black += 1
                if(self.squares[i][j] == self.RED):
                    red += 1
        print("Red Piece Left: {}/12".format(red))
        print("Black Piece Left: {}/12".format(black))

    def draw_king_circle(self):
        '''
        Function -- draw_king_circle
            Draw the white circle on piece if one piece becomes a king.
        Parameters:
            Nothing
        Returns:
            Nothing.
        '''
        KING_NUMBER = 4
        corner = - self.board_size / 2 - 1
        newcorner = corner + self.SQUARE / 2
        newcornery = corner + self.SQUARE / KING_NUMBER
        for i in range(self.NUM_SQUARES):
            for j in range(self.NUM_SQUARES):
                if(self.king_state[i][j] == 1):
                    color = "white"
                    self.pen.color(color)
                    self.pen.setposition(newcorner + self.SQUARE * j,
                                         newcornery + self.SQUARE * i)
                    draw_empty_circle(self.pen, self.SQUARE / KING_NUMBER)

    def clear_state(self, begin, end):
        '''
        Function -- clear_state
            Clear the king-state, if the piece is no longer a king.
        Parameters:
            begin -- The start position of the piece.
            end -- The end postion of the piece.
        Returns:
            Nothing.
        '''
        distancex = end[0] - begin[0]
        deltax = distancex / abs(distancex)
        a = begin[0]
        distancey = end[1] - begin[1]
        deltay = distancey / abs(distancey)
        b = begin[1]
        for i in range(1, abs(distancex)):
            self.king_state[int(a + deltax)][int(b + deltay)] = 0
            a += deltax
            b += deltay

    def exchange_king_state(self):
        '''
        Function -- exchange_king_state
            Exchange the king state if it is moved.
        Parameters:
            Nothing
        Returns:
            Nothing
        '''
        x = self.curr_pos[0]
        y = self.curr_pos[1]
        x_new = self.cell_to_move[0]
        y_new = self.cell_to_move[1]
        old_state = self.king_state[x][y]
        new_state = self.king_state[x_new][y_new]
        self.king_state[x][y] = new_state
        self.king_state[x_new][y_new] = old_state

    def update_new_king(self):
        '''
        Function -- update_new_king
            Update a piece into a king when it is qualified.
        Parameters:
            Nothing
        Returns:
            Nothing
        '''
        x = self.cell_to_move[0]
        y = self.cell_to_move[1]
        if(self.turn == self.BLACK):
            if(x == 7):
                self.king_state[x][y] = 1  # king is 1
        if(self.turn == self.RED):
            if(x == 0):
                self.king_state[x][y] = 1

    def second_click_empty_check(self):
        '''
        Function -- second_click_empty_check
            Check whether the second click is qualified.
        Parameters:
            Nothing
        Returns:
            Return true if it is qualified, otherwise, return false.
        '''
        if(self.squares[self.cell_to_move[0]][self.cell_to_move[1]]
                != self.EMPTY):
            return False
        else:
            return True

    def second_click_boundary_check(self):
        '''
        Function -- second_click_boundary_check
            Check whether the second click is in the boundary.
        Parameters:
            Nothing
        Returns:
            Return true if it is in the boundary, otherwise, return false.
        '''
        if (self.cell_to_move[0] >= self.UPPER_LIMIT or
            self.cell_to_move[1] >= self.UPPER_LIMIT or
            self.cell_to_move[0] < self.LOWER_LIMIT or
                self.cell_to_move[1] < self.LOWER_LIMIT):
            return False
        else:
            return True

    def append_place_movable(self):
        '''
        Function -- append_place_movable
            Append movable piece into a list.
        Parameters:
            Nothing
        Returns:
            Return that list.
        '''
        global empty_place
        if(self.turn == self.BLACK):
            opp = self.RED
        if(self.turn == self.RED):
            opp = self.BLACK
        empty_place = []
        self.move_to_place = []
        placex = self.curr_pos[0]
        placey = self.curr_pos[1]

        if(self.king_state[placex][placey] == 1):
            move_place = self.four_place_list
        else:
            if(self.turn == self.RED):
                move_place = [[-1, 1], [-1, -1]]
            elif(self.turn == self.BLACK):
                move_place = [[1, 1], [1, -1]]
        for i in move_place:
            x = placex + i[0]
            y = placey + i[1]
            if(not self.boundary(x) or not self.boundary(y)):
                continue
            else:
                empty_place.append([placex + i[0], placey + i[1]])
        may_be_can_eat = False
        may_be_can_eat_list = []

        for i in empty_place:
            if(self.squares[i[0]][i[1]] == opp):
                may_be_can_eat = True
                may_be_can_eat_list.append(i)

        if(may_be_can_eat):
            for i in may_be_can_eat_list:
                if(self.check_may_be_eat_list(i, self.curr_pos)):
                    self.move_to_place.append(really_can_move_place)
                    # attention :append one position
                    print("1 Append_place_movable function:",
                          self.move_to_place)
        if(len(self.move_to_place) == 0):  # all of them are empty
            for i in empty_place:
                if(self.king_state[self.curr_pos[0]][self.curr_pos[1]] == 1):
                    if(self.squares[i[0]][i[1]] == self.EMPTY):
                        if(i not in self.move_to_place):
                            self.move_to_place.append(i)
                            print("2 Append_place_movable function:",
                                  self.move_to_place)
                else:
                    if(self.turn == self.BLACK):
                        if(i[0] - self.curr_pos[0]) > 0:
                            if(self.squares[i[0]][i[1]] == self.EMPTY):
                                if(i not in self.move_to_place):
                                    self.move_to_place.append(i)
                                    print("3 Append_place_movable function:",
                                          self.move_to_place)
                    if(self.turn == self.RED):
                        if(i[0] - self.curr_pos[0]) < 0:
                            if(self.squares[i[0]][i[1]] == self.EMPTY):
                                if(i not in self.move_to_place):
                                    self.move_to_place.append(i)
                                    print("4 Append_place_movable function:",
                                          self.move_to_place)
        print("You can move the piece to:", self.move_to_place)
        return self.move_to_place

    def check_may_be_eat_list(self, i, position):
        '''
            Function -- check_may_be_eat_list
                Add the pieces may be eaten into the list.
            Parameters:
                i -- The current position.
                postion -- The position need to move.
            Returns:
                Return true if the piece in the list can be eaten.
        '''
        global really_can_move_place
        really_can_move_place = []
        now_x = position[0]
        now_y = position[1]
        deltax = i[0] - now_x
        deltay = i[1] - now_y
        nextx = i[0] + deltax
        nexty = i[1] + deltay
        next_pos = [nextx, nexty]
        now_pos = [i[0], i[1]]
        # print("now_pos:", now_pos, "next_pos:", next_pos)
        if(self.boundary(nextx) and self.boundary(nexty)):
            if(self.squares[next_pos[0]][next_pos[1]] == self.EMPTY):
                really_can_move_place = next_pos
                return True
            elif(self.squares[next_pos[0]][next_pos[1]] == self.turn):
                return False
            else:
                return self.check_may_be_eat_list(next_pos, now_pos)
        else:  # out of boundary
            return False

    def check_cur_same_color(self):
        '''
            Function -- check_cur_same_color
                Check whether the four pieces around the central piece
                are all the same color.
            Parameters:
                Nothing
            Returns:
                If the four pieces around the central piece are all the same
                color with the central one, return false.
        '''
        global cur_around
        cur_around = []
        placex = self.curr_pos[0]
        placey = self.curr_pos[1]
        move_place = self.four_place_list
        for i in move_place:
            x = placex + i[0]
            y = placey + i[1]
            if(not self.boundary(x) or not self.boundary(y)):
                continue
            else:
                place = [x, y]
                cur_around.append(place)
        for i in cur_around:
            if(self.squares[i[0]][i[1]] != self.turn):
                return True
        return False

    def draw(self):
        '''
        Function -- draw
            Draw the piece when the piece is moved.
        Parameters:
            Nothing
        Returns:
            Nothing
        '''
        corner = - self.board_size / 2 - 1
        newcorner = corner + self.SQUARE / 2
        for row in range(self.NUM_SQUARES):
            for col in range(self.NUM_SQUARES):
                # choose the color
                color = self.squares[row][col]
                self.pen.color("light gray", color)
                self.pen.setposition(newcorner + self.SQUARE * col,
                                     corner + self.SQUARE * row)
                if col % 2 != row % 2:
                    draw_circle(self.pen, self.SQUARE / 2)

    def check_empty_or_selfcolor(self):
        '''
        Function -- check_empty_or_selfcolor
            Check whether the clicking piece is valid.
        Parameters:
            Nothing
        Returns:
            If the piece is in right color, return true, otherwise,
            return false.
        '''
        if(self.squares[self.curr_pos[0]][self.curr_pos[1]] == self.turn):
            return True
        else:
            return False

    def boundary_check(self):
        '''
        Function -- boundary_check
            Check whether the clicking piece is in the boundary.
        Parameters:
            Nothing
        Returns:
            Return false if it is out of boundary.
        '''
        if(self.curr_pos[0] >= self.UPPER_LIMIT or
            self.curr_pos[1] >= self.UPPER_LIMIT or
            self.curr_pos[0] < self.LOWER_LIMIT or
                self.curr_pos[1] < self.LOWER_LIMIT):
            return False
        else:
            return True

    def change_turn(self):
        '''
        Function -- change_turn
            Change the default piece color.
        Parameters:
            Nothing
        Returns:
            Nothing
        '''
        if(self.turn == self.BLACK):
            self.turn = self.RED
        elif(self.turn == self.RED):
            self.turn = self.BLACK

    def non_king_move_check(self):
        '''
        Function -- non_king_move_check
            Check whether the non-king-move is valid or not.
        Parameters:
            Nothing
        Returns:
            Return true if it is valid, false otherwise.
        '''
        delta_y = self.cell_to_move[1] - self.curr_pos[1]
        delta_x = self.cell_to_move[0] - self.curr_pos[0]
        cur_x = self.curr_pos[0]
        cur_y = self.curr_pos[1]
        if(self.king_state[cur_x][cur_y] == 1):
            if(abs(delta_x) != abs(delta_y)):
                return False
            else:
                return True
        else:
            if(self.turn == self.BLACK and delta_x <= 0):
                print("Non-king-black should move up.")
                return False
            elif(self.turn == self.RED and delta_x >= 0):
                print("Non-king-red should move down.")
                return False
            elif(abs(delta_x) != abs(delta_y)):
                return False
            else:
                return True

    def boundary(self, x):
        '''
        Function -- boundary
            Check whether the non-king-move is in the boundary or not.
        Parameters:
            x - The postion of piece.
        Returns:
            Return true if it is in the boundary, false otherwise.
        '''
        if(int(x) > self.UPPER_LIMIT - 1 or int(x) < self.LOWER_LIMIT):
            return False
        return True

    def append_move_place(self):
        '''
        Function -- append_move_place
            Append the movable place of non-king-piece into the list.
        Parameters:
            Nothing
        Returns:
            Nothing
        '''
        global empty_place
        empty_place = []
        placex = self.curr_pos[0]
        placey = self.curr_pos[1]
        move_place = self.four_place_list
        for i in move_place:
            x = placex + i[0]
            y = placey + i[1]
            if(not self.boundary(x) or not self.boundary(y)):
                continue
            else:
                empty_place.append([placex + i[0], placey + i[1]])
        for i in empty_place:
            if(self.turn == self.BLACK):
                if(i[0] - self.curr_pos[0]) > 0:
                    if(self.squares[i[0]][i[1]] == self.EMPTY):
                        if(i not in self.move_to_place):
                            self.move_to_place.append(i)
            if(self.turn == self.RED):
                if(i[0] - self.curr_pos[0]) < 0:
                    if(self.squares[i[0]][i[1]] == self.EMPTY):
                        if(i not in self.move_to_place):
                            self.move_to_place.append(i)

    def cur_same_color(self):
        '''
        Function -- cur_same_color
            Check the four pieces around the central non-king piece
            are all the same or not.
        Parameters:
            Nothing
        Returns:
            If the four pieces around the central non-king piece are all the
            same color with the central one, return false.
        '''
        global cur_around
        if(self.turn == self.BLACK):
            opp = self.RED
        if(self.turn == self.RED):
            opp = self.BLACK
        cur_around = []
        placex = self.curr_pos[0]
        placey = self.curr_pos[1]
        move_place = self.four_place_list
        for i in move_place:
            x = placex + i[0]
            y = placey + i[1]
            if(not self.boundary(x) or not self.boundary(y)):
                continue
            else:
                cur_around.append([placex + i[0], placey + i[1]])
        for i in cur_around:
            if(self.squares[i[0]][i[1]] != self.turn):
                if(self.squares[i[0]][i[1]] == opp):
                    self.check_to_eat(i)
                return True
        return False

    def check_to_eat(self, i):
        '''
        Function -- check_to_eat
            Check the four pieces around the central non-king piece
            can be eaten or not.
        Parameters:
            i -- The positon need to move.
        Returns:
            If the four pieces around the central non-king piece can be
            eaten, return false. Return true otherwise.
        '''
        if(self.turn == self.BLACK):
            opp = self.RED
        if(self.turn == self.RED):
            opp = self.BLACK
        deltax = i[0] - self.curr_pos[0]
        deltay = i[1] - self.curr_pos[1]
        nextx = i[0] + deltax
        nexty = i[1] + deltay
        next_pos = [nextx, nexty]
        if(self.boundary(nextx) and self.boundary(nexty)):
            if(self.squares[next_pos[0]][next_pos[1]] == self.EMPTY):
                if(next_pos not in self.move_to_place):
                    self.move_to_place.append(next_pos)
                    self.is_able_to_eat = True
                return True
            elif(self.squares[next_pos[0]][next_pos[1]] == opp):
                return self.check_to_eat(next_pos)
            else:
                self.is_able_to_eat = False
                return False
        else:
            return False

    def clear(self, begin, end):
        '''
        Function -- clear
            Clear the piece, if the piece is eaten.
        Parameters:
            begin -- The start place of the piece.
            end -- The end place of the piece.
        Returns:
            Nothing
        '''
        self.has_eaten = False
        distancex = end[0] - begin[0]
        if(abs(distancex) > 1):
            self.has_eaten = True
        deltax = distancex / abs(distancex)
        a = begin[0]
        distancey = end[1] - begin[1]
        deltay = distancey / abs(distancey)
        b = begin[1]
        for i in range(1, abs(distancex)):
            self.squares[int(a + deltax)][int(b + deltay)] = self.EMPTY
            a += deltax
            b += deltay
