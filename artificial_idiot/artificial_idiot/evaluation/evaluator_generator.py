import abc
import numpy as np
from math import log
from functools import lru_cache


exit_positions = {
    "red": ((3, -3), (3, -2), (3, -1), (3, 0)),
    "green": ((-3, 3), (-2, 3), (-1, 3), (0, 3)),
    "blue": ((0, -3), (-1, -2), (-2, -1), (-3, 0))
}
exit_corner = {
    "red": ((3, -3), (3, 0)),
    "green": ((-3, 3), (0, 3)),
    "blue": ((0, -3), (-3, 0))
}

NEEDED = 4


@lru_cache(maxsize=10)
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


@lru_cache(maxsize=10)
def shortest_exit_distance(piece, state, player):
    pieces = state.piece_to_pos[player]
    _exit_positions = [pos for pos in exit_positions[player]
                       if ((not state.occupied(pos)) or (pos in pieces))]
    # return 1000000 all exit position is blocked
    distance = 1000000
    for exit_pos in _exit_positions:
        distance = min(grid_dist(piece, exit_pos), distance)
    return distance


@lru_cache(maxsize=10)
def exit_distance(piece, state, player):
    if player == 'red':
        return 3 - piece[0]
    if player == 'green':
        return 3 - piece[1]
    if player == 'blue':
        return 3 + piece[0]


@lru_cache(maxsize=10)
def exit_corner_distance(piece, state, players):
    """
    Compute the distance from a piece to corner of some players.
    """
    dists = []
    occupied_dists = []
    pos_to_piece = state.pos_to_piece
    # For all players you want to block
    for player in players:
        for corner in exit_corner[player]:
            # If not occupied, or occupied by others try go for it
            if corner not in state.pos_to_piece or \
                    pos_to_piece[corner] != pos_to_piece[corner] \
                    or corner == piece:
                dists.append(grid_dist(corner, piece))
            # Else
            else:
                occupied_dists.append(grid_dist(corner, piece))
        if dists:
            return min(dists)
    if dists:
        return min(dists)
    # Didn't find any place
    else:
        return min(occupied_dists)


@lru_cache(maxsize=10)
def sum_exit_distance(state, player):
    pieces = state.piece_to_pos[player]
    distances = {}
    for piece in pieces:
        distances[piece] = exit_distance(piece, state, player)
    return sum(distances.values())


@lru_cache(maxsize=10)
def num_exited_piece(state, player):
    completed = state.completed
    n_exited_pieces = completed[player]
    return n_exited_pieces


@lru_cache(maxsize=10)
def num_board_piece(state, player):
    piece_to_pos = state.piece_to_pos
    n_pieces = len(piece_to_pos[player])
    return n_pieces


@lru_cache(maxsize=10)
def sum_number_pieces(state, player):
    return num_board_piece(state, player) + num_exited_piece(state, player)


@lru_cache(maxsize=10)
def sum_completed_piece(state, player):
    n_complete = state.completed[player]
    return n_complete


@lru_cache(maxsize=10)
def other_player_piece_worth(state, player):
    numbers = []
    for other_player in state.code_map:
        if other_player == player:
            continue
        numbers.append(sum_number_pieces(state, other_player))
    difference = max(numbers) - min(numbers)
    return sum(numbers) + difference


@lru_cache(maxsize=10)
def leading_opponent_and_neg_distance(state, player):
    numbers = {}
    for other_player in state.code_map:
        if other_player == player:
            continue
        numbers[player] = \
            modified_negative_sum_distance(state, other_player)
    return min(numbers.items(), key=lambda x: x[1])


@lru_cache(maxsize=10)
def leading_opponent_negative_distance(state, player):
    opponent, opponent_neg_dist = \
        leading_opponent_and_neg_distance(state, player)
    return opponent_neg_dist


@lru_cache(maxsize=10)
def modified_negative_sum_distance(state, player):
    pieces = state.piece_to_pos[player]
    # print(len(pieces), pieces, player, state.piece_to_pos)
    n_completed = state.completed[player]
    if n_completed >= 4:
        return 10000000
    distances = {}
    for piece in pieces:
        distances[piece] = exit_distance(piece, state, player)
    if len(pieces) + n_completed < NEEDED:
        # try to compete for more pieces
        return -28
    sorted_distance = sorted(distances.values())
    # Only consider the top 4 when have more
    return -sum(sorted_distance[:NEEDED - n_completed])


@lru_cache(maxsize=10)
def excess_piece_negative_sum_distance(state, player, offset=7):
    pieces = state.piece_to_pos[player]
    n_completed = state.completed[player]
    # No spare pieces
    if NEEDED >= len(pieces) + n_completed:
        return 0
    first_opponent, opponent_neg_dist = \
        leading_opponent_and_neg_distance(state, player)
    distances = {}
    for piece in pieces:
        distances[piece] = exit_distance(piece, state, player)
    sorted_distance = sorted(distances.items(), key=lambda x: x[1])
    excess_pieces = sorted_distance[NEEDED-n_completed:]
    distances = {}
    for piece, _ in excess_pieces:
        distances[piece] = exit_corner_distance(piece, state,
                                                (first_opponent,))
    # Only consider the top 4 when have more
    return -sum(distances.values()) + offset * len(distances)


