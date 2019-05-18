from artificial_idiot.search.search import Search
from artificial_idiot.util.queue import PriorityQueueImproved
from artificial_idiot.game.node import Node
from artificial_idiot.game.state import State
from artificial_idiot.game.game import Problem, Game
from collections import defaultdict as dd


class AStar(Search):
    """
    This static AStar search is used for finding the optimal path for exiting
    when the player is not near enemy and have enough piece to exit to win.
    (Note this includes case where only one player is left.)
    """
    def __init__(self):
        super().__init__()
        self.solution = None
        # remove all agent's pieces
        self.goal = None

        # A mapping for heuristic distances
        self.colour = None
        self.heuristic_distance = dd(float)

    def search(self, game, state, **kwargs):
        if self.solution is None:
            # TODO finish this part
            self._build_heuristic_distance(game)
            self.astar_search(game, self.heuristic_distance.__getitem__)

    @classmethod
    def best_first_graph_search(cls, problem, f, show=False, **kwargs):
        """Search the nodes with the lowest f scores first.
        You specify the function f(node) that you want to minimize; for example,
        if f is a heuristic estimate to the goal, then we have greedy best
        first search; if f is node.depth then we have breadth-first search.
        There is a subtlety: the line "f = memoize(f, 'f')" means that the f
        values will be cached on the nodes as they are computed. So after doing
        a best first search you can examine the f values of the path returned.
        """
        node = Node(problem.initial)
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
            if problem.goal_test(node.state):
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

    @classmethod
    def astar_search(cls, problem, h=None, *args, **kwargs):
        """A* search is best-first graph search with f(n) = g(n)+h(n).
        You need to specify the h function when you call astar_search, or
        else in your Problem subclass."""
        h = h or problem.h
        # h = memoize(h or problem.h, 'h')
        return cls.best_first_graph_search\
            (problem, lambda n: n.path_cost + h(n), *args, **kwargs)

    def _build_heuristic_distance(self, problem):
        """
        Build the heuristic map used for searching by Dijkstra's Algorithm
        """
        goal = self.goal
        frontier = PriorityQueueImproved('min',
                                         f=self.heuristic_distance.__getitem__)
        # For all exit positions
        for pos in problem._exit_positions[self.colour]:
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
            for dq, dr in problem._move:
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
