from util.misc import is_in
from util import class_property
from state import State
import abc
import copy
from math import inf


class Problem(abc.ABC):
    """
    The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions.
    """

    def __init__(self, initial, goal=None):
        """
        The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments.
        """
        self.initial = initial
        self.goal = goal

    @abc.abstractmethod
    def actions(self, state):
        """
        Return the actions that can be executed in the given
        state. The result would typically be a list, but if there are
        many actions, consider yielding them one at a time in an
        iterator, rather than building them all at once.
        """
        pass

    @abc.abstractmethod
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        pass

    def goal_test(self, state):
        """
        Return True if the state is a goal. The default method compares the
        state to self.goal or checks for state in self.goal if it is a
        list, as specified in the constructor. Override this method if
        checking against a single self.goal is not enough.
        """
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        else:
            return state == self.goal

    def path_cost(self, c, state1, action, state2):
        """
        Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path.
        """
        return c + 1

    @abc.abstractmethod
    def value(self, state):
        """
        For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value.
        """
        pass


class StaticProblem(Problem):
    """
    Static Search problem for project part A
    """
    _exit_positions = {
        0: ((3, -3), (3, -2), (3, -1), (3, 0)),
        1: ((-3, 3), (-2, 3), (-1, 3), (0, 3)),
        2: ((0, -3), (-1, -2), (-2, -1), (-3, 0))
    }

    def __init__(self, initial, colour):
        """
        initial state is supplied by the problem
        goal state is initial state without any agent's pieces
        """
        super().__init__(initial)
        # remove all agent's pieces
        self.goal = initial.copy()
        self.goal.delete_colour(colour)

        # Keys: possible moves.   Values: State of current move
        # 0: Not determined, 1: Can Move, 2: Can jump, 3: no action here
        self._move = {
            (+1, -1): 0, (0, -1): 0, (-1, 0): 0,
            (-1, +1): 0, (0, +1): 0, (+1, 0): 0
        }

    def actions(self, state):
        """
        Yield all possible moves in a given state
        If no movement is possible then returns null
        Movement is encoding using (current pos, next pos)
        0. Exit (current pos, (infinity, infinity))
        1. Move 
        2. Jump 
        """
        # for each piece try all possible moves
        for q, r in state.forward_dict[state.colour]:
            # exit
            if (q, r) in self.exit_positions:
                yield ((q, r), (inf, inf))

            for i, j in self._move:
                next_pos = (q+i, r+j)
                # FIXME this part is definitely bugged, You need to check if outside board as well.
                # Move
                if next_pos not in state.backward_dict.keys():
                    yield ((q, r), next_pos)
                # Jump
                next_pos = (q+i*2, r+j*2)
                if next_pos not in state.backward_dict.keys():
                    yield ((q, r), next_pos)

    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        fr, to = action
        forward_dict = state.forward_dict
        colour = state.colour
        next_colour = state.next_colour()

        # update dictionary
        forward_dict[colour].remove(fr)
        forward_dict[colour].add(to)

        # Construct the new state
        return State(forward_dict, next_colour)

    def value(self, state):
        raise NotImplementedError

    @class_property
    def exit_positions(cls):
        return copy.copy(cls._exit_positions)


if __name__ == "__main__":
    # test for static problem class
    pass
