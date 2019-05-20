from artificial_idiot.search.search import Search


class MultiPlayerSearch(Search):
    #  3 player -> beginning: book + search
    def __init__(self, book=None, search=None):
        self.book = book
        self.book_finished = False
        self.search = search

    def search(self, game, state, **kwargs):
        if not self.book_finished:
            return self.book.search(game, state, **kwargs)
        return self.search.search(game, state, **kwargs)

