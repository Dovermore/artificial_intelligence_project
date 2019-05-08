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
    """
    An evaluator that only consider amount of exited pieces
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def __call__(self, state, *args, **kwargs):
        return state.completed[state.colour]


if __name__ == '__main__':
    from artificial_idiot.state import State
    import json
    from artificial_idiot.util.json_parser import JsonParser
    f = open("../tests/min_branch_factor.json")
    pos_dict, colour, completed = JsonParser(json.load(f)).parse()
    state = State(pos_dict, colour, completed)
    evaluator = DummyEvaluator()
    print(evaluator(state))