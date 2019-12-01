#!/usr/bin/env python3

import sys

if __name__ == "__main__":

    categories = [
        "Firefox",
        "fish",
        "nv",
        "sudo",
        "htop",
        "Pcbnew",
        "Eeschema",
        "Assign Footprints",
        "None",
        "Arduino",
        ".py",
        "IPython",
    ]
    categories = {c: 0 for c in categories}

    with open(sys.argv[1], "r") as f:
        for line in f:
            time, name = eval(line)
            name = str(name)

            found_category = False
            for category in categories:
                if category in name:
                    categories[category] += 1
                    found_category = True
                    break

            if not found_category:
                print(name)

    print(categories)
