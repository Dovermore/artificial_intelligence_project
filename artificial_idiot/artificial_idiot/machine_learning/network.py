from collections import deque


class Network(object):
    def __init__(self, layers, learning_rate, loss):
        self.layers = layers
        self.loss = loss
        self._learning_rate = learning_rate

    @property
    def learning_rate(self):
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, v):
        self._learning_rate = v

    def forward(self, inputs):
        activation = inputs
        for l in self.layers:
            activation = l.forward(activation)
        return activation

    def train_step(self, mini_batch):
        mini_batch_inputs, mini_batch_outputs = mini_batch
        zs = deque([mini_batch_inputs])
        activation = mini_batch_inputs
        for l in self.layers:
            z, activation = l.train_forward(activation)
            zs.appendleft(z)

        loss_err = self.loss.deriv((activation, mini_batch_outputs))
        lz = zs.popleft()
        backwarded_err = loss_err
        grads = deque()
        for l in reversed(self.layers):
            layer_err = l.get_layer_error(lz, backwarded_err) #local
            lz = zs.popleft()
            grads.appendleft(l.get_grad(lz, layer_err))
            backwarded_err = l.backward(layer_err) # backwarded error

        # update step
        for l in self.layers:
            l.update(self.learning_rate * grads.popleft())

        assert len(grads) == 0
