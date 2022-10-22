import os
from PIL import Image, ImageFont, ImageDraw

def message(experiment, exec_time, label=""):
    return "\n".join(
        [
            "-"*10,
            "Experiment:" + " ".join([label, experiment.label]),
            "Result: " + str(experiment.result),
            "Execution time: " + str(exec_time)
        ]
    )

def isfloat(number):
    try:
        float(number)
    except ValueError:
        return False
    return True

def sanitate(string:str):
    return string.replace(' ', '_').replace('.', '_')

def shortened_number(number: str):
    return round(float(number), 4) if isfloat(number) else number

def filename(path, *args):
    return os.path.join(path, "_".join([sanitate(x) for x in args])+".png")