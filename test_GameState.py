'''
Shengguo Zhou
Final Project final version
CS 5001, Fall 2021

This is a test file. Here is all the functions can be tested.
'''

from GameState import GameState


def test_constructor():
    game_state = GameState()
    assert(not game_state.has_eaten)
    assert(game_state.board_size == 400)
    assert(game_state.turn == "black")


def test_cell_conversion():
    game_state = GameState()
    assert(game_state.cell_conversion(55, 55) == [5, 5])
    assert(game_state.cell_conversion(-55, -55) == [2, 2])
    assert(game_state.cell_conversion(-100, 60) == [5, 2])


def test_boundary():
    game_state = GameState()
    assert(game_state.boundary(6))
    assert(not game_state.boundary(-1))
    assert(not game_state.boundary(8))


def test_change_turn():
    game_state = GameState()
    game_state.change_turn()
    assert(game_state.turn == "dark red")
    game_state.has_eaten = True
    game_state.change_turn()
    assert(game_state.turn == "black")


def test_check_check_eat_list():
    game_state = GameState()
    i = [2, 0]
    position = [3, 1]
    assert(not game_state.check_check_eat_list(i, position))
    position = [2, 0]
    i = [3, 1]
    assert(game_state.check_check_eat_list(i, position))


def test_second_click_empty_check():
    game_state = GameState()
    game_state.cell_to_move = [1, 1]
    assert(game_state.second_click_empty_check())
    game_state.cell_to_move = [5, 2]
    assert(not game_state.second_click_empty_check())


def test_check_cur_same_color():
    game_state = GameState()
    game_state.curr_pos = [3, 1]
    assert(game_state.check_cur_same_color())
    game_state.curr_pos = [0, 3]
    assert(not game_state.check_cur_same_color())
