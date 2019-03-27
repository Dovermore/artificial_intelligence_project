"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
"""

import sys
import json

from util.json_parser import parse
from state import State
from problem import StaticProblem
from search import (best_first_graph_search, astar_search,
                    depth_first_tree_search)
from util.misc import format_action


def main():
    with open(sys.argv[1]) as file:
        json_loader = json.load(file)
        forward_dict, colour = parse(json_loader, "A")
        state = State(forward_dict, colour)

        print("----------------------------------------")
        print(str(state))
        print("----------------------------------------")
        print(state.__str__(True))
        print("----------------------------------------")
        static_problem = StaticProblem(state, colour)
        final_node = astar_search(static_problem, show=True)
        # final_node = depth_first_tree_search(static_problem, show=True)
        print("----------------------------------------")
        print("----------------------------------------")
        print(final_node.path)
        print([format_action(i) for i in final_node.solution])


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
