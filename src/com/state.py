import os
import sys
sys.path.append("~/Project/artificial_intelligence_project/src/com")

from util.class_property import classproperty
from util.misc import print_board
from copy import copy, deepcopy


class State:
    """
    State class stores current node state, the state is represented
    as two dictionaries of forward position mapping and backward position
    mapping.
    piece_code -> [(x1, y1), (x2, y2), (x3, y3)...]
    (x1, y1) -> piece_code
    """
    _code_map = {"red": 0, "green": 1, "blue": 2, "blocks": 3}
    _rev_code_map = {value: key for key, value in _code_map.items()}
    _goal_map = {}

    def __init__(self, forward_dict, backward_dict, color):
        self._forward_dict = forward_dict
        self._backward_dict = backward_dict
        self._color = self._code_map[color]

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        # Hash doesn't work on dictionary
        return (self._forward_dict == other._forward_dict and
                self._backward_dict == other._backward_dict and
                self._color == other._color)

    @property
    def forward_dict(self):
        return copy(self._forward_dict)

    @property
    def backward_dict(self):
        return copy(self._backward_dict)

    @property
    def color(self):
        return self._color

    @classproperty
    def code_map(cls):
        return copy(cls._code_map)

    @code_map.setter
    def code_map(cls, code_map):
        cls._code_map = code_map

    def __str__(self, debug=False):
        # need a copy here
        backward_dict = self.backward_dict
        # Make the name shorter so display normally
        backward_dict = {key: self._rev_code_map[value][:3] for key, value
                         in backward_dict.items()}
        return print_board(backward_dict, debug=debug, printed=False)


if __name__ == "__main__":
    # Test for class property
    assert State.code_map == {"red": 0, "green": 1, "blue": 2, "blocks":3}
    State.code_map = {}
    assert State.code_map == {}

    forward_dict = {0: [(0, 0), (0, -1), (-2, 1)], 3: [(-1, 0), (-1, 1), (1, 1), (3, -1)]}
    backward_dict = {(0, 0): 0, (0, -1): 0, (-2, 1): 0, (-1, 0): 3, (-1, 1): 3, (1, 1): 3, (3, -1): 3}
    state = State(forward_dict, backward_dict, "red")
    print(state.forward_dict, state.backward_dict, state.code_map)
    assert State.code_map == {}
    state2 = State(forward_dict, backward_dict, "red")
    assert state == state2



