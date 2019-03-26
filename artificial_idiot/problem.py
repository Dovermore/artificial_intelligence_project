from artificial_idiot.util.misc import is_in
from artificial_idiot.state import State
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

    @class_property
    def exit_positions(cls):
        return copy.copy(cls._exit_positions)

    def __init__(self, initial, color):
        """Initalize the problem
        
        Determine goal state which is inital state without any agent's piece

        Arguments:
            initial (State): supplied by the problem
            color (int) : color of the agent
        """

        # remove all agent's pieces
        goal = initial.copy()
        goal.delete_color(color)
        super.__init__(initial, goal)

    def validate(self, next_pos, state):
        """Validates if this position on board can be moved to

        Arguments:
            next_pos (tuple) : (r, q) representation of the position
            state (State) : current board state

        Returns:
            Boolean -- if move is possible or not
        """
        r, q = next_pos
        # check if 
        # check if moving out of bound
        if r < -3 or r > 3:
            return False
        if q < -3 or q > 3:
            return False
        if abs(r+q) > 3:
            return False
        # check if position is unoccupied
        return next_pos not in state.backward_dict

    def actions(self, state):
        """Yield all possible moves in a given state

        Exit means moving to position (infinity, infinity)
        Actions are eveluated in this order: Exit -> Move -> Jump
        If no movement is possible then returns null

        Arguments:
            state (State) : current state of the board
        
        Yields:
            action (tuple) -- encoded as ((from position), (to position))
        """

        move = [(+1, -1), (0, -1), (-1, 0), (-1, +1), (0, +1)]

        # for each piece try all possible moves
        for q, r in state.forward_dict[state.color]:
            # exit
            if (q, r) in self._exit_positions:
                yield ((q, r), (inf, inf))
            # move
            for i, j in move:
                next_pos = (q+i, r+j)
                if self.validate(next_pos, state):
                    yield ((q, r), next_pos)
            # jump
            for i, j in move:
                next_pos = (q+i*2, r+j*2)
                if self.validate(next_pos, state):
                    yield ((q, r), next_pos)

        def result(self, state, action):
            """Enact the action on to current state
            
            Arguments:
                state (State) : current state
                action (tuple) : defined by self.actions(State) method
            
            Returns:
                State -- state that results from executing the given action
            """

            state = state.copy()
            fr, to = action
            color = state.color
            # move 
            state.forward_dict[color].remove(fr)
            state.forward_dict[color].add(to)
            del state.backward_dict[fr]
            state.backward_dict[fr] = color
            return state



if __name__ == "__main__":
    # test for static problme class
    pass
