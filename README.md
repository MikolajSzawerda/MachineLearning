# Introduction to Artificial Intelligence

Set of projects that I had to implement for Introduction to Artificial Intelligence Course at Warsaw University of Technology.

Used languages:
- Python(implementation),
- R(data visualization)

Used libraries:
- autograd, numpy, pandas, scikit-learn, scipy
- ggplot2, tidyr, dplyr, gt

## Content

### Gradient Descent

Implement the gradient descent algorithm. Then test the convergence of the algorithm using the following function:

$$
q(x)=\sum_{i=1}^{n}{\alpha^{\frac{n-1}{i-1}}x_i^2, x \in [-100, 100]^n \subset \mathbb{R}^n}
$$

Investigate the effect of the learning rate value on method convergence and run time.

### Evolution Algorithms

Design and implement an evolutionary algorithm.
Then examine its convergence on the functions F1 and F9 from the CEC2017 benchmark for dimensionality n = 10.
In addition, compare the convergence of the evolutionary algorithm on the indicated functions with your own implementation of the gradient descent algorithm.

### MinMax

Implement the min-max algorithm in a tic-tac-toe game on a 3x3 board.
The program should play itself and visualize successive game states on the terminal.
Investigate the effect of game tree search depth on the quality of the results obtained.

### SVM

Implement the SVM algorithm and test the performance of the algorithm when applied to the Wine Quality Data Set.
To adapt the dataset to a binary classification problem, digitize the response variable.
Investigate the influence of hyperparameters on the performance of the implemented algorithm.
In your research, consider two different kernel functions learned in the lecture.

### Neural Network

Implement a multi-layer perceptron that will be used to approximate the function.

$$
f(x)=x^2 sin(x) + 50sin(2x)
$$

Investigate:
- influence of the number of neurons in the layer on the quality of the obtained approximation
- differences in the quality of approximation depending on the use
of the gradient method or the evolutionary method to find network weights.

### QLearning

Implement the Q-learning algorithm. Then, using the Taxi environment, examine the impact of hyperparameters (learning rate)
and the learned exploration strategies on the performance of the algorithm.

### Naive Bayes

Implement a naive Bayes classifier and test the performance of the algorithm when applied to the Iris Data Set.
