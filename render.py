import player
import level
import events
import math
import tkinter as tk


def init():
    global win
    global can
    global p_circle
    win = tk.Tk()
    can = tk.Canvas(win, bg="dark grey",
                    width=win.winfo_screenwidth(),
                    height=win.winfo_screenheight())
    p_circle = can.create_oval(player.x - player.radius,
                               player.y - player.radius,
                               player.x + player.radius,
                               player.y + player.radius,
                               fill="red")
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
    player.dir = (player.dir + events.turn_dir*player.turn_speed) % (math.pi*2)
    player.x += math.cos(player.dir) * events.move_dir * player.walk_speed
    player.y += math.sin(player.dir) * events.move_dir * player.walk_speed


def draw():
    can.coords(p_circle,
               player.x - player.radius, player.y - player.radius,
               player.x + player.radius, player.y + player.radius)
