from matplotlib import pyplot as plt
import numpy as np
from Experiment import Experiment, Recorder



class Plotter:

    def __init__(self):
        plt.style.use('ggplot')

    def isconverging(self, data):
        data_at_inf = data[-len(data)//10:]
        return abs(min(data_at_inf)-max(data_at_inf))<=1e-2

    def plot(self, experiment: "Experiment"):
        fig, ax = plt.subplots(2)
        for recorder in experiment.recorders:
            x, y = list(zip(*[(d.iteration, d.y) for d in recorder.logs]))
            ax[0].plot(x, y, label=recorder.name)
            ax[0].set_yscale("log")
            if self.isconverging(y):
                ax[1].plot(x, y, label=recorder.name)
                ax[1].set_yscale("log")
        plt.legend()
        plt.tight_layout()
        # plt.savefig(title)
        plt.show()

    def comparison_plot(self, *experiments):
        fig, ax = plt.subplots(len(experiments))
        for i, experiment in enumerate(experiments):
            for recorder in experiment.recorders:
                x, y = list(zip(*[(d.iteration, d.y) for d in recorder.logs]))
                ax[i].plot(x, y, label=recorder.name)
                ax[i].set_yscale("log")
        plt.legend()
        plt.tight_layout()
        # plt.savefig(title)
        plt.show()

    def plot_path(self, experiment: "Experiment"):
        for recorder in experiment.recorders:
            x, y = list(zip(*[(dp.x[0], dp.x[1]) for dp in recorder.logs]))
            X, Y = np.meshgrid(np.linspace(-10, 10, 256), np.linspace(-10, 10, 256),)
            Z = experiment.func([X, Y])
            levels = np.linspace(np.min(Z), np.max(Z), 20)
            plt.contour(X, Y, Z, levels=levels)
            plt.plot(x, y, '-o')
        plt.show()

    def plot_recorder(self, recorder: "Recorder"):
        x, y = list(zip(*[(d.iteration, d.y) for d in recorder.logs]))
        plt.plot(x, y, label=recorder.name)
        plt.legend()
        plt.tight_layout()
        # plt.savefig(title)
        plt.show()

    def plot_path(self, recorder: "Recorder", func):
        x, y = list(zip(*[(dp.x[0], dp.x[1]) for dp in recorder.logs]))
        X, Y = np.meshgrid(np.linspace(-10, 10, 256), np.linspace(-10, 10, 256),)
        Z = func([X, Y])
        levels = np.linspace(np.min(Z), np.max(Z), 20)
        plt.contour(X, Y, Z, levels=levels)
        plt.plot(x, y, '-o')
        plt.show()