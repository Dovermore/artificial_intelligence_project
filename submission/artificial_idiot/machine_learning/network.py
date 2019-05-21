from collections import deque
import pickle  # Python serialisation library
import os
import os.path as path
from datetime import datetime


dirname = os.path.dirname(__file__)
start = datetime.now().strftime("%Y%m%d%H%M%S")
default_save_path = path.join(dirname, start, "network")
default_checkpoint_path = path.join(dirname, start, "checkpoints")


class Network:
    """
    This class defines how to train the neural network
    """
    def __init__(self, layers, learning_rate, loss,
                 save_to=default_save_path,
                 checkpoint_path=default_checkpoint_path):
        """
        __init__ the nerwork class for training, by specifying a set of layers
        the dimension of layers must agree.
        A learning rate, and a loss function to compute lsos with
        :param layers: :AbstractBaseLayer: Layers that the data will pass
            through
        :param learning_rate: The learning rate of the network
        :param loss: Loss function to use.
        :param save_to: save to certain path
        :param checkpoint_path: where the checkpoints are saved to
        """
        self.layers = layers
        self.loss = loss
        self.learning_rate = learning_rate
        self.save_to = save_to
        self.checkpoint_path = checkpoint_path

    def forward(self, X, y=None, train=False):
        """
        Forward propagation of the neural network (or linear model)
        :param X: The feature vector
        :param y: The labels
        :param train: if training mode is on
        :return: The output of network
        """
        # X -> z1 -> a1 -> z2 -> a2 ... -> zn -> y_hat, loss = J(y - y_hat)
        zs = deque([X])
        activation = X
        # print("====================")
        for layer in self.layers:
            z, activation = layer.forward(activation, True)
            zs.appendleft(z)
            # print(activation)
        # print("====================")
        # print(activation)
        # print("====================")
        if train:
            return activation, zs
        return activation

    def _compute_gradients(self, zs, d_yhat):
        z = zs.popleft()
        da = d_yhat
        gradients = deque()
        for layer in reversed(self.layers):
            # DJ/Dz_i = DJ/Da_i * Da_i/Dz_i
            dz = layer.compute_dz(z, da)
            # if d_yhat[0][0] != 0:
            #     print(layer, dz, da)
            z = zs.popleft()
            # DJ/Dw_i = DJ/Dz_i * Dz_i/Dw_i
            gradient = layer.compute_dw(z, dz)
            gradients.appendleft(gradient)
            # DJ/Da_i-1 = DJ/Dz_i * Dz/Da_i-1
            da = layer.compute_prev_da(dz)
        return gradients

    def _apply_gradients(self, gradients):
        for layer in self.layers:
            # W_t+1 = W_t - theta * gard
            layer.update(self.learning_rate * gradients.popleft())
        assert len(gradients) == 0

    def backward(self, X, y):
        """
        One pass of backward propagation, updating parameters based on the
        given mini_batch of data
        :param X: value of X feature set
        :param y: value of y label set
        """
        y_hat, zs = self.forward(X, 1, True)
        dy_hat = self.loss.derivative(y_hat, y)
        gradients = self._compute_gradients(zs, dy_hat)
        self._apply_gradients(gradients)

    @staticmethod
    def from_file(file):
        with open(file, "rb") as file:
            return pickle.load(file)

    def save_checkpoint(self):
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        os.makedirs(self.checkpoint_path, exist_ok=True)
        with open(path.join(self.checkpoint_path, f"checkpoint_{now}"),
                  "wb") as f:
            pickle.dump(self, f)

    def save_final(self):
        if not path.exists(self.save_to):
            os.makedirs(os.path.dirname(self.save_to), exist_ok=True)
        with open(self.save_to, "wb") as f:
            pickle.dump(self, f)

