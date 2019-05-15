from unittest import TestCase
from artificial_idiot.evaluation.evaluator_generator import *
from artificial_idiot.game.state import State
from artificial_idiot.util.json_parser import JsonParser
import json


def parse_state(file_name):
    f = open(file_name)
    pos_dict, colour, completed = JsonParser(json.load(f)).parse()
    return State(pos_dict, colour, completed)


class TestUtilityDistance(TestCase):

    def test_no_exit(self):
        utility = SimpleEG.utility_distance
        state = parse_state("../../tests/no_exit.json")
        print(state)
        print(utility(state, 'red'))
        self.assertEqual(utility(state, 'red'), 0)

    def test_move_one_by_one(self):
        utility = SimpleEG.utility_distance
        state1 = parse_state("../../tests/move1.json")
        state2 = parse_state("../../tests/move2.json")
        player = 'red'
        print(state1)
        print(state2)
        self.assertGreater(utility(state1, player), utility(state2, player))

    def test_jump(self):
        utility = SimpleEG.utility_distance
        state1 = parse_state("../../tests/jump_not_move.json")
        state2 = parse_state("../../tests/move_not_jump.json")
        player = 'red'
        print(state1)
        print(utility(state1, player))
        print(state2)
        print(utility(state2, player))

