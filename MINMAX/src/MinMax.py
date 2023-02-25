from TicTacToe import Player, Game, State, GameState
from random import choice


class MinMax:
    def __init__(self, depth=5, max_player=Player('x'), min_player=Player('o')):
        self.max_player = max_player
        self.min_player = min_player
        self.depth = depth
        self.players = {
            True: self.max_player,
            False: self.min_player
        }
        self.payoff = {
            self.max_player.char: 10000,
            self.min_player.char: -10000,
            'draw': 0
        }
        self.heuristic_matrix = [
            3, 2, 3,
            2, 4, 2,
            3, 2, 3
        ]
        self.heuristic_sign = {
            self.max_player.char: 1,
            self.min_player.char: -1,
            ' ': 0
        }

    def heuristic(self, state: 'State', game_state: 'GameState') -> int:
        if game_state.terminal:
            return self.payoff[game_state.result]
        return sum((
            self.heuristic_sign[x] * self.heuristic_matrix[i]
            for i, x in enumerate(state.board)
        ))

    def generate_successors(self, state: 'State', max_move: bool):
        char = self.players[max_move].char
        for i in state.empty_spaces:
            yield state.transform_state(i, char)

    @staticmethod
    def _find_all_optimas(collection, compare):
        optimum = compare(collection, key=lambda x: x[1])[1]
        return [x[0] for x in collection if x[1] == optimum]

    def get_optimal_move(self, state: 'State', player: Player):
        if Game.check_game_state(state).terminal:
            raise ValueError("Game is in terminal state!")
        is_max = True
        if player == self.min_player:
            is_max = False
        results = [(i, self.minimax(state.transform_state(i, player.char), self.depth-1, not is_max))
                   for i in state.empty_spaces]
        if is_max:
            return choice(self._find_all_optimas(results, max))
        return choice(self._find_all_optimas(results, min))

    def minimax(self, state: 'State', d, max_move: bool):
        game_state = Game.check_game_state(state)
        if game_state.terminal or d == 0:
            return self.heuristic(state, game_state)
        payoffs = []
        for successor in self.generate_successors(state, max_move):
            payoffs.append(self.minimax(successor, d - 1, not max_move))
        if max_move:
            return max(payoffs)
        return min(payoffs)
