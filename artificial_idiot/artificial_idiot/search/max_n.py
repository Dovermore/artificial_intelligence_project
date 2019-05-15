from math import inf

from artificial_idiot.search.search import Search


class MaxN(Search):
    """
    Generic Max N algorithm
    """

    def __init__(self, evaluate, cut_off_test, n_player):
        """
        Initialize A Max N search algorithm
        :param evaluate: func, that returns the utility of a state
        :param cut_off_test: func, tests if to stop evaluating this state
        :param n_player: int, number of players
        """
        self._eval = evaluate
        self._n = n_player
        self._cut_off_test = cut_off_test

    def _evaluate(self, state):
        return self._eval(state)

    def _recursive_max_search(self, game, state, depth):
        player = state.colour
        # cut off test
        if self._cut_off_test(state, depth=depth) or game.terminal_state(state):
            return self._evaluate(state), None
        # initialize utility to be the worst possible
        v_max = None
        a_best = None
        for a in game.actions(state):
            result_state = game.result(state, a)
            v, _ = self._recursive_max_search(game, result_state, depth=depth+1)
            # print(result_state)
            # print(f'{v(player):.2f} value for {player} for ^^^ state \nResult {v("red"):.2f} for red')
            if v_max is None:
                a_best = a
                v_max = v
            # found a better utility
            if v(player) > v_max(player):
                v_max = v
                a_best = a
        return v_max, a_best

    def search(self, game, state, depth=1, **kwargs):
        # no exploration needed if only there is no choice to be made
        actions = game.actions(state)
        if len(actions) == 1:
            return actions[0]
        # find best action
        _, a = self._recursive_max_search(game, state, depth)
        return a

