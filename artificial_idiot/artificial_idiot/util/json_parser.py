from collections import defaultdict as dd


class JsonParser:
    # map fr_code[i] to to_code[i]
    fr_code = ["red", "green", "blue"]
    to_code = ["red", "green", "blue"]

    def __init__(self, json_loader):
        self.json_loader = json_loader
        self.colour = self.json_loader["colour"]

    # TODO return number of completed pieces
    def parse(self, pos_dict=True):
        if pos_dict:
            d = self.parse_pos_a()
        else:
            d = self.parse_piece_a()
        return d, self.colour, self.parse_completed()

    def parse_completed(self):
        completed_code = "completed"
        completed = {}
        c = self.json_loader[completed_code]
        for i in range(len(self.fr_code)):
            completed[self.to_code[i]] = c[self.fr_code[i]]
        return completed

    def parse_pos_a(self):
        pos_dict = dd(str)
        for i in range(len(self.fr_code)):
            for pos in self.json_loader[self.fr_code[i]]:
                pos_dict[tuple(pos)] = self.to_code[i]
        return pos_dict

    def parse_piece_a(self):
        piece_dict = dd(list)

        # Initialise pieces no matter what.
        piece_dict[self.colour] = []
        for i in range(len(self.fr_code)):
            piece_dict[self.to_code[i]] = []

        for i in range(len(self.fr_code)):
            for pos in self.json_loader[self.fr_code[i]]:
                piece_dict[self.to_code[i]].append(tuple(pos))
        return piece_dict


if __name__ == "__main__":
    import json

    def test_initial_state():
        pos_dict_ans = {(-3, 0): 'red', (-3, 1): 'red', (-3, 2): 'red', (-3, 3): 'red', (0, -3): 'green', (1, -3): 'green', (2, -3): 'green', (3, -3): 'green', (0, 3): 'blue', (1, 2): 'blue', (2, 1): 'blue', (3, 0): 'blue'}
        piece_dict_ans = {'red': [(-3, 0), (-3, 1), (-3, 2), (-3, 3)], 'green': [(0, -3), (1, -3), (2, -3), (3, -3)], 'blue': [(0, 3), (1, 2), (2, 1), (3, 0)]}
        colour_ans = "red"
        completed_ans = {"red" : 0, "blue" : 0, "green":0}
        with open("../../tests/red_initial_state.json") as f:
            json_loader = json.load(f)
            json_parser = JsonParser(json_loader)
            pos_dict, colour, completed = json_parser.parse()
            assert(colour == colour_ans)
            assert(completed == completed_ans)
            assert(piece_dict_ans == dict(json_parser.parse_piece_a()))
            assert(pos_dict_ans == dict(pos_dict))

    # UCT
    test_initial_state()
