import sys
import re
from collections import OrderedDict

def getopts(argv):
    opts = {}  # Empty dictionary to store key-value pairs.
    while argv:  # While there are arguments left to parse...
        if argv[0][0] == '-':  # Found a "-name value" pair.
            opts[argv[0]] = argv[1]  # Add key and value to the dictionary.
        argv = argv[1:]  # Reduce the argument list by copying it starting from index 1.
    return opts

def hex_to_rgb(value):
    """Return red, green, blue for the given hex color."""
    value = value.lstrip('#')
    lv = len(value)
    tupl = tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))
    final = ','.join(map(str, tupl))
    return final


def main():
    """Main conversion function"""
    args = getopts(sys.argv)
    fname = args['-f']

    mintty_keys = ["BackgroundColour", "ForegroundColour", "CursorColour",
                    "Black", "BoldBlack", "Red", "BoldRed", "Green",
                    "BoldGreen", "Yellow", "BoldYellow", "Blue",
                    "BoldBlue", "Magenta", "BoldMagenta", "Cyan",
                    "BoldCyan", "White", "BoldWhite"]          
    rgb_vals = []

    with open(fname) as f:
        data = f.read()
        # get rid of comments, unneeded info
        first_strip = data.rpartition('use_theme_colors = False')[-1]
        hex_vals = re.findall('#.{1,6}', first_strip)
        hex_vals.insert(1, hex_vals[1])
        rgb_vals = map(hex_to_rgb, hex_vals)

    mintty_tuples_list = zip(mintty_keys, rgb_vals)
    # print mintty_tuples_list

    for i in range(0, len(mintty_tuples_list)):
        curr_key = mintty_tuples_list[i][0]
        curr_val = mintty_tuples_list[i][1]
        finalStr = curr_key + "=" + curr_val
        print finalStr


main()