from abc import abstractmethod, ABC
import numpy as np


class Layer(ABC):
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
        self.n_in = n_in
        self.n_out = n_out
        self.W = weight_init(n_in, n_out)
        self.activation = activation

    def forward(self, X, training=False):
        z = X.dot(self.W)
        a = self.activation.compute(z)
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


class Convolution(Layer):
    """
    Defines a convolution layer, i.e. 2-d input with filter for network
    """
    # TODO change to horizontal_stride and vertical_stride
    def __init__(self, fshape, activation, filter_init, strides=1):
        self.fshape = fshape
        self.strides = strides
        self.filters = filter_init(self.fshape)
        self.activation = activation

    def forward(self, X, training=False):
        out_shape = (X.shape[1] - self.fshape[0]) / self.strides + 1
        out = np.zeros((X.shape[0], out_shape, out_shape, self.fshape[-1]))
        for j in range(out_shape):
            for i in range(out_shape):
                out[:, j, i, :] = \
                    np.sum(X[:, j * self.strides:j * self.strides
                                                 + self.fshape[0], i * self.strides:i * self.strides
                           + self.fshape[1], :, np.newaxis] * self.filters,
                           axis=(1, 2, 3))
        if training:
            return out, self.activation.compute(out)
        return self.activation.compute(out)

    def compute_dz(self, z, da):
        return da * self.activation.derivative(z)

    def compute_prev_da(self, dz):
        map_shape = (dz.shape[1] - 1) * self.strides + self.fshape[0]
        backward_derivative = np.zeros((dz.shape[0], map_shape, map_shape,
                                        self.fshape[-2]))
        s = (backward_derivative.shape[1] - self.fshape[0]) / self.strides + 1
        for j in range(s):
            for i in range(s):
                backward_derivative[:, j * self.strides:j * self.strides +
                                    self.fshape[0], i * self.strides:i
                                    * self.strides + self.fshape[1]] += \
                    np.sum(self.filters[np.newaxis, ...]
                           * dz[:, j:j + 1, i:i + 1, np.newaxis, :], axis=4)
        return backward_derivative

    def compute_dw(self, z, dz):
        total_layer_error = np.sum(dz, axis=(0, 1, 2))
        filters_error = np.zeros(self.fshape)
        shape = (z.shape[1] - self.fshape[0]) / self.strides + 1
        summed_inputs = np.sum(z, axis=0)
        for j in range(shape):
            for i in range(shape):
                filters_error += \
                    summed_inputs[j * self.strides:j * self.strides
                                  + self.fshape[0], i * self.strides:i
                                  * self.strides + self.fshape[1], :,
                                  np.newaxis]
        return filters_error * total_layer_error

    def update(self, dw):
        self.filters -= dw


class Flatten(Layer):
    """
    Flattens a convolution layer to a 1-d vector (Used in FC)
    """
    def __init__(self, shape):
        self.shape = shape

    def forward(self, X, train=False):
        z = np.reshape(X, (X.shape[0], -1))
        return z, z

    def compute_dz(self, z, da):
        return da

    def compute_prev_da(self, z):
        return np.reshape(z, (z.shape[0],) + self.shape)

    def compute_dw(self, z, dz):
        return 0.

    def update(self, dw):
        pass
