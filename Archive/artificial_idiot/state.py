from util.class_property import classproperty
from util.misc import print_board
from copy import copy
from util.mycopy import deepcopy


class State:
    """
    State class stores current node state, the state is represented
    as two dictionaries of forward position mapping and backward position
    mapping.
    piece_code -> [(x1, y1), (x2, y2), (x3, y3)...]
    (x1, y1) -> piece_code
    """
    # Records all generated states
    generated_states = {}

    _code_map = {"red": 0, "green": 1, "blue": 2, "block": 3}
    _print_map = {"red": "🔴", "green": "✅",
                  "blue": "🔵", "block": "⬛"}
    _rev_code_map = {value: key for key, value in _code_map.items()}

    def __new__(cls, pos_to_piece, colour):
        """
        Return the same instance if the positions indicated are completely the
        same as some previously created instances

        Use new to cache the instances for faster comparison,
        and also used for a better find in queue
        """
        frozen_pos = frozenset(pos_to_piece.keys())
        if frozenset(pos_to_piece.keys()) in cls.generated_states:
            return cls.generated_states[frozen_pos]
        else:
            return super(State, cls).__new__(cls)

    def __init__(self, pos_to_piece, colour, frozen=None):
        # DO THIS FIRST, OR THE LOOP OVERRIDES IT
        self._colour = colour
        # Map from positions to pieces
        self._pos_to_piece = pos_to_piece
        self._piece_to_pos = {col: [] for col in self._code_map}
        for location, colour in self._pos_to_piece.items():
            self._piece_to_pos[colour].append(location)

        if frozen is not None:
            self._frozen = frozen
        else:
            self._frozen = frozenset(self._pos_to_piece.keys())
        self._hash = hash(self._frozen)

    @property
    def piece_to_pos(self):
        # Need to deepcopy this for there are mutable lists
        return deepcopy(self._piece_to_pos)

    @property
    def pos_to_piece(self):
        return copy(self._pos_to_piece)

    @property
    def colour(self):
        return self._colour

    @classproperty
    def code_map(cls):
        return copy(cls._code_map)

    @code_map.setter
    def code_map(cls, code_map):
        cls._code_map = code_map

    def __repr__(self, **kwargs):
        # need a copy here
        pos_to_piece = self.pos_to_piece
        # Make the name shorter so display normally
        # pos_to_piece = {key: value[:3] for key, value
        #                 in pos_to_piece.items()}
        pos_to_piece = {key: self._print_map[value] for key, value
                        in pos_to_piece.items()}

        msg = f"Colour: {self._colour}"
        if "message" in kwargs:
            kwargs["message"] += msg
        else:
            kwargs["message"] = msg

        return print_board(pos_to_piece, **kwargs)

    def next_colour(self):
        """
        :return: The next active colour after current execution
        """
        return self._colour

    def occupied(self, pos):
        return pos not in self._pos_to_piece

    @staticmethod
    def inboard(pos):
        r, q = pos
        return abs(r) <= 3 and abs(q) <= 3 and abs(r+q) <= 3

    @classmethod
    def goal_state(cls, state, goal_colour):
        pos_to_piece = state.pos_to_piece
        # remove goal colour
        pos_to_piece = {k: v for k, v in pos_to_piece.items()
                        if v != goal_colour}
        return cls(pos_to_piece, goal_colour)

    def __hash__(self):
        # only need hash those two
        return self._hash

    def __eq__(self, other):
        # First compare hash, if hash is successful, compare id
        # last compare the content for a fast comparison
        # (This is based on experimental result of comparison speed)
        return (self._hash == hash(other) and
                (self is other or
                 self._frozen == other._frozen and
                 self._colour == other._colour))

    def __lt__(self, other):
        # There is no preference between states with same path cost
        return True
