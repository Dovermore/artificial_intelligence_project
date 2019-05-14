from artificial_idiot.search.search import Search
from artificial_idiot.game.state import State
from artificial_idiot.machine_learning.network import Network
from artificial_idiot.game.node import Node
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

    def forward(self, states, colours):
        array = []
        for state, colour in zip(states, colours):
            array.append(self.feature_extractor(state))
        print(array)
        return self.network.forward(np.array(array))

    def td_train(self, game, initial_node=None, explore=0.1, n=1000,
                 theta=0.05, checkpoint_interval=50, policy=None):
        # TODO make it possible to plug in other agents by using
        self.network.learning_rate = theta
        # Generate episodes of game based on current policy
        # -> Update the value for each player
        for i in range(n):
            node = initial_node
            # We record three player simultaneously
            rewards = [[], [], []]
            states = [[], [], []]
            cur_value = 0
            next_value = 0
            while node is not None:
                # TODO replace this by any policy for bootstrapping
                cur_value = next_value
                node, next_value = self.policy(game, node, explore=explore)
                colour = node.state.colour
                for code in range(3):
                    if len(rewards[i]) > 3:
                        rewards.pop(0)
                    rewards[i].append(node.reward[i])
                    if len(states[i]) > 3:
                        states.pop(0)
                    states.append(node.state.red_perspective(colour))
                code = node.state.code_map[colour]
                state_vector = self.feature_extractor(states[code])
                reward = sum(rewards[code])
                X = np.expand_dims(state_vector, axis=0)
                y = np.array([next_value + reward])
                self.network.backward((X, y))
            if i % checkpoint_interval == 0:
                self.network.check_point()
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

    def policy(self, game, state, explore=0.):
        node = Node(state)
        children = tuple(node.expand(game))
        if random() < explore:
            return children[randint(0, len(children))]
        else:
            states = [child.state for child in children]
            colours = [node.state.colour] * len(tuple(children))
            values = self.forward(states, colours).reshape(-1)
            index = np.argmax(values)
            child = children[index]
            return child.action, values[index]

    def simulate_episode(self, game, initial_node=None,
                         explore=0.1, policy=None):
        if policy is None:
            policy = self.policy
        episode = [initial_node]
        node = initial_node
        while node is not None:
            node = policy(game, node, explore=explore)
            episode.append(node)
        return episode


def simple_grid_extractor(states):
    # TODO rotate based on colour
    # First Represent States
    assert len(states) > 0
    state = states[0]
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
