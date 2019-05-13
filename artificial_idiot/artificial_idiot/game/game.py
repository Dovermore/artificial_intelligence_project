from artificial_idiot.util.misc import is_in
from artificial_idiot.game.state import State
from artificial_idiot.game.node import Node
import abc
from functools import lru_cache


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


class Game(BoardProblem):
    """
    Holds all rules for the game
    static variables are defined in BoardProblem class
    """

    def __init__(self, colour, state, evaluator):
        super().__init__(state)
        self.evaluator = evaluator
        self.colour = colour

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
        # TODO change the order of the loops
        for q, r in state.piece_to_pos[state.colour]:
            for move in cls._move:
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
            exit_ready_pos = cls._exit_positions[state.colour]
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
        next_colour = State.next_colour(state.colour)
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

    def value(self, state, *args, **kwargs):
        return self.evaluator(state, *args, **kwargs)

    @staticmethod
    def terminal_state(state):
        if isinstance(state, Node):
            return max(state.state.completed.values()) == 4
        return max(state.completed.values()) == 4

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


if __name__ == "__main__":
    # test to convert player pieces
    from artificial_idiot.util.json_parser import JsonParser
    import json

    def test_jump():
        f = open("../tests/jump.json")
        json_loader = json.load(f)
        json_parser = JsonParser(json_loader)
        pos_dict, player, completed = json_parser.parse()
        game = Game(player, State(pos_dict, player, completed=completed))
        f.close()

        f = open("../tests/jump_ans.json")
        json_loader = json.load(f)
        json_parser = JsonParser(json_loader)
        pos_dict_ans, player_ans, completed_ans = json_parser.parse()
        f.close()

        print(game)
        state = game.initial_state
        state = game.result(state, ((-3, 0), (-1,-2), "JUMP"))
        assert(dict(state.pos_to_piece) == pos_dict_ans)
        assert(game.colour == player_ans)
        print(state.completed)
        assert(state.completed == completed_ans)
        print(game)

    def test_exit():
        f = open("../tests/simple.json")
        pos_dict, colour, completed = JsonParser(json.load(f)).parse()
        game = Game(colour, State(pos_dict, colour, completed))
        print(game.initial_state)
        assert([i for i in game.actions(game.initial_state)] == [((3, -3), None, 'EXIT'), ((3, -3), (3, -2), 'MOVE'), ((3, -3), (2, -2), 'MOVE'), ((3, -3), (2, -3), 'MOVE')])

    test_jump()
    print("="*10)
    test_exit()





