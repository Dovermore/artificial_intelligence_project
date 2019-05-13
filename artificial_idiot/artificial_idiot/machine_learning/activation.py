from abc import abstractmethod, ABC
import numpy as np


class AbstractActivation(ABC):
    @abstractmethod
    def compute(self, x):
        raise NotImplementedError()

    @abstractmethod
    def deriv(self, x):
        raise NotImplementedError()

class Relu(AbstractActivation):
    def compute(self, x):
        return np.maximum(0, x)

    def deriv(self, x):
        return 1. * (x > 0)

class Sigmoid(AbstractActivation):
    def compute(self, x):
        return 1. / (1. + np.exp(-x))

    def deriv(self, x):
        y = self.compute(x)
        return y * (1. - y)

class Loss(AbstractActivation):
    pass

class MeanSquaredError(Loss):
    def compute(self, Z):
        X, Y = Z
        return (1. / 2. * X.shape[0]) * ((X - Y) ** 2.)

    def deriv(self, Z):
        X, Y = Z
        return (X - Y) / X.shape[0]

relu = Relu()
sigmoid = Sigmoid()

mse = MeanSquaredError()
