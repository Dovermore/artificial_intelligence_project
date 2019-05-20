from abc import abstractmethod, ABC


class Layer(ABC):
    def __init__(self):
        # TODO implement dropout
        # For drop-out
        self.mask = None
        # TODO implement momentum gradient descent
        # For momentum gradient descent
        self.velocity = 0

    @abstractmethod
    def forward(self, X, training=False):
        """
        Compute forward value of a layer
        :param X: The input to the layer, dimension must agree
        :param training: specifies how the behave differently for different
            phase
        :return: Forward layer output
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_dz(self, z, da):
        """
        Compute error of a layer using the unactivated value z and error from
        output layer.
        DJ/Dz_i = DJ/Da_i * Da_i/Dz_i
        :param z: The value of
        :param da: The derivative of activation
        :return: dz: The derivative of affine transformed input (z)
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_prev_da(self, dz):
        """
        Compute derivative for activation function of previous layer
        """
        raise NotImplementedError()

    @abstractmethod
    def compute_dw(self, inputs, layer_err):
        raise NotImplementedError()

    @abstractmethod
    def update(self, dw):
        raise NotImplementedError()


class FullyConnected(Layer):
    def __init__(self, n_in, n_out, activation, weight_init):
        super().__init__()
        self.n_in = n_in
        self.n_out = n_out
        self.W = weight_init(n_in, n_out)
        self.activation = activation

    # TODO add mask for dropout
    def forward(self, X, training=False, dropout=0.6):
        z = X.dot(self.W)
        # print(z)
        a = self.activation.compute(z)
        # print(a)
        if training:
            return z, a
        return a

    def compute_dz(self, z, backwarded_err):
        """
        Chain rule, a = activation(z)
        dy/dz = dy/da * da/dz
        """
        return backwarded_err * self.activation.derivative(z)

    def compute_prev_da(self, z):
        """
        Chain rule, z = X @ w, a = relu(z)
        dy/dw = dy/dz * dz/dw
        """
        return z.dot(self.W.T)

    def compute_dw(self, z, dz):
        # DJ/Dw_i = DJ/Dz_i * Dz_i/Dw_i = z * dz
        return z.T.dot(dz)

    def update(self, dw):
        self.W -= dw

