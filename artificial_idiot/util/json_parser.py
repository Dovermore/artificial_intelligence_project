from collections import defaultdict as dd


def parse(json_loader, phase):
    if phase == "A":
        colour = json_loader["colour"]
        block = "block"
        forward_dict = dd(list)

        for pos in json_loader["pieces"]:
            forward_dict[colour].append(tuple(pos))
        for pos in json_loader["blocks"]:
            forward_dict[block].append(tuple(pos))
        return forward_dict, colour


if __name__ == "__main__":
    # Test for phase
    import json

    with open("tests/part_a/test0.json") as f:
        json_loader = json.load(f)
        print(json_loader)
        print(parse(json_loader, "A"))
