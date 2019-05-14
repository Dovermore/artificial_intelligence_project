from math import inf

from artificial_idiot.search.search import Search


class MaxN(Search):
    """
    Generic Maxn algorithm
    """

    def __init__(self, evaluate, cut_off_test, n_player):
        """
        Initialize A Maxn search algorithm
        :param evaluate: func, that returns the utility of a state
        :param cut_off_test: func, tests if to stop evaluating this state
        :param n_player: int, number of players
        """
        self._eval = evaluate
        self._n = n_player
        self._cut_off_test = cut_off_test

    def _evaluate(self, state):
        """
        calculate the utility of a given state
        :param state:
        :return: a utility vector
        """
        v = []
        for index in range(self._n):
            v.append(self._eval(state, state.rev_code_map[index]))
        return v

    def _recursive_max_search(self, game, state, depth):
        # cut off test
        if self._cut_off_test(state, depth=depth) or game.terminal_state(state):
            return self._evaluate(state), None
        player = state.code_map[state.colour]
        # initialize utility to be the worst possible
        v_max = [-inf] * self._n
        a_best = None
        for a in game.actions(state):
            v, _ = self._recursive_max_search(game, game.result(state, a), depth=depth+1)
            # found a better utility
            if v[player] > v_max[player]:
                v_max = v
                a_best = a
        return v_max, a_best

    def search(self, game, state, depth=1, **kwargs):
        # no exploration needed if only there is no choice to be made
        actions = game.actions(state)
        if len(actions) == 1: return actions[0]
        # cut off test
        _, a = self._recursive_max_search(game, state, depth)
        return a


# class MaxNLazy(Search):
#
#     def __init__(self, evaluate, cut_off_test, n_player):
#         self._eval = evaluate
#         self._n = n_player
#         self._cut_off_test = cut_off_test
#
#     # return the utility of that state for that player
#     def _evaluate(self, state, player_color):
#         player_index = state.code_map[player_color]
#         return self._eval(state, player_index)
#
#     def search(self, game, state, depth=1, **kwargs):
#         # cut off test
#         if self._cut_off_test(state, depth=depth):
#             return self._evaluate(state), None
#         player = state.code_map[state.colour]
#         # initialize utility to be the worst possible
#         v_max = [-inf] * self._n
#         a_best = None
#         # try all actions
#         for a in game.actions(state):
#             v, _ = self.search(game, game.result(state, a), depth=depth+1)
#             # found a better utility
#             if v[player] > v_max[player]:
#                 v_max = v
#                 a_best = a
#         return v_max, a_best
