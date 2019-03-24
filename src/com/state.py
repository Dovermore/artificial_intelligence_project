from com.util.class_property import classproperty
from copy import copy, deepcopy


class State:
    """
    State class stores states current node has, the state is represented
    as two dictionaries of forward position mapping and backward position
    mapping.
    piece_code -> [(x1, y1), (x2, y2), (x3, y3)...]
    (x1, y1) -> piece_code
    """

    _code_map = {"red": 0, "green": 1, "blue": 2, "blocks": 3}

    def __init__(self, forward_dict, backward_dict, turn):
        self._forward_dict = forward_dict
        self._backward_dict = backward_dict
        self._turn = turn

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        # Hash doesn't work on dictionary
        return (self._forward_dict == other._forward_dict and
                self._backward_dict == other._backward_dict and
                self._turn == other._turn)

    @property
    def forward_dict(self):
        return copy(self._forward_dict)

    @property
    def backward_dict(self):
        return copy(self._backward_dict)

    @classproperty
    def code_map(cls):
        return copy(cls._code_map)

    @code_map.setter
    def code_map(cls, code_map):
        cls._code_map = code_map


if __name__ == "__main__":
    # Test for class property
    assert State.code_map == {"red": 0, "green": 1, "blue": 2, "blocks":3}
    State.code_map = {}
    assert State.code_map == {}

    forward_dict = {0: [(0, 0), (0, -1), (-2, 1)], 3: [(-1, 0), (-1, 1), (1, 1), (3, -1)]}
    backward_dict = {(0, 0): 0, (0, -1): 0, (-2, 1): 0, (-1, 0): 3, (-1, 1): 3, (1, 1): 3, (3, -1): 3}
    state = State(forward_dict, backward_dict)
    print(state.forward_dict, state.backward_dict, state.code_map)
    assert State.code_map == {}
    state2 = State(forward_dict, backward_dict)
    assert state == state2



