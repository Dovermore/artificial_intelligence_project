from unittest import TestCase
from artificial_idiot.game.game import Game
from artificial_idiot.game.state import State
from artificial_idiot.evaluation.evaluator_generator import NaiveEvaluatorGenerator, MinimaxEvaluator
from artificial_idiot.util.json_parser import JsonParser
from artificial_idiot.search.mini_max import AlphaBetaSearch
from artificial_idiot.search.search_cutoff.cutoff import DepthLimitCutoff
import json


def parse_state(file_name):
    f = open(file_name)
    pos_dict, colour, completed = JsonParser(json.load(f)).parse()
    return State(pos_dict, colour, completed)


class TestParnoidPlayer(TestCase):
    # num_exited_piece, total_number_pieces, utility_distance
    """
    * weights are defined beforehand
    An evaluator that considers
    1. (max) number of player piece
    2. (max neg) leading player's distance from winning
    3. (max) distance of excess piece to opponent exit,
        try to block leading player from exiting
    4. (max neg) net worth of other players' pieces
    5. (max) negative sum distance to goal
    6. (max) number of completed piece
    """
    weights = [100, -10, 6, -60, 5, 1000]
    evaluator_generator = MinimaxEvaluator(weights)
    cutoff = DepthLimitCutoff(2)
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

    def test_exit(self):
        search = self.search
        state = parse_state("../../tests/please_exit.json")
        print(state)
        game = Game('red', state)
        best_action = search.search(game, state)
        print(best_action)
        self.assertEqual('EXIT', best_action[-1])

    def test_pass(self):
        search = self.search
        state = parse_state("../../tests/pass.json")
        print(state)
        game = Game('blue', state)
        best_action = search.search(game, state)
        self.assertTupleEqual((None, None, 'PASS'), best_action)

    def test_dominates(self):
        search = self.search
        state = parse_state("../../tests/red_dominates.json")
        print(state)
        game = Game('blue', state)
        best_action = search.search(game, state)
        print(best_action)

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
