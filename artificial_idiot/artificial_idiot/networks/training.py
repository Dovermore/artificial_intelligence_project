from artificial_idiot.networks import networks
from artificial_idiot.search.RL import (
    ParametrisedRL, simple_grid_extractor
)
from artificial_idiot.search.random import Random
from artificial_idiot.search.uct import UCTSearch
from artificial_idiot.search.max_n import MaxN
from artificial_idiot.search.open_game import OpeningGame

from artificial_idiot.search.search_cutoff.cutoff import DepthLimitCutoff
from artificial_idiot.evaluation.evaluator import (
    DummyEvaluator, WinLossEvaluator, MyEvaluator
)

from artificial_idiot.game.node import Node, BasicUCTNode
from artificial_idiot.game.state import State
from artificial_idiot.game.game import Game, NodeGame
from artificial_idiot.player import Player
import random
from copy import deepcopy

initial_state = State(Player.start_config, "red")
game = Game("red", initial_state, DummyEvaluator())

nn = networks.simple_linear_network()

agent = ParametrisedRL(nn, simple_grid_extractor)
agent.td_train(game, initial_state)

