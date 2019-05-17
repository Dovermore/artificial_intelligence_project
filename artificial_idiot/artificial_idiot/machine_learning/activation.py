from abc import abstractmethod, ABC
import numpy as np


class AbstractActivation(ABC):
    """
    Abstract class for activation functions.
    """
    @abstractmethod
    def compute(self, X, y=None):
        """
        Computed during forward propagation
        """
        raise NotImplementedError()

    @abstractmethod
    def derivative(self, X, y=None):
        """
        Computed during backward propagation
        :param X: Input to activation function
        :param y: placeholder
        :return: the value after activation
        """
        raise NotImplementedError()


class Relu(AbstractActivation):
    def compute(self, X, y=None):
        return np.maximum(0, X)

    def derivative(self, X, y=None):
        return 1 * (X > 0)


class Sigmoid(AbstractActivation):
    def compute(self, X, y=None):
        return 1 / (1 + np.exp(-X))

    def derivative(self, X, y=None):
        y = self.compute(X)
        return y * (1 - y)


class LeakyRelu(AbstractActivation):
    def compute(self, X, y=None):
        return np.maximum(0.01 * X, X)

    def derivative(self, X, y=None):
        g = 1 * (X > 0)
        g[g == 0] = 0.01
        return g


class Linear(AbstractActivation):
    def compute(self, X, y=None):
        return X

    def derivative(self, X, y=None):
        return 1


class SoftMax(AbstractActivation):

    def compute(self, X, y=None):
        assert np.ndim(X) == 2
        x = X - np.max(X, axis=1, keepdims=True)
        exp_x = np.exp(x)
        s = exp_x / np.sum(exp_x, axis=1, keepdims=True)
        return s

    def derivative(self, X, y=None):
        return np.ones(X.shape)


class Loss(AbstractActivation, ABC):
    pass


class XEntropy(Loss):
    def _softmax(self, X, y=None):
        exponential_X = np.exp(X - np.max(X, axis=1)[..., np.newaxis])
        return exponential_X/np.sum(exponential_X, axis=1, keepdims=True)

    def compute(self, X, y=None):
        sf = self._softmax(X)
        return -np.log(sf[np.arange(X.shape[0]),
                          np.argmax(y, axis=1)]) / X.shape[0]

    def derivative(self, X, y=None):
        error = self._softmax(X)
        return (error - y) / X.shape[0]


class MSE(Loss):
    def compute(self, X, y=None):
        return (1. / 2. * X.shape[0]) * ((X - y) ** 2.)

    def derivative(self, X, y=None):
        return (X - y) / X.shape[0]


class BinaryXEntropy(Loss):
    def __init__(self):
        super().__init__()
        self.epsilon = 1e-12

    def compute(self, X, y=None):
        outputs = np.clip(X, self.epsilon, 1 - self.epsilon)
        return np.mean(-np.sum(y * np.log(X) + (1 - y) * np.log(1 - outputs),
                               axis=1))

    def derivative(self, X, y=None):
        X = np.clip(X, self.epsilon, 1 - self.epsilon)
        divisor = np.maximum(X * (1 - X), self.epsilon)
        return (X - y) / divisor

