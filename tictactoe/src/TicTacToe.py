from collections import namedtuple


Player = namedtuple("Player", "char")
GameState = namedtuple("GameState", "terminal result")


class State:
    def __init__(self, board=None):
        if board is None:
            board = tuple(' ' for _ in range(9))
        self.board = board

    def __iter__(self):
        self.it = 0
        return self

    def __next__(self):
        if self.it < 3:
            result = self.get_row(self.it)
        elif self.it < 6:
            result = self.get_column(self.it % 3)
        elif self.it < 8:
            result = self.get_diagonal(self.it % 2)
        else:
            raise StopIteration
        self.it += 1
        return result

    def get_row(self, n):
        return self.board[3*n:3*n+3]

    def get_column(self, n):
        return tuple(self.board[3*i+n] for i in range(3))

    def get_diagonal(self, n):
        if n == 0:
            return tuple(self.board[i] for i in [0, 4, 8])
        return tuple(self.board[i] for i in [2, 4, 6])

    @property
    def empty_spaces(self):
        return [i for i in range(9) if self.board[i] == ' ']

    def transform_state(self, index, char):
        if self.board[index] != ' ':
            raise ValueError("Field is not empty!")
        return State(self.board[:index]+(char,)+self.board[index+1:])

    def __str__(self):
        return '\n'.join(('|'.join(self.get_row(i)) for i in range(3)))


class Game:
    def __init__(self, player1: Player, player2: Player):
        self.board = State()
        self.players = (player1, player2)
        self.current_turn = 0
        self.game_state = GameState(False, 0)

    @property
    def current_player(self):
        return self.players[self.current_turn % 2]

    def make_move(self, index):
        if self.game_state.terminal:
            raise ValueError("Game has ended!")
        self.board = self.board.transform_state(index, self.current_player.char)
        self.current_turn += 1
        self.game_state = self.check_game_state(self.board)

    @staticmethod
    def check_game_state(board: State):
        terminal_flag = True
        for row in board:
            chars = set(row)
            if ' ' not in chars:
                if len(chars) == 1:
                    return GameState(True, chars.pop())
            else:
                terminal_flag = False
        return GameState(terminal_flag, 'draw')

    def play(self, p1_input, p2_input):
        recorder = []
        while not self.game_state.terminal:
            recorder.append(''.join(self.board.board))
            if self.current_turn % 2 == 0:
                move = p1_input()
            else:
                move = p2_input()
            self.make_move(move)
        recorder.append(''.join(self.board.board))
        return self.game_state.result, recorder
