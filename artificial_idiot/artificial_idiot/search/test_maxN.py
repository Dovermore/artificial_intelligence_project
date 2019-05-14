from unittest import TestCase
from artificial_idiot.game.game import Game
from artificial_idiot.game.state import State
from artificial_idiot.evaluation.evaluator_generator import NaiveEvaluatorGenerator
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


class TestMaxN(TestCase):
    weights = [5, 2, 0.7]
    evaluator_generator = NaiveEvaluatorGenerator(weights)
    cutoff = DepthLimitCutoff(3)
    search = MaxN(evaluator_generator, cutoff, 3)

    def test_must_exit(self):
        search = self.search
        state = parse_state("../../tests/all_should_exit.json")
        print(state)

        game = Game('red', state)

        best_action = search.search(game, state)
        self.assertTupleEqual(best_action, ((3, 0), None, 'EXIT'))

        state = change_state_color(state, 'green')
        best_action = search.search(game, state)
        self.assertTupleEqual(best_action, ((-3, 3), None, 'EXIT'))

        state = change_state_color(state, 'blue')
        best_action = search.search(game, state)
        self.assertTupleEqual(best_action, ((0, -3), None, 'EXIT'))

    def test_initial_move(self):
        search = self.search
        state = parse_state("../../tests/red_initial_state.json")
        print(state)

        game = Game('red', state)
        best_action = search.search(game, state)
        print(best_action)
