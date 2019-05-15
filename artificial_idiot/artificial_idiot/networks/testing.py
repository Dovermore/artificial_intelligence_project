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


architectures = networks.architectures


loading = True
if loading:
    time_stamp = 20190515224313
    path = f"/Users/Dovermore/Documents/2019t1/COMP30024-AritificialIntelligence/ArtificialIdiotProject/artificial_idiot/artificial_idiot/machine_learning/{time_stamp}"
    checkpoint_path = f"{path}/checkpoints"
    checkpoint_files = glob.glob(f'{checkpoint_path}/*')
    latest_checkpoint = max(checkpoint_files, key=os.path.getctime)
    final_file = f"{path}/network"
    model = latest_checkpoint
    agent = ParametrisedRL.from_file(model, simple_grid_extractor)
else:
    # agent = ParametrisedRL(*architectures["two_sig"])
    agent = ParametrisedRL(*architectures["four_lkrl"])
    pass


# node_type = WinningRLNode
node_type = InitialRLNode

# policy = "greedy"
policy = "choice"

# debug = 3
# debug = 2
debug = 1

explore = 0
# explore = 0.1
# explore = 0.5

checkpoint_interval = 9999


initial_state = State(Player.start_config, "red")
game = Game("red", initial_state, DummyEvaluator())
agent.td_train(game, initial_state, debug=debug,
               node_type=node_type, policy=policy,
               explore=explore, checkpoint_interval=checkpoint_interval)
