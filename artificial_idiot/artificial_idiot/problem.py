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

    @abc.abstractmethod
    def value(self, state):
        """
        For optimization problems, each state has a value.  Hill-climbing
        and related algorithms try to maximize this value.
        """
        pass


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


class PathFindingProblem(BoardProblem):
    """
    Static Search problem for project part A
    """
    def __init__(self, initial, colour):
        """
        initial state is supplied by the problem
        goal state is initial state without any agent's pieces
        """
        super().__init__(initial)
        # remove all agent's pieces
        self.goal = State.goal_state(initial, colour)

        # A mapping for heuristic distances
        self.colour = colour
        self.heuristic_distance = dd(float)
        self._build_heuristic_distance()

    def _build_heuristic_distance(self):
        """
        Build the heuristic map used for searching by Dijkstra's Algorithm
        """
        goal = self.goal
        frontier = PriorityQueueImproved('min',
                                         f=self.heuristic_distance.__getitem__)
        # For all exit positions
        for pos in self._exit_positions[self.colour]:
            # If the exit position is not occupied by other pieces
            if pos not in goal.pos_to_piece:
                # Set initial heuristic to 1, and add to start
                self.heuristic_distance[pos] = 1
                frontier.append(pos)

        # While search is not ended
        while frontier:
            pos = frontier.pop()
            q, r = pos
            # Explore all space near current place
            cost = self.heuristic_distance[pos]
            for dq, dr in self._move:
                for move in range(1, 3):
                    next_pos = (q + dq * move, r + dr * move)
                    # If the moved position is valid, update it with cost + 1,
                    # Else simply continue next loop
                    if (not State.inboard(next_pos) or
                            next_pos in goal.pos_to_piece):
                        continue
                    # Get value in dictionary
                    h_val = self.heuristic_distance.get(next_pos, None)

                    # Not yet navigated to or can be updated
                    if h_val is None or h_val > cost + 1:
                        # Update dictionary entry
                        self.heuristic_distance[next_pos] = cost + 1
                        # Update the value in queue
                        frontier.append(next_pos)

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
                move_pos = (q+i, r+j)
                jump_pos = (q+i*2, r+j*2)
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
        fr, to, mv = action
        pos_to_piece = state.pos_to_piece
        colour = state.colour
        next_colour = state.next_colour()
        # update dictionary
        pos_to_piece.pop(fr)
        if to is not None:
            pos_to_piece[to] = colour

        # Construct the new state
        return State(pos_to_piece, next_colour)

    def value(self, state):
        raise NotImplementedError

    @classproperty
    def exit_positions(cls):
        return copy(cls._exit_positions)

    def h0(self, node):
        state = node.state
        colour = node.state.colour

        dists = 0
        for position in state.piece_to_pos[state.colour]:
            dists += (min([self.grid_dist(position, exit_position) for
                           exit_position in self._exit_positions[colour]
                           if exit_position not in
                           state.piece_to_pos["block"]])
                      + 1) // 2
        return dists

    @staticmethod
    def grid_dist(pos1, pos2):
        """
        Get the grid distance between two different grid locations
        :param pos1: first position (tuple)
        :param pos2: second position (tuple)
        :return: The `manhattan` distance between those two positions
        """
        x1, y1 = pos1
        x2, y2 = pos2

        dy = y2 - y1
        dx = x2 - x1

        # If different sign, take the max of difference in position
        if dy * dx < 0:
            return max([abs(dy), abs(dx)])
        # Same sign or zero just take sum
        else:
            return abs(dy + dx)

    def h(self, node):
        state = node.state
        return sum((self.heuristic_distance[pos] for pos in
                    node.state._piece_to_pos[state.colour]))

    def goal_test(self, state):
        return state == self.goal


if __name__ == "__main__":
    # test for static problem class
    pass
