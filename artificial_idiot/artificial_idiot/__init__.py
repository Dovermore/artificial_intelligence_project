from artificial_idiot.player import *

print("======================")
red = ParanoidPlayer_Naive
green = MaxNPlayer
# blue = MaxNPlayer

# Player = PlayerFactory.get_type_factory(MaxNPlayer)()
# Player = PlayerFactory.get_type_factory(Player)(
#     search_algorithm=OpenGameBook("gather"), game_type=Game,
#     evaluator=player_evaluator)

weights = [10, 100, 1]
evaluator_generator = NaiveEvaluatorGenerator(weights)
cutoff = DepthLimitCutoff(2)
open_book = OpenGameBook("gather")
search = AlphaBetaSearch(evaluator_generator, cutoff)

three_player = MultiPlayerSearch(book=open_book, search_algorithm=search)
two_player = MultiPlayerSearch(search_algorithm=search)
one_player = AStar()

composite_search = CompositionSearch(three_player, two_player, one_player)

blue = PlayerFactory.get_type_factory(Player)(
    search_algorithm=composite_search,
    game_type=Game
)
