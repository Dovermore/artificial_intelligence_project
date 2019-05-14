import abc
import os
from os import path
from pickle import dump, load

from artificial_idiot.search.open_game import dirname


class AbstractActionBook:
    """
    This class manages all actions and applying actions, loaded by opening
    game search to give the opening move for player
    """
    def __init__(self, name):
        """
        Init the ActionBook for use
        :param name: The name of the strategy
        """
        self.name = name
        self.save_to = path.join(dirname, "open_book", self.name)

    @abc.abstractmethod
    def get_action(self, state):
        pass

    @abc.abstractmethod
    def put_action(self, state, action):
        raise NotImplementedError()

    def save(self):
        if not path.exists(self.save_to):
            os.makedirs(os.path.dirname(self.save_to), exist_ok=True)
        with open(self.save_to, "wb") as f:
            dump(self, f)

    @staticmethod
    def read(name):
        save_file = path.join(dirname, "open_book", name)
        assert path.exists(save_file)
        with open(save_file, "rb") as f:
            return load(f)


class SimpleActionBook(AbstractActionBook):
    """
    This class manages all actions and applying actions, loaded by opening
    game search to give the opening move for player
    """

    def __init__(self, name):
        super().__init__(name)
        self.actions = []

    def get_action(self, state):
        if self.actions:
            return self.actions.pop(0)

    def put_action(self, state, action):
        self.actions.append(action)

    def save(self):
        if not path.exists(self.save_to):
            os.makedirs(os.path.dirname(self.save_to), exist_ok=True)
        with open(self.save_to, "wb") as f:
            dump(self, f)

    @staticmethod
    def read(name):
        save_file = path.join(dirname, "open_book", name)
        assert path.exists(save_file)
        with open(save_file, "rb") as f:
            return load(f)

