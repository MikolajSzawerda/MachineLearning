import numpy as np
import numpy.random as npr
import numpy.ma as nma
import gym
from random import choices, randint
from tqdm import tqdm
import pandas as pd
from copy import deepcopy
from abc import ABC
from experiments import get_experiments
from time import process_time
from collections import namedtuple
from concurrent.futures import ProcessPoolExecutor
from warnings import simplefilter
simplefilter(action='ignore', category=DeprecationWarning)

SPACE_SHAPE = (500, 6)
Result = namedtuple("Result", "name filename time r_m r_std discount learning_rate strategy param t_max episodes")


def play(env, q_table, n=100):
    rewards = []
    t_max = 30
    for _ in range(n):
        t = 0
        terminal = False
        state, possible_actions = env.reset()
        reward = 0
        while t < t_max and not terminal:
            action = np.argmax(nma.masked_array(q_table[state, :], 1 - possible_actions['action_mask']))
            observation = env.step(action)
            reward += observation[1]
            state = observation[0]
            possible_actions = observation[4]
            terminal = observation[2] or observation[3]
        rewards.append(reward)
    env.close()
    return rewards


class ABCStrategy(ABC):
    def get_action(self, q_table, state) -> int:
        pass


class EpsilonStrategy(ABCStrategy):
    def __init__(self, random_strategy: ABCStrategy, greedy_strategy: ABCStrategy, **kwargs):
        self.weights = [kwargs['param'], 1 - kwargs['param']]
        self.strategies = [random_strategy, greedy_strategy]

    def get_action(self, q_table, state):
        strategy = choices(self.strategies, self.weights)[0]
        return strategy.get_action(q_table, state)


class BoltzmanStrategy(ABCStrategy):
    def __init__(self, **kwargs):
        self.tau = kwargs['param']

    def get_action(self, q_table, state):
        exped = np.exp(np.divide(q_table[state, :], self.tau))
        return choices(range(6), np.divide(exped, np.sum(exped)))[0]


class RandomStrategy(ABCStrategy):
    def __init__(self, **kwargs):
        pass

    def get_action(self, q_table, state):
        return randint(0, 5)


class GreedyStrategy(ABCStrategy):
    def __init__(self, **kwargs):
        pass

    def get_action(self, q_table, state):
        return np.argmax(q_table[state, :])


class LeastUsedStrategy(ABCStrategy):
    def __init__(self, weights, **kwargs):
        self.weights = weights

    def get_action(self, q_table, state):
        normalized = np.divide(self.weights[state, :], np.sum(self.weights[state, :]))
        return choices(range(6), np.divide(1 - normalized, np.sum(1 - normalized)))[0]


class CounterStrategy(ABCStrategy):
    def __init__(self, **kwargs):
        self.c_table = np.ones(SPACE_SHAPE)
        random_strategy = LeastUsedStrategy(self.c_table, **kwargs)
        self.strategy = EpsilonStrategy(random_strategy, GreedyStrategy(**kwargs), **kwargs)

    def get_action(self, q_table, state):
        action = self.strategy.get_action(q_table, state)
        self.c_table[state, action] += 1
        return action


class QLearn:
    @staticmethod
    def _get_strategy(strategy_type, **kwargs):
        if strategy_type == 'epsilon':
            return EpsilonStrategy(RandomStrategy(), GreedyStrategy(), **kwargs)
        elif strategy_type == 'boltzman':
            return BoltzmanStrategy(**kwargs)
        elif strategy_type == 'counter':
            return CounterStrategy(**kwargs)
        elif strategy_type == 'greedy':
            return GreedyStrategy(**kwargs)
        raise AttributeError

    def __init__(self, **kwargs):
        self.t_max = kwargs['t_max']
        self.e_max = kwargs['episodes']
        self.discount = kwargs['discount']
        self.learning_rate = kwargs['learning_rate']
        self.strategy = self._get_strategy(kwargs['strategy'], **kwargs)
        self.q_table = npr.uniform(0.0, 1.0, SPACE_SHAPE)

    def train(self):
        q_tables = []
        save_rate = self.e_max // 100
        env = gym.make("Taxi-v3")
        for episode in range(self.e_max):
            terminal = False
            t = 0
            state, _ = env.reset()
            while t < self.t_max and not terminal:
                action = self.strategy.get_action(self.q_table, state)
                observation = env.step(action)
                best_future = np.max(self.q_table[observation[0], :])
                current = self.q_table[state, action]
                delta = observation[1] + self.discount * best_future - current
                self.q_table[state, action] += self.learning_rate * delta
                state = observation[0]
                t += 1
                terminal = observation[2] or observation[3]
            if episode % save_rate == 0:
                q_tables.append(deepcopy(self.q_table))
        env.close()
        return q_tables


def evaluate_table(q_table):
    env = gym.make("Taxi-v3")
    return play(env, q_table, 10)


def evaluate_evolution(q_tables):
    return [evaluate_table(table) for table in q_tables]


def perform_experiment(experiment):
    q_learn = QLearn(**experiment)
    start = process_time()
    q_tables = q_learn.train()
    end = process_time()
    pd.DataFrame(evaluate_evolution(q_tables)).to_csv(f'results/{experiment["filename"]}_episodes.csv')
    final_result = play(gym.make("Taxi-v3"), q_tables[-1], 1000)
    pd.DataFrame(final_result, columns=['reward']).to_csv(f'results/{experiment["filename"]}_final.csv')
    return Result(time=end - start, r_m=np.average(final_result),
                  r_std=np.std(final_result), **experiment)


if __name__ == '__main__':
    with ProcessPoolExecutor() as executor:
        results = []
        experiments = get_experiments()
        for result in tqdm(executor.map(perform_experiment, experiments),
                           total=len(experiments)):
            results.append(result)
            pd.DataFrame(results).to_csv(f'results/experiments.csv')
