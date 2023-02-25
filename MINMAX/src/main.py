from MinMax import MinMax
from TicTacToe import Game, Player
import pandas as pd
from itertools import product
from tqdm import tqdm
import time
import csv

def p1_input():
    return int(input("x: "))


def p2_input():
    return int(input("o: "))


def explore_depth(p1_depth, p2_depth):
    max_player, min_player = Player('x'), Player('o')
    results = []
    for _ in tqdm(range(15)):
        game = Game(max_player, min_player)
        p1_minimax = MinMax(p1_depth, max_player, min_player)
        p2_minimax = MinMax(p2_depth, max_player, min_player)
        def p1_input():
            return p1_minimax.get_optimal_move(game.board, max_player)
        def p2_input():
            return p2_minimax.get_optimal_move(game.board, min_player)
        start = time.process_time()
        label, moves = game.play(p1_input, p2_input)
        end = time.process_time()
        results.append([p1_depth, p2_depth, label, end-start, *moves])
    return results

def interactive_play():
    max_player, min_player = Player("x"), Player("o")
    p1_minimax = MinMax(2, max_player, min_player)
    p2_minimax = MinMax(2, max_player, min_player)
    game = Game(max_player, min_player)
    def p1_input():
        return p1_minimax.get_optimal_move(game.board, max_player)
    def p2_input():
        return p2_minimax.get_optimal_move(game.board, min_player)
    game.interactive_play(p1_input, p2_input, True)


if __name__ == '__main__':
    results = []
    for (p1_d, p2_d) in product(range(1, 10), range(1, 10)):
        results.extend(explore_depth(p1_d, p2_d))
    df = pd.DataFrame(results)
    df.columns = ['p1_depth', 'p2_depth', 'result', 'time', *[str(i) for i in range(10)]]
    df.to_csv("../results/results.csv", quoting=csv.QUOTE_NONNUMERIC)
    print(df)
    # interactive_play()
    # explore_depth(9, 9)
