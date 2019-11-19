#!/usr/bin/env python3

import sys

with open(sys.argv[1], "r") as f:
    for line in f:
        words = line.split(" ")
        nanos = int(words[0])
        seconds = nanos / 1000 / 1000 / 1000
        if words[1] == "motion":
            pass
        elif words[1] == "button":
            pass
        else:
            raise ValueError("message {} is not recognized".format(words[1]))
