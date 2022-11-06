import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot(filename, ax):
    df = pd.read_json(filename)
    ax.plot(df['t'], df['population_y'].apply(np.mean))
    ax.plot(df['t'], df['population_y'].apply(np.min))
    # ax.plot(df['t'], df['population_y'].apply(np.max))
    ax.set_yscale('log')


def plot_sigma(filename, ax):
    df = pd.read_json(filename)
    ax.plot(df['t'], df['population_sigma'].apply(np.mean))
    # ax.plot(df['t'], df['population_sigma'].apply(np.min))
    # ax.plot(df['t'], df['population_sigma'].apply(np.max))
    # ax.set_yscale('log')


if __name__ == "__main__":
    filename = "../results/st_test.json"
    fig, ax = plt.subplots(1, 2)
    plot(filename, ax[0])
    plot_sigma(filename, ax[1])
    fig.show()