@lru_cache(maxsize=10)
def regular_neg_corner_distance(state, player):
    pieces = state.piece_to_pos[player]
    opponents = tuple(i for i in state.code_map if i != player)
    distances = {}
    for piece in pieces:
        distances[piece] = exit_corner_distance(piece, state, opponents)
    return -sum(distances.values())


@lru_cache(maxsize=10)
def sum_number_needed_pieces(state, player):
    return min(num_board_piece(state, player) +
               num_exited_piece(state, player), 4)


@lru_cache(maxsize=10)
def excess_pieces(state, player):
    return sum_number_pieces(state, player) - 4


@lru_cache(maxsize=10)
def utility_completed_piece(state, player):
    # if there not enough pieces to exit to win
    # then player is punished if choose to exit
    exited = num_exited_piece(state, player)
    n = exited + num_board_piece(state, player)
    if n < NEEDED:
        return -exited
    else:
        return exited


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
        # print(f"evaluating for {player}")
        if player in self._value:
            return self._value[player]
        X = np.array([fn(self._state, player) if self._weights[i] != 0 else
                      0 for i, fn in enumerate(self._funcs)])
        X = X.T
        # print(X)
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
    def negative_distance(state, player):
        return -sum_exit_distance(state, player)

    @staticmethod
    def utility_exit_pieces(state, player):
        exited = num_exited_piece(state, player)
        if sum_number_pieces(state, player) < 4:
            return -exited
        return exited

    # weights in the format of [pieces, exited, distance]
    def __init__(self, weights,  *args, **kwargs):
        self._weights = weights

        func = [self.utility_exit_pieces, sum_number_pieces,
                self.negative_distance]
        self._eval = FunctionalEvaluatorGenerator(self._weights, func)
        super().__init__(*args, **kwargs)

    # returns an evaluator for that state
    def __call__(self, state, *args, **kwargs):
        return self._eval(state)


class AdvanceEG(EvaluatorGenerator):
    """
    * weights are defined beforehand
    An evaluator that only considers
    1. Number of your pieces
    2. Distance to exit
    3. Number of exited pieces
    """
    @staticmethod
    def utilty_distance_piece(piece, state, player):
        MAX_DISTANCE = 6
        distance = exit_distance(piece, state, player)
        if distance > MAX_DISTANCE:
            return 0
        s = MAX_DISTANCE - distance
        return -1 / 24 * s ** 2 + 4 * s

    @staticmethod
    def utility_distance(state, player):
        pieces = state.piece_to_pos[player]
        return sum([AdvanceEG.utilty_distance_piece(piece, state, player) for piece in pieces])

    @staticmethod
    def utility_completed_piece(state, player):
        # return 0 if the player don't enough pieces
        NEEDED = 4
        exited = num_exited_piece(state, player)
        n = exited + num_board_piece(state, player)
        if n < NEEDED:
            return 0
        else:
            return exited

    @staticmethod
    def utility_pieces(state, player):
        n = num_exited_piece(state, player) + num_board_piece(state, player)
        # log(0) is close to -inf
        if n == 0:
            return -1000000
        return 10*log(n)+3*n

    # weights in the format of [utility_distance, utility_pieces]
    def __init__(self, weights,  *args, **kwargs):
        self._weights = weights

        func = [self.utility_pieces, self.utility_completed_piece,
                self.utility_distance]
        self._eval = FunctionalEvaluatorGenerator(self._weights, func)
        super().__init__(*args, **kwargs)

    # returns an evaluator for that state
    def __call__(self, state, *args, **kwargs):
        return self._eval(state)


class MinimaxEvaluator(EvaluatorGenerator):
    """
    * weights are defined beforehand
    An evaluator that considers
    1. (max) number of player piece
    2. (max neg) leading player's distance from winning
    3. (max) distance of excess piece to opponent exit,
        try to block leading player from exiting
    4. (max neg) net worth of other players' pieces
    5. (max) negative sum distance to goal
    6. (max) number of completed piece
    """

    def __init__(self, weights,  *args, **kwargs):
        func = [
            sum_number_needed_pieces,
            leading_opponent_negative_distance,
            excess_piece_negative_sum_distance,
            other_player_piece_worth,
            modified_negative_sum_distance,
            sum_completed_piece,
            excess_pieces,
            regular_neg_corner_distance
        ]
        # print('the weights are:', weights)
        assert len(weights) != func
        self._weights = weights
        self._eval = FunctionalEvaluatorGenerator(self._weights, func)
        super().__init__(*args, **kwargs)

    # returns an evaluator for that state
    def __call__(self, state, *args, **kwargs):
        return self._eval(state)

