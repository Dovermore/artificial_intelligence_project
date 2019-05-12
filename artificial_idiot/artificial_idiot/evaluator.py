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
     2. distance to exit
     3. amount of nodes
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def __call__(self, state, player, *args, **kwargs):
        return state.completed[player]


if __name__ == '__main__':
    from artificial_idiot.state import State
    import json
    from artificial_idiot.util.json_parser import JsonParser
    f = open("../tests/evaluator_test.json")
    pos_dict, colour, completed = JsonParser(json.load(f)).parse()
    state = State(pos_dict, colour, completed)
    evaluator = MyEvaluator()
    assert(evaluator(state, 'red') == 3)
    assert(evaluator(state, 'green') == 2)
    assert(evaluator(state, 'blue') == 4)
