from artificial_idiot.player import *

print("======================")
pp = ParanoidPlayer_Naive
mn = MaxNPlayer

"""
* weights are defined beforehand
An evaluator that considers
1. (max) number of needed player piece
2. (max neg) leading player's distance from winning
3. (max) offset negative distance of excess piece to opponent exit
    try to block leading player from exiting
4. (max neg) networth of other players' pieces
5. (max) negative sum distance to goal
6. (max) number of completed piece
7. (max) excess pieces
8. (max) negative corner distance
9. (max) pieces in corner
10. (min) piece in edge of enemy exit
"""
# open_book = OpenGameBook("gather")
open_book = OpenGameBook("edge")
# open_book = None

# weights = [100, -7, 2, -10, 1, 10, 20]
# weights = [100, -20, 15, -50, 15, 14, 80]
# defensive_weights = [100, -10, 6, -60, 5, 1000]
cutoff = DepthLimitCutoff(4)

# weights = [10, 100, 1]
# evaluator_generator = NaiveEvaluatorGenerator(weights)

# Help aggressively take over pieces
aggressive_weights = [1000, -10, 80, -500, 10, 0, 1000, 40, 200, -19]
evaluator_generator = MinimaxEvaluator(aggressive_weights)
aggressive_search = AlphaBetaSearch(evaluator_generator, cutoff)

# Help guide toward exit
defensive_weights = [1000, -10, 1, -5, 30, 200, 100, 0, 5, -5]
evaluator_generator = MinimaxEvaluator(defensive_weights)
defensive_search = AlphaBetaSearch(evaluator_generator, cutoff)


cutoff = DepthLimitCutoff(2)
# Help aggressively take over pieces
evaluator_generator = MinimaxEvaluator(aggressive_weights)
simple_aggressive_search = AlphaBetaSearch(evaluator_generator, cutoff)

# Help guide toward exit
evaluator_generator = MinimaxEvaluator(defensive_weights)
simple_defensive_search = AlphaBetaSearch(evaluator_generator, cutoff)


composite_search = CompositionSearch(open_book, aggressive_search,
                                     defensive_search,
                                     simple_aggressive_search,
                                     simple_defensive_search)

mix = PlayerFactory.get_type_factory(Player)(
    search_algorithm=composite_search,
    game_type=Game
)

# red, green, blue = mix, RandomPlayer, RandomPlayer
# red, green, blue = pp, GreedyPlayer, GreedyPlayer
# red, green, blue = mix, GreedyPlayer, GreedyPlayer
# red, green, blue = mix, pp, pp
red, green, blue = mix, pp, mn
