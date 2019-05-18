from artificial_idiot.player import *

print(help('modules'))
print("======================")
P0 = ParanoidPlayer_Naive
P1 = RandomAgent
P2 = MaxNAgent
Player = Player


# Player = PlayerFactory.get_type_factory(MaxNPlayer)()
Player = PlayerFactory.get_type_factory(Player)(
    search_algorithm=OpenGameBook("gather"), game_type=Game,
    evaluator=player_evaluator)
