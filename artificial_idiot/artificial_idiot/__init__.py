from artificial_idiot.player import *

print("======================")
pp = ParanoidPlayer_Naive
mn = MaxNPlayer

"""
* weights are defined beforehand
An evaluator that considers
1. (max) number of player piece
2. (max neg) leading player's distance from winning
3. (max) offset negative distance of excess piece to opponent exit,
    try to block leading player from exiting
4. (max neg) networth of other players' pieces
5. (max) negative sum distance to goal
6. (max) number of completed piece
7. (max) excess pieces
8. (max) negative corner distance (very low weight, only triggered when
        not enough piece)
"""

# open_book = OpenGameBook("gather")
open_book = OpenGameBook("edge")
# open_book = None

# weights = [100, -7, 2, -10, 1, 10, 20]
# weights = [100, -20, 15, -50, 15, 14, 80]
# defensive_weights = [100, -10, 6, -60, 5, 1000]
cutoff = DepthLimitCutoff(4)

aggressive_weights = [100, -5, 10, -10, 1, 20, 100, 1]
evaluator_generator = MinimaxEvaluator(aggressive_weights)
aggressive_search = AlphaBetaSearch(evaluator_generator, cutoff)

defensive_weights = [100, 0, 0, 0, 1, 50, 50, 0]
evaluator_generator = MinimaxEvaluator(defensive_weights)
defensive_search = AlphaBetaSearch(evaluator_generator, cutoff)

composite_search = CompositionSearch(open_book, aggressive_search,
                                     defensive_search)

mix = PlayerFactory.get_type_factory(Player)(
    search_algorithm=composite_search,
    game_type=Game
)

# red, green, blue = mix, RandomPlayer, RandomPlayer
red, green, blue = mix, GreedyPlayer, GreedyPlayer
# red, green, blue = mix, pp, mn
