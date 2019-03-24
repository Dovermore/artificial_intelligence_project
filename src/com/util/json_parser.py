from collections import defaultdict as dd


def parse(json_loader, mapping, phase):
    if phase == "A":
        player_code = mapping[json_loader["colour"]]
        block_code = mapping["blocks"]
        forward_dict = dd(list)
        backward_dict = dd(int)

        for pos in json_loader["pieces"]:
            tuple_pos = tuple(pos)
            forward_dict[player_code].append(tuple_pos)
            backward_dict[tuple_pos] = player_code
        for pos in json_loader["blocks"]:
            tuple_pos = tuple(pos)
            forward_dict[block_code].append(tuple_pos)
            backward_dict[tuple_pos] = block_code
        return forward_dict, backward_dict


if __name__ == "__main__":
    # Test for phase
    import json
    import os
    import os.path as path

    with open("tests/part_a/test0.json") as f:
        json_loader = json.load(f)
        print(json_loader)
        print(parse(json_loader, {"red": 0, "blocks": 3}, "A"))
