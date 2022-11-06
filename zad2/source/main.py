from source.Evolution import evolution_algorithm
from source.GradientDescent import gradient_descent
import json

if __name__ == '__main__':
    params = {
        'strength': 0.03,
        'elite': 1,
        'pop_size': 20,
        't_max': 2000,
        'init_pop_size': 10,
        'reruns': 20,
        'dim': 10
    }
    exp = [
        {
            'title': "Tets",
            'kwargs': params
        }
    ]
    
    with open("evolution.json", 'w') as fh:
        json.dump(exp, fh, indent=4)