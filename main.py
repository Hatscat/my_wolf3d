#!/usr/bin/env python3

import player
import level
import events
import render


if __name__ == "__main__":
    print("Have fun!")
    level.init(32, 32)
    events.init()
    player.init(160, 90)
    render.init()
