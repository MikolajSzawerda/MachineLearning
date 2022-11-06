from math import sqrt

import numpy as np
import numpy.random as npr
from collections import namedtuple
from random import choices

Entity = namedtuple("Entity", "x value sigma")
DataPoint = namedtuple("DataPoint", "t population")


def strategy_opo(func, x0, **kwargs):
    logs = []
    t = 0
    ls = 0
    parent = x0
    sigma = kwargs['sigma']
    a = kwargs['adaptation']
    while t <= kwargs['t_max']:
        x = parent.x + sigma * npr.normal(size=kwargs['dim'])
        mutant = Entity(x, func(x), sigma)
        if mutant.value <= parent.value:
            ls += 1
            parent = mutant
        if t % a == 0:
            if ls / a > 1 / 5:
                sigma *= 1.22
            if ls / a < 1 / 5:
                sigma *= 0.82
            ls = 0
        logs.append(DataPoint(t, [mutant, parent]))
        t += 1
    return logs


def stop_condition(t, **kwargs):
    return t >= kwargs['t_max']


def reproduce(**kwargs):
    pass


def mutate(population, func, **kwargs):
    a = npr.normal()
    b = npr.normal(size=kwargs['dim'])
    tau = 1/sqrt(2*kwargs['dim'])
    taup = 1/sqrt(2*sqrt(kwargs['dim']))
    mutants = []
    for p in population:
        sigma = p.sigma*np.exp(taup*a+tau*b)
        x = p.x+sigma*npr.normal(size=kwargs['dim'])
        mutants.append(Entity(x, func(x), sigma))
    return mutants


def strategy_evolution(func, init_pop, **kwargs):
    logs = []
    t = 0
    population = init_pop
    leader = min(population, key=lambda x: x.value)
    while not stop_condition(t, **kwargs):
        population = choices(population, k=kwargs['lambda'])
        mutants = mutate(population, func, **kwargs)
        candidate = min(mutants, key=lambda x: x.value)
        if candidate.value <= leader.value:
            leader = candidate
        mutants.extend(population)
        population = sorted(mutants, key=lambda x:x.value)[:kwargs['mi']]
        logs.append(DataPoint(t, population))
        t += 1
    return logs, leader
