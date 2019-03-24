import abc


class SimpleProblemSolvingAgentProgram(abc.ABC):
    """Abstract framework for a problem-solving agent. [Figure 3.1]"""

    def __init__(self, initial_state=None):
        """State is an abstract representation of the state
        of the world, and seq is the list of actions required
        to get to a particular state from the initial state(root)."""
        self.state = initial_state
        self.seq = []

    def __call__(self, percept):
        """[Figure 3.1] Formulate a goal and problem, then
        search for a sequence of actions to solve it."""
        self.state = self.update_state(self.state, percept)
        if not self.seq:
            goal = self.formulate_goal(self.state)
            problem = self.formulate_problem(self.state, goal)
            self.seq = self.search(problem)
            if not self.seq:
                return None
        return self.seq.pop(0)

    @abc.abstractmethod
    def update_state(self, state, percept):
        pass

    @abc.abstractmethod
    def formulate_goal(self, state):
        pass

    @abc.abstractmethod
    def formulate_problem(self, state, goal):
        pass

    @abc.abstractmethod
    def search(self, problem):
        pass

