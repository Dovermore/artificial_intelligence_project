from artificial_idiot.search.search import Search
from artificial_idiot.evaluation.evaluator_generator import *


class CompositionSearch(Search):
    """
    Defines a composite search pattern where based on the number of players
    alive the behavior will swap to different search methods
        3 player -> beginning: book + search
        2 player -> search
        1 player -> part A heuristic
    """
    def __init__(self, book=None, aggressive=None, defensive=None):
        self.book = book
        self.aggressive = aggressive
        self.defensive = defensive

    def search(self, game, state, **kwargs):
        if not state.piece_to_pos[state.colour]:
            return None, None, "PASS"

        if self.book is not None:
            action = self.book.search(game, state)
            if action is not None:
                return action
        print(f"Aggressive: {self.should_aggressive(game, state)}")
        if self.should_aggressive(game, state):
            return self.aggressive.search(game, state, **kwargs)
        else:
            return self.defensive.search(game, state, **kwargs)

    @staticmethod
    def should_aggressive(game, state):
        piece_to_pos = state.piece_to_pos
        distances = sorted(
            [(modified_negative_sum_distance(state, player), player)
             for player in piece_to_pos], reverse=True)
        print(distances, state.colour)
        # Losing
        if distances[0][1] != state.colour and \
                distances[0][1] != distances[1][1]:
            return True
        return False

