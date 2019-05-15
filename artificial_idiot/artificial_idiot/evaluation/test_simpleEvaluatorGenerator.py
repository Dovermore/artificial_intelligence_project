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
        utility = SimpleEvaluatorGenerator.utility_distance
        state = parse_state("../../tests/no_exit.json")
        print(state)
        print(utility(state, 'red'))
        self.assertEqual(utility(state, 'red'), 0)

    def move_one_by_one(self):
        utility = SimpleEvaluatorGenerator.utility_distance
        state = parse_state("../../tests/no_exit.json")