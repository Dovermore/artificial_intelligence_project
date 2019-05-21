from artificial_idiot.search.search import Search
from artificial_idiot.game.state import State
from artificial_idiot.machine_learning.network import Network
from artificial_idiot.game.node import (
    Node, RLNode, InitialRLNode, WinningRLNode
)
import numpy as np
from random import random
from artificial_idiot.util.misc import randint
from time import sleep
from scipy.special import softmax


class ParametrisedRL(Search):
    """
    A monte carlo based reinforcement learning
    """
    def __init__(self, network, feature_extractor):
        super().__init__()
        self.network = network
        self.feature_extractor = feature_extractor

    def search(self, game, state, **kwargs):
        return self.greedy_policy(game, state, 0)

    @classmethod
    def from_file(cls, path, feature_extractor):
        nn = Network.from_file(path)
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

    def greedy_policy(self, game, state, explore=0., node_type=InitialRLNode,
                      train=False):
        if game.terminal_state(state):
            return None, None
        node = node_type(state)
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

    def choice_policy(self, game, state, explore=0., node_type=InitialRLNode,
                      train=False):
        if game.terminal_state(state):
            return None, None
        node = node_type(state)
        children = tuple(node.expand(game))
        if random() < explore:
            children = (children[randint(0, len(children))],)
        states = [child.state for child in children]
        if train:
            values, zs = self.forward(states, train=train)
            values = values.reshape(-1)
        else:
            values = self.forward(states).reshape(-1)
        probs = softmax(values)
        child = np.random.choice(children, size=1, p=probs)[0]
        if train:
            # zs = deque([z[index] for z in zs])
            # return child.action, child, values[index], zs
            return child.action, child
        return child.action

    def td_train(self, game, initial_state=None, explore=0.1, n=1000,
                 theta=0.05, checkpoint_interval=20, gamma=0.9,
                 node_type=InitialRLNode, policy="choice", debug=0):
        # TODO make it possible to plug in other agents
        self.network.learning_rate = theta
        initial_node = node_type(initial_state, rewards=(0, 0, 0))

        if policy == "greedy":
            policy = self.greedy_policy
        elif policy == "choice":
            policy = self.choice_policy
        else:
            raise ValueError("Invalid policy")

        # Generate episodes of game based on current policy
        # -> Update the value for each player
        losses = []

        episodes = []
        count = 0
        length = 0
        for i in range(n):
            node = initial_node
            # We record three player simultaneously
            loss = 0

            episode_actions = []
            episode_states = []
            episode_rewards = []

            # while not game.terminal_state(node.state):
            while True:

                # TODO replace this by any policy for bootstrapping
                # TODO use the current value to compute!

                current_colour = node.state.colour
                current_code = node.state.code_map[current_colour]

                # Rotate the state to make current colour be red
                current_state = node.state.red_perspective(current_colour)
                # Get the results
                action, next_node = policy(game, current_state,
                                           explore=explore,
                                           node_type=node_type, train=True)

                # Update
                # Here is the model assumption
                # The player's turn (who's time to choose action)
                # --------------------
                # g   b   r   g   b   r   g ...
                # 1   2   3   4   5   6   7
                # In reality, we should be computing three values for each
                # node. But we cheat here. We only compute the value wrt
                # current actor: The values are like this. (for r only)
                #                     * here now
                #         v   v'      v''
                #             o
                #           /
                # o - o - o - o           o
                #   ^       \           /
                # Other       o - o - o - o
                # branch                \
                # unknown                 o
                # p_s[r]:[0   1   2   *]
                # We say that vt'' -> vt', and vt' +

                # # (Experimental, try to solve the after state problem)
                # # Update estimation of v' based on v''
                # # Then update the estimation v based on v'
                # # Get y
                # # 1. Get current state (already have)
                # # 2. Get feature vector
                # current_state_vector = self.feature_extractor(current_state)
                # # 3. Compute v'
                # v_prime = \
                #     self.network.forward(np.array([current_state_vector]))
                # ### THERE is no reward here!
                # # 4. Get y from v'
                # y = v_prime
                #
                # # Get X
                # # 1. Get prev state
                # prev_state = player_states[current_code][1]
                # # 2. Get feature vector as X
                # prev_state_vector = \
                #     self.feature_extractor(prev_state)
                # X = np.array([prev_state_vector])
                # # Backward propagation
                # self.network.backward(X, y)

                # Update the estimation of previous state v and v'
                # Get y
                # 1. Get next state
                next_state = next_node.state
                # 2. Get feature vector
                next_state_vector = self.feature_extractor(next_state)
                # 3. Compute v'
                v_prime = \
                    self.network.forward(np.array([next_state_vector]))
                # 4. Get reward
                reward = next_node.rewards[0]
                # 5. Get v' + reward as y
                y = gamma * v_prime + reward
                # Get X
                # 1. Get current state
                # 2. Get feature vector as X
                current_state_vector = self.feature_extractor(current_state)
                X = np.array([current_state_vector])
                # Backward propagation
                y_hat_old = self.network.forward(X)
                # if y[0][0] != y_hat_old[0][0]:
                #     print("====================")
                #     print(y_hat_old, y)
                self.network.backward(X, y)
                y_hat = self.network.forward(X)
                # if y[0][0] != y_hat[0][0]:
                    # print(y_hat, y)
                    # assert abs(y[0][0] - y_hat[0][0]) < abs(y[0][0] - y_hat_old[0][0])
                    # print("====================")
                loss += self.network.loss.compute(y_hat, y)
                count += 1

                if game.terminal_state(next_node.state):
                    break

                fr, to, move = action
                fr = State.rotate_pos("red", current_colour, fr)
                to = State.rotate_pos("red", current_colour, to)
                action = (fr, to, move)

                node = next_node
                # Back to original perspective
                node.original_perspective(current_colour)

                episode_actions.append(action)
                episode_states.append(node.state)
                episode_rewards.append(node.rewards)

                if debug:
                    print(node)
                    sleep(debug)

            print(len(episode_states))
            print(f"Episode: {i}")

            # Store them for now
            episodes.append((episode_states, episode_actions, episode_rewards))
            length += len(episode_states)

            if i % checkpoint_interval == checkpoint_interval - 1:
                losses.append((i, loss))
                print(f"Episode: {i}\n"
                      f"        loss={loss/count}\n"
                      f"        average episode={length/checkpoint_interval}")
                count = 0
                length = 0
                self.network.save_checkpoint()
        self.network.save_final()

    def td_train2(self, game, initial_state=None, explore=0.1, n=1000,
                 theta=0.05, checkpoint_interval=20, gamma=0.9,
                 node_type=InitialRLNode, policy="choice", debug=0):
        # TODO make it possible to plug in other agents
        self.network.learning_rate = theta
        initial_node = node_type(initial_state, rewards=(0, 0, 0))

        if policy == "greedy":
            policy = self.greedy_policy
        elif policy == "choice":
            policy = self.choice_policy
        else:
            raise ValueError("Invalid policy")

        # Generate episodes of game based on current policy
        # -> Update the value for each player
        losses = []

        episodes = []
        count = 0
        length = 0
        for i in range(n):
            node = initial_node
            # We record three player simultaneously
            player_rewards = [[], [], []]
            player_states = [[], [], []]
            player_actions = [None, None, None]
            loss = 0

            episode_actions = []
            episode_states = []
            episode_rewards = []

            while game.terminal_state(node.state):

                # TODO replace this by any policy for bootstrapping
                # TODO use the current value to compute!

                current_colour = node.state.colour
                current_code = node.state.code_map[current_colour]

                action = player_actions[current_code]
                # Update
                if action is not None:
                    # Here is the model assumption
                    # The player's turn (who's time to choose action)
                    # --------------------
                    # g   b   r   g   b   r   g ...
                    # 1   2   3   4   5   6   7
                    # In reality, we should be computing three values for each
                    # node. But we cheat here. We only compute the value wrt
                    # current actor: The values are like this. (for r only)
                    #                     * here now
                    #         v   v'      v''
                    #             o
                    #           /
                    # o - o - o - o           o
                    #   ^       \           /
                    # Other       o - o - o - o
                    # branch                \
                    # unknown                 o
                    # p_s[r]:[0   1   2   *]
                    # We say that vt'' -> vt', and vt' +

                    # # (Experimental, try to solve the after state problem)
                    # # Update estimation of v' based on v''
                    # # Then update the estimation v based on v'
                    # # Get y
                    # # 1. Get current state
                    # current_state = node.state.red_perspective(current_colour)
                    # # 2. Get feature vector
                    # current_state_vector = \
                    #     self.feature_extractor(current_state)
                    # # 3. Compute v'
                    # v_prime = \
                    #     self.network.forward(np.array([current_state_vector]))
                    # ### THERE is no reward here!
                    # # 4. Get y from v'
                    # y = v_prime
                    #
                    # # Get X
                    # # 1. Get prev state
                    # prev_state = player_states[current_code][1]
                    # # 2. Get feature vector as X
                    # prev_state_vector = \
                    #     self.feature_extractor(prev_state)
                    # X = np.array([prev_state_vector])
                    # # Backward propagation
                    # self.network.backward(X, y)

                    # Update the estimation of previous state v and v'
                    # Get y
                    # 1. Get current state
                    current_state = \
                        node.state.red_perspective(current_colour)
                    # 2. Get feature vector
                    current_state_vector = \
                        self.feature_extractor(current_state)
                    # 3. Compute v'
                    v_prime = \
                        self.network.forward(np.array([current_state_vector]))
                    # 4. Get reward
                    reward = sum(player_rewards[current_code])
                    # 5. Get v' + reward as y
                    y = gamma * v_prime + reward
                    # Get X
                    # 1. Get prev state
                    prev_state = player_states[current_code][0]
                    # 2. Get feature vector as X
                    prev_state_vector = \
                        self.feature_extractor(prev_state)
                    X = np.array([prev_state_vector])
                    # Backward propagation
                    self.network.backward(X, y)

                    y_hat = self.network.forward(X)
                    loss += self.network.loss.compute(y_hat, y)
                    count += 1

                # Rotate the state to make current colour be red
                current_state = node.state.red_perspective(current_colour)

                # Get the results
                action, node = policy(game, current_state, explore=explore,
                                      node_type=node_type, train=True)

                if node is None or action is None:
                    break

                fr, to, move = action
                fr = State.rotate_pos("red", current_colour, fr)
                to = State.rotate_pos("red", current_colour, to)
                action = (fr, to, move)
                player_actions[current_code] = action

                # Back to red perspective
                node.original_perspective(current_colour)

                episode_actions.append(action)
                episode_states.append(node.state)
                episode_rewards.append(node.rewards)

                if debug:
                    print(node)
                    sleep(debug)

                for _colour, _code in State.code_map.items():
                    player_rewards[_code].append(node.rewards[_code])
                    if len(player_rewards[_code]) > 3:
                        player_rewards[_code].pop(0)
                    player_states[_code].append(node.state.red_perspective(
                        current_colour))
                    if len(player_states[_code]) > 3:
                        player_states[_code].pop(0)

            # TODO process final state
            winner = node.parent.state.colour


            print(f"Episode: {i}")

            # Store them for now
            episodes.append((episode_states, episode_actions, episode_rewards))
            length += len(episode_states)

            if i % checkpoint_interval == checkpoint_interval - 1:
                losses.append((i, loss))
                print(f"Episode: {i}\n"
                      f"        loss={loss/count}\n"
                      f"        average episode={length/checkpoint_interval}")
                count = 0
                length = 0
                self.network.save_checkpoint()
        self.network.save_final()

def simple_grid_extractor(state):
    """
    Encode the state by simply using a 37 * 3 vector
    :param state: The state to extract representation from
    :return: The vectorised state for feeding into neural network
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


def full_grid_extractor(state):
    """
    Encode the state by 37 * 3 + 3 for completed and
    :param state: The state to extract representation from
    :return: The vectorised state for feeding into neural network
    """
    state_vector = simple_grid_extractor(state)
    # Extract completed pieces
    for i in range(3):
        colour = state.rev_code_map[i]
        number = state.completed[colour]
        state_vector.append(number)

    # Encode the turn of player
    next_code = state.code_map[state.colour]
    for i in range(3):
        if i == next_code:
            state_vector.append(1)
        else:
            state_vector.append(0)
    return state_vector

