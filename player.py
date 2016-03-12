import math
import level
import events


def init(_cell_size):
    global x, y, px, py, cell_size, cell, angle, walk_speed, turn_speed, radius
    cell_size = _cell_size
    px, py = x, y = 0, 0
    cell = 0
    angle = 1.57
    walk_speed = 1.
    turn_speed = 0.06
    radius = cell_size // 4


def get_cell(_x, _y):
    return int((x // cell_size) + ((y // cell_size) * level.w))


def set_cell(_cell):
    global x, y, cell
    cell = _cell
    x = (cell % level.w) * cell_size + cell_size // 2
    y = (cell // level.w) * cell_size + cell_size // 2


def set_xy(_x, _y):
    global x, y, px, py, cell
    px, py = x, y
    x, y = _x, _y
    cell = get_cell(x, y)


def turn():
    global angle, turn_speed
    angle = (angle + events.turn_dir * turn_speed) % (math.pi * 2)


def move():
    global x, y, px, py, angle, walk_speed, radius
    nx = x + math.cos(angle) * events.move_dir * walk_speed
    ny = y + math.sin(angle) * events.move_dir * walk_speed
    if level.get_cell_val(get_cell(nx, ny)) == level.path_id:
        set_xy(nx, ny)
    else:
        x, y = px, py


def update():
    if events.turn_dir != 0:
        turn()
    if events.move_dir != 0:
        move()
