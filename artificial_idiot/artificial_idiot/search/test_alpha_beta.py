from unittest import TestCase
from artificial_idiot.game.game import Game
from artificial_idiot.game.state import State
from artificial_idiot.evaluation.evaluator_generator import NaiveEvaluatorGenerator, AdvanceEG
from artificial_idiot.util.json_parser import JsonParser
from artificial_idiot.search.mini_max import AlphaBetaSearch
from artificial_idiot.search.search_cutoff.cutoff import DepthLimitCutoff
import json
from artificial_idiot.util.misc import print_board


def parse_state(file_name):
    f = open(file_name)
    pos_dict, colour, completed = JsonParser(json.load(f)).parse()
    return State(pos_dict, colour, completed)


class TestParnoidPlayer(TestCase):
    # utility_pieces, num_exited_piece, total_number_pieces, utility_distance
    weights = [10, 100, 20, 1]
    evaluator_generator = NaiveEvaluatorGenerator(weights)
    cutoff = DepthLimitCutoff(4)
    search = AlphaBetaSearch(evaluator_generator, cutoff)

    def test_initial(self):
        search = self.search
        state = parse_state("../../tests/red_initial_state.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        print(best_action)

    def test_must_exit(self):
        search = self.search
        state = parse_state("../../tests/must_exit_0.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        self.assertEqual(best_action[-1], 'EXIT')

    def test_eat_green(self):
        search = self.search
        state = parse_state("../../tests/eat_green.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        self.assertTupleEqual(((0, 0), (2, -2), 'JUMP'), best_action)

    def test_move(self):
        search = self.search
        state = parse_state("../../tests/move.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        print(best_action)
        self.assertEqual(((1, 0), 'MOVE'), best_action[1:])

    def test_jump(self):
        search = self.search
        state = parse_state("../../tests/jump.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        self.assertEqual(((0, 0), (2, -2), 'JUMP'), best_action)

    def test_inch_forward(self):
        search = self.search
        state = parse_state("../../tests/inch_forward.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        print(best_action)
        self.assertEqual(((-3, 2), (-2, 2), 'MOVE'), best_action)

    def test_avoid_eaten(self):
        search = self.search
        state = parse_state("../../tests/avoid_eaten.json")
        print(state)

        game = Game('red', state)
        best_action = search.search(game, state)
        self.assertTupleEqual(((-2, -1), (-3, 0), 'MOVE'), best_action)

    def test_eat_blue(self):
        search = self.search
        state = parse_state("../../tests/eat_blue.json")
        print(state)

        game = Game('red', state)
        best_action = search.search(game, state)
        self.assertTupleEqual(((0, 0), (2, -2), 'JUMP'), best_action)

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

    def test_pass(self):
        search = self.search
        state = parse_state("../../tests/pass.json")
        print(state)
        game = Game('blue', state)
        best_action = search.search(game, state)
        self.assertTupleEqual((None, None, 'PASS'), best_action)

    def test_weird(self):
        search = self.search
        state = parse_state("../../tests/weird.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        print(best_action)

    def test_busy(self):
        search = self.search
        state = parse_state("../../tests/busy.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        print(best_action)
