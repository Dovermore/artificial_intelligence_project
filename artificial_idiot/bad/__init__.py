from artificial_idiot.search.bad import Bad
from artificial_idiot.player import PlayerFactory, Player


Player = PlayerFactory.get_type_factory(Player)(search_algorithm=Bad())
