"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Chuanyuan Liu, Zhuoqun Huang
"""

import abc
import random
from math import inf


class Search(abc.ABC):
    """
    Generic search algorithm
    """
    @abc.abstractmethod
    def search(self, game, **kwargs):
        """
        Return the best action
        :param game: a class that describes the game
        :return: an action
        """
        raise NotImplementedError

class MaxnAbstract(Search):
    """
    Generic Maxn algorithm
    """

    def __init__(self, evaluate, n):
        """
        Initialize A Maxn search algorithm
        :param evaluate: func, returns the utility of a state
        :param n: int, number of players
        """
        self._eval = evaluate
        self._n = n

    @abc.abstractmethod
    def cut_off_test(self, state, **kwargs):
        """
        Reduce the depth of the search
        :param state:
        :return: boolean, whether we should stop searching
        """
        pass

    def _evaluate(self, state, depth):
        """
        calculate the utiltiy of a given state
        :param state:
        :return: a utility vector
        """
        v = []
        for i in self._n:
            v.append(eval(state))
        return self._eval(state)

    def search(self, game, **kwargs):
        if self.cut_off_test(game.state):
            return (self._evaluate(game.state, depth=None), None)
        player = game.state.codemap[game.state.color]
        # initialize utility to be the worst possible
        v_max = [-inf] * self._n
        a_best = None
        # try all actions
        for a in game.actions(game.state):
            v, _ = self.search(game)
            # found a better utility
            if v[player] > v_max[player]:
                v_max = v
                a_best = a
        return (v_max, a_best)


class MaxTest(MaxnAbstract):

    def cut_off_test(self, state, depth=None, **kwargs):
        if depth > self._n:
            return False
        return True


class RandomMove(Search):

    def __init__(self, seed):
        self.seed = seed
        random.seed(seed)

    def search(self, game, **kwargs):
        actions = [a for a in game.actions(game.state)]
        print(actions)
        i = random.randrange(len(actions))
        return actions[i]
