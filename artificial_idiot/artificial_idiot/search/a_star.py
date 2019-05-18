from artificial_idiot.search.search import Search
from artificial_idiot.util.queue import PriorityQueueImproved
from artificial_idiot.game.node import Node
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

        self.initial_state = None
        # remove all agent's pieces
        self.goal = None

        # A mapping for heuristic distances
        self.colour = None
        self.heuristic_distance = dd(float)

        self.final_node = None

    def search(self, game, state, **kwargs):
        if self.solution is None:
            # build heuristic distance
            self.heuristic_distance = state.heuristic_distance
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
            print("====================")
            print(node.state)
            print(node.path_cost)
            print()
            print(len(explored))
            print("====================")
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


        return self.heuristic_distance

    def h(self, node):
        state = node.state
        return sum((self.heuristic_distance[pos] for pos in
                    node.state.piece_to_pos[state.colour]))
