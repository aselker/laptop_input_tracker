#!/usr/bin/env python3

# From https://stackoverflow.com/a/42404044/2597381

import sys
import os
import subprocess
import re
import time


def get_active_window_title():
    root = subprocess.Popen(
        ["xprop", "-root", "_NET_ACTIVE_WINDOW"], stdout=subprocess.PIPE
    )
    stdout, stderr = root.communicate()

    m = re.search(b"^_NET_ACTIVE_WINDOW.* ([\w]+)$", stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(
            ["xprop", "-id", window_id, "WM_NAME"], stdout=subprocess.PIPE
        )
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        return match.group("name").strip(b'"')

    return None


if __name__ == "__main__":
    assert sys.argv[1]
    titles = []

    while True:
        title = get_active_window_title()
        titles.append((time.time(), title))
        if len(titles) > 32:
            with open(sys.argv[1], "a") as f:
                for pair in titles:
                    f.write(str(pair))
                    f.write("\n")
            titles = []
        time.sleep(1)
