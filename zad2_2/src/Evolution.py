import numpy as np
import numpy.random as npr
from collections import namedtuple
from random import choices, getrandbits

Entity = namedtuple("Entity", "x value")
DataPoint = namedtuple("DataPoint", "t population")


def stop_condition(t, **kwargs):
    return t >= kwargs['t_max']


# tournament
def reproduce(population, **kwargs):
    max_n = len(population)
    tournaments = [npr.randint(0, max_n, 2) for _ in range(kwargs['pop_size'])]
    return [min(population[i], population[j], key=lambda x: x.value)
            for (i, j) in tournaments]


# # roulette
# def reproduce(population, **kwargs):
#     s = sum([x.value for x in population])
#     max_v = max([x.value for x in population])
#     min_v = min([x.value for x in population])
#     p = [(max_v-x.value+min_v)/s for x in population]
#     return choices(population, p, k=kwargs['pop_size'])

def mutate(population, func, **kwargs):
    mutants = []
    for p in population:
        x = p.x + kwargs['strength'] * npr.normal(size=len(p.x))
        mutants.append(Entity(x, func(x)))
    return mutants


# # empty
# def crossover(population, **kwargs):
#     return population


# #uniform crosssover
# def crossover(population, **kwargs):
#     max_n = len(population)
#     parents = [npr.randint(0, max_n, 2) for _ in range(kwargs['pop_size'])]
#     children = []
#     for (i, j) in parents:
#         genes = zip(population[i].x, population[j].x)
#         children.append(
#             Entity(np.array([x[getrandbits(1)] for x in genes]), -1)
#         )
#     return children

# # mean
# def crossover(population, **kwargs):
#     max_n = len(population)
#     parents = [npr.randint(0, max_n, 2) for _ in range(kwargs['pop_size'])]
#     weight = npr.normal(size=kwargs['dim'])
#     return [Entity(weight*population[i].x+(1-weight)*population[j].x, -1) for (i, j) in parents]

# elite selection
def select(mutants, old_population, **kwargs):
    mutants.extend(sorted(old_population, key=lambda x: x.value)[:kwargs['elite']])
    return sorted(mutants, key=lambda x: x.value)[:kwargs['pop_size']]


# non elite
# def select():
#     pass


def classic_evolution(func, init_pop, **kwargs):
    logs = []
    t = 0
    population = init_pop
    leader = min(population, key=lambda x: x.value)
    while not stop_condition(t, **kwargs):
        newborns = reproduce(population, **kwargs)
        # newborns = crossover(newborns, **kwargs)
        mutants = mutate(newborns, func, **kwargs)
        candidate = min(mutants, key=lambda x: x.value)
        if candidate.value <= leader.value:
            leader = candidate
        population = select(mutants, population, **kwargs)
        logs.append(DataPoint(t, population))
        t += 1
    return logs, leader
