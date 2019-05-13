import numpy as np


def normalised_initialiser(factor=1):
    """
    Get an initialiser with pre-specified normalisation factor
    :return: A initialiser for weights
    """
    def initialiser(n_in, n_out):
        """
        The weight initialiser for a general relu/sigmoid
        unit for fully connected nodes (i.e. simple FFNN)
        :param n_in: The input dimension of weight matrix
        :param n_out: The output dimension of weight matrix
        :return: The initialised matrix
        """
        return np.random.rand(n_in, n_out)*np.sqrt(factor/(n_in+n_out))
    return initialiser
