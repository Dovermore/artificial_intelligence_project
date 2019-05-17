from artificial_idiot.search.action_book.action_book import SimpleActionBook
from artificial_idiot.search.search import Search


class OpeningGame(Search):
    """
    This class defines the open game search strategy
    """

    STRATEGIES = {"gather"}

    def __init__(self, strategy="gather"):
        """
        Init with pre-computed strategy pattern in our open book database
        :param strategy: the name of the strategy
        """
        assert strategy in self.STRATEGIES
        self.action_book = SimpleActionBook.read(strategy)
        self.action = None

    def search(self, game, state, **kwargs):
        self.action = self.action_book.get_action(state)
        return self.action
