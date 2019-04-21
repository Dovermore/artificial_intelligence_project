"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Chuanyuan Liu, Zhuoqun Huang
"""

import abc



class Search(abc.ABC):
    """
    Generic search algorithm
    """
    @abc.abstractmethod
    def search(self, s, player):
        """
        Return the best action
        :param s: state of the board
        :param player: the encoding of the player
        :return: an action
        """
        raise NotImplementedError


class MaxnAbstract(Search):
    """
    Generic Maxn algorithm
    """
    _eval = None

    def __init__(self, evaluate):
        self._eval = evaluate

    @abc.abstractmethod
    def cut_off_test(self, state):
        """
        Reduce the depth of the search
        :param state:
        :return: boolean, whether we should stop searching
        """
        raise NotImplementedError

    def _evaluate(self, state):
        return self._eval(state)

    def search(self, s, player):
        if self.cut_off_test(s):
            return self._evaluate(s), Action(Action.actions)



class MaxnTest(MaxnAbstract):
    pass


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    test = MaxnTest()
