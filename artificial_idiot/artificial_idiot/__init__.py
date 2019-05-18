from artificial_idiot.player import ParanoidPlayer_Naive, RandomAgent, MaxNPlayer, Player, Game

print("======================")
P0 = RandomAgent
P1 = MaxNPlayer
P2 = ParanoidPlayer_Naive

# Player = PlayerFactory.get_type_factory(MaxNPlayer)()
# Player = PlayerFactory.get_type_factory(Player)(
#     search_algorithm=OpenGameBook("gather"), game_type=Game,
#     evaluator=player_evaluator)
