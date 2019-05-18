from artificial_idiot.util.misc import is_in
from artificial_idiot.game.state import State
from artificial_idiot.game.node import Node
import abc
from functools import lru_cache
from copy import deepcopy
from collections import defaultdict as dd
from artificial_idiot.util.queue import PriorityQueueImproved
from artificial_idiot.util.misc import print_board


class Problem(abc.ABC):
    """
    The abstract class for a formal problem. You should subclass
    this and implement the methods actions and result, and possibly
    __init__, goal_test, and path_cost. Then you will create instances
    of your subclass and solve them with the various search functions.
    """

    def __init__(self, state, goal=None):
        """
        The constructor specifies the state state, and possibly a goal
        state, if there is a unique goal. Your subclass's constructor can add
        other arguments.
        """
        self.initial_state = state
        self.goal = goal
        self.colour = None

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
        state1 via action, assuming cost c to get up to state1. If the game
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
    exit_positions = {
        "red": ((3, -3), (3, -2), (3, -1), (3, 0)),
        "green": ((-3, 3), (-2, 3), (-1, 3), (0, 3)),
        "blue": ((0, -3), (-1, -2), (-2, -1), (-3, 0))
    }

    # possible moves.
    moves = (
        (+1, -1), (1, 0), (0, 1),
        (-1, +1), (-1, 0), (0, -1)
    )


class Game(BoardProblem):
    """
    Holds all rules for the game
    static variables are defined in BoardProblem class
    """

    def __init__(self, colour, state):
        super().__init__(state)
        # self.evaluator = evaluator
        self.colour = colour
        self.heuristic_distance = dd(float)
        self.build_heuristic_distance(deepcopy(state))
        State.heuristic_distance = self.heuristic_distance
        print_board(self.heuristic_distance)

    def build_heuristic_distance(self, state):
        """
        Build the heuristic map used for searching by Dijkstra's Algorithm
        """
        # Remove other players (this static search don't care
        # about other players)
        self.colour = state.colour
        colours_to_remove = set(state.code_map.keys())
        colours_to_remove.remove(self.colour)
        # Remove other colours
        initial_state = self.remove_colours(state, colours_to_remove)
        # Now remove the player colour
        # TODO improve this to only consider necessary pieces?
        self.goal = self.generate_goal(initial_state, self.colour)

        goal = self.goal
        frontier = PriorityQueueImproved('min',
                                         f=self.heuristic_distance.__getitem__)
        # For all exit positions (We don't care about other players)
        for pos in self.exit_positions[self.colour]:
            # Set initial heuristic to 1, and add to start
            self.heuristic_distance[pos] = 1
            frontier.append(pos)

        # While search is not ended
        while frontier:
            pos = frontier.pop()
            q, r = pos
            # Explore all space near current place
            cost = self.heuristic_distance[pos]
            for dq, dr in self.moves:
                for move in range(1, 2):
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

    @staticmethod
    def remove_colours(state, colours):
        pos_to_piece = state.pos_to_piece
        state_colour = state.colour
        # remove goal colour
        pos_to_piece = {k: v for k, v in pos_to_piece.items()
                        if v not in colours}
        return State(pos_to_piece, state_colour)

    def generate_goal(self, state, colour):
        piece_remaining = len(state.piece_to_pos[colour])
        completed = deepcopy(state.completed)
        completed[colour] += piece_remaining
        state = self.remove_colours(state, [colour])
        state.completed = completed
        return state

    @classmethod
    @lru_cache(10000)
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
        actions = []
        if cls.terminal_state(state):
            return actions
        # Jump -> move -> exit
        # for each piece try all possible moves
        # Not using deepcopy here because no need to
        move_actions = []
        for move in cls.moves:
            for q, r in state.piece_to_pos[state.colour]:
                i, j = move
                move_to = (q + i, r + j)
                jump_to = (q + i * 2, r + j * 2)
                # If that direction is possible to move
                if state.inboard(move_to):
                    if not state.occupied(move_to):
                        move_actions.append(((q, r), move_to, "MOVE"))
                    # Jump (still need to check inboard)
                    elif state.inboard(jump_to) and \
                            not state.occupied(jump_to):
                        actions.append(((q, r), jump_to, "JUMP"))
        # no move possible return None
        if move_actions:
            for action in move_actions:
                actions.append(action)
        for q, r in state.piece_to_pos[state.colour]:
            exit_ready_pos = cls.exit_positions[state.colour]
            # exit
            if (q, r) in exit_ready_pos:
                actions.append(((q, r), None, "EXIT"))
        return actions if len(actions) > 0 else [(None, None, "PASS")]

    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state by a given actor. The action must be one of
        self.actions(state).
        """
        # TODO next color is a rule that should belong in the Game class
        next_colour = state.next_colour(state.colour)
        completed = state.completed.copy()

        fr, to, mv = action
        pos_to_piece = state.pos_to_piece

        if mv == "PASS":
            return State(state.pos_to_piece, next_colour, state.completed)

        # update dictionary
        colour = pos_to_piece.pop(fr)
        if to is not None:
            pos_to_piece[to] = colour
        # one piece moved out
        else:
            if colour in completed:
                completed[colour] = completed[colour] + 1
            else:
                completed[colour] = 1

        if mv == "JUMP":
            leap_frog = (fr[0] + to[0])/2, (fr[1] + to[1])/2
            pos_to_piece[leap_frog] = colour

        # Construct the new state
        return State(pos_to_piece, next_colour, completed)

    def update(self, colour, action):
        """
        Update the state by the given action
        :param colour: player who made the move
        :param action: an action
        """
        self.initial_state = self.result(self.initial_state, action)

    # def value(self, state, *args, **kwargs):
    #     return self.evaluator(state, *args, **kwargs)

    @staticmethod
    def terminal_state(state):
        if isinstance(state, Node):
            return max(state.state.completed.values()) == 4
        return max(state.completed.values()) == 4

    def integer_distance(self, state, colour):
        dists = 0
        for position in state.piece_to_pos[colour]:
            dists += (min([self.grid_dist(position, exit_position) for
                           exit_position in self.exit_positions[colour]])
                      + 1) // 2
        return dists

    def float_distance(self, state, colour):
        dists = 0
        for position in state.piece_to_pos[colour]:
            dists += (min([self.grid_dist(position, exit_position) for
                           exit_position in self.exit_positions[colour]])
                      + 1) / 2
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

    def __str__(self):
        return str(self.initial_state)


class NodeGame(Game):
    """
    A expansion to the base game. Also stores a root node for search with
    memory (Learning)
    """
    # @classmethod
    # def actions(cls, state):
    #     """
    #     # TODO Possible subclassing of this to make more efficient
    #     :param state:
    #     :return:
    #     """
    #     return super().actions(state)

    def update(self, colour, action):
        for child in self.initial_state.expand(self):
            if child.action == action:
                self.initial_state = child
                return
        else:
            raise ValueError(f"No corresponding action {action} found."
                             f"Possible actions are "
                             f"{[child.action for child in self.initial_state.children]}")


class RewardedGame(Game):
    pass







