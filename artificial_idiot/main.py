"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
"""

import sys
import json

from util.json_parser import parse
from state import State
from problem import PathFindingProblem
from search import (best_first_graph_search, astar_search,
                    depth_first_tree_search)
from util.misc import format_action, print_board
from time import sleep


def main():
    with open(sys.argv[1]) as file:
        json_loader = json.load(file)
        forward_dict, colour = parse(json_loader, "A")
        state = State(forward_dict, colour)

        print("----------------------------------------")
        print(str(state))
        print("----------------------------------------")
        print(state.__repr__(debug=True))
        print("----------------------------------------")
        path_finding_problem = PathFindingProblem(state, colour)
        print_board(path_finding_problem.heuristic_distance)
        print_board(path_finding_problem.goal.pos_to_piece)
        final_node = astar_search(path_finding_problem, show=False)
        # final_node = depth_first_tree_search(static_problem, show=True)
        print("----------------------------------------")
        print("----------------------------------------")
        print(final_node.path)
        animate_path(final_node, 0.5)


def animate_path(final_node, wait: float = 1):
    path_action = zip(final_node.path, final_node.solution)
    prev_len = 0
    for path, action in path_action:
        print("\b"*prev_len)
        message = path.__repr__(message=format_action(action), debug=True,
                                printed=False)
        prev_len = len(message)
        print(message)
        sleep(wait)
    print([format_action(i) for i in final_node.solution])
    print(len(final_node.solution))


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
