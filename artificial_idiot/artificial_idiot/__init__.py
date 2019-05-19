from artificial_idiot.player import ParanoidPlayer_Naive, GreedyPlayer, RandomPlayer, MaxNPlayer, Player, Game, ParanoidPlayer_Advance

print("======================")
red = ParanoidPlayer_Naive
green = MaxNPlayer
blue = MaxNPlayer

# Player = PlayerFactory.get_type_factory(MaxNPlayer)()
# Player = PlayerFactory.get_type_factory(Player)(
#     search_algorithm=OpenGameBook("gather"), game_type=Game,
#     evaluator=player_evaluator)
