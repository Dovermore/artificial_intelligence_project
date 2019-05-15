from artificial_idiot.search.search import Search
from artificial_idiot.game.state import State
from artificial_idiot.machine_learning.network import Network
from artificial_idiot.game.node import Node, RLNode
from collections import deque
import numpy as np
from random import random
from artificial_idiot.util.misc import randint


class ParametrisedRL(Search):
    """
    A monte carlo based reinforcement learning
    """
    def __init__(self, network, feature_extractor):
        super().__init__()
        self.network = network
        self.feature_extractor = feature_extractor

    def search(self, game, state, **kwargs):
        return self.policy(game, state, 0)

    @classmethod
    def from_file(cls, path, feature_extractor):
        with open(path, "rb") as f:
            nn = Network.from_file(f)
        return cls(nn, feature_extractor)

    def forward(self, states, train=False):
        array = []
        for state in states:
            array.append(self.feature_extractor(state))
        array = np.array(array)
        if train:
            return self.network.forward(array, 1, train=train)
        else:
            return self.network.forward(np.array(array))

    def policy(self, game, state, explore=0., train=False):
        node = RLNode(state)
        children = tuple(node.expand(game))
        if random() < explore:
            children = (children[randint(0, len(children))],)
        states = [child.state for child in children]
        if train:
            values, zs = self.forward(states, train=train)
            values = values.reshape(-1)
        else:
            values = self.forward(states).reshape(-1)
        index = np.argmax(values)
        child = children[index]
        if train:
            # zs = deque([z[index] for z in zs])
            # return child.action, child, values[index], zs
            return child.action, child
        return child.action

    def td_train(self, game, initial_state=None, explore=0.1, n=1000,
                 theta=0.05, checkpoint_interval=50, gamma=0.9, policy=None):
        # TODO make it possible to plug in other agents by using
        self.network.learning_rate = theta
        initial_node = RLNode(initial_state, rewards=(0, 0, 0))
        # Generate episodes of game based on current policy
        # -> Update the value for each player
        losses = []
        for i in range(n):
            node = initial_node
            # We record three player simultaneously
            player_rewards = [[], [], []]
            player_states = [[], [], []]
            player_actions = [None, None, None]
            loss = 0
            while not game.terminal_state(node.state):
                # TODO replace this by any policy for bootstrapping
                # TODO use the current value to compute!

                current_colour = node.state.colour
                current_code = node.state.code_map[current_colour]

                action = player_actions[current_code]
                # Update
                if action is not None:
                    # (Experimental) Update estimation of v+1 based on v
                    # Update the estimation of v+1 and v'
                    # Get y
                    # 1. Get current state
                    current_state = node.state.red_perspective(current_colour)
                    # 2. Get feature vector
                    current_state_vector = \
                        self.feature_extractor(current_state)
                    # 3. Compute v'
                    v_prime = \
                        self.network.forward(np.array([current_state_vector]))
                    ### THERE is no reward here!
                    # 4. Get y from v'
                    y = np.array([v_prime])
                    # TODO this part can be simplified by using previous result
                    # Get X
                    # 1. Get prev state
                    prev_state = self \
                        .feature_extractor(player_states[current_code][1])
                    # 2. Get feature vector as X
                    prev_state_vector = \
                        self.feature_extractor(prev_state)
                    X = np.array([prev_state_vector])
                    # Backward propagation
                    self.network.backward(X, y)

                    # Update the estimation of previous state v and v'
                    # Get y
                    # 1. Get current state
                    # current_state = \
                    #     node.state.red_perspective(current_colour)
                    # 2. Get feature vector
                    # current_state_vector = \
                    #     self.feature_extractor(current_state)
                    # 3. Compute v'
                    v_prime = \
                        self.network.forward(np.array([current_state_vector]))
                    # 4. Get reward
                    reward = sum(player_rewards[current_code])
                    # 5. Get v' + reward as y
                    y = np.array([v_prime + reward])
                    # TODO this part can be simplified by using previous result
                    # Get X
                    # 1. Get prev state
                    prev_state = self\
                        .feature_extractor(player_states[current_code][0])
                    # 2. Get feature vector as X
                    prev_state_vector = \
                        self.feature_extractor(prev_state)
                    X = np.array([prev_state_vector])
                    # Backward propagation
                    self.network.backward(X, y)

                    if i % checkpoint_interval == 0:
                        y_hat = self.network.forward(X)
                        loss += self.network.loss.compute(y_hat, y)

                # Rotate the state to make current colour be red
                current_state = node.state.red_perspective(current_colour)
                # action, node, next_value, player_zs = \
                #     self.policy(game, node.state, explore=explore,
                #                 train=True)

                # Get the results
                action, node = \
                    self.policy(game, current_state, explore=explore,
                                train=True)
                # Back to red perspective
                state = node.state
                node = RLNode(state.original_perspective(current_colour))

                # print(node)

                for _colour, _code in State.code_map.items():
                    player_rewards[_code].append(node.rewards[_code])
                    if len(player_rewards[_code]) > 3:
                        player_rewards[_code].pop(0)
                    player_states[_code].append(node.state.red_perspective(
                        current_colour))
                    if len(player_states[_code]) > 3:
                        player_states[_code].pop(0)

            # TODO process information from terminal node
            if i % checkpoint_interval == 0:
                losses.append((i, loss))
                print(f"Episode: {i}\n"
                      f"        loss={loss}")
                self.network.save_checkpoint()
        self.network.save_final()

    # def policy(self, game, node, explore=0.):
    #     children = node.expand(game)
    #     if random() < explore:
    #         return children[randint(0, len(children))]
    #     else:
    #         states = [child.state for child in children]
    #         colours = [node.state.colour] * len(children)
    #         values = self.forward(states, colours).reshape(-1)
    #         index = np.argmax(values)
    #         child = children[index]
    #         return child.action, values[index]


def simple_grid_extractor(state):
    """
    A chain of states to
    :param state:
    :return:
    """
    # First Represent States
    state_vector = []
    for r in range(-3, 4):
        for q in range(max(-3, -3-r), min(4, 4+r)):
            append = [0, 0, 0]
            if (r, q) in state._pos_to_piece:
                append[State.code_map[state._pos_to_piece[(r, q)]]] = 1
            state_vector += append
    return state_vector

    # def tree_policy(self, game):
    #     """
    #     Get the child node of a UCT node. If the node is expanded then return
    #     the best node, else get a random unexplored node
    #     :param game: The game the node is in (rules of expansion)
    #     :return: A move given by the above selection rule
    #     """
    #     # Initialise the nodes
    #     if self.unexpanded_children is None:
    #         self.unexpanded_children = list(self.expand(game))
    #         shuffle(self.unexpanded_children)
    #     remaining = len(self.unexpanded_children)
    #     if remaining > 0:
    #         child = self.unexpanded_children.pop()
    #         return child
    #     else:
    #         # Somehow this beats max([(f(v),v) for v in children])
    #         children = list(self.children.values())
    #         # This is a leaf node
    #         if not len(children):
    #             return None
    #         keys = [self.child_value(child) for child in children]
    #         return children[keys.index(max(keys))]
