import abc


class Evaluator(abc.ABC):
    """
    The class to wrap a evaluation function disregard of the internal and
    provide a function interface to the player class for evaluating player's
    situation
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


class DummyEvaluator(Evaluator):

    def __init__(self, *args, **kwargs):
        """
        No setup
        """
        super().__init__(*args, **kwargs)
        pass

    def __call__(self, state, *args, **kwargs):
        """
        This is dummy evaluator, will always return 0 for all states
        """
        return 0

