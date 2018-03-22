import sys
import re
from functools import reduce
import os

hex_rgx = '#[0-9a-fA-F]+'

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts


def hex_to_rgb(hex_val):
    """Return red, green, blue for the given hex color."""
    h_len = len(hex_val)
    tupl = tuple(int(hex_val[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))
    final = ','.join(map(str, tupl))
    return final


def merge_dicts(*dicts):
    return reduce(lambda a, d: a.update(d) or a, dicts, {})


def main():
    """Main parsing function"""
    args  = getopts(sys.argv)
    if "-f" not in args:
        print("\nError: no file input.")
        print("USAGE: python minttify.py -f [terminator config file]\n")
        return
    fname = args['-f']
    rgb_vals = list()
    background = tuple()
    foreground = tuple()
    cursor = tuple()
    final_str = str()
    colors_dict = dict()

    mintty_keys     =  ["BackgroundColour", "ForegroundColour", "CursorColour",
                        "Black", "BoldBlack", "Red", "BoldRed", "Green",
                        "BoldGreen", "Yellow", "BoldYellow", "Blue",
                        "BoldBlue", "Magenta", "BoldMagenta", "Cyan",
                        "BoldCyan", "White", "BoldWhite"] 

    terminator_keys = ["Black", "Red", "Green", "Yellow", "Blue", "Magenta",
                        "Cyan", "White", "BoldBlack", "BoldRed", "BoldGreen",
                        "BoldYellow", "BoldBlue", "BoldMagenta", "BoldCyan",
                        "BoldWhite"]        

    with open(fname) as f:
        for line in f:
            line = line.strip()
            match = re.search('\[\[.*\]\]', line) # match profiles

            # ignore irrelevant lines
            if (len(line) == 0 or line[0] == "#" or match or
                "use_theme_colors" in line or "background_image" in line or
                '#' not in line):
                continue
            hex_val = re.search(hex_rgx, line).group(0).strip('#')
            rgb_val = hex_to_rgb(hex_val)

            if "background_color" in line:
                colors_dict["BackgroundColour"] = rgb_val
            elif "foreground_color" in line:
                colors_dict["ForegroundColour"] = rgb_val
            elif "cursor_color" in line:
                colors_dict["CursorColour"] = rgb_val
            elif "palette" in line:
                rgb_vals =  map(hex_to_rgb, [s.strip('#') for s in  re.findall(hex_rgx, line)])
            else:
                continue

        if "CursorColour" not in colors_dict.keys():
            colors_dict["CursorColour"] = colors_dict["ForegroundColour"]

    index_map = {v: i for i, v in enumerate(mintty_keys)}
    rest_of_dict = dict(zip(terminator_keys, rgb_vals))
    colors_dict = merge_dicts(colors_dict, rest_of_dict)
    colors_tuple_list = sorted(colors_dict.items(), key=lambda pair: index_map[pair[0]])
    b_name = os.path.splitext(fname)[0]

    f_out = open(b_name + ".minttyrc","w+")

    for i in range(0, len(colors_tuple_list)):
        curr_elem = colors_tuple_list[i]
        curr_key = curr_elem[0]
        curr_val = curr_elem[1]
        final_str = curr_key + "=" + curr_val + "\n"
        f_out.write(final_str)

    f_out.close()

main()
