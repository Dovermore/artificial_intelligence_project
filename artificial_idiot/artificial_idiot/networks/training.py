from artificial_idiot.networks import networks
from artificial_idiot.search.RL import (
    ParametrisedRL, simple_grid_extractor
)
from artificial_idiot.evaluation.evaluator import (
    DummyEvaluator
)
import glob
import os

from artificial_idiot.game.state import State
from artificial_idiot.game.game import Game
from artificial_idiot.player import Player
from artificial_idiot.game.node import *

time_stamp = 20190515204758
path = f"/Users/Dovermore/Documents/2019t1/COMP30024-AritificialIntelligence/ArtificialIdiotProject/artificial_idiot/artificial_idiot/machine_learning/{time_stamp}"
checkpoint_path = f"{path}/checkpoints"
checkpoint_files = glob.glob(f'{checkpoint_path}/*')
latest_checkpoint = max(checkpoint_files, key=os.path.getctime)
final_file = f"{path}/network"


architectures = networks.architectures
initial_state = State(Player.start_config, "red")
game = Game("red", initial_state, DummyEvaluator())

four_layer_relu_model = latest_checkpoint
# agent = ParametrisedRL(*architectures["two_sig"])
# agent = ParametrisedRL(*architectures["four_lkrl"])
agent = ParametrisedRL.from_file(four_layer_relu_model, simple_grid_extractor)
# agent.td_train(game, initial_state, debug=1, checkpoint_interval=10)
# agent.td_train(game, initial_state, debug=0.01, node_type=InitialRLNode)
agent.td_train(game, initial_state, debug=0.01, node_type=WinningRLNode)

