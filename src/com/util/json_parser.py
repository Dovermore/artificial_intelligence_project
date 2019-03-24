from collections import defaultdict as dd


def parse_phase_a(json_loader, mapping):
    player_code = mapping[json_loader["color"]]
    block_code = mapping["blocks"]
    forward_dict = dd(list)
    backward_dict = {}

    for pos in json_loader["pieces"]:
        tuple_pos = tuple(pos)
        forward_dict[player_code].append(tuple_pos)
        backward_dict[tuple_pos] = player_code
    for pos in json_loader["blocks"]:
        tuple_pos = tuple(pos)
        forward_dict[block_code].append(tuple_pos)
        backward_dict[tuple_pos] = block_code
    return forward_dict, backward_dict

