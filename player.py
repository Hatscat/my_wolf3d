import math
import level
import events


def init(_cell_size):
    global x, y, px, py, cell_size, cell, angle, walk_speed, turn_speed, radius
    cell_size = _cell_size
    px, py = x, y = 0, 0
    cell = 0
    angle = 1.57
    walk_speed = 2.
    turn_speed = 0.06
    radius = cell_size // 4
    init_digball()


def init_digball():
    global ball_state, ball_x, ball_y, ball_angle, ball_speed
    ball_state = 0
    ball_x, ball_y = x, y
    ball_angle = angle
    ball_speed = walk_speed * 3.


def get_cell(_x, _y):
    return int((_x // cell_size) + ((_y // cell_size) * level.w))


def set_cell(_cell):
    global x, y, cell
    cell = _cell
    x = (cell % level.w) * cell_size + cell_size // 2
    y = (cell // level.w) * cell_size + cell_size // 2


def set_xy(_x, _y):
    global x, y, px, py, cell, ball_x, ball_y
    px, py = x, y
    x, y = _x, _y
    cell = get_cell(x, y)
    if ball_state == 0:
        ball_x, ball_y = x, y


def turn():
    global angle, turn_speed, ball_angle
    angle = (angle + events.turn_dir * turn_speed) % (math.pi * 2)
    if ball_state == 0:
        ball_angle = angle


def move():
    global x, y, px, py, angle, walk_speed, radius
    nx = x + math.cos(angle) * events.move_dir * walk_speed
    ny = y + math.sin(angle) * events.move_dir * walk_speed
    if level.get_cell_val(get_cell(nx, ny)) == level.path_id:
        set_xy(nx, ny)
    else:
        set_xy(px, py)


def update():
    if events.turn_dir != 0:
        turn()
    if events.move_dir != 0:
        move()


def update_digball():
    global ball_state, ball_x, ball_y, ball_angle, ball_speed, radius
    if ball_state == 1:
        ball_x -= math.cos(ball_angle) * ball_speed
        ball_y -= math.sin(ball_angle) * ball_speed
        bc = get_cell(ball_x, ball_y)
        if math.hypot(x - ball_x, y - ball_y) > ball_speed * 12:
            ball_state = 2
        elif level.get_cell_val(bc) == level.wall_id:
            ball_state = 2
            lw = level.w
            cx = bc % lw
            if bc > lw and bc < level.cells_nb-lw and cx > 0 and cx < lw-1:
                level.rows[bc // lw][cx] = level.path_id
    elif ball_state == 2:
        ball_x += (x - ball_x) / 8
        ball_y += (y - ball_y) / 8
        if math.hypot(x - ball_x, y - ball_y) < radius:
            ball_state = 0
            ball_x, ball_y = x, y
