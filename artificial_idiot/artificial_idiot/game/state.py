from copy import copy
from artificial_idiot.util.misc import print_board

# I have to factor this out from python for some strange static variable
# scoping problem
CODE_MAP = {"red": 0, "green": 1, "blue": 2}
REV_CODE_MAP = {
    value: key for key, value in CODE_MAP.items()
}


class State:
    """
    State class stores current node state, the state is represented
    as two dictionaries of forward position mapping and backward position
    mapping.
    piece_code -> [(x1, y1), (x2, y2), (x3, y3)...]
    (x1, y1) -> piece_code
    """
    code_map = CODE_MAP
    rev_code_map = REV_CODE_MAP
    print_map = {"red": "🔴", "green": "✅", "blue": "🔵"}

    # cycle the players:
    #    player:: red:   red -> red,   green -> green, blue -> blue
    #    player:: green: red -> blue,  green -> red,   blue -> green
    #    player:: blue:  red -> green, green -> blue,  blue -> red
    perspective_mapping = {
        fr:
            {
                to: REV_CODE_MAP[(to_code - fr_code) % 3]
                for to, to_code in CODE_MAP .items()
            }
        for fr, fr_code in CODE_MAP.items()
    }

    # TODO make checking fo completed faster/ and more robust
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
            completed = {col: 0 for col in self.code_map}
        self.completed = completed
        self.frozen = None
        self._hash = None

    def occupied(self, pos):
        return pos in self._pos_to_piece

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
        piece_to_pos = {col: [] for col in self.code_map}
        for location, colour in self._pos_to_piece.items():
            piece_to_pos[colour].append(location)
        return piece_to_pos

    @property
    def pos_to_piece(self):
        return copy(self._pos_to_piece)

    @property
    def colour(self):
        return self._colour

    @classmethod
    def next_colour(cls, color):
        """
        :return: The next active colour after current execution
        """
        i = cls.code_map[color] + 1
        # went over, start again
        return cls.rev_code_map[i % 3]

    @classmethod
    def rotate_pos(cls, fr_color, to_color, pos):
        if pos is None:
            return None
        # grab distance between color
        f = cls.code_map[fr_color]
        t = cls.code_map[to_color]
        if t < f:
            dist = t + 3 - f
        else:
            dist = t - f
        for i in range(dist):
            x, z = pos
            y = -(x + z)
            pos = (y, x)
        return pos

    def red_perspective(self, colour):
        """
        change player to red
        always return a new state
        :return: a state where current player is red
        """
        mapping = self.perspective_mapping[colour]
        mapped_colour = mapping[self.colour]

        if colour == "red":
            pos_to_piece = self.pos_to_piece
            completed = copy(self.completed)
            return State(pos_to_piece, mapped_colour, completed)
        pos_to_piece = {
            self.rotate_pos(fr, mapping[fr], pos): mapping[fr]
            for pos, fr in self._pos_to_piece.items()
        }
        completed = {
            mapping[fr]: num for fr, num in self.completed.items()
        }
        return State(pos_to_piece, mapped_colour, completed)

    def original_perspective(self, colour):
        """
        Change from rotated perspective back to original mapping
        :param colour: The colour that's being rotated
        :return: The reverse rotated map
        """
        return self.red_perspective(self.perspective_mapping[colour]["red"])

    def __repr__(self, **kwargs):
        # need a copy here
        pos_to_piece = self.pos_to_piece
        # Make the name shorter so display normally
        # pos_to_piece = {key: value[:3] for key, value
        #                 in pos_to_piece.items()}
        pos_to_piece = {key: self.print_map[value] for key, value
                        in pos_to_piece.items()}
        msg = f"Colour: {self._colour}"
        if "message" in kwargs:
            kwargs["message"] += msg
        else:
            kwargs["message"] = msg
        return f"Colour: {self.colour}\n" + \
               print_board(pos_to_piece, **kwargs, printed=False) + \
            "\n# Completed: " + str(self.completed)

    def __hash__(self):
        if self.frozen is None:
            self.frozen = frozenset(self._pos_to_piece.items())
            self._hash = hash(self.frozen)
        return self._hash

    def __eq__(self, other):
        # First compare hash, if hash is successful, compare id
        # last compare the content for a fast comparison
        # (This is based on experimental result of comparison speed)
        return (hash(self) == hash(other) and
                self.frozen == other.frozen and
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


if __name__ == '__main__':
    def rotate_test():
        test = State({(1, -1): "red", (0, 0): "green", (0, 1): "blue"}, "blue", {"blue": 1})
        check = State({(-1, 0): "red", (0, 1): "green", (0, 0): "blue"}, "red", {"red": 1})
        red_perspective = test.red_perspective("blue")
        blue_perspective = red_perspective.original_perspective("blue")
        print(test)
        print(check)
        print(red_perspective)
        print(blue_perspective)

        assert (check == red_perspective)
        assert (test == blue_perspective)


    def color_test():
        assert (State.next_colour("red") == "green")
        assert (State.next_colour("blue") == "red")
        assert (State.next_colour("green") == "blue")


    def rotate_action_test():
        assert(State.rotate_pos("green", "blue", (0, -3)) == (3,0))
        assert(State.rotate_pos("green", "red", (0, -3)) == (-3, 3))

    # UCT next color
    color_test()
    # UCT rotate state
    rotate_test()
    # rotate action
    rotate_action_test()
