from artificial_idiot.player import *

print("======================")
pp = ParanoidPlayer_Naive
mn = MaxNPlayer

"""
* weights are defined beforehand
An evaluator that considers
1. (max) number of player piece
2. (max neg) leading player's distance from winning
3. (max) distance of excess piece to opponent exit,
    try to block leading player from exiting
4. (max neg) networth of other players' pieces
5. (max) negative sum distance to goal
6. (max) number of completed piece
7. (max) number of excess piece
"""

weights = [100, -10, 6, -20, 5, 20, 80]
evaluator_generator = MinimaxEvaluator(weights)
cutoff = DepthLimitCutoff(3)
# open_book = OpenGameBook("gather")
open_book = None
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
