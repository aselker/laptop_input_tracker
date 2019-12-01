#!/usr/bin/env python3

import sys
import pickle


def parse_motion_word(word):
    assert word[:2] == "a["
    axis = int(word[2])
    pos = int(word[5:])
    return axis, pos


if __name__ == "__main__":
    assert sys.argv[1], sys.argv[2]

    positions = [(None, None, None)]

    with open(sys.argv[1], "r") as f:
        for line in f:
            words = line.split(" ")
            words = [w for w in words[:-1] if w]  # Remove empty words, and trailing \n

            timestamp = int(words[0]) / 1000 / 1000 / 1000  # Get timestamp in seconds

            if words[1] == "motion":
                position = list(positions[-1])
                position[0] = timestamp
                for word in words[2:]:
                    axis, pos = parse_motion_word(word)
                    if axis == 0:
                        position[1] = pos
                    if axis == 1:
                        position[2] = pos

                positions.append(tuple(position))

            elif words[1] == "button":
                if words[2] == "press":
                    pass  # Put button-handling code here
                elif words[2] == "release":
                    pass
                else:
                    raise ValueError(
                        "button action {} is not recognized".format(words[2])
                    )

            else:
                raise ValueError("message {} is not recognized".format(words[1]))

    pickle.dump(positions, open(sys.argv[2], "wb"))
