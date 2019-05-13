import abc
import numpy as np

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
    # the distance is 'infinite' if all exit positions are blocked
    exit_positions = [pos for pos in _exit_positions[player] if not state.occupied(pos)]
    distances = {}
    for piece in state.piece_to_pos[player]:
        distances[piece] = 100000
        for exit_pos in exit_positions:
            distances[piece] = min(grid_dist(piece, exit_pos), distances[piece])
    return sum(distances.values())


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


class NaiveEvaluator(Evaluator):
    """
    An evaluator that only considers
    -- weights are defined beforehand
    1. Number of your pieces on the board
    2. Number of your exited pieces
    3. Reciprocal of the sum of grid distance of each nodes to nearest exit
    """

    # weights for pieces, exited, distance
    def __init__(self, weights,  *args, **kwargs):
        self._weights = weights
        super().__init__(*args, **kwargs)

    # returns how good the state is for a given player
    def __call__(self, state, player, *args, **kwargs):
        piece_to_pos = state.piece_to_pos
        completed = state.completed
        n_pieces = len(piece_to_pos[player])
        n_exited_pieces = completed[player]
        sum_distance = sum_shortest_exit_distance(state, player)
        return sum([n_pieces, n_exited_pieces, sum_distance])


class FunctionalEvaluator(Evaluator):
    """
    Evaluate a state based on set of features computed by functions and
    return single scalar indicating the value of the state.

    The value is computed by feeding an arbitrary function to the state

    Assumption:
    functions(state) -> list
    """
    def __init__(self, functions, *args, **kwargs):
        self._functions = functions
        super().__init__(*args, **kwargs)

    def __call__(self, state, player, weights, *args, **kwargs):
        X = np.concatenate([fn(state) for fn in self._functions])
        # reshape to a row vector then perform the matrix multiplication
        return X.reshape(1, -1) @ weights

