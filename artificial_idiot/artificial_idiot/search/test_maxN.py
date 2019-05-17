from unittest import TestCase
from artificial_idiot.game.game import Game
from artificial_idiot.game.state import State
from artificial_idiot.evaluation.evaluator_generator import (
    NaiveEvaluatorGenerator, AdvanceEG
)
from artificial_idiot.util.json_parser import JsonParser
from artificial_idiot.search.max_n import MaxN
from artificial_idiot.search.search_cutoff.cutoff import DepthLimitCutoff
import json


def parse_state(file_name):
    f = open(file_name)
    pos_dict, colour, completed = JsonParser(json.load(f)).parse()
    return State(pos_dict, colour, completed)


def change_state_color(state, color):
    return State(state.pos_to_piece, color, state.completed)


# class TestMaxN(TestCase):
#     weights = [5, 2, 0.7]
#     evaluator_generator = NaiveEvaluatorGenerator(weights)
#     cutoff = DepthLimitCutoff(3)
#     search = MaxN(evaluator_generator, cutoff, 3)
#
#     def test_initial_move(self):
#         search = self.search
#         state = parse_state("../../tests/red_initial_state.json")
#         print(state)
#
#         game = Game('red', state)
#         best_action = search.search(game, state)
#         print(best_action)
#
#     def test_avoid_eaten(self):
#         search = self.search
#         state = parse_state("../../tests/avoid_eaten.json")
#         print(state)
#
#         game = Game('red', state)
#         best_action = search.search(game, state)
#         print(best_action)


class TestMyMaxN(TestCase):
    # self.utility_pieces, num_exited_piece, self.utility_distance
    weights = [1, 100, 1]
    evaluator_generator = AdvanceEG(weights)
    cutoff = DepthLimitCutoff(3)
    search = MaxN(evaluator_generator, cutoff, 3)

    def test_must_exit(self):
        search = self.search
        state = parse_state("../../tests/must_exit_0.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        self.assertEqual(best_action[-1], 'EXIT')

        state = parse_state("../../tests/must_exit_1.json")
        print(state)
        best_action = search.search(game, state)
        self.assertEqual(best_action[-1], 'EXIT')

        state = parse_state("../../tests/must_exit_2.json")
        print(state)
        best_action = search.search(game, state)
        self.assertEqual(best_action[-1], 'EXIT')

        state = parse_state("../../tests/must_exit_3.json")
        print(state)
        best_action = search.search(game, state)
        self.assertEqual(best_action[-1], 'EXIT')

    def test_avoid_eaten(self):
        search = self.search
        state = parse_state("../../tests/avoid_eaten.json")
        print(state)

        game = Game('red', state)
        best_action = search.search(game, state)
        self.assertTupleEqual(best_action, ((-2, -1), (-3, 0), 'MOVE'))

    def test_eat_blue(self):
        search = self.search
        state = parse_state("../../tests/eat_blue.json")
        print(state)

        game = Game('red', state)
        best_action = search.search(game, state)
        self.assertTupleEqual(best_action, ((0, 0), (2, -2), 'JUMP'))

    def test_should_not_exit(self):
        search = self.search
        state = parse_state("../../tests/should_not_exit.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        self.assertNotEqual(best_action[-1], 'EXIT')

    def test_move_not_jump(self):
        search = self.search
        state = parse_state("../../tests/move_not_jump.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        print(best_action)

    def test_weird(self):
        search = self.search
        state = parse_state("../../tests/weird.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        print(best_action)
