from unittest import TestCase
from artificial_idiot.evaluation.evaluator import *
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
        evaluator = FunctionalEvaluator(functions)
        state = parse_state("../../tests/evaluator_test.json")
        self.assertEqual(evaluator(state, 'red', weights), 3)
        self.assertEqual(evaluator(state, 'green', weights), 3)
        self.assertEqual(evaluator(state, 'blue', weights), 3)



class TestNaiveEvaluator(TestCase):

    def test_exit(self):
        # weights in the format of [pieces, exited, distance]
        weights = [5, 2, 0.7]
        evaluator = NaiveEvaluator(weights)
        state = parse_state("../../tests/evaluator_test.json")
        print(state)
        self.assertEqual(evaluator(state, 'red'), 11)
        self.assertAlmostEqual(evaluator(state, 'green'), 20.1, places=1)
        self.assertEqual(evaluator(state, 'blue'), 708)


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