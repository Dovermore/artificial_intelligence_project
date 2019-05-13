from abc import abstractmethod, ABC


class AbstractLayer(ABC):

    @abstractmethod
    def forward(self, inputs, training=True):
        """
        Compute forward value of a layer
        :param inputs: The input to the layer, dimension must agree
        :param training: specifies how the behave differently for different
            phase
        :return: Forward layer output
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_dz(self, z, backward_err):
        """
        Compute error of a layer using the unactivated value z and error from
        output layer.
        :param z: The value of
        :param backward_err:
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_prev_da(self, z):
        """
        Compute derivative for activation function of previous layer
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_dw(self, inputs, layer_err):
        raise NotImplementedError()

    @abstractmethod
    def update(self, grad):
        raise NotImplementedError()


class FullyConnected(AbstractLayer):
    def __init__(self, n_in, n_out, activation, weight_init):
        self.n_in = n_in
        self.n_out = n_out
        self.W = weight_init(n_in, n_out)
        self.activation = activation

    def forward(self, inputs, training=False):
        z = inputs.dot(self.W)
        a = self.activation.compute(z)
        if training:
            return z, a
        return a

    def compute_dz(self, z, backwarded_err):
        return backwarded_err * self.activation.derivative(z)

    def compute_prev_da(self, z):
        """
        Chain rule, z = X @ w, a = relu(z)
        dy/dw = dy/dz * dz/dw
        """
        return z.dot(self.W.T)

    def compute_dw(self, inputs, layer_err):
        return inputs.T.dot(layer_err)

    def update(self, grad):
        self.W -= grad
