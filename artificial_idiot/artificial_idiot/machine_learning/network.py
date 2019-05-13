from collections import deque
import pickle # Python serialisation library


class Network:
    """
    This class defines how to train the neural network
    """
    def __init__(self, layers, learning_rate, loss):
        """
        __init__ the nerwork class for training, by specifying a set of layers
        the dimension of layers must agree.
        A learning rate, and a loss function to compute lsos with
        :param layers: :AbstractBaseLayer: Layers that the data will pass
            through
        :param learning_rate: The learning rate of the network
        :param loss: Loss function to use.
        """
        self.layers = layers
        self.loss = loss
        self._learning_rate = learning_rate

    @property
    def learning_rate(self):
        """
        Gett of the learning rate of the network
        :return: The learning rate
        """
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, theta):
        """
        Setter of the learning rate
        :param theta: The value to set the learning rate to.
        """
        self._learning_rate = theta

    def forward(self, inputs):
        """
        Forward propagation of the neural network (or linear model)
        :param inputs: The input vector
        :return: The output of network
        """
        activation = inputs
        for l in self.layers:
            activation = l.forward(activation)
        return activation

    def backward(self, mini_batch):
        """
        One pass of backward propagation, updating parameters based on the
        given mini_batch of data
        :param mini_batch: The minibatch of data to train on
        """

        # X -> z1 -> a1 -> z2 -> a2 ... -> zn -> y_hat, loss = J(y - y_hat)
        mini_batch_inputs, mini_batch_outputs = mini_batch
        zs = deque([mini_batch_inputs])
        activation = mini_batch_inputs
        for layer in self.layers:
            z, activation = layer.forward(activation, True)
            zs.appendleft(z)
        d_yhat = self.loss.deriv((activation, mini_batch_outputs))
        z = zs.popleft()
        da = d_yhat
        gradients = deque()
        for layer in reversed(self.layers):
            # DJ/Dz_i = DJ/Da_i * Da_i/Dz_i
            dz = layer.get_dz(z, da) #local
            z = zs.popleft()
            # DJ/Dw_i = DJ/Dz_i * Dz_i/Dw_i
            gradient = layer.get_dw(z, dz)
            gradients.appendleft(gradient)
            # DJ/Da_i-1 = DJ/Dz_i * Dz/Da_i-1
            da = layer.get_da_prev(dz)

        for layer in self.layers:
            # W_t+1 = W_t - theta * gard
            layer.update(self.learning_rate * gradients.popleft())

        assert len(gradients) == 0

    def serialise(self):
        # pickle.
        pass
