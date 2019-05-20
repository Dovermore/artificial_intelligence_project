from artificial_idiot.search.search import Search


class CompositionSearch(Search):
    """
    Defines a composite search pattern where based on the number of players
    alive the behavior will swap to different search methods
        3 player -> beginning: book + search
        2 player -> search
        1 player -> part A heuristic
    """
    def __init__(self, three_strat=None, two_strat=None, one_strat=None):
        self.three = three_strat
        self.two = two_strat
        self.one = one_strat

    def search(self, game, state, **kwargs):
        if not state.piece_to_pos[state.colour]:
            return None, None, "PASS"
        if len(state.remaining_colours) == 3:
            return self.three.search(game, state, **kwargs)
        elif len(state.remaining_colours) == 2:
            return self.two.search(game, state, **kwargs)
        else:
            print('One Search')
            return self.one.search(game, state, **kwargs)
