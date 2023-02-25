from itertools import product
import numpy as np

discounts = (0.1, 0.9)
learning_rates = (0.1, 0.5, 1.0, 1.3)
strategies = ('epsilon', 'boltzman', 'counter')
strategies_param = (0.1, 1.0)

T_MAX = 30
EPISODES = 5000

def get_experiments():
    experiments = []
    for d, lr, s, sp in product(discounts, learning_rates,
                                strategies, strategies_param):
        name = f'{s} {d} {lr} {sp}'
        filename = name.replace(' ', '_').replace('.', '')
        experiments.append({
            'name': name,
            'filename': filename,
            't_max': T_MAX,
            'episodes': EPISODES,
            'discount': d,
            'learning_rate': lr,
            'strategy': s,
            'param': sp
        })
    return experiments
