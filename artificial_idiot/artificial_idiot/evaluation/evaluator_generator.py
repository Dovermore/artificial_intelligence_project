import abc
import numpy as np
from math import log

_exit_positions = {
    "red": ((3, -3), (3, -2), (3, -1), (3, 0)),
    "green": ((-3, 3), (-2, 3), (-1, 3), (0, 3)),
    "blue": ((0, -3), (-1, -2), (-2, -1), (-3, 0))
}


def grid_dist(pos1, pos2):
    """
    Get the grid distance between two different grid locations
    :param pos1: first position (tuple)
    :param pos2: second position (tuple)
    :return: The `manhattan` distance between those two positions
    """
    x1, y1 = pos1
    x2, y2 = pos2

    dy = y2 - y1
    dx = x2 - x1

    # If different sign, take the max of difference in position
    if dy * dx < 0:
        return max([abs(dy), abs(dx)])
    # Same sign or zero just take sum
    else:
        return abs(dy + dx)


def sum_shortest_exit_distance(state, player):
    pieces = state.piece_to_pos[player]
    exit_positions = [pos for pos in _exit_positions[player] if ((not state.occupied(pos)) or (pos in pieces))]
    distances = {}
    for piece in pieces:
        distances[piece] = 1000000
        for exit_pos in exit_positions:
            distances[piece] = min(grid_dist(piece, exit_pos), distances[piece])
    if len(distances) == 0:
        return 0
    return sum(distances.values())


def num_exited_piece(state, player):
    completed = state.completed
    n_exited_pieces = completed[player]
    return n_exited_pieces


def num_board_piece(state, player):
    piece_to_pos = state.piece_to_pos
    n_pieces = len(piece_to_pos[player])
    return n_pieces


class EvaluatorGenerator(abc.ABC):
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


class DummyEvaluator(EvaluatorGenerator):
    """
    An evaluator that only consider amount of exited pieces
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def __call__(self, state, player, *args, **kwargs):
        return 0


class WinLossEvaluator(EvaluatorGenerator):
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


class FunctionalEvaluator:

    def __init__(self, state, weights, funcs):
        self._state = state
        self._weights = weights
        self._funcs = funcs
        self._value = dict()

    def __call__(self, player):
        if player in self._value:
            return self._value[player]
        X = np.array([fn(self._state, player) for fn in self._funcs])
        X = X.T
        value = np.dot(X, self._weights)
        self._value[player] = value
        return value


class FunctionalEvaluatorGenerator(EvaluatorGenerator):
    """
    Evaluate a state based on set of features computed by functions and
    return single scalar indicating the value of the state.

    The value is computed by feeding an arbitrary function to the state
    """
    def __init__(self, weights, functions, *args, **kwargs):
        self._functions = functions
        self._weights = weights
        super().__init__(*args, **kwargs)

    def __call__(self, state, *args, **kwargs):
        return FunctionalEvaluator(state, self._weights, self._functions)


class NaiveEvaluatorGenerator(EvaluatorGenerator):
    """
    * weights are defined beforehand
    An evaluator that only considers
    1. Number of your pieces on the board
    2. Number of your exited pieces
    3. Reciprocal of the sum of grid distance of each nodes to nearest exit
    """

    @staticmethod
    def reciprocal_distance(state, player):
        value = sum_shortest_exit_distance(state, player)
        if value == 0:
            value = 0.5
        return 1/value

    @staticmethod
    def negative_distance(state, player):
        return -sum_shortest_exit_distance(state, player)

    # weights in the format of [pieces, exited, distance]
    def __init__(self, weights,  *args, **kwargs):
        self._weights = weights

        func = [num_board_piece, num_exited_piece, self.negative_distance]
        self._eval = FunctionalEvaluatorGenerator(self._weights, func)
        super().__init__(*args, **kwargs)

    # returns an evaluator for that state
    def __call__(self, state, *args, **kwargs):
        return self._eval(state)


class SimpleEvaluatorGenerator(EvaluatorGenerator):
    """
    * weights are defined beforehand
    An evaluator that only considers
    1. Number of your pieces
    2. Distance to exit
    """

    @staticmethod
    def utility_distance(state, player):
        MAX_DISTANCE = 24
        dist = sum_shortest_exit_distance(state, player)
        # distance has no utility if exit is blocked
        if dist > MAX_DISTANCE:
            return 0
        # exited pieces have value -1 each
        dist -= num_exited_piece(state, player)
        # mirror and shift s to maximize value, it is max N after all
        s = -dist + MAX_DISTANCE
        # further discussed in report
        if 0 <= s <= MAX_DISTANCE:
            return -1/MAX_DISTANCE*s**2+4*s
        elif MAX_DISTANCE < s <= 28:
            return 2*s**2-94*s+1176
        else:
            raise ValueError("distance is not in range of 0 <= s <= 28")

    @staticmethod
    def utility_pieces(state, player):
        n = num_exited_piece(state, player) + num_board_piece(state, player)
        return 10*log(n)+3*n

    # weights in the format of [utility_distance, utility_pieces]
    def __init__(self, weights=(1, 1),  *args, **kwargs):
        self._weights = weights

        func = [self.utility_distance, self.utility_pieces]
        self._eval = FunctionalEvaluatorGenerator(self._weights, func)
        super().__init__(*args, **kwargs)

    # returns an evaluator for that state
    def __call__(self, state, *args, **kwargs):
        return self._eval(state)
