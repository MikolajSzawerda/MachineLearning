import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from os.path import join as pjoin
from collections import namedtuple
from Experiments import expr
path = "../results"
gradients = []
classic_comp9 = [x for x in expr.keys() if 'csc_9' in x]
classic_comp1 = [x for x in expr.keys() if 'csc_1' in x]
se_comp1 = [x for x in expr.keys() if 'sec_1' in x]
se_comp9 = [x for x in expr.keys() if 'sec_9' in x]

def remove_outliers(df, col):
    mean = df[col].mean()
    std = df[col].std()
    return df[(df[col] <= mean+0.1*std)][col]

def plot(ax, experiments):
    for name in experiments:
        desc = expr[name]
        filename = pjoin(path, name + "_br.json")
        df = pd.read_json(filename)
        ax.plot(df['t'], df['population_y'].apply(np.mean), label=desc)
        # ax.plot(df['t'], df['population_y'].apply(np.min), label='min')
        # ax.plot(df['t'], df['population_y'].apply(np.max), label='max')
    ax.set_yscale('log')
    ax.set_ylabel("q(x)")
    ax.set_xlabel("t", loc="right")
    ax.get_yaxis().get_major_formatter().labelOnlyBase = False
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.07),
          fancybox=True, shadow=True, ncol=2)


def plot_sigma(ax, experiments):
    for name in experiments:
        desc = expr[name]
        filename = pjoin(path, name + "_br.json")
        df = pd.read_json(filename)
        ax.plot(df['t'], df['population_sigma'].apply(np.mean), label=desc)
        # ax.plot(df['t'], df['population_sigma'].apply(np.min), label=desc)
        # ax.plot(df['t'], df['population_sigma'].apply(np.max), label=desc)
    ax.set_xlabel("t")
    ax.set_ylabel("σ(t)")
    # ax.set_yscale('log')
    # ax.legend()


def plot_results_hist(ax, experiments):
    results, labels = [], []
    for name in experiments:
        filename = pjoin(path, name+"_r.csv")
        results.append(remove_outliers(pd.read_csv(filename), 'results'))
        labels.append(expr[name])
    ax.hist(results, 10, label=labels)
    ax.set_xlabel("q(x)")
    ax.legend()


def plot_boxplot(filename, ax):
    df = pd.read_csv(filename)
    ax.boxplot(df['results'])
    ax.set_yscale('log')


def summary_table(experiments):
    summary = []
    Row = namedtuple("Row", "name min max mean std")
    for name in experiments:
        desc = expr[name]
        filename = pjoin(path, name+"_r.csv")
        df = pd.read_csv(pjoin(path, filename))['results']
        summary.append(Row(desc, df.min(), df.max(), df.mean(), df.std()))
    return pd.DataFrame(summary).sort_values(by='min')


def plot_population_variety(ax, experiments):
    for name in experiments:
        filename = pjoin(path, name+"_br.json")
        df = pd.read_json(filename)
        df['x_mean'] = df['population_x'].apply(lambda x: np.std(np.linalg.norm(x, axis=1)))
        df = df[df.x_mean >=1e-12]
        ax.plot(df['t'], df['x_mean'], label=expr[name])
    ax.set_yscale("log")
    # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
    #           fancybox=True, shadow=True, ncol=2)


if __name__ == "__main__":
    se_comp9.remove('sec_9mccb')
    se_comp9.remove('sec_9uccb')
    se_comp9.remove('sec_9mccs')
    # current_expr = ['gd_9best', 'csc_9tmces', 'sec_9mcpd']
    current_expr = se_comp9
    table = summary_table(current_expr)
    table.to_csv(pjoin(path, "gradient_comp.csv"))
    print(table)
    fig, ax = plt.subplots(1)
    fig3, ax3 = plt.subplots(2)
    fig3.set_size_inches(10, 10)
    plot_population_variety(ax3[0], current_expr)
    handles, labels = ax3[0].get_legend_handles_labels()
    fig3.legend(handles, labels, ncol=5)
    plot(ax, current_expr)
    plot_sigma(ax3[1], current_expr)
    fig2, ax2 = plt.subplots(1)
    plot_results_hist(ax2, current_expr)
    # plot_boxplot(file_results, ax2[1])
    fig.tight_layout()
    fig.show()
    fig2.tight_layout()
    fig2.show()
    fig3.tight_layout()
    fig3.show()
