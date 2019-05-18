from math import inf
from artificial_idiot.search.search import Search


# Alpha - Beta search
# from AIMA p 170
class AlphaBetaSearch(Search):

    def __init__(self, utility_generator, terminal_test):
        self.terminal_test = terminal_test
        self.utility_generator = utility_generator

    def min_value(self, game, state, depth, a, p):
        if self.terminal_test(state, depth):
            utility = self.utility_generator(state)
            return utility('red'), None
        depth += 1
        v = +inf
        action = None
        # take two steps assuming opponents are in alliance
        for green_action in game.actions(state):
            state_1 = game.result(state, green_action)
            for blue_action in game.actions(state_1):
                state_2 = game.result(state_1, blue_action)
                v_, action = self.max_value(game, state_2, depth, a, p)
                # print(f'{depth} {green_action} {blue_action} {float(v_):.2}')
                v = min(v, v_)
                if v <= a:
                    return v, action
                p = min(p, v)
        return v, action

    def max_value(self, game, state, depth, a, p):
        if self.terminal_test(state, depth):
            utility = self.utility_generator(state)
            return utility('red'), None
        depth += 1
        v = -inf
        best_action = None
        for action in game.actions(state):
            # print(action)
            s_ = game.result(state, action)
            v_, _ = self.min_value(game, s_, depth, a, p)
            # print(f'{depth} {action} {float(v_):.2}')
            # print(a, p)
            if v_ > v:
                best_action = action
                v = v_
            # opponent won't allow you to chose a better move
            if v >= p:
                return v, action
            a = max(a, v)
        return v, best_action

    def search(self, game, state, depth=0):
        best_v, best_action = self.max_value(game, state, depth, -inf, inf)
        # print('Best utility is', best_v)
        return best_action
