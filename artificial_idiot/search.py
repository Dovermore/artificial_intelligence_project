from node import Node
from util.misc import memoize
from util.queue import PriorityQueue


def best_first_graph_search(problem, f):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    f = memoize(f, 'f')
    node = Node(problem.initial)
    frontier = PriorityQueue('min', f)
    frontier.append(node)
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if child.state not in explored and child not in frontier:
                frontier.append(child)
            elif child in frontier:
                if f(child) < frontier[child]:
                    del frontier[child]
                    frontier.append(child)
    return None


def astar_search(problem, h=None):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n))


# def depth_limited_search(problem, limit=50):
#     """[Figure 3.17]"""
#     def recursive_dls(node, problem, limit):
#         if problem.goal_test(node.state):
#             return node
#         elif limit == 0:
#             return 'cutoff'
#         else:
#             cutoff_occurred = False
#             for child in node.expand(problem):
#                 result = recursive_dls(child, problem, limit - 1)
#                 if result == 'cutoff':
#                     cutoff_occurred = True
#                 elif result is not None:
#                     return result
#             return 'cutoff' if cutoff_occurred else None

