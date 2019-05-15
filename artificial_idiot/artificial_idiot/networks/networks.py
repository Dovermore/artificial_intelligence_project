from artificial_idiot.machine_learning import (
    layer, activation, network, misc
)
from artificial_idiot.networks.const import (
    N_simple_grid_extractor
)

from artificial_idiot.search.RL import (
    simple_grid_extractor,
    full_grid_extractor
)


def simple_linear_network():
    # Simple Linear unit
    n_in = N_simple_grid_extractor
    n_out = 1
    theta = 0.05

    layers = [
        layer.FullyConnected(n_in, n_out, activation=activation.Linear(),
                             weight_init=misc.normalised_initialiser(1))
    ]
    return network.Network(layers, theta, loss=activation.MSE())


def two_layer_sigmoid_network():
    n_in = N_simple_grid_extractor
    n_out1 = n_in // 2
    n_out2 = 1
    theta = 0.05
    layers = [
        layer.FullyConnected(n_in, n_out1, activation=activation.Sigmoid(),
                             weight_init=misc.normalised_initialiser(1)),
        layer.FullyConnected(n_out1, n_out2, activation=activation.Linear(),
                             weight_init=misc.normalised_initialiser(1)),
    ]
    return network.Network(layers, theta, loss=activation.MSE())


def four_layer_leaky_relu_network():
    n_in = N_simple_grid_extractor
    n_out1 = n_in * 2 // 3
    n_out2 = n_out1 * 2 // 3
    n_out3 = n_out2 * 2 // 3
    n_out4 = 1
    theta = 0.05
    layers = [
        layer.FullyConnected(n_in, n_out1, activation=activation.LeakyRelu(),
                             weight_init=misc.normalised_initialiser(1)),
        layer.FullyConnected(n_out1, n_out2, activation=activation.LeakyRelu(),
                             weight_init=misc.normalised_initialiser(1)),
        layer.FullyConnected(n_out2, n_out3, activation=activation.LeakyRelu(),
                             weight_init=misc.normalised_initialiser(1)),
        layer.FullyConnected(n_out3, n_out4, activation=activation.LeakyRelu(),
                             weight_init=misc.normalised_initialiser(1)),
    ]
    return network.Network(layers, theta, loss=activation.MSE())


architectures = {
    "linear": (simple_linear_network(), simple_grid_extractor),
    "two_sig": (two_layer_sigmoid_network(), simple_grid_extractor),
    "four_lkrl": (four_layer_leaky_relu_network(), simple_grid_extractor)
}
