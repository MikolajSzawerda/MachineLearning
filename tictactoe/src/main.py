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


if __name__ == '__main__':
    max_player, min_player = Player('x'), Player('o')
    df = pd.DataFrame()
    results = []
    depths = product(range(1, 10), range(1, 10))
    for p1_depth, p2_depth in tqdm(depths):
        game = Game(max_player, min_player)
        p1_minimax = MinMax(p1_depth, max_player, min_player)
        p2_minimax = MinMax(p2_depth, min_player, max_player)

        def p1_input():
            return p1_minimax.get_optimal_move(game.board, max_player)

        def p2_input():
            return p2_minimax.get_optimal_move(game.board, min_player)
        start = time.process_time()
        label, moves = game.play(p1_input, p2_input)
        end = time.process_time()
        results.append([p1_depth, p2_depth, label, end-start, *moves])
    df = pd.DataFrame(results)
    df.columns = ['p1_depth', 'p2_depth', 'result', 'time', *[str(i) for i in range(10)]]
    df.to_csv("../results/results.csv", quoting=csv.QUOTE_NONNUMERIC)
    print(df)

