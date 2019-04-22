import abc
from artificial_idiot import evaluator
from artificial_idiot.state import State


player_evaluator = evaluator.DummyEvaluator()


class Player(abc.ABC):
    @abc.abstractmethod
    def __init__(self, colour, search_algorithm=None,
                 evaluator=player_evaluator):
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
        self.colour = colour
        # TODO other basic position set up
        self._internal_state = None
        self.state = State.rotate_state()

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


class ArtificialIdiot(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def action(self):
        pass

    def update(self, colour, action):
        pass


class DummyPlayer(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def action(self):
        pass

    def update(self, colour, action):
        pass

    def evaluate(self, state, *args, **kwargs):
        return super().evaluate(state, *args, **kwargs)
