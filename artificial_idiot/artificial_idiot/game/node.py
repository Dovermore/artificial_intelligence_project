from math import sqrt, log
from random import shuffle
from artificial_idiot.util.misc import randint


class Node:
    """A node in a search tree. Contains a pointer to the parent (the node
    that this is a successor of) and to the actual state for this node. Note
    that if a state is arrived at by two paths, then there are two nodes with
    the same state.  Also includes the action that got us to this state, and
    the total path_cost (also known as g) to reach the node.  Other functions
    may add an f and h value; see best_first_graph_search and astar_search for
    an explanation of how the f and h values are handled. You will not need to
    subclass this class."""
    total_nodes_created = 0

    def __init__(self, state, parent=None, action=None, path_cost=0):
        """Create a search tree Node, derived from a parent by an action."""
        Node.total_nodes_created += 1
        self.state = state
        self.parent = parent
        self.action = action
        # TODO change path cost to evaluation value where higher the better
        self.path_cost = path_cost
        self.depth = 0
        self.children = {}
        if parent:
            self.depth = parent.depth + 1
        self.children = {}

    def __repr__(self, transition=False, **kwargs):
        return "<Node {}>".format(self.state.__repr__(**kwargs))

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, game):
        """List the nodes reachable in one step from this node."""
        # Generator of children nodes
        children = (self.child_node(game, action)
                    for action in game.actions(self.state))
        return children

    def child_node(self, game, action):
        """
        Generate child node based on game and action
        """
        # Only generate if not previously generated
        if action not in self.children:
            next_state = game.result(self.state, action)
            next_node = self.__class__(next_state, self, action,
                                       game.path_cost(
                                           self.path_cost, self.state, action,
                                           next_state))
            self.children[action] = next_node
        else:
            next_node = self.children[action]
        return next_node

    @property
    def solution(self):
        """Return the sequence of actions to go from the root to this node."""
        return [node.action for node in self.path[1:]]

    @property
    def path(self):
        """
        Return a list of nodes forming the path from the root to this node.
        """
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__() and \
               self.state == other.state

    def __hash__(self):
        return self.state.__hash__()


class BasicUCTNode(Node):
    c = 2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO this should be replaced by more advanced evaluation
        #      in future version
        self.wins = 0
        self.visits = 0
        # What child aren't explored yet
        self.unexpanded_children = None
        self.sorted_children = []

    @classmethod
    def set_c(cls, c):
        cls.c = c

    def update(self, result, *args, **kwargs):
        """
        Update the state of current node
        # TODO override this for a better model
        :param result: The outcome of the game. 0 for lose 1 for win
        """
        self.wins += (result == 1)
        self.visits += 1

    def tree_policy(self, game):
        """
        Get the child node of a UCT node. If the node is expanded then return
        the best node, else get a random unexplored node
        :param game: The game the node is in (rules of expansion)
        :return: A move given by the above selection rule
        """
        # TODO update policy to be more abstracted
        # Initialise the nodes
        if self.unexpanded_children is None:
            self.unexpanded_children = list(self.expand(game))
            shuffle(self.unexpanded_children)
        remaining = len(self.unexpanded_children)
        if remaining > 0:
            child = self.unexpanded_children.pop()
            return child
        else:
            # Somehow this beats max([(f(v),v) for v in children])
            children = list(self.children.values())
            # This is a leaf node
            if not len(children):
                return None
            keys = [self.child_value(child) for child in children]
            return children[keys.index(max(keys))]

    def default_policy(self, game):
        # Use the game default policy plus some random
        actions = list(game.actions(self.state))
        return self.child_node(game, actions[randint(0, len(actions))])

    def show_path(self):
        path = self.path
        for node in path:
            print(f"{hash(node)%9999}: [{node.wins:4d}, {node.visits:4d}]",
                  end=" --> ")
        print("<?>")

    def child_value(self, child):
        return (child.wins / child.visits
                + sqrt(self.c * log(self.visits) / child.visits))
