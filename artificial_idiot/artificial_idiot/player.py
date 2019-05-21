from artificial_idiot.search.randomsearch import RandomSearch
from artificial_idiot.search.uct import UCTSearch
from artificial_idiot.search.max_n import MaxN
from artificial_idiot.search.RL import ParametrisedRL
from artificial_idiot.search.mini_max import AlphaBetaSearch
from artificial_idiot.search.open_game_book import OpenGameBook
from artificial_idiot.search.composition_strategy import CompositionSearch
from artificial_idiot.search.multi_player_search import MultiPlayerSearch
from artificial_idiot.search.search_cutoff.cutoff import DepthLimitCutoff
from artificial_idiot.evaluation.evaluator_generator import (
    DummyEvaluator, WinLossEvaluator, NaiveEvaluatorGenerator, AdvanceEG,
    MinimaxEvaluator
)
from artificial_idiot.search.mini_max import AlphaBetaSearch
from artificial_idiot.game.node import Node, BasicUCTNode
from artificial_idiot.game.state import State
from artificial_idiot.game.game import Game, NodeGame
import random
from copy import deepcopy



player_evaluator = DummyEvaluator()
winloss_evaluator = WinLossEvaluator()


class Player:
    start_config = {
        (-3, 0): "red",
        (-3, 1): "red",
        (-3, 2): "red",
        (-3, 3): "red",
        (0, -3): "green",
        (1, -3): "green",
        (2, -3): "green",
        (3, -3): "green",
        (0, 3): "blue",
        (1, 2): "blue",
        (2, 1): "blue",
        (3, 0): "blue"
    }

    def __init__(self, colour, search_algorithm=None, game_type=Game,
                 evaluator=player_evaluator, initial_state=None):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (Red, Green or Blue). The value will be one of the
        strings "red", "green", or "blue" correspondingly.

        You can parse any valid board state to UCT the Agent
        However the Agent assumes the states are valid
        """
        self.colour = colour
        self.search_algorithm = search_algorithm

        self.code_map = State.code_map
        self.rev_code_map = State.rev_code_map

        # cycle the players:
        #    player:: red:   red -> red,   green -> green, blue -> blue
        #    player:: green: red -> blue,  green -> red,   blue -> green
        #    player:: blue:  red -> green, green -> blue,  blue -> red
        self.referee_to_player_mapping = State.perspective_mapping[colour]
        self.player_to_referee_mapping = {
            value: key for key, value in
            self.referee_to_player_mapping.items()}

        # The initial player is red, convert it to the rotate perspective
        state = State(self.start_config, colour=self
                      .referee_to_player_mapping["red"])

        # Colour of the game is different from the color of the state
        self.game = game_type("red", state)

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. If there are no allowed
        actions, your player must return a pass instead. The action (or pass)
        must be represented based on the above instructions for representing
        actions.
        """
        action = self.search_algorithm.search(self.game,
                                              self.game.initial_state)
        return self.convert_action(action, "referee")

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player’s
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red",
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or
        pass) conforming to the above in- structions for representing actions.

        You may assume that action will always correspond to an allowed action
        (or pass) for the player colour (your method does not need to validate
        the action/pass against the game rules).
        """
        player_action = self.convert_action(action, 'player')
        self.game.update(colour, player_action)

    def convert_action(self, action, convert_to):
        """
        Convert action format as well as perspective.
        :param action: The action to convert
        :param convert_to: The converted perspective
        :return: Converted action
        """
        if convert_to == "player":
            return self.convert_action_perspective(
                self.convert_action_format(action, convert_to), convert_to)
        elif convert_to == "referee":
            return self.convert_action_format(
                self.convert_action_perspective(action, convert_to),
                convert_to)
        else:
            raise ValueError(convert_to + "mode is not valid")

    def convert_action_perspective(self, action, convert_to):
        """
        This further converts the converted format from convert_action_to
        to the corresponding player perspective
        :param action: the action to translate. Format (fr, to, type)
        :param convert_to: To whose perspective should the convert to
        :return: The converted perspective
        """
        fr, to, move = action
        # No need for change if pass
        if action == "PASS":
            return action
        if convert_to == "player":
            new_fr = State.rotate_pos(self.colour, "red", fr)
            new_to = State.rotate_pos(self.colour, "red", to)
        elif convert_to == "referee":
            new_fr = State.rotate_pos("red", self.colour, fr)
            new_to = State.rotate_pos("red", self.colour, to)
        else:
            raise ValueError(convert_to + "mode is not valid")
        return new_fr, new_to, move

    @staticmethod
    def convert_action_format(action, convert_to):
        """
        Convert action from player/referee representation to the other
        representation.
        :param action: The action to convert
        :param convert_to: The representation to convert to
        :return:
        """
        # convert referee action encoding to player's encoding
        if convert_to == "player":
            move, pos = action
            if move == 'PASS':
                fr = None
                to = None
            elif move == 'EXIT':
                fr = pos
                to = None
            else:
                fr, to = pos
            return fr, to, move
        elif convert_to == "referee":
            fr, to, move = action
            if move == 'EXIT':
                return 'EXIT', fr
            if move == 'PASS':
                return 'PASS', None
            return move, (fr, to)
        else:
            raise ValueError(convert_to + "mode is not valid")

    @property
    def state(self):
        # TODO DEEPCOPY to be safe
        return self.game.initial_state


class ArtificialIdiot(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def action(self):
        pass

    def update(self, colour, action):
        pass


class RandomPlayer(Player):
    def __init__(self, colour, initial_state=None, seed=None):
        if seed is None:
            seed = random.random()
        print("* seed is:", seed)
        super().__init__(colour, search_algorithm=RandomSearch(seed),
                         initial_state=initial_state)


class ParanoidAgent(Player):
    def __init__(self, color, evaluator_generator, cutoff):
        search_algorithm = AlphaBetaSearch(evaluator_generator, cutoff)
        super().__init__(color, search_algorithm=search_algorithm)

    def action(self):
        player_action = self\
            .search_algorithm.search(self.game, self.game.initial_state)
        return self.convert_action(player_action, 'referee')


class MaxNPlayer(Player):
    """
    A wrapper class for referee that uses interface given by referee
    Here we use best hyperparameter
    """
    def __init__(self, color):
        # self.utility_pieces, num_exited_piece, self.utility_distance
        # utility_pieces, num_exited_piece, total_number_pieces, utility_distance
        weights = [10, 100, 1]
        evaluator_generator = NaiveEvaluatorGenerator(weights)
        cutoff = DepthLimitCutoff(3)
        search_algorithm = MaxN(evaluator_generator, cutoff, n_player=3)
        super().__init__(color, search_algorithm=search_algorithm,
                         initial_state=None)


class ParanoidPlayer_Advance(ParanoidAgent):
    def __init__(self, color):
        # utility_pieces, num_exited_piece, total_number_pieces, utility_distance
        weights = [10, 100, 1]
        evaluator_generator = NaiveEvaluatorGenerator(weights)
        cutoff = DepthLimitCutoff(4)
        super().__init__(color, evaluator_generator, cutoff)



class ParanoidPlayer_Naive(ParanoidAgent):
    def __init__(self, color):
        # utility_pieces, num_exited_piece, total_number_pieces, utility_distance
        weights = [10, 100, 1]
        evaluator_generator = NaiveEvaluatorGenerator(weights)
        cutoff = DepthLimitCutoff(4)
        super().__init__(color, evaluator_generator, cutoff)


class GreedyPlayer(ParanoidAgent):
    """
    A greedy player is Parnoid Agent with with 0 layer look a head
    """
    def __init__(self, color):
        # self.utility_pieces, num_exited_piece, self.utility_distance
        # utility_pieces, num_exited_piece, total_number_pieces, utility_distance
        weights = [10, 100, 1]
        evaluator_generator = NaiveEvaluatorGenerator(weights)
        cutoff = DepthLimitCutoff(1)
        super().__init__(color, evaluator_generator, cutoff)


class BasicUCTPlayer(Player):
    """
    Basic UCT player. Uses upper confidence monte carlo search algorithm
    """
    def __init__(self, colour, evaluator=winloss_evaluator,
                 game_type=NodeGame, node_type=BasicUCTNode,
                 initial_state=None, *args, **kwargs):
        search = UCTSearch(*args, **kwargs)
        super().__init__(colour, search, game_type, evaluator, initial_state)
        state = self.game.initial_state
        self.game = game_type(colour="red",
                              state=node_type(state))


class RLPlayer(Player):
    """
    Basic TD learning agent
    """
    def __init__(self, colour, search_algorithm=ParametrisedRL, game_type=Game,
                 evaluator=player_evaluator, initial_state=None):
        super().__init__(colour, search_algorithm, game_type, evaluator,
                         initial_state)


class PlayerFactory:
    @staticmethod
    def get_type_factory(type):
        def get_player_factory(*args, **kwargs):
            def get_player(player):
                return type(player, *deepcopy(args), **deepcopy(kwargs))
            return get_player
        return get_player_factory
