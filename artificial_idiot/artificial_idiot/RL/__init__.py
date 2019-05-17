from artificial_idiot.player import *
import glob
import os

time_stamp = 20190516001133
path = f"/Users/Dovermore/Documents/2019t1/COMP30024-AritificialIntelligence/ArtificialIdiotProject/artificial_idiot/artificial_idiot/machine_learning/{time_stamp}"
checkpoint_path = f"{path}/checkpoints"
checkpoint_files = glob.glob(f'{checkpoint_path}/*')
latest_checkpoint = max(checkpoint_files, key=os.path.getctime)
final_file = f"{path}/network"
model = latest_checkpoint
agent = ParametrisedRL.from_file(model, simple_grid_extractor)


# Player = PlayerFactory.get_type_factory(MaxNPlayer)()
Player = PlayerFactory.get_type_factory(RLPlayer)(
    search_algorithm=OpeningGame("gather"), game_type=Game,
    evaluator=player_evaluator)
