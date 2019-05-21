from artificial_idiot.search.search import Search
from artificial_idiot.util.queue import PriorityQueueImproved
from artificial_idiot.game.node import Node
from artificial_idiot.game.state import State
from collections import defaultdict as dd
from copy import deepcopy


class AStar(Search):
    """
    This static AStar search is used for finding the optimal path for exiting
    when the player is not near enemy and have enough piece to exit to win.
    (Note this includes case where only one player is left.)
    """
    def __init__(self, type=0):
        super().__init__()
        self.type = type
        self.solution = None
        self.initial_state = None
        # remove all agent's pieces
        self.goal = None

        # A mapping for heuristic distances
        self.colour = None
        self.heuristic_distance = dd(float)
        self.final_node = None

    def recompile(self):
        self.solution = None

    def search(self, game, state, **kwargs):
        if self.solution is None:
            # Remove other players (this static search don't care
            # about other players)
            self.colour = state.colour
            # Remove other colours
            self.initial_state = AStarState.from_state(state, self.colour)
            # Now remove the player colour
            # TODO improve this to only consider necessary pieces?
            self.goal = self.initial_state.generate_goal(self.initial_state,
                                                         self.colour)
            # Start search
            self.heuristic_distance = game.heuristic_distance
            self.final_node = self\
                .astar_search(game, self.h)
            # Get solution
            self.solution = self.final_node.solution
        return self.solution.pop(0)

    def goal_test(self, state, type=0):
        """
        A very simple goal test, that's **not** admissible
        """
        if type == 0:
            return state.completed[self.colour] >= 4
        elif type == 1:
            return state.goal == self.goal

    def best_first_graph_search(self, problem, f, show=False, **kwargs):
        """Search the nodes with the lowest f scores first.
        You specify the function f(node) that you want to minimize; for example,
        if f is a heuristic estimate to the goal, then we have greedy best
        first search; if f is node.depth then we have breadth-first search.
        There is a subtlety: the line "f = memoize(f, 'f')" means that the f
        values will be cached on the nodes as they are computed. So after doing
        a best first search you can examine the f values of the path returned.
        """
        node = Node(self.initial_state)
        frontier = PriorityQueueImproved('min', f)
        frontier.append(node)
        explored = set()
        while frontier:

            node = frontier.pop()
            if show:
                print(f"Depth: {node.depth}")
                print(f"Heuristic: {problem.h(node)}")
                print(len(explored))
                print(node.__repr__(**kwargs))
            if node.state == self.goal:
                return node
            explored.add(node.state)
            for child in node.expand(problem):
                if child in frontier:
                    f_val = f(child)
                    if f_val < frontier[child]:
                        frontier.update(f_val, child)
                elif child.state not in explored:
                    frontier.append(child)
        return None

    def astar_search(self, problem, h=None, *args, **kwargs):
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""
        h = h or problem.h
        # h = memoize(h or problem.h, 'h')
        return self.best_first_graph_search\
            (problem, lambda n: n.path_cost + h(n), *args, **kwargs)

    def h(self, node):
        state = node.state
        return sum((self.heuristic_distance[pos] for pos in
                    node.state.piece_to_pos[state.colour]))


class AStarState(State):
    code_map = {"red": 0, "green": 1, "blue": 2, "block": 3}

    rev_code_map = {
        value: key for key, value in code_map.items()
    }

    @classmethod
    def from_state(cls, state, colour):
        n_completed = state.completed[colour]
        colours_to_remove = set(state.code_map.keys())
        colours_to_remove.remove(colour)
        excess_colours_removed = cls.remove_colours(state, colours_to_remove)
        distances = {}
        for piece in excess_colours_removed.piece_to_pos[colour]:
            distances[piece] = \
                cls.exit_distance(piece, excess_colours_removed, colour)
        piece_to_convert = sorted(distances,
                                  key=distances.__getitem__)[4-n_completed:]
        pos_to_piece = excess_colours_removed.pos_to_piece
        for piece in piece_to_convert:
            pos_to_piece[piece] = "block"
        return cls(pos_to_piece, colour)

    def next_colour(self, colour):
        """
        :return: The next active colour after current execution
        """
        return colour

    @classmethod
    def remove_colours(cls, state, colours):
        pos_to_piece = state.pos_to_piece
        state_colour = state.colour
        # remove goal colour
        pos_to_piece = {k: v for k, v in pos_to_piece.items()
                        if v not in colours}
        return cls(pos_to_piece, state_colour)

    def generate_goal(self, state, colour):
        piece_remaining = len(state.piece_to_pos[colour])
        completed = deepcopy(state.completed)
        completed[colour] += piece_remaining
        state = self.remove_colours(state, [colour])
        state.completed = completed
        return state

    @staticmethod
    def exit_distance(piece, state, player):
        if player == 'red':
            return 3 - piece[0]
        if player == 'green':
            return 3 - piece[1]
        if player == 'blue':
            return 3 + piece[0]
