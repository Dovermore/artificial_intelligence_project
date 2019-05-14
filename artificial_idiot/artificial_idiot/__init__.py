from artificial_idiot.player import *

# Player = PlayerFactory.get_type_factory(MaxNPlayer)()
Player = PlayerFactory.get_type_factory(Player)(
    search_algorithm=OpeningGame("gather"), game_type=Game,
    evaluator=player_evaluator)

if __name__ == "__main__":
    import json
    from artificial_idiot.util.json_parser import JsonParser

    def random_agent_test():
        player = RandomAgent(colour="red", initial_state=None, seed=10)
        red_move =('MOVE', ((-3, 0), (-2, -1)))
        green_move = ("MOVE", ((0, -3), (0, -2)))
        blue_move = ('MOVE', ((3,0), (2,0)))
        assert (player.action() == red_move)
        player.update("red", red_move)
        player.update("green", green_move)
        player.update("blue", blue_move)
        assert (player.action() == ('MOVE', ((-3, 3), (-2, 2))))
        player.update("blue", ("PASS", None))

    def max_n_agent_test():
        f = open("../tests/bug1.json")
        pos_dict, colour, completed = JsonParser(json.load(f)).parse()
        initial_state = State(pos_dict, colour, completed)
        evaluator = MyEvaluator()
        cutoff = DepthLimitCutoff(max_depth=3)
        player = MaxNAgent(colour="red", initial_state=initial_state,
                           evaluator=evaluator, cutoff=cutoff)
        print(player.state)
        print(player.action())

    def random_agent_pass_test():
        f = open("../tests/bug1.json")
        pos_dict, colour, completed = JsonParser(json.load(f)).parse()
        initial_state = State(pos_dict, colour, completed)
        player = RandomAgent(colour="red", initial_state=initial_state,
                             seed=10)
        print(player.state)
        print(player.action())

    random_agent_test()
    max_n_agent_test()
    random_agent_pass_test()
