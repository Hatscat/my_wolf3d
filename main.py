#!/usr/bin/env python3

import player
import level
import events
import render


if __name__ == "__main__":
    print("Have fun!")
    player.init(8)
    level.init(160, 90)
    events.init()
    render.init()
