import pytest
from TicTacToe import State, GameState, Player, Game


@pytest.fixture
def filled_board():
    return (
        'x', ' ', 'o',
        'o', 'x', ' ',
        'o', 'o', 'x'
    )


def test_iterating(filled_board):
    iters = [
        ('x', ' ', 'o'), ('o', 'x', ' '), ('o', 'o', 'x'),
        ('x', 'o', 'o'), (' ', 'x', 'o'), ('o', ' ', 'x'),
        ('x', 'x', 'x'), ('o', 'x', 'o')
    ]
    generated = [x for x in State(filled_board)]
    assert iters == generated


def test_transforming(filled_board):
    old_state = State(filled_board)
    new_state = old_state.transform_state(1, 'o')
    changed_board = list(filled_board)
    changed_board[1] = 'o'
    changed_board = tuple(changed_board)
    assert new_state.board == changed_board
    with pytest.raises(ValueError):
        new_state.transform_state(1, 'x')


def test_game_winning():
    game = Game(Player("x"), Player('o'))
    assert game.game_state.terminal is False
    for i in [0, 1, 4, 2, 8]:
        game.make_move(i)
    assert game.game_state == GameState(True, 'x')


def test_game_draw():
    game = Game(Player('x'), Player('o'))
    for i in [0, 1, 2, 3, 5, 4, 7, 8, 6]:
        game.make_move(i)
    assert game.game_state == GameState(True, 'draw')