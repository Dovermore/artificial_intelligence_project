from artificial_idiot.player import *

print("======================")
pp = ParanoidPlayer_Naive
mn = MaxNPlayer

weights = [10, -2, 4, -0.5, 2, 0.5]
evaluator_generator = MinimaxEvaluator(weights)
cutoff = DepthLimitCutoff(3)
open_book = OpenGameBook("gather")
search = AlphaBetaSearch(evaluator_generator, cutoff)

three_player = MultiPlayerSearch(book=open_book, search_algorithm=search)
two_player = MultiPlayerSearch(search_algorithm=search)
one_player = AStar()

composite_search = CompositionSearch(three_player, two_player, one_player)

mix = PlayerFactory.get_type_factory(Player)(
    search_algorithm=composite_search,
    game_type=Game
)


red, green, blue = pp, mn, mix
