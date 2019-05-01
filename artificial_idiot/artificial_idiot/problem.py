from artificial_idiot.util.misc import is_in
from artificial_idiot.util.class_property import classproperty
from artificial_idiot.state import State
from copy import copy
from collections import defaultdict as dd

import abc
from artificial_idiot.util.queue import PriorityQueueImproved


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

    # @abc.abstractmethod
    # def value(self, state):
    #     """
    #     For optimization problems, each state has a value.  Hill-climbing
    #     and related algorithms try to maximize this value.
    #     """
    #     pass


class BoardProblem(Problem, abc.ABC):
    _exit_positions = {
        "red": ((3, -3), (3, -2), (3, -1), (3, 0)),
        "green": ((-3, 3), (-2, 3), (-1, 3), (0, 3)),
        "blue": ((0, -3), (-1, -2), (-2, -1), (-3, 0))
    }

    # possible moves.
    _move = (
        (+1, -1), (1, 0), (0, 1),
        (-1, +1), (-1, 0), (0, -1)
    )


class Game(BoardProblem):
    """
    Holds all rules for the game
    static variables are defined in BoardProblem class
    """

    def __init__(self, initial, color):
        super().__init__(initial)
        self.color = color

    @classmethod
    def actions(cls, state):
        """
        Yield all possible moves in a given state

        Exit means moving to position (infinity, infinity)
        Actions are eveluated in this order: Exit -> Move -> Jump
        If no movement is possible then returns null

        Arguments:
            state (State) : current state of the board

        Yields:
            action (tuple) -- encoded as ((from position), (to position))
        """
        # for each piece try all possible moves
        # Not using deepcopy here because no need to
        for q, r in state._piece_to_pos[state.colour]:
            exit_ready_pos = cls._exit_positions[state.colour]
            # exit
            if (q, r) in exit_ready_pos:
                yield ((q, r), None, "EXIT")
                return  # End the function if can exit

            for move in cls._move:
                i, j = move
                move_pos = (q + i, r + j)
                jump_pos = (q + i * 2, r + j * 2)
                # If that direction is possible to move
                if not state.inboard(move_pos):
                    continue
                # Move (No need to check inboard)
                elif state.occupied(move_pos):
                    yield ((q, r), move_pos, "MOVE")
                # Jump (still need to check inboard)
                elif state.occupied(jump_pos) and state.inboard(jump_pos):
                    yield ((q, r), jump_pos, "JUMP")

    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        # TODO use rotate state so that the result is always red
        fr, to, mv = action
        pos_to_piece = state.pos_to_piece
        colour = state.colour
        next_colour = State.next_colour(state.colour)
        completed = state.completed

        # update dictionary
        pos_to_piece.pop(fr)
        if to is not None:
            pos_to_piece[to] = colour
        # one piece moved out
        else:
            if colour in completed:
                completed[colour] = completed[colour] + 1
            else:
                completed[colour] = 1

        # Construct the new state
        return State(pos_to_piece, next_colour, completed)

    def update(self, action):
        """
        Update the state by the given action
        :param action: an action
        """
        self.initial = self.result(self.initial, action)



if __name__ == "__main__":
    # test for static problem class
    pass
