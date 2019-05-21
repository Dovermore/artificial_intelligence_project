from math import inf
from artificial_idiot.search.search import Search
from random import random


# Alpha - Beta search
# from AIMA p 170
class AlphaBetaSearch(Search):

    def __init__(self, utility_generator, terminal_test):
        self.terminal_test = terminal_test
        self.utility_generator = utility_generator
        self.debug = False

    def state_value(self, state):
        utility_generator = self.utility_generator(state)
        return utility_generator("red")

    # def min_value(self, game, state, depth, a, b):
    #     if self.terminal_test(state, depth):
    #         return self.utility_generator(state)("red"), None
    #     depth += 1
    #     value = +inf
    #
    #     actions = game.actions(state)
    #     states = map(lambda x: game.result(state, x), actions)
    #     actions_states = map(lambda x:
    #                          (self.state_value(x[1]),
    #                           random(), x[0], x[1]), zip(actions, states))
    #     actions_states = sorted(actions_states)
    #     for _, _, green_action, state_1 in actions_states:
    #         actions = game.actions(state_1)
    #         states = map(lambda x: game.result(state_1, x), actions)
    #         actions_states = map(lambda x:
    #                              (self.state_value(x[1]),
    #                               random(), x[0], x[1]), zip(actions, states))
    #         actions_states = sorted(actions_states)
    #
    #         for _, _, blue_action, state_2 in actions_states:
    #             new_value, opponent_action = self.max_value(game, state_2,
    #                                                         depth, a, b)
    #             if self.debug:
    #                 print(f'{depth} {green_action} {blue_action} '
    #                       f'{float(new_value):.3}')
    #             value = min(value, new_value)
    #             if value <= a:
    #                 return value, None
    #             b = min(b, value)
    #     return value, None

    def min_value(self, game, state, depth, a, b):
        if self.terminal_test(state, depth):
            return self.utility_generator(state)("red"), None
        depth += 1
        value = +inf
        actions = game.actions(state)
        states = list(map(lambda x: game.result(state, x), actions))

        actions_states = list(zip(actions, states))
        actions_states = filter(lambda x: x[0][2] == "JUMP", actions_states)
        for green_action, state_1 in actions_states:
            jumping_colour, jumpedover_colour = \
                game.jump_action_classification(state, green_action)
            if jumpedover_colour != "red":
                continue
            actions_1 = game.actions(state_1)
            states_1 = map(lambda x: game.result(state_1, x), actions_1)
            actions_states = list(zip(actions_1, states_1))
            actions_states = filter(lambda x: x[0][2] == "JUMP",
                                    actions_states)

            for blue_action, state_2 in actions_states:
                jumping_colour, jumpedover_colour = \
                    game.jump_action_classification(state_1, blue_action)
                if jumpedover_colour != "red":
                    continue
                new_value, opponent_action = self.max_value(game, state_2,
                                                            depth, a, b)
                if self.debug:
                    print(f'{depth} {green_action} {blue_action} '
                          f'{float(new_value):.3}')
                value = min(value, new_value)
                if value <= a:
                    return value, None
                b = min(b, value)
        if value != +inf:
            return value, None

        actions_states = map(lambda x:
                             (self.state_value(x[1]),
                              random(), x[0], x[1]), zip(actions, states))
        actions_states = sorted(actions_states)

        for _, _, green_action, state_1 in actions_states[:1]:
            actions = game.actions(state_1)
            states = map(lambda x: game.result(state_1, x), actions)
            actions_states = map(lambda x:
                                 (self.state_value(x[1]),
                                  random(), x[0], x[1]), zip(actions, states))
            actions_states = sorted(actions_states)

            for _, _, blue_action, state_2 in actions_states[:1]:
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
        states = list(map(lambda x: game.result(state, x), actions))
        actions_states = map(lambda x:
                             (self.state_value(x[1]),
                              random(), x[0], x[1]), zip(actions, states))
        actions_states = sorted(actions_states, reverse=True)

        if depth == 1:
            for _, _, action, child in actions_states:
                jump_type = game.jump_action_classification(state, action)
                if jump_type is not None and jump_type[0] != jump_type[1]:
                    break
            else:
                depth = self.terminal_test.max_depth - 1
            for _, _, action, child in actions_states:
                new_value, opponent_action = self.min_value(game, child,
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
        # No need to search for the best one
        else:
            for _, _, action, child in actions_states:
                if action[2] in ["JUMP", "EXIT"]:
                    new_value, opponent_action = self.min_value(game, child,
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

    # def max_value(self, game, state, depth, a, b):
    #     if self.terminal_test(state, depth):
    #         return self.utility_generator(state)("red"), None
    #     depth += 1
    #     value = -inf
    #     best_action = None
    #
    #     actions = game.actions(state)
    #     states = list(map(lambda x: game.result(state, x), actions))
    #     actions_states = map(lambda x:
    #                          (self.state_value(x[1]),
    #                           random(), x[0], x[1]), zip(actions, states))
    #     actions_states = sorted(actions_states, reverse=True)
    #
    #     for _, _, action, child in actions_states:
    #         new_value, opponent_action = self.min_value(game, child,
    #                                                     depth, a, b)
    #         # print(new_value)
    #         if self.debug:
    #             print(f'{depth} {action} {float(new_value):.3}')
    #         if new_value > value:
    #             best_action = action
    #             value = new_value
    #         # opponent won't allow you to chose a better move
    #         if value >= b:
    #             return value, best_action
    #         a = max(a, value)
    #     return value, best_action

    def search(self, game, state, depth=0):
        best_v, best_action = self.max_value(game, state, depth, -inf, inf)
        if (self.debug):
            print('Best utility is', best_v)
        return best_action
