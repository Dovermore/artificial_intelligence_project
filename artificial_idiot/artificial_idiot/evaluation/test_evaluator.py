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

    def test_no_exit_and_exited(self):
        # blue have exited so it should have the highest value
        # red can't exit because green is blocking it
        # weights in the format of [pieces, exited, distance]
        weights = [5, 2, 0.7]
        evaluator_generator = NaiveEvaluatorGenerator(weights)
        state = parse_state("../../tests/evaluator_test.json")
        print(state)
        evaluator = evaluator_generator(state)
        self.assertAlmostEqual(evaluator('red'), 11, places=1)
        self.assertAlmostEqual(evaluator('green'), 20.039, places=3)
        self.assertEqual(evaluator('blue'), 708)


class TestSumShortestExitDistance(TestCase):

    def test_no_block(self):
        state = parse_state("../../tests/empty_board_for_red.json")
        self.assertTrue(sum_shortest_exit_distance(state, 'red') == 12)

    def test_one_exit_position(self):
        state = parse_state("../../tests/only_one_exit_pos_for_red.json")
        self.assertTrue(sum_shortest_exit_distance(state, 'red') == 15)

    def test_no_exit(self):
        state = parse_state("../../tests/no_exit.json")
        self.assertTrue(sum_shortest_exit_distance(state, 'red') >= 10000)