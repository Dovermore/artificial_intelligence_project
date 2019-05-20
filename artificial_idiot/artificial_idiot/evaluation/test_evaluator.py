from unittest import TestCase
from artificial_idiot.evaluation.evaluator_generator import *
from artificial_idiot.game.state import State
from artificial_idiot.util.json_parser import JsonParser
import json


def parse_state(file_name):
    f = open(file_name)
    pos_dict, colour, completed = JsonParser(json.load(f)).parse()
    return State(pos_dict, colour, completed)


def return_1(state, player):
    return 1


class TestFunctionalEvaluator(TestCase):

    def test_basic(self):
        n_parameters = 3
        weights = [1]*n_parameters
        functions = [return_1]*n_parameters
        evaluator_generator = FunctionalEvaluatorGenerator(weights, functions)
        state = parse_state("../../tests/evaluator_test.json")
        evaluator = evaluator_generator(state)
        self.assertEqual(evaluator('red'), 3)
        self.assertEqual(evaluator('green'), 3)
        self.assertEqual(evaluator('blue'), 3)


class TestNaiveEvaluator(TestCase):
    weights = [10, 100, 1]
    evaluator_generator = NaiveEvaluatorGenerator(weights)

    def test_eat_green(self):
        evaluator = self.evaluator_generator
        state = parse_state("../../tests/eat_green_better_move.json")
        print(state)
        value1 = evaluator(state)('red')
        print(value1)

        state = parse_state("../../tests/eat_green_wost_move.json")
        print(state)
        value2 = evaluator(state)('red')
        print(value2)

        self.assertGreater(value1, value2)



