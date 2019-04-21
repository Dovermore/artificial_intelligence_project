"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: Chuanyuan Liu, Zhuoqun Huang
"""

import sys
import json

from artificial_idiot.util import JsonParser
from artificial_idiot.state import State
from artificial_idiot.problem import PathFindingProblem
from artificial_idiot.algorithm import (astar_search)
from artificial_idiot.util import format_action, print_board
from time import sleep
from artificial_idiot.node import Node


def main():
    with open(sys.argv[1]) as file:
        animate = False
        detailed = False
        brief = False
        analysis = False
        if len(sys.argv) > 2:
            if sys.argv[2] == "brief":
                brief = True
            elif sys.argv[2] == "analysis":
                analysis = True
            else:
                animate = bool(sys.argv[2])
        if len(sys.argv) > 3:
            detailed = bool(sys.argv[3])

        json_loader = json.load(file)

        json_parser = JsonParser(json_loader, "A")

        pos_dict, colour = json_parser.parse(True)
        state = State(pos_dict, colour)

        path_finding_problem = PathFindingProblem(state, colour)
        if detailed:
            print_board(path_finding_problem.heuristic_distance)
            print_board(path_finding_problem.goal.pos_to_piece)

        # final_node = depth_first_tree_search(path_finding_problem)
        final_node = astar_search(path_finding_problem, show=detailed,
                                  printed=False)
        # final_node = dijkstra_search(path_finding_problem)

        if analysis:
            print(path_finding_problem.initial)
            print('name:', sys.argv[1])
            print('n_steps:', len(final_node.solution))
            print('n_nodes:', Node.total_nodes_created)

        if final_node is None:
            print("Final Node is None!")
            return

        if animate:
            print(final_node.path)
            animate_path(final_node, 0.5)
        else:
            if brief:
                print(len(final_node.solution))
            else:
                for action in final_node.solution:
                    print(format_action(action))


def animate_path(final_node, wait: float = 1):
    path_action = zip(final_node.path, final_node.solution)
    prev_len = 0
    for path, action in path_action:
        sys.stdout.write("\b"*prev_len)
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
