from node import Node
from util.misc import memoize
from util.queue import PriorityQueueImproved


def best_first_graph_search(problem, f, show=False, **kwargs):
    """Search the nodes with the lowest f scores first.
    You specify the function f(node) that you want to minimize; for example,
    if f is a heuristic estimate to the goal, then we have greedy best
    first search; if f is node.depth then we have breadth-first search.
    There is a subtlety: the line "f = memoize(f, 'f')" means that the f
    values will be cached on the nodes as they are computed. So after doing
    a best first search you can examine the f values of the path returned."""
    # f = memoize(f, 'f')
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


def astar_search(problem, h=None, *args, **kwargs):
    """A* search is best-first graph search with f(n) = g(n)+h(n).
    You need to specify the h function when you call astar_search, or
    else in your Problem subclass."""
    h = h or problem.h
    # h = memoize(h or problem.h, 'h')
    return best_first_graph_search(problem, lambda n: n.path_cost + h(n),
                                   *args, **kwargs)


def dijkstra_search(problem):
    """
    Best first search that uses g(n) to evaluate cost
    :param problem:
    :return: final node
    """
    return best_first_graph_search(problem, lambda n: n.path_cost)


def depth_first_tree_search(problem, show=False):
    """Search the deepest nodes in the search tree first.
        Search through the successors of a problem to find a goal.
        The argument frontier should be an empty queue.
        Repeats infinitely in case of loops. [Figure 3.7]"""

    frontier = [Node(problem.initial)]  # Stack
    explored = set()

    while frontier:
        node = frontier.pop()
        explored.add(node.state)
        if show:
            print(node)
        if problem.goal_test(node.state):
            return node
        for child in node.expand(problem):
            if child.state not in explored:
                frontier.append(child)
    return None


def depth_limited_search(problem, limit=50):
    """[Figure 3.17]"""
    def recursive_dls(node, problem, limit):
        if problem.goal_test(node.state):
            return node
        elif limit == 0:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in node.expand(problem):
                result = recursive_dls(child, problem, limit - 1)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else None

