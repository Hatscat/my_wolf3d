import player
from random import randint


def init(_w, _h):
    global w, h, cells_nb, rows, path_id, wall_id
    w, h = _w, _h
    cells_nb = w * h
    path_id = 0
    wall_id = 1
    rows = []
    for y in range(h):
        rows.append([])
        for x in range(w):
            rows[y].append(path_id)
    fill_base()
    fill_neighbors(6)


def get_cell_val(_cell):
    y, x = divmod(_cell, w)
    return rows[y][x]


def fill_base():
    global w, h, cells_nb, rows, wall_id
    for y in range(h):
        rows[y][0] = rows[y][w-1] = wall_id
    for x in range(w):
        rows[0][x] = rows[h-1][x] = wall_id
    for i in range(int(cells_nb * 0.375)):
        y, x = divmod(randint(1, cells_nb-2), w)
        while rows[y][x] == wall_id:
            y, x = divmod(randint(1, cells_nb-2), w)
        rows[y][x] = wall_id


def fill_neighbors(iterations):
    global w, h, rows, path_id, wall_id
    for y in range(1, h-1):
        for x in range(1, w-1):
            sx = slice(x-1, x+2)
            c1 = (rows[y-1][sx] + rows[y][sx] + rows[y+1][sx]).count(wall_id)
            if iterations < 4 or y < 2 or y > h-3 or x < 2 or x > w-3:
                if c1 > 4:
                    rows[y][x] = wall_id
                else:
                    rows[y][x] = path_id
                    player.set_cell(x + y * w)
            else:
                g = rows[y-2][sx] + rows[y+2][sx]
                for i in range(y-2, y+3):
                    g.append(rows[i][x-2])
                    g.append(rows[i][x+2])
                c2 = c1 + g.count(wall_id)
                rows[y][x] = wall_id if c1 > 4 or c2 < 9 else path_id
    iterations -= 1
    if iterations > 0:
        fill_neighbors(iterations)
