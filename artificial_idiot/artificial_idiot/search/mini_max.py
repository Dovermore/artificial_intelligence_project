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
        value = +inf

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
                new_value, opponent_action = self.max_value(game, state_2,
                                                            depth, a, b)
                if self.debug:
                    print(f'{depth} {green_action} {blue_action} '
                          f'{float(new_value):.3}')
                value = min(value, new_value)
                if value <= a:
                    return value, None
                b = min(b, value)
        return value, None

    def max_value(self, game, state, depth, a, b):
        if self.terminal_test(state, depth):
            return self.utility_generator(state)("red"), None
        depth += 1
        value = -inf
        best_action = None

        actions = game.actions(state)
        states = map(lambda x: game.result(state, x), actions)
        states = sorted(states,
                        key=lambda x: self.utility_generator(x)("red"),
                        reverse=True)

        for action, state in zip(actions, states):
            if self.debug:
                print(action)
            new_value, opponent_action = self.min_value(game, state,
                                                          depth, a, b)
            if self.debug:
                print(f'{depth} {action} {float(new_value):.3}')
            if new_value > value:
                best_action = action
                value = new_value
            # opponent won't allow you to chose a better move
            if value >= b:
                return value, best_action
            a = max(a, value)
        return value, best_action

    def search(self, game, state, depth=0):
        best_v, best_action = self.max_value(game, state, depth, -inf, inf)
        if (self.debug):
            print('Best utility is', best_v)
        return best_action
