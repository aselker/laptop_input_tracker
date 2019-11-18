#!/usr/bin/env python3

"""
Logs frequencies of keys and key pairs, e.g. "t" then "h"
"""

import os
import sys
import time
import pyxhook
import pickle

log_file_name = sys.argv[1]

recent_history = {}
last_key = "space"
second_last_key = "space"


def OnKeyPress(event):
    global last_key
    global second_last_key

    recent_history[event.Key] = recent_history.get(event.Key, 0) + 1

    pair = (last_key, event.Key)
    recent_history[pair] = recent_history.get(pair, 0) + 1

    triple = (second_last_key, last_key, event.Key)
    recent_history[triple] = recent_history.get(triple, 0) + 1

    second_last_key = last_key
    last_key = event.Key


# create a hook manager object
new_hook = pyxhook.HookManager()
new_hook.KeyDown = OnKeyPress
# set the hook
new_hook.HookKeyboard()
new_hook.start()


if not os.path.isfile(log_file_name):
    pickle.dump({}, open(log_file_name, "wb"))


while True:
    if sum(recent_history.values()) > 12:
        all_history = pickle.load(open(log_file_name, "rb"))
        for key, value in recent_history.items():
            all_history[key] = all_history.get(key, 0) + recent_history[key]
        pickle.dump(all_history, open(log_file_name, "wb"))
        recent_history = {}

    time.sleep(1)
