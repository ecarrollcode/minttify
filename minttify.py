import sys
import re
from collections import OrderedDict

hex_rgx = '#[0-9a-fA-F]+'

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def get_hex_to_rgb(line):
    """Return red, green, blue for the given hex color."""
    hex_val = re.search(hex_rgx, line).group(0).strip('#')
    h_len = len(hex_val)
    tupl = tuple(int(hex_val[i:i + h_len // 3], 16) for i in range(0, h_len, h_len // 3))
    final = ','.join(map(str, tupl))
    return final


def main():
    """Main parsing function"""
    args  = getopts(sys.argv)
    fname = args['-f']
    mintty_dict = dict()
    rgb_vals = list()
    hex_vals = list()
    background = tuple()
    foreground = tuple()
    cursor = tuple()

    mintty_keys  = ["BackgroundColour", "ForegroundColour", "CursorColour"]
    palette_keys = ["Black", "BoldBlack", "Red", "BoldRed", "Green",
                    "BoldGreen", "Yellow", "BoldYellow", "Blue",
                    "BoldBlue", "Magenta", "BoldMagenta", "Cyan",
                    "BoldCyan", "White", "BoldWhite"]          

    with open(fname) as f:
        for line in f:
            line = line.strip()
            match = re.search('\[\[.*\]\]', line) # match profiles

            # ignore irrelevant lines
            if len(line) == 0 or line[0] == "#" or match or "use_theme_colors" in line:
                continue
            hex_val = get_hex_to_rgb(line)
            hex_vals = list()

            if "background_color" in line:
                mintty_dict["BackgroundColour"] = hex_val
            elif "foreground_color" in line:
                mintty_dict["ForegroundColour"] = hex_val
            elif "palette" in line:
                hex_vals = [s.strip('#') for s in  re.findall(hex_rgx, line)]
                print hex_vals





            # hex_vals.insert(1, hex_vals[1])
            # rgb_vals = map(get_hex_to_rgb, hex_vals)

    mintty_tuples_list = zip(mintty_keys, rgb_vals)

    for i in range(0, len(mintty_tuples_list)):
        curr_key = mintty_tuples_list[i][0]
        curr_val = mintty_tuples_list[i][1]
        finalStr = curr_key + "=" + curr_val


main()