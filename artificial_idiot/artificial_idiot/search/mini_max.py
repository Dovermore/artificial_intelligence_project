from math import inf
from artificial_idiot.search.search import Search


# Alpha - Beta search
# from AIMA p 170
class AlphaBetaSearch(Search):

    def __init__(self, utility_generator, terminal_test):
        self.terminal_test = terminal_test
        self.utility_generator = utility_generator
        self.debug = False

    def min_value(self, game, state, depth, a, p):
        if self.terminal_test(state, depth):
            utility_generator = self.utility_generator(state)
            return utility_generator('red'), None
        depth += 1
        utility = +inf

        actions = game.actions(state)
        # TODO
        # take two steps assuming opponents are in alliance
        for green_action in actions:
            state_1 = game.result(state, green_action)
            for blue_action in game.actions(state_1):
                state_2 = game.result(state_1, blue_action)
                v_, opponent_action = self.max_value(game, state_2, depth, a, p)
                if self.debug:
                    print(f'{depth} {green_action} {blue_action} {float(v_):.3}')
                utility = min(utility, v_)
                if utility <= a:
                    return utility, None
                p = min(p, utility)
        return utility, None

    def max_value(self, game, state, depth, a, p):
        if self.terminal_test(state, depth):
            utility_generator = self.utility_generator(state)
            return utility_generator('red'), None
        depth += 1
        utility = -inf
        best_action = None
        for action in game.actions(state):
            if (self.debug):
                print(action)
            s_ = game.result(state, action)
            new_utility, opponent_action = self.min_value(game, s_, depth, a, p)
            if (self.debug):
                print(f'{depth} {action} {float(new_utility):.3}')
            if new_utility > utility:
                best_action = action
                utility = new_utility
            # opponent won't allow you to chose a better move
            if utility >= p:
                return utility, best_action
            a = max(a, utility)
        return utility, best_action

    def search(self, game, state, depth=0):
        best_v, best_action = self.max_value(game, state, depth, -inf, inf)
        if (self.debug):
            print('Best utility is', best_v)
        return best_action
