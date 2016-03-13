import player
import level
import events
import tkinter as tk
#import _thread
#import threading
#from multiprocessing import Pool


def init():
    global win, can, mode_3d, pool
    #pool = Pool(processes=8)
    win = tk.Tk()
    can = tk.Canvas(win, bg="dark grey",
                    width=win.winfo_screenwidth(),
                    height=win.winfo_screenheight())
    mode_3d = False
    setup_2d()
    #setup_3d()
    can.bind("<KeyPress>", events.key_pressed)
    can.bind("<KeyRelease>", events.key_released)
    can.focus_set()
    can.pack()
    win.attributes("-fullscreen", True)
    loop()
    win.mainloop()
    win.destroy()


def setup_2d():
    global p_circle, p_cell, p_ball, cell_w, cell_h, walls
    cell_w = win.winfo_screenwidth() // level.w
    cell_h = win.winfo_screenheight() // level.h
    walls = {}
    for y in range(level.h):
        for x in range(level.w):
            if level.rows[y][x] == level.wall_id:
                walls[x+y*level.w] = can.create_rectangle(
                    x * cell_w, y * cell_h,
                    x * cell_w + cell_w, y * cell_h + cell_h,
                    fill="#220")
    p_cell = can.create_rectangle(0, 0, 0, 0, fill="#0f0")
    p_ball = can.create_oval(0, 0, 0, 0, fill="#ff0")
    p_circle = can.create_oval(0, 0, 0, 0, fill="#f00")


def setup_3d():
    global win, can, img_3d, px_size, px_nb, px_w, px_h
    px_w = 160
    px_h = 90
    px_nb = px_w * px_h
    px_size = min(win.winfo_screenwidth()//px_w, win.winfo_screenheight()//px_h)
    """
    img_3d = tk.PhotoImage(width=px_w*px_size, height=px_h*px_size)
    can.create_image(win.winfo_screenwidth()//2, win.winfo_screenheight()//2,
                     anchor=tk.CENTER, image=img_3d, state=tk.NORMAL)
    """
    img_3d = []
    for y in range(px_h):
        for x in range(px_w):
            img_3d.append(can.create_rectangle(
                x * px_size, y * px_size,
                x * px_size + px_size, y * px_size + px_size,
                width=0))


def loop():
    global can, mode_3d
    update()
    if events.switch:
        events.switch = False
        can.delete("all")
        if mode_3d:
            mode_3d = False
            setup_2d()
        else:
            mode_3d = True
            setup_3d()
    if mode_3d:
        draw_3d()
    else:
        draw_2d()
    win.after(20, loop)


def update():
    if events.fire:
        events.fire = False
        if player.ball_state == 0:
            player.ball_state = 1
    player.update()
    player.update_digball()


def draw_2d():
    global win, can, p_circle, p_cell, cell_w, cell_h, walls
    px = player.x * (cell_w / player.cell_size)
    py = player.y * (cell_h / player.cell_size)
    pr = player.radius * (cell_w / player.cell_size)
    can.coords(p_circle, px - pr, py - pr, px + pr, py + pr)
    cy, cx = divmod(player.cell, level.w)
    can.coords(p_cell, cx * cell_w, cy * cell_h,
               cx * cell_w + cell_w, cy * cell_h + cell_h)
    bx = player.ball_x * (cell_w / player.cell_size)
    by = player.ball_y * (cell_h / player.cell_size)
    br = max(1, pr - 1)
    can.coords(p_ball, bx - br, by - br, bx + br, by + br)
    for c in walls.keys():
        if level.get_cell_val(c) != level.wall_id:
            can.delete(walls[c])
            del walls[c]
            break


def draw_3d():
    import time
    global can, img_3d, px_w, px_h, px_nb
    dists = []
    """
    colors = ""
    for y in range(px_h):
        row = "{"
        for x in range(px_w):
            if not y:  # first row
                dists.append(128)
            color = (int(time.clock()*150%255), 0, 0)
            row += ("#%02x%02x%02x " % color) * px_size
        colors += (row + "} ") * px_size
    img_3d.put(colors)
    """
    for i in range(px_nb):
        y, x = divmod(i, px_w)
        if not y:  # first row
            dists.append(0)
        c = (int(time.clock()*150%255), x%255, y%255)
        can.itemconfig(img_3d[i], fill="#%02x%02x%02x " % c)
    """
    for i in range(px_nb):
        pool.apply_async(px_draw, [i])
    """
    """
    try:
        _thread.start_new_thread(px_draw, (i,))
    except:
        pass
    """
    """
    t = threading.Thread(target=px_draw, args=(i,))
    t.start()
    """


def px_draw(i):
    import time
    global can, img_3d, px_w, px_h, px_nb
    y, x = divmod(i, px_w)
    #if not y:  # first row
        #dists.append(0)
    c = (int(time.clock()*150%255), x%255, y%255)
    can.itemconfig(img_3d[i], fill="#%02x%02x%02x " % c)
