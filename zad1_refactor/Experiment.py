from dataclasses import dataclass


@dataclass
class DataPoint:
    iteration: int
    x: list
    y: float


class Recorder:

    def __init__(self, name):
        self.logs = []
        self.name = name
        self.result = None

    def pushLog(self, data: "tuple[DataPoint]"):
        self.logs.append(data)

    def saveResult(self, value):
        self.result = value


class Experiment:

    def __init__(self, func=None):
        self.recorders = []
        self.result = float("inf")
        self.func = func
        self.best_recorder = None

    def appendRecorder(self, recorder: "Recorder"):
        self.recorders.append(recorder)
        if recorder.result < self.result:
            self.result = recorder.result
            self.best_recorder = recorder
