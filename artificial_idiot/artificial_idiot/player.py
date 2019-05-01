import abc
from artificial_idiot.util.json_parser import JsonParser
from artificial_idiot import evaluator
from artificial_idiot.state import State
from artificial_idiot.problem import Game
from artificial_idiot.search import RandomMove
import json


player_evaluator = evaluator.DummyEvaluator()


class Player(abc.ABC):

    def __init__(self, true_colour, search_algorithm=RandomMove(),
                 evaluator=player_evaluator, problem=Game):
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
        self.colour = true_colour
        self.search_class = search_algorithm

        # load up the initial state
        json_loader = json.load(open("../tests/red_initial_state.json"))
        print(json_loader)
        json_parser = JsonParser(json_loader)
        pos_dict, colour = json_parser.parse(pos_dict=True)
        state = State.state_to_red(State(pos_dict, "red"))
        self._game = Game(state, "red")

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


class RandomAgent(Player):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pass

    def action(self):
        fr, to, move = self.search_class.search(self._game.initial, self._game)
        fr = State.rotate_pos(self._game.initial.colour, self.colour, fr)
        to = State.rotate_pos(self._game.initial.colour, self.colour, to)
        return fr, to, move

    def update(self, colour, action):
        move, coord = action
        fr, to = coord
        fr = State.rotate_pos(self.colour, self._game.initial.colour, fr)
        to = State.rotate_pos(self.colour, self._game.initial.colour, to)
        self._game.update((fr, to, move))

    def evaluate(self, state, *args, **kwargs):
        return super().evaluate(state, *args, **kwargs)

if __name__ == "__main__":
    player = RandomAgent(true_colour="red")
    print(player.action())