from artificial_idiot.search.search import Search


class CompositionSearch(Search):
    # TODO Combine different strategies:
    #  3 player -> beginning: book + A star + search
    #  2 player -> paranoid
    #  1 player -> part A heuristic
    def __init__(self, three=None, two=None, one=None):
        self.three = three
        self.two = two
        self.one = one

    def search(self, game, state, **kwargs):
        if len(state.remaining_colours) == 3:
            return self.three(game, state)
        elif len(state.remaining_colours) == 2:
            return self.two(game, state)
        else:
            return self.one(game, state)


