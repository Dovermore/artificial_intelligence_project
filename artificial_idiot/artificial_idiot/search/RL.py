from artificial_idiot.search.search import Search
from artificial_idiot.game.state import State
import numpy as np
import pickle
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
        # TODO implement
        pass

    @classmethod
    def load(cls, path):
        with open(path) as f:
            return pickle.load(f)

    def forward(self, states, colours):
        array = []
        for state, colour in zip(states, colours):
            array.append(self.feature_extractor(state, colour))
        return self.network.forward(np.array(array))

    def train(self, game, initial_node=None, explore=0.1, n=1000,
              theta=0.05, batch_size=20, checkpoint_interval=50):
        episodes = []
        # Generate episodes of game based on current policy
        for i in range(batch_size):
            self.simulate_episode(game, initial_node)
        # Update the value for each player
        for i in range(n):
            for episode in episodes:
                for initial_node in reversed(episode):
                    colour = initial_node.state.colour

                    node = initial_node
                    # Compute reward and make the state list for processing
                    # Don't need action, the policy is fixed
                    states = []
                    reward = 0
                    # Count the rewards now
                    for j in range(3):
                        if node is None:
                            break
                        reward += node.reward[0]
                        states.append(node.state.red_perspective(colour))
                        node = node.parent
                    state_vector = self.feature_extractor(states)
                    # TODO update the NN by the features
            if i % checkpoint_interval == 0:
                self.network.check_point()
        self.network.save_final()

    def policy(self, game, node, explore=0.):
        children = node.expand(game)
        if random() < 0.1:
            return children[randint(0, len(children))]
        else:
            states = [child.state for child in children]
            colours = [node.state.colour] * len(children)
            values = self.forward(states, colours).reshape(-1)
            index = np.argmax(values)
            child = children[index]
            return child.action

    def simulate_episode(self, game, initial_node=None, explore=0.1, policy=None):
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
    assert len(states > 0)
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
