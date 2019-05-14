from artificial_idiot.machine_learning import (
    layer, activation, network, misc
)
from artificial_idiot.networks.const import (
    N_simple_grid_extractor
)

# Simple Linear unit
n_in = N_simple_grid_extractor
n_out = 1
theta = 0.05

layers = [
    layer.FullyConnected(n_in, n_out, activation=activation.Linear(),
                         weight_init=misc.normalised_initialiser(1))
]


def simple_linear_network():
    return network.Network(layers, theta, loss=activation.MSE)

