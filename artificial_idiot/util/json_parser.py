from collections import defaultdict as dd


class JsonParser:
    block = "block"

    def __init__(self, json_loader, phase):
        self.phase = phase
        self.json_loader = json_loader
        self.colour = self.json_loader["colour"]

    def parse(self, pos_dict=True):
        if self.phase == "A":
            if pos_dict:
                d = self.parse_pos_a()
            else:
                d = self.parse_piece_a()
            return d, self.colour

    def parse_pos_a(self):
        pos_dict = dd(str)
        for pos in self.json_loader["pieces"]:
            pos_dict[tuple(pos)] = self.colour
        for pos in self.json_loader["blocks"]:
            pos_dict[tuple(pos)] = self.block
        return pos_dict

    def parse_piece_a(self):
        piece_dict = dd(list)

        # Initialise the blocks and pieces no matter what.
        piece_dict[self.colour] = []
        piece_dict[self.block] = []

        for pos in self.json_loader["pieces"]:
            piece_dict[self.colour].append(tuple(pos))
        for pos in self.json_loader["blocks"]:
            piece_dict[self.block].append(tuple(pos))
        return piece_dict


if __name__ == "__main__":
    # Test for phase
    import json

    with open("tests/part_a/test0.json") as f:
        json_loader = json.load(f)
        print(json_loader)
        json_parser = JsonParser(json_loader, "A")
