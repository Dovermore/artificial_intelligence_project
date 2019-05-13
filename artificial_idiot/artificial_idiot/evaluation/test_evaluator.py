from unittest import TestCase
from artificial_idiot.evaluation.evaluator import *
from artificial_idiot.game.state import State
from artificial_idiot.util.json_parser import JsonParser
import json


def parse_state(file_name):
    f = open(file_name)
    pos_dict, colour, completed = JsonParser(json.load(f)).parse()
    return State(pos_dict, colour, completed)


def foo(state):
    return [1, 2, 3]


class TestFunctionalEvaluator(TestCase):

    def test_basic(self):
        n_parameters = 3
        weights = [1]*n_parameters
        functions = [foo]*n_parameters
        evaluator = FunctionalEvaluator(functions)
        state = parse_state("../../tests/evaluator_test.json")
        utility_value = list(evaluator(state, weights))
        self.assertListEqual(utility_value, [3, 6, 9])


class TestNaiveEvaluator(TestCase):

    def test_exit(self):
        # weights in the format of [pieces, exited, distance]
        weights = [7, 9, 1]
        evaluator = NaiveEvaluator(weights)
        state = parse_state("../../tests/evaluator_test.json")
        print(state)
        self.assertTrue(evaluator(state, 'red') == 3)
        self.assertTrue(evaluator(state, 'green') == 2)
        self.assertTrue(evaluator(state, 'blue') == 4)


class TestSumShortestExitDistance(TestCase):

    def test_no_block(self):
        state = parse_state("../../tests/empty_board_for_red.json")
        self.assertTrue(sum_shortest_exit_distance(state, 'red') == [12])

    def test_one_exit_position(self):
        state = parse_state("../../tests/only_one_exit_pos_for_red.json")
        self.assertTrue(sum_shortest_exit_distance(state, 'red') == [15])

    def test_no_exit(self):
        state = parse_state("../../tests/no_exit.json")
        self.assertTrue(sum_shortest_exit_distance(state, 'red') >= [10000])