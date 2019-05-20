from math import inf
from artificial_idiot.search.search import Search


# Alpha - Beta search
# from AIMA p 170
class AlphaBetaSearch(Search):

    def __init__(self, utility_generator, terminal_test):
        self.terminal_test = terminal_test
        self.utility_generator = utility_generator
        self.debug = False

    def state_value(self, state, colour):
        utility_generator = self.utility_generator(state)
        return utility_generator(colour), None

    def min_value(self, game, state, depth, a, b):
        if self.terminal_test(state, depth):
            return self.utility_generator(state)("red"), None
        depth += 1
        utility = +inf

        actions = game.actions(state)
        states = map(lambda x: game.result(state, x), actions)
        states = sorted(states,
                        key=lambda x: self.utility_generator(x)("red"),
                        reverse=True)

        for green_action, state_1 in zip(actions, states):
            state_1 = game.result(state, green_action)

            actions = game.actions(state_1)
            states = map(lambda x: game.result(state, x), actions)
            states = sorted(states,
                            key=lambda x: self.utility_generator(x)("red"),
                            reverse=True)

            for blue_action, state_2 in zip(actions, states):
                v_, opponent_action = self.max_value(game, state_2,
                                                     depth, a, b)
                if self.debug:
                    print(f'{depth} {green_action} {blue_action} '
                          f'{float(v_):.3}')
                utility = min(utility, v_)
                if utility <= a:
                    return utility, None
                b = min(b, utility)
        return utility, None

    def max_value(self, game, state, depth, a, b):
        if self.terminal_test(state, depth):
            return self.utility_generator(state)("red"), None
        depth += 1
        utility = -inf
        best_action = None

        actions = game.actions(state)
        states = map(lambda x: game.result(state, x), actions)
        states = sorted(states,
                        key=lambda x: self.utility_generator(x)("red"),
                        reverse=True)

        for action, state in zip(actions, states):
            if self.debug:
                print(action)
            new_utility, opponent_action = self.min_value(game, state,
                                                          depth, a, b)
            if self.debug:
                print(f'{depth} {action} {float(new_utility):.3}')
            if new_utility > utility:
                best_action = action
                utility = new_utility
            # opponent won't allow you to chose a better move
            if utility >= b:
                return utility, best_action
            a = max(a, utility)
        return utility, best_action

    def search(self, game, state, depth=0):
        best_v, best_action = self.max_value(game, state, depth, -inf, inf)
        if (self.debug):
            print('Best utility is', best_v)
        return best_action
