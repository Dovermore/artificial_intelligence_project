from artificial_idiot.search.search import Search


class CompositionSearch(Search):
    # TODO Combine different strategies:
    #  3 player -> beginning: book + search
    #  2 player -> search
    #  1 player -> part A heuristic
    def __init__(self, three_strat=None, two_start=None, one_start=None):
        self.three = three_strat
        self.two = two_start
        self.one = one_start

    def search(self, game, state, **kwargs):
        if len(state.remaining_colours) == 3:
            return self.three(game, state)
        elif len(state.remaining_colours) == 2:
            return self.two(game, state)
        else:
            return self.one(game, state)
