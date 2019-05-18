from artificial_idiot.player import RandomAgent
from artificial_idiot.player import Player, PlayerFactory


Player = PlayerFactory.get_type_factory(RandomAgent)()
