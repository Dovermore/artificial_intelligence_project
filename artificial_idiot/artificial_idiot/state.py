from artificial_idiot.util.class_property import classproperty
from artificial_idiot.util.misc import print_board
from copy import copy


class State:
    """
    State class stores current node state, the state is represented
    as two dictionaries of forward position mapping and backward position
    mapping.
    piece_code -> [(x1, y1), (x2, y2), (x3, y3)...]
    (x1, y1) -> piece_code
    """
    _code_map = {"red": 0, "green": 1, "blue": 2}
    _print_map = {"red": "🔴", "green": "✅",
                  "blue": "🔵"}
    _rev_code_map = {value: key for key, value in _code_map.items()}

    def __init__(self, pos_to_piece, colour, completed=None):
        """
        Captures all the information about the state
        :param colour: string that represent the current player
        :param pos_to_piece: a dictionary {pos : piece type}
        :param completed: a dictionary {piece type : number of exited}
        """

        # This is the current active colour
        self._colour = colour
        # Map from positions to pieces
        self._pos_to_piece = pos_to_piece
        self._piece_to_pos = None

        if completed is None:
            completed = {col: 0 for col in self._code_map}
        self.completed = completed

        self.frozen = frozenset(self._pos_to_piece.keys())
        self._hash = hash(self.frozen)

    def occupied(self, pos):
        return pos not in self._pos_to_piece

    @classproperty
    def code_map(cls):
        return copy(cls._code_map)

    @classproperty
    def rev_code_map(cls):
        return copy(cls._rev_code_map)

    @classproperty
    def rev_code_map(cls):
        return cls._rev_code_map

    # @property
    # def piece_to_pos(self):
    #     # Only compute this when needed
    #     if self._piece_to_pos is None:
    #         self._piece_to_pos = {col: [] for col in self._code_map}
    #         for location, colour in self._pos_to_piece.items():
    #             self._piece_to_pos[colour].append(location)
    #     # Need to deepcopy this for there are mutable lists
    #     return deepcopy(self._piece_to_pos)

    @property
    def piece_to_pos(self):
        # One time computation, this one might be faster.
        # As this is not used frequently
        piece_to_pos = {col: [] for col in self._code_map}
        for location, colour in self._pos_to_piece.items():
            piece_to_pos[colour].append(location)
        return piece_to_pos

    @property
    def pos_to_piece(self):
        return copy(self._pos_to_piece)

    @property
    def colour(self):
        return self._colour

    @code_map.setter
    def code_map(cls, code_map):
        cls._code_map = code_map

    @classmethod
    def next_colour(cls, color):
        """
        :return: The next active colour after current execution
        """
        i = cls._code_map[color] + 1
        # went over, start again
        return cls._rev_code_map[i % 3]

    @classmethod
    def rotate_pos(cls, fr_color, to_color, pos):
        # grab distance between color
        f = cls._code_map[fr_color]
        t = cls._code_map[to_color]
        if t < f:
            dist = t + 3 - f
        else:
            dist = t - f
        for i in range(dist):
            x, z = pos
            y = -(x + z)
            pos = (y, x)
        return pos

    # TODO use rotate pos there
    def state_to_red(self):
        """
        change player to red
        always return a new state
        :return: a state where current player is red
        """
        if self.colour == "blue":
            rotate = 1
        elif self.colour == "gree":
            rotate = 2
        else:
            rotate = 0
        state = copy(self)
        for i in range(rotate):
            state = State.rotate_120(state)
        return state

    @classmethod
    def rotate_120(cls, state):
        """
        Helper function to create a new state by rotating the current state
        Color of the pieces also change:
        red -> green
        blue -> red
        green -> blue
        :param state: The state to rotate
        :return ns: the result of rotating state by 120 degrees clockwise
        """
        # change player
        color = State.next_colour(state._colour)
        # change color of completed nodes
        completed = {}
        for p in state.completed:
            completed[State.next_colour(p)] = state.completed[p]
        # rotate board
        pos_to_piece = {}
        for pos in state._pos_to_piece:
            # https://www.redblobgames.com/grids/hexagons/#rotation
            x, z = pos
            y = -(x+z)
            color = State.next_colour(state._pos_to_piece[pos])
            pos_to_piece[(y, x)] = color

        return State(pos_to_piece, color, completed)

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
        return print_board(pos_to_piece, **kwargs, printed=False) + \
            "\n# Completed: " + str(self.completed)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        # First compare hash, if hash is successful, compare id
        # last compare the content for a fast comparison
        # (This is based on experimental result of comparison speed)
        return (isinstance(other, State) and
                self._hash == hash(other) and
                self.frozen == other._frozen and
                self._colour == other._colour and
                self._pos_to_piece == other._pos_to_piece
                )

    def __lt__(self, other):
        # There is no preference between states with same path cost
        return True

    @staticmethod
    def inboard(pos):
        r, q = pos
        return abs(r) <= 3 and abs(q) <= 3 and abs(r+q) <= 3

    @staticmethod
    def gety(r, q):
        return -(r + q)

    # @classmethod
    # def rotate_pos_120(cls, pos, n):
    #     """
    #     Rotate a position by 120 degree, n times clockwise
    #     :param pos: (x, z)
    #     :param n: number of rotation of 120 degree
    #     :return: rotated position
    #     """
    #     n %= 3
    #     x, z = pos
    #     y = -(x + z)
    #     # "Hard code" the logic as it won't change
    #     if n == 1:
    #         return y, x
    #     elif n == 2:
    #         return z, y
    #     return pos
    #
    # @classmethod
    # def rotate_pos_colour(cls, pos, from_colour, to_colour):
    #     """
    #     Rotate the position based on the given colour
    #     :param pos: The position to be rotated
    #     :param from_colour: From which colour's position
    #     :param to_colour: To which colour's position
    #     :return: Rotated position
    #     """
    #     n = cls._code_map[to_colour] - cls._code_map[from_colour]
    #     return State.rotate_pos_120(pos, n)


if __name__ == '__main__':
    def rotate_test():
        test = State({(1, -1): "red", (0, 0): "green", (0, 1): "blue"}, "blue", {"blue": 1})
        check = State({(-1, 0): "red", (0, 1): "green", (0, 0): "blue"}, "red", {"red": 1})
        assert (check == State.rotate_120(test))
        assert (check == State.state_to_red(test))


    def color_test():
        assert (State.next_colour("red") == "green")
        assert (State.next_colour("blue") == "red")
        assert (State.next_colour("green") == "blue")


    def rotate_action_test():
        assert(State.rotate_pos("green", "blue", (0, -3)) == (3,0))
        assert(State.rotate_pos("green", "red", (0, -3)) == (-3, 3))

    # test next color
    color_test()
    # test rotate state
    rotate_test()
    # rotate action
    rotate_action_test()
