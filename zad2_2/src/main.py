from Evolution import classic_evolution, Entity
import numpy.random as npr
import numpy as np
from cec2017.simple import *
from StrategyEvolution import strategy_opo, strategy_evolution, Entity as SEntity
import pandas as pd
from collections import namedtuple


def save_results(filename, results, dp):
    splitted_results = [
        dp(x.t, *list(zip(*x[1]))) for x in results
    ]
    pd.DataFrame(splitted_results).to_json(filename)


if __name__ == "__main__":
    func = f1
    # dp = namedtuple("dp", "t population_x population_y")
    # results, leader = classic_evolution(func, [
    #     Entity(x, func(x)) for x in [np.full(10, 100)]
    # ], **{
    #     'strength': 1,
    #     'elite': 1,
    #     'pop_size': 20,
    #     't_max': 2000,
    #     'dim': 10
    # })
    # dp = namedtuple("dp", "t population_x population_y population_sigma")
    # x = [100 for _ in range(10)]
    # se = SEntity(x, func(x), 1)
    # results = strategy_opo(func, se, **{
    #     'adaptation': 2,
    #     't_max': 1000,
    #     'sigma': se.sigma,
    #     'dim': len(x)
    # })
    # leader = results[-1].population[0]
    dp = namedtuple("dp", "t population_x population_y population_sigma")
    results, leader = strategy_evolution(func, [
        SEntity(x, func(x), npr.normal(size=10)) for x in [npr.uniform(-100, 100, 10) for _l in range(50)]
    ], **{
        'mi': 50,
        'lambda': 200,
        'dim': 10,
        't_max': 1000
    })
    save_results("../results/st_test.json", results, dp)
    print(leader.value)