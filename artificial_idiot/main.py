"""
COMP30024 Artificial Intelligence, Semester 1 2019
Solution to Project Part A: Searching

Authors: 
"""

import sys
import json

from util.json_parser import parse
from state import State


def main():
    with open(sys.argv[1]) as file:
        json_loader = json.load(file)
        forward_dict, colour = parse(json_loader, "A")
        state = State(forward_dict, colour)

        print(str(state))
        print(state.__str__(True))


# when this module is executed, run the `main` function:
if __name__ == '__main__':
    main()
