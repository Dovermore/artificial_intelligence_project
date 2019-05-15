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

architectures = {
    "linear": (networks.simple_linear_network(), simple_grid_extractor),
    "two_sig": (networks.two_layer_sigmoid_network(), simple_grid_extractor),
    "four_lkrl": (networks.four_layer_leaky_relu_network(),
                  simple_grid_extractor)
}
initial_state = State(Player.start_config, "red")
game = Game("red", initial_state, DummyEvaluator())

agent = ParametrisedRL(*architectures["two_sig"])
agent.td_train(game, initial_state, debug=False, checkpoint_interval=10)
# agent.td_train(game, initial_state)

