from artificial_idiot.search.search import Search


class MultiPlayerSearch(Search):

    def __init__(self, book=None, search_algorithm=None):
        self.book = book
        self.book_finished = False
        if book is None:
            self.book_finished = True
        self.search_algorithm = search_algorithm

    def search(self, game, state, **kwargs):
        if not self.book_finished:
            action = self.book.search(game, state, **kwargs)
            if action is not None:
                return action
            else:
                self.book_finished = True
        return self.search_algorithm.search(game, state, **kwargs)

