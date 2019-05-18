from artificial_idiot.search.search import Search


class Bad(Search):

    """
    This class defines bad strategy fro testing only
    """

    def __init__(self) -> None:
        super().__init__()
        self.bad_actions = None

    def search(self, game, state, **kwargs):
        if self.bad_actions is None:
            self.bad_actions = self.generate_bad_action()
        return next(self.bad_actions)

    @staticmethod
    def generate_bad_action():
        forward = 1
        while True:
            if forward % 2:
                yield (-3, 0), (-2, 0), "MOVE"
            else:
                yield (-2, 0), (-3, 0), "MOVE"
            forward += 1
