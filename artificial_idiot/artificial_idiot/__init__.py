from artificial_idiot.player import ParanoidPlayer_Naive, GreedyPlayer, RandomPlayer, MaxNPlayer, ParanoidPlayer_Advance

print("======================")
red = MaxNPlayer
green = ParanoidPlayer_Naive
blue = RandomPlayer

# Player = PlayerFactory.get_type_factory(MaxNPlayer)()
# Player = PlayerFactory.get_type_factory(Player)(
#     search_algorithm=OpenGameBook("gather"), game_type=Game,
#     evaluator=player_evaluator)
