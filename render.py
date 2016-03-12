import player
import level
import events
import math
import tkinter as tk


def init():
    global win, can, p_circle, p_cell, cell_w, cell_h
    win = tk.Tk()
    can = tk.Canvas(win, bg="dark grey",
                    width=win.winfo_screenwidth(),
                    height=win.winfo_screenheight())
    cell_w = win.winfo_screenwidth() // level.w
    cell_h = win.winfo_screenheight() // level.h
    for y in range(level.h):
        for x in range(level.w):
            if level.rows[y][x] == level.wall_id:
                can.create_rectangle(x * cell_w, y * cell_h,
                                     x * cell_w + cell_w, y * cell_h + cell_h,
                                     fill="#220")
    p_cell = can.create_rectangle(0, 0, 0, 0, fill="#0f0")
    p_circle = can.create_oval(0, 0, 0, 0, fill="#f00")
    can.bind("<KeyPress>", events.key_pressed)
    can.bind("<KeyRelease>", events.key_released)
    can.focus_set()
    can.pack()
    win.attributes("-fullscreen", True)
    loop()
    win.mainloop()
    win.destroy()


def loop():
    update()
    draw()
    win.after(20, loop)


def update():
    player.update()


def draw():
    global win, can, p_circle, p_cell, cell_w, cell_h
    px = player.x * (cell_w / player.cell_size)
    py = player.y * (cell_h / player.cell_size)
    pr = player.radius * (cell_w / player.cell_size)
    can.coords(p_circle, px - pr, py - pr, px + pr, py + pr)
    cy, cx = divmod(player.cell, level.w)
    can.coords(p_cell, cx * cell_w, cy * cell_h,
               cx * cell_w + cell_w, cy * cell_h + cell_h)
