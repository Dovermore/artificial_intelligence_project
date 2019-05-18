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
    def __init__(self):
        super().__init__()
        self.solution = None

        self.initial_state = None
        # remove all agent's pieces
        self.goal = None

        # A mapping for heuristic distances
        self.colour = None
        self.heuristic_distance = dd(float)

        self.final_node = None

    def search(self, game, state, **kwargs):
        if self.solution is None:
            # Remove other players (this static search don't care
            # about other players)
            self.colour = state.colour
            colours_to_remove = set(state.code_map.keys())
            colours_to_remove.remove(self.colour)
            # Remove other colours
            self.initial_state = self.remove_colours(state, colours_to_remove)
            # Now remove the player colour
            # TODO improve this to only consider necessary pieces?
            self.goal = self.generate_goal(self.initial_state, self.colour)

            # Start search
            self._build_heuristic_distance(game)
            print(self.heuristic_distance)
            self.final_node = self\
                .astar_search(game, self.h)
            # Get solution
            self.solution = self.final_node.solution
        # TODO check state and recompute path
        return self.solution.pop(0)

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

    def _build_heuristic_distance(self, problem):
        """
        Build the heuristic map used for searching by Dijkstra's Algorithm
        """
        goal = self.goal
        frontier = PriorityQueueImproved('min',
                                         f=self.heuristic_distance.__getitem__)
        # For all exit positions (We don't care about other players)
        for pos in problem.exit_positions[self.colour]:
            # Set initial heuristic to 1, and add to start
            self.heuristic_distance[pos] = 1
            frontier.append(pos)

        # While search is not ended
        while frontier:
            pos = frontier.pop()
            q, r = pos
            # Explore all space near current place
            cost = self.heuristic_distance[pos]
            for dq, dr in problem.moves:
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

    def h(self, node):
        state = node.state
        return sum((self.heuristic_distance[pos] for pos in
                    node.state.piece_to_pos[state.colour]))
