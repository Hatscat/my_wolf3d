def init():
    global turn_dir, move_dir, keys
    turn_dir = move_dir = 0
    keys = {
        "left": ["Left", "q", "Q",  "a", "A"],
        "right": ["Right", "d", "D"],
        "up": ["Up", "z", "Z", "w", "W"],
        "down": ["Down", "s", "S"]
    }


def key_pressed(_event):
    global turn_dir, move_dir, keys
    k = _event.keysym
    if k == "Escape":
        exit("hope you enjoyed, see you :)")
    if k in keys["left"]:
        turn_dir = -1
    elif k in keys["right"]:
        turn_dir = 1
    if k in keys["up"]:
        move_dir = -1
    elif k in keys["down"]:
        move_dir = 1


def key_released(_event):
    global turn_dir, move_dir, keys
    k = _event.keysym
    if k in keys["left"] or k in keys["right"]:
        turn_dir = 0
    elif k in keys["up"] or k in keys["down"]:
        move_dir = 0
