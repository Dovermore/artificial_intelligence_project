import abc
from artificial_idiot import evaluator
from artificial_idiot.state import State
from artificial_idiot.problem import Game
from artificial_idiot.search import RandomMove

player_evaluator = evaluator.DummyEvaluator()


def convert_action_to(action, convert_to):
    # convert referee action encoding to player's encoding
    if convert_to == "player":
        move, pos = action
        if move == 'PASS':
            return None
        elif move == 'EXIT':
            fr = pos
            to = None
        else:
            fr, to = pos
        return fr, to, move
    elif convert_to == "referee":
        if action is None:
            return 'PASS', None
        fr, to, move = action
        if move == 'EXIT':
            return 'EXIT', fr
        return move, (fr, to)
    else:
        raise ValueError(convert_to + "mode is not valid")


class AbstractPlayer(abc.ABC):

    start_config = {
        "red": [

            (-3, 1),
            (-3, 2),
            (-3, 3)
        ],
        "green": [
            (0, -3),
            (1, -3),
            (2, -3),
            (3, -3)
        ],
        "blue": [
            (0, 3),
            (1, 2),
            (2, 1),
            (3, 0)
        ]
    }

    def __init__(self, player, search_algorithm=None,
                 evaluator=player_evaluator, initial_state=None):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (Red, Green or Blue). The value will be one of the
        strings "red", "green", or "blue" correspondingly.
        """
        self.evaluator = evaluator
        self.player = player
        self.search_algorithm = search_algorithm

        state = State
        # Colour of the game is different from the color of the state
        self._game = Game(player, state)

    @abc.abstractmethod
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
        return "PASS", None

    @abc.abstractmethod
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
        pass

    def evaluate(self, state, *args, **kwargs):
        """
        This method is the evaluation function for a state. The method should
        always evaluate based on the perspective of a red player
        :param state: The state to compute evaluation with
        :return: The evaluated value of a state
        """
        return self.evaluator(state, *args, **kwargs)


class ArtificialIdiot(AbstractPlayer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def action(self):
        pass

    def update(self, colour, action):
        pass


class RandomAgent(AbstractPlayer):
    def __init__(self, player):
        super().__init__(player, search_algorithm=RandomMove(10))
        pass

    def action(self):
        player_action = self.search_algorithm.search(self._game)
        return convert_action_to(player_action, 'referee')

    def update(self, colour, action):
        player_action = convert_action_to(action, 'player')
        self._game.update(colour, player_action)
        print("# PLAYER", self.player)
        print(self._game.state)

    @property
    def state(self):
        # TODO DEEPCOPY
        return self._game.state


class MaxNAgent(AbstractPlayer):
    def __init__(self, player):
        super().__init__(player, search_algorithm=RandomMove(10))
        pass

    def action(self):
        player_action = self.search_algorithm.search(self._game)
        return convert_action_to(player_action, 'referee')

    def update(self, colour, action):
        player_action = convert_action_to(action, 'player')
        self._game.update(colour, player_action)
        print("# PLAYER", self.player)
        print(self._game.state)

    @property
    def state(self):
        # TODO DEEPCOPY
        return self._game.state



if __name__ == "__main__":
    # TODO handle test cases where player have to pass
    #  or opponent passes
    def random_agent_test():
        player = RandomAgent(player="red")
        assert (player.action() == ('MOVE', ((-3, 2), (-2, 1))))
        print(player.state)
        action = ("MOVE", ((0, -3), (0, -2)))
        player.update("green", action)
        print(player.state)
        assert (player.action() == ('MOVE', ((1, -3), (1, -2))))
        player.update("blue", ("PASS", None))

    def max_n_agent_test():
        pass
