from artificial_idiot.search.a_star import AStar
from artificial_idiot.player import Player, PlayerFactory, RandomAgent, ParanoidAgent, MaxNAgent
from artificial_idiot.evaluation.evaluator_generator import *
from artificial_idiot.search.search_cutoff import *


Player = PlayerFactory.get_type_factory(Player)(search_algorithm=AStar())

P0 = PlayerFactory.get_type_factory(RandomAgent)()

# utility_pieces, num_exited_piece, utility_distance
weights = [2, 100, 1]
# colour, initial_state, evaluator, cutoff
P1 = PlayerFactory.get_type_factory(MaxNAgent)(evaluator=NaiveEvaluatorGenerator(weights), cutoff=DepthLimitCutoff(3))
# colour, initial_state, evaluator, cutoff
P2 = PlayerFactory.get_type_factory(ParanoidAgent)(evaluator=NaiveEvaluatorGenerator(weights), cutoff=DepthLimitCutoff(4))