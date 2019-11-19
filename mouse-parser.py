#!/usr/bin/env python3

import sys


def parse_motion_word(word):
    assert word[:2] == "a["
    axis = int(word[2])
    pos = int(word[5:])
    return axis, pos


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        for line in f:
            words = line.split(" ")
            words = [w for w in words[:-1] if w]  # Remove empty words, and trailing \n
            nanos = int(words[0])
            seconds = nanos / 1000 / 1000 / 1000
            if words[1] == "motion":
                if len(words[2:]) == 2:
                    _, x_pos = parse_motion_word(words[2])
                    _, y_pos = parse_motion_word(words[3])
                else:
                    axis, pos = parse_motion_word(words[2])

            elif words[1] == "button":
                if words[2] == "press":
                    pass
                elif words[2] == "release":
                    pass
                else:
                    raise ValueError(
                        "button action {} is not recognized".format(words[2])
                    )

            else:
                raise ValueError("message {} is not recognized".format(words[1]))
