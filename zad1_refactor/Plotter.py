import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from Experiment import Experiment, Recorder
from utils import *


class Plotter:

    def __init__(self, path="results"):
        plt.style.use('ggplot')
        matplotlib.use('Agg')
        self.path=path

    def isconverging(self, data):
        data_at_inf = data[-len(data)//10:]
        return abs(min(data_at_inf)-max(data_at_inf))<=1e-2


    def plot(self, experiment: "Experiment", title, scale="symlog", percentage=1.0):
        fig, ax = plt.subplots()
        experiment.recorders.sort(key=lambda x: x.result)
        num_of_recorders = int(len(experiment.recorders)*percentage)
        recorders_to_plot = experiment.recorders[:num_of_recorders]
        for recorder in recorders_to_plot:
            x, y = list(zip(*[(d.iteration, d.y) for d in recorder.logs]))
            ax.plot(x, y, label=shortened_number(recorder.label))
        ax.set_yscale(scale, linthresh=1e-20)
        ax.set_ylabel("q(X)")
        ax.set_xlabel("t - # iteracji")
        ax.set_title(title)
        ax.legend()
        fig.tight_layout()
        fig.set_size_inches(12, 12)
        fig.savefig(filename(self.path, title), dpi=200)

    def comparison_plot(self, title, percentage=1.0, *experiments):
        fig, ax = plt.subplots(len(experiments))
        for i, experiment in enumerate(experiments):
            experiment.recorders.sort(key=lambda x: x.result)
            num_of_recorders = int(len(experiment.recorders)*percentage)
            recorders_to_plot = experiment.recorders[:num_of_recorders]
            for recorder in recorders_to_plot:
                x, y = list(zip(*[(d.iteration, d.y) for d in recorder.logs]))
                ax[i].plot(x, y, label=shortened_number(recorder.label))
            ax[i].set_yscale("symlog", linthresh=1e-20)
            ax[i].set_ylabel("q(X)")
            ax[i].set_xlabel("t - # iteracji")
            # ax[i].set_title(title)
            ax[i].legend()
            fig.tight_layout()
            # fig.set_size_inches(12, 12)
        fig.savefig(filename(self.path, title), dpi=200)

    def plot_paths(self, experiment: "Experiment", domain, title="", percentage=1.0):
        num_of_recorders = int(len(experiment.recorders)*percentage)
        recorders_to_plot = experiment.recorders[:num_of_recorders]
        fig, ax = plt.subplots()
        for recorder in recorders_to_plot:
            x, y = list(zip(*[(dp.x[0], dp.x[1]) for dp in recorder.logs]))
            X, Y = np.meshgrid(*[np.linspace(dim[0], dim[1], 256) for dim in domain])
            Z = experiment.func([X, Y])
            levels = np.linspace(np.min(Z), np.max(Z), 20)
            ax.contour(X, Y, Z, levels=levels)
            ax.plot(x, y, '-o', label=recorder.label)
            ax.legend()
        fig.set_size_inches(12, 12)
        fig.savefig(filename(self.path, title), dpi=200)


    def plot_recorder(self, recorder: "Recorder", title, scale="symlog"):
        fig, ax = plt.subplots()
        x, y = list(zip(*[(d.iteration, d.y) for d in recorder.logs]))
        ax.plot(x, y, label=shortened_number(recorder.label))
        if scale == "symlog":
            ax.set_yscale(scale, linthresh=1e-20)
        else:
            ax.set_yscale(scale)
        ax.set_ylabel("q(X)")
        ax.set_xlabel("t - # iteracji")
        ax.set_title(title)
        ax.legend()
        fig.tight_layout()
        fig.savefig(filename(self.path, title))


    def plot_path(self, recorder: "Recorder", func):
        x, y = list(zip(*[(dp.x[0], dp.x[1]) for dp in recorder.logs]))
        X, Y = np.meshgrid(np.linspace(-10, 10, 256), np.linspace(-10, 10, 256),)
        Z = func([X, Y])
        levels = np.linspace(np.min(Z), np.max(Z), 20)
        plt.contour(X, Y, Z, levels=levels)
        plt.plot(x, y, '-o')
        plt.show()