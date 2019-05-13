from abc import abstractmethod, ABC
import numpy as np


class AbstractActivation(ABC):
    """
    Abstract class for activation functions.
    """
    @abstractmethod
    def compute(self, x):
        """
        Computed during forward propagation
        """
        raise NotImplementedError()

    @abstractmethod
    def derivative(self, x):
        """
        Computed during backward propagation
        :param x:
        :return:
        """
        raise NotImplementedError()


class Relu(AbstractActivation):
    def compute(self, x):
        return np.maximum(0, x)

    def derivative(self, x):
        return 1 * (x > 0)


class Sigmoid(AbstractActivation):
    def compute(self, x):
        return 1 / (1 + np.exp(-x))

    def derivative(self, x):
        y = self.compute(x)
        return y * (1 - y)


class LeakyRelu(AbstractActivation):
    def compute(self, x):
        return np.maximum(0.01, x)

    def derivative(self, x):
        g = 1 * (x > 0)
        g[g == 0] = 0.01
        return g

class Linear(AbstractActivation):
    def compute(self, x):
        return x

    def derivative(self, x):
        return 1


class Loss(AbstractActivation):
    pass


class CrossEntropy(Loss):
    def _softmax(self, X):
        expvx = np.exp(X - np.max(X, axis=1)[..., np.newaxis])
        return expvx/np.sum(expvx, axis=1, keepdims=True)

    def compute(self, Z):
        X, Y = Z
        sf = self._softmax(X)
        return -np.log(sf[np.arange(X.shape[0]),
                          np.argmax(Y, axis=1)]) / X.shape[0]

    def derivative(self, Z):
        X, Y = Z
        err = self._softmax(X)
        return (err - Y) / X.shape[0]


class MeanSquaredError(Loss):
    def compute(self, Z):
        X, Y = Z
        return (1. / 2. * X.shape[0]) * ((X - Y) ** 2.)

    def derivative(self, Z):
        X, Y = Z
        return (X - Y) / X.shape[0]
