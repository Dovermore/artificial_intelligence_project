from artificial_idiot.search import a_star
from artificial_idiot.search import composition
from artificial_idiot.search import search
from artificial_idiot.search import max_n
from artificial_idiot.search import open_game
from artificial_idiot.search import random
from artificial_idiot.search import paranoid
from artificial_idiot.search import uct


from artificial_idiot.search.search_cutoff import cutoff


if __name__ == '__main__':
    MaxN = max_n.MaxN
    from artificial_idiot.evaluation.evaluator import MyEvaluator
    from artificial_idiot.search.search_cutoff.cutoff import DepthLimitCutoff
    from artificial_idiot.game import Game
    from artificial_idiot.game.state import State
    from artificial_idiot.util.json_parser import JsonParser
    import json

    def test_exit():
        f = open("../tests/simple.json")
        pos_dict, colour, completed = JsonParser(json.load(f)).parse()
        evaluator = MyEvaluator()
        game = Game(colour, State(pos_dict, colour, completed), evaluator)
        cutoff = DepthLimitCutoff(max_depth=3)
        search = MaxN(evaluator, cutoff, n_player=3)
        print(search.search(game, game.initial_state))

    def test_only_one_possible_move():
        f = open("../tests/only_one_move.json")
        evaluator = MyEvaluator()
        pos_dict, colour, completed = JsonParser(json.load(f)).parse()
        game = Game(colour, State(pos_dict, colour, completed), evaluator)
        cutoff = DepthLimitCutoff(max_depth=3)
        search = MaxN(evaluator, cutoff, n_player=3)
        print(search.search(game, game.initial_state))

    # test_exit()
    test_only_one_possible_move()
