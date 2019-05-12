"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Chuanyuan Liu, Zhuoqun Huang
"""

import abc
import random
from math import inf
from artificial_idiot.node import BasicUCTNode


class Search(abc.ABC):
    """
    Generic search algorithm
    """
    @abc.abstractmethod
    def search(self, game, state, **kwargs):
        """
        Return the best action
        :param game: a class that describes the game
        :param state: state of the board
        :return: an action
        """
        raise NotImplementedError


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

    def search(self, game, state, depth=1, **kwargs):
        # cut off test
        if self._cut_off_test(state, depth=depth):
            return self._evaluate(state), None
        player = state.code_map[state.colour]
        # initialize utility to be the worst possible
        v_max = [-inf] * self._n
        a_best = None
        actions = list(game.actions(state))
        # no exploration needed if only there is choice to be made
        if len(actions) < 2: return actions[0];
        for a in actions:
            v, _ = self.search(game, game.result(state, a), depth=depth+1)
            # found a better utility
            if v[player] > v_max[player]:
                v_max = v
                a_best = a
        return v_max, a_best


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

class RandomMove(Search):

    def __init__(self, seed):
        self.seed = seed
        random.seed(seed)

    def search(self, game, state, **kwargs):
        actions = [a for a in game.actions(game.initial_state)]
        i = random.randrange(len(actions))
        return actions[i]


class UCTSearch(Search):
    def __init__(self, c=2, node_type=BasicUCTNode):
        self.c = c
        self.node_type = node_type
        self.node_type.set_c(c)
        self.initial_node = None

    def select_expand(self, game):
        """
        Fully expand path of the tree down to the leave node.
        :param game: The game the path is in
        :return: The terminal node of such path
        """
        parent = None
        node = game.initial_state

        # Fully expanded and not leaf
        while node.unexpanded_children is not None and \
                len(node.unexpanded_children) == 0 and node is not None:
            parent = node
            node = node.tree_policy(game)
        # Found a leaf of the whole tree
        if node is None:
            return parent
        # Half way through the tree, half-way through the tree, now *expand*
        else:
            parent = node
            node = node.tree_policy(game)
            return node if node is not None else parent

    def simulation(self, game, node):
        while not game.terminal_state(node.state):
            node = node.default_policy(game)
        return node

    def back_prop(self, game, leaf, result, *args, **kwargs):
        node = leaf
        # Back prop till the root node (but not include that)
        while node is not None:
            node.update(result, *args, **kwargs)
            # Some how got to a node without parent but is not root
            node = node.parent

    def search(self, game, state, iteration=100, max_depth=-1,
               max_time=-1, training=True):
        # TODO add depth, time and cutoff
        # TODO fix this iteration
        while iteration > 0:
            # Get a leaf
            expanded = self.select_expand(game)
            print("==================== before ====================")
            expanded.show_path()
            leaf = self.simulation(game, expanded)
            result = game.evaluator(leaf.state, "red")
            print(f"---------- {result} ----------")
            self.back_prop(game, expanded, result=game.evaluator(
                leaf.state, "red"))
            iteration -= 1
            print("-------------------- after --------------------")
            expanded.show_path()
        return game.initial_state.tree_policy(game).action


if __name__ == '__main__':
    from artificial_idiot.evaluator import AbstractWeightEvaluator
    from artificial_idiot.cutoff import DepthLimitCutoff
    from artificial_idiot.game import Game
    from artificial_idiot.state import State
    from artificial_idiot.util.json_parser import JsonParser
    import json

    def test_max_n():
        f = open("../tests/simple.json")
        pos_dict, colour, completed = JsonParser(json.load(f)).parse()
        evaluator = AbstractWeightEvaluator()
        game = Game(colour, State(pos_dict, colour, completed), evaluator)
        cutoff = DepthLimitCutoff(max_depth=2)
        search = MaxN(evaluator, cutoff, n_player=3)
        print(search.search(game, game.initial_state))

    def test_only_one_possible_move():
        f = open("../tests/only_one_move.json")
        evaluator = AbstractWeightEvaluator()
        pos_dict, colour, completed = JsonParser(json.load(f)).parse()
        game = Game(colour, State(pos_dict, colour, completed), evaluator)
        cutoff = DepthLimitCutoff(max_depth=2)
        search = MaxN(evaluator, cutoff, n_player=3)
        print(search.search(game, game.initial_state))

    test_max_n()
    test_only_one_possible_move()

