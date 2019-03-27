from util.class_property import classproperty
from util.misc import print_board
from copy import copy, deepcopy
from collections import defaultdict as dd


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

    def __init__(self, forward_dict, colour):
        # DO THIS FIRST, OR THE LOOP OVERRIDES IT
        self._colour = colour
        # Map from piece to positions
        self._forward_dict = forward_dict
        # Map from positions to pieces
        self._backward_dict = dd(str)
        # Derive the backward mapping
        for colour, locations in self._forward_dict.items():
            for location in locations:
                self._backward_dict[location] = colour

    def __eq__(self, other):
        # Has to first be same class
        if not isinstance(other, self.__class__):
            return False
        return (self._backward_dict == other._backward_dict and
                self._colour == other._colour)

    @property
    def forward_dict(self):
        # Need to deepcopy this for there are mutable lists
        return deepcopy(self._forward_dict)

    @property
    def backward_dict(self):
        return copy(self._backward_dict)

    @property
    def colour(self):
        return self._colour

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
        backward_dict = {key: value[:3] for key, value
                         in backward_dict.items()}
        return print_board(backward_dict, debug=debug, printed=False,
                           message=f"Colour: {self._colour}")

    def delete_colour(self, colour):
        """
        Removes all the pieces of that colour from the board
        colour must be a string
        """
        # remove the pieces of the given colour
        for location in self._forward_dict[colour]:
            del self._backward_dict[location]
        del self._forward_dict[colour]

    def next_colour(self):
        """
        :return: The next active colour after current execution
        """
        return self._colour

    def occupied(self, pos):
        return pos not in self._backward_dict

    @staticmethod
    def inboard(pos):
        r, q = pos
        return not (r < -3 or r > 3 or q < -3 or q > 3 or abs(r+q) > 3)

    @classmethod
    def goal_state(cls, state, goal_colour):
        forward_dict = state.forward_dict
        backward_dict = state.backward_dict

        if goal_colour:
            # remove the pieces of the given colour
            for location in forward_dict[goal_colour]:
                del backward_dict[location]
            del forward_dict[goal_colour]
        return cls(forward_dict, goal_colour)

    def __hash__(self):
        # only need hash those two
        return hash(frozenset(self._backward_dict)) ^ hash(self._colour)

    def __lt__(self, other):
        # There is no preference between states with same path cost
        return True


if __name__ == "__main__":
    # Test for class property
    assert State.code_map == {"red": 0, "green": 1, "blue": 2, "blocks":3}
    State.code_map = {}
    assert State.code_map == {}

    forward_dict = {0: [(0, 0), (0, -1), (-2, 1)], 3: [(-1, 0), (-1, 1), (1, 1), (3, -1)]}
    state = State(forward_dict, "red")
    print(state.forward_dict, state.backward_dict, state.code_map)
    assert State.code_map == {}
    state2 = State(forward_dict, "red")
    assert state == state2



