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
    weights = [5, 2, 0.7]
    evaluator_generator = NaiveEvaluatorGenerator(weights)

    def test_no_exit_and_exited(self):
        # blue have exited so it should have the highest value
        # red can't exit because green is blocking it
        # weights in the format of [pieces, exited, distance]
        evaluator_generator = self.evaluator_generator
        state = parse_state("../../tests/evaluator_test.json")
        print(state)
        evaluator = evaluator_generator(state)
        self.assertAlmostEqual(evaluator('red'), 11, places=1)
        self.assertAlmostEqual(evaluator('green'), 20.039, places=3)
        self.assertEqual(evaluator('blue'), 8.7)

    def test_varied_distance(self):
        evaluator_generator = self.evaluator_generator
        state = parse_state("../../tests/varied_distance.json")
        print(state)
        evaluator = evaluator_generator(state)
        self.assertAlmostEqual(evaluator('red'), 11.7, places=1)
        self.assertEqual(evaluator('green'), 11.7)
        self.assertEqual(evaluator('blue'), 11.35)


class TestSumShortestExitDistance(TestCase):

    def test_no_block(self):
        state = parse_state("../../tests/empty_board_for_red.json")
        print(state)
        self.assertEqual(sum_shortest_exit_distance(state, 'red'), 12)

    def test_one_exit_position(self):
        state = parse_state("../../tests/only_one_exit_pos_for_red.json")
        print(state)
        self.assertEqual(sum_shortest_exit_distance(state, 'red'), 15)

    def test_no_exit(self):
        state = parse_state("../../tests/no_exit.json")
        print(state)
        self.assertEqual(sum_shortest_exit_distance(state, 'red'), 4000000)

    def test_move_one_by_one(self):
        utility = SimpleEG.utility_distance
        state1 = parse_state("../../tests/move1.json")
        state2 = parse_state("../../tests/move2.json")
        player = 'red'
        print(state1)
        print(state2)
        self.assertGreater(utility(state1, player), utility(state2, player))

