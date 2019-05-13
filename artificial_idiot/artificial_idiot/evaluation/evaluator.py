import abc
import numpy as np


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
    def __call__(self, state, player, *args, **kwargs):
        """
        Compute the value of a state based on the input.
        This will always compute wrt the perspective of a red player
        :param state: The state to evaluate on
        :return: int, The value of that specific state
        """
        pass


class DummyEvaluator(Evaluator):
    """
    An evaluator that only consider amount of exited pieces
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def __call__(self, state, player, *args, **kwargs):
        return 0


class WinLossEvaluator(Evaluator):
    """
    Return 1 if win, -1 if lost, else 0
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, state, player, *args, **kwargs):
        if state.completed[player] == 4:
            return 1
        for p in state.completed:
            if state.completed[p] == 4:
                return -1
        return 0


class MyEvaluator(Evaluator):
    """
    An evaluator that only considers
     1. amount of exited pieces
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, state, player, *args, **kwargs):
        return state.completed[player]


class WeightedEvaluator(Evaluator):
    """
    An evaluator that takes in functions that
    1. takes in current state
    returns how valuable the state is for a given player in the forms of
     np.array
    The values are concatenated by the order of function list
    These values are then multiplied by the weights
    """
    def __init__(self, functions, *args, **kwargs):
        self._functions = functions
        super().__init__(*args, **kwargs)

    def __call__(self, state, player, weights, *args, **kwargs):
        X = np.concatenate([fn(state) for fn in self._functions])
        # reshape to a row vector then perform the matrix multiplication
        return X.reshape(1, -1) @ weights


class FunctionalEvaluator(Evaluator):
    """
    Evaluate a state based on set of features computed by functions and
    return single scalar indicating the value of the state.

    The value is computed by feeding an arbitrary function to the state
    """
    def __init__(self, functions, *args, **kwargs):
        self._functions = functions
        super().__init__(*args, **kwargs)

    def __call__(self, state, player, weights, *args, **kwargs):
        X = np.concatenate([fn(state) for fn in self._functions])
        # reshape to a row vector then perform the matrix multiplication
        return X.reshape(1, -1) @ weights


if __name__ == '__main__':
    from artificial_idiot.game.state import State
    import json
    from artificial_idiot.util.json_parser import JsonParser
    f = open("../tests/evaluator_test.json")
    pos_dict, colour, completed = JsonParser(json.load(f)).parse()
    state = State(pos_dict, colour, completed)
    evaluator = MyEvaluator()
    assert(evaluator(state, 'red') == 3)
    assert(evaluator(state, 'green') == 2)
    assert(evaluator(state, 'blue') == 4)
