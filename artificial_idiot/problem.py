from util.misc import is_in
from util.class_property import classproperty
from state import State
import abc
from copy import copy


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
        "red": ((3, -3), (3, -2), (3, -1), (3, 0)),
        "green": ((-3, 3), (-2, 3), (-1, 3), (0, 3)),
        "blue": ((0, -3), (-1, -2), (-2, -1), (-3, 0))
    }

    # possible moves.
    _move = (
        (+1, -1), (0, -1), (-1, 0),
        (-1, +1), (0, +1), (+1, 0)
    )

    def __init__(self, initial, colour):
        """
        initial state is supplied by the problem
        goal state is initial state without any agent's pieces
        """
        super().__init__(initial)
        # remove all agent's pieces
        self.goal = initial.copy()
        self.goal.delete_colour(colour)

    @classmethod
    def actions(cls, state):
        """Yield all possible moves in a given state

        Exit means moving to position (infinity, infinity)
        Actions are eveluated in this order: Exit -> Move -> Jump
        If no movement is possible then returns null

        Arguments:
            state (State) : current state of the board
        
        Yields:
            action (tuple) -- encoded as ((from position), (to position))
        """
        # for each piece try all possible moves
        for q, r in state.forward_dict[state.colour]:
            # exit
            if (q, r) in cls._exit_positions:
                yield ((q, r), None)

            for move in cls._move:
                i, j = move
                move_pos = (q+i, r+j)
                jump_pos = (q+i*2, r+j*2)
                # If that direction is possible to move
                if not state.inboard(move_pos):
                    continue
                # Move
                elif state.occupied(move_pos):
                    yield ((q, r), move_pos)
                # Jump
                elif state.occupied(jump_pos):
                    yield ((q, r), jump_pos)

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
        # If None then don't do anything
        if to is not None:
            forward_dict[colour].add(to)

        # Construct the new state
        return State(forward_dict, next_colour)

    def value(self, state):
        raise NotImplementedError

    @classproperty
    def exit_positions(cls):
        return copy(cls._exit_positions)

    @classmethod
    def h(cls, node):
        # state = node.state
        return 0


if __name__ == "__main__":
    # test for static problem class
    pass
