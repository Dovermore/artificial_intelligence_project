from artificial_idiot.search.search import Search
from artificial_idiot.evaluation.evaluator_generator import *
from time import process_time


class CompositionSearch(Search):
    """
    Defines a composite search pattern where based on the number of players
    alive the behavior will swap to different search methods
        3 player -> beginning: book + search
        2 player -> search
        1 player -> part A heuristic
    """
    def __init__(self, book=None, aggressive=None, defensive=None,
                 simple_aggressive=None, simple_defensive=None):
        self.book = book
        self.aggressive = aggressive
        self.defensive = defensive
        self.simple_aggressive = simple_aggressive
        self.simple_defensive = simple_defensive
        self.total_time = 0

    def search(self, game, state, **kwargs):

        start = process_time()
        if not state.piece_to_pos[state.colour]:
            return None, None, "PASS"

        if self.book is not None:
            action = self.book.search(game, state)
            if action is not None:
                return action

        if self.total_time < 50:
            aggressive = self.aggressive
            defensive = self.defensive
        else:
            aggressive = self.simple_aggressive
            defensive = self.simple_defensive

        print(f"Aggressive: {self.should_aggressive(game, state)}")
        if self.should_aggressive(game, state):
            action = aggressive.search(game, state, **kwargs)
        else:
            action = defensive.search(game, state, **kwargs)
        self.total_time += process_time() - start
        return action

    @staticmethod
    def should_aggressive(game, state):
        piece_to_pos = state.piece_to_pos
        neg_distances = sorted(
            [(modified_negative_sum_distance(state, player), player)
             for player in piece_to_pos], reverse=True)
        print(neg_distances, state.colour)
        # Losing
        max_neg_dist = neg_distances[0][0]
        for dist, player in neg_distances:
            if player == state.colour and dist < max_neg_dist:
                return True
        return False

