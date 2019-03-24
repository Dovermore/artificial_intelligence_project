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

    _code_map = {"red": 0, "green": 1, "blue": 2, "blocks":3}

    @classproperty
    def code_map(cls):
        return copy(cls._code_map)

    @code_map.setter
    def code_map(cls, code_map):
        cls._code_map = code_map
    pass


if __name__ == "__main__":
    print(State.code_map)
    State.code_map = {}
    print(State.code_map)
