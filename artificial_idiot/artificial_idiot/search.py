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
        # try all actions
        for a in game.actions(state):
            v, _ = self.search(game, game.result(state, a), depth=depth+1)
            # found a better utility
            if v[player] > v_max[player]:
                v_max = v
                a_best = a
        return v_max, a_best


class RandomMove(Search):

    def __init__(self, seed):
        self.seed = seed
        random.seed(seed)

    def search(self, game, state, **kwargs):
        actions = [a for a in game.actions(game.initial_state)]
        i = random.randrange(len(actions))
        return actions[i]


class UCBSearch(Search):
    def __init__(self, c=2, node_type=BasicUCTNode):
        self.c = c
        self.node_type = node_type
        self.node_type.set_c(c)

    def tree_policy(self, game, initial_node):
        """
        Fully expand path of the tree down to the leave node.
        :param game: The game the path is in
        :param initial_node: The node to start search with
        :return: The terminal node of such path
        """
        node = initial_node
        while not game.terminal_node(node):
            if not node.isFullyExpanded():
                return game.expand(node)
            else:
                node = node.bestChild(node)

        return node

    def search(self, game, state, c=2, node_type=BasicUCTNode):
        node = node_type(game.initial_state)
        node_type.set_c(c)
        while not game.terminal_node(node):
            if not node.isFullyExpanded():
                return game.expand(node)
            else:
                node = node.bestChild(node)

        return node

if __name__ == '__main__':
    from artificial_idiot.evaluator import *
    from artificial_idiot.cutoff import DepthLimitCutoff
    from artificial_idiot.game import Game
    from artificial_idiot.state import State
    from artificial_idiot.util.json_parser import JsonParser
    import json

    def test_max_n():
        f = open("../tests/simple.json")
        pos_dict, colour, completed = JsonParser(json.load(f)).parse()
        game = Game(colour, State(pos_dict, colour, completed))
        evaluator = MyEvaluator()
        cutoff = DepthLimitCutoff(max_depth=2)
        search = MaxN(evaluator, cutoff, n_player=3)
        print(search.search(game, game.initial_state))

    test_max_n()

