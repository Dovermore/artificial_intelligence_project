from artificial_idiot.search.a_star import AStar
from artificial_idiot.player import Player, PlayerFactory


Player = PlayerFactory.get_type_factory(Player)(search_algorithm=AStar())
