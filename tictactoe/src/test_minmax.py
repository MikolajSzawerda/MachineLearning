import pytest
from MinMax import MinMax
from TicTacToe import *


def empty_board():
    return State(tuple(' ' for _ in range(9)))


def filled_board():
    return State((
        'x', 'o', ' ',
        ' ', 'x', ' ',
        ' ', ' ', 'o'
    ))


def won_board():
    return State((
        'x', 'o', ' ',
        ' ', 'x', ' ',
        'o', ' ', 'x'
    ))


def barely_won_board():
    return State((
        'x', 'o', ' ',
        ' ', 'x', ' ',
        'o', ' ', ' '
    ))


def draw_board():
    return State((
        'o', 'x', 'x',
        'x', 'x', 'o',
        'o', 'o', 'x'
    ))


@pytest.mark.parametrize("board,result", [
    (empty_board(), 0),
    (filled_board(), 2),
    (won_board(), 10000),
    (draw_board(), 0)
])
def test_heuristic(board, result):
    minimax = MinMax()
    game_state = Game.check_game_state(board)
    given_result = minimax.heuristic(board, game_state)
    assert result == given_result


def test_finding_terminal_state():
    board = barely_won_board()
    minimax = MinMax()
    move = minimax.get_optimal_move(board, minimax.max_player)
    assert move == 8

