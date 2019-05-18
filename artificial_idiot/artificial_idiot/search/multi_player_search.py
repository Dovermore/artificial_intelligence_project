from artificial_idiot.search.search import Search


class MultiPlayerSearch(Search):
    #  3 player -> beginning: book + search + a star
    def __init__(self, book=None, search=None, a_star=None):
        self.book = book
        self.book_finished = False
        self.search = search
        self.a_star = a_star

    def search(self, game, state, **kwargs):
        pass

