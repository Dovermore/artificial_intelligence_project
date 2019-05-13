from artificial_idiot.search.search import Search
from artificial_idiot.game.node import BasicUCTNode


class UCTSearch(Search):
    def __init__(self, c=2, node_type=BasicUCTNode):
        self.c = c
        self.node_type = node_type
        self.node_type.set_c(c)
        self.initial_node = None

    def select_expand(self, game):
        """
        Fully expand path of the tree down to the leave node.
        :param game: The game the path is in
        :return: The terminal node of such path
        """
        parent = None
        node = game.initial_state

        # Fully expanded and not leaf
        while node.unexpanded_children is not None and \
                len(node.unexpanded_children) == 0 and node is not None:
            parent = node
            node = node.tree_policy(game)
        # Found a leaf of the whole tree
        if node is None:
            return parent
        # Half way through the tree, half-way through the tree, now *expand*
        else:
            parent = node
            node = node.tree_policy(game)
            return node if node is not None else parent

    def simulation(self, game, node):
        while not game.terminal_state(node.state):
            node = node.default_policy(game)
        return node

    def back_prop(self, game, leaf, result, *args, **kwargs):
        node = leaf
        # Back prop till the root node (but not include that)
        while node is not None:
            node.update(result, *args, **kwargs)
            # Some how got to a node without parent but is not root
            node = node.parent

    def search(self, game, state, iteration=10, max_depth=-1,
               max_time=-1, training=True):
        # TODO add depth, time and cutoff
        # TODO fix this iteration
        while iteration > 0:
            # Get a leaf
            expanded = self.select_expand(game)
            # print("==================== before ====================")
            # expanded.show_path()
            leaf = self.simulation(game, expanded)
            result = game.evaluator(leaf.state, "red")
            # print(f"---------- {result} ----------")
            self.back_prop(game, expanded, result=game.evaluator(
                leaf.state, "red"))
            iteration -= 1
            # print("-------------------- after --------------------")
            # expanded.show_path()
        return game.initial_state.tree_policy(game).action

