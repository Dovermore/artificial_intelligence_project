import abc


class Cutoff(abc.ABC):
    """
    The class to wrap a cut off UCT function disregard of the internal and
    provide a function interface to the player class for evaluating when
    evaluation is no longer needed
    """
    @abc.abstractmethod
    def __init__(self, *args, **kwargs):
        """
        Initialise the evaluator
        """
        pass

    @abc.abstractmethod
    def __call__(self, state, *args, **kwargs):
        """
        Compute the value of a state based on the input.
        This will always compute wrt the perspective of a red player
        :param state: The state to evaluate on
        :return: int, The value of that specific state
        """
        pass


class DepthLimitCutoff(Cutoff):
    """
    return true for cut off when depth > max depth
    """
    def __init__(self, max_depth=None, *args, **kwargs):
        self.max_depth = max_depth
        super().__init__(*args, **kwargs)
        pass

    def __call__(self, state, depth=None, *args, **kwargs):
        return self.max_depth < depth




