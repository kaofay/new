from vpython import *
import tkinter as tk
from tkinter import ttk
import math
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False
def run_simulation():
    try:
        v = float(ev.get())
        a = float(ea.get()) if motion_var.get() == "拋物線" else 0
        a = math.radians(a)
        g = 9.8
        selected_motion = motion_var.get()

        ball.clear_trail()
        if selected_motion == "拋物線":
            vx = v * math.cos(a)
            vy = v * math.sin(a)
            ball.pos = vector(-15, 0, 0)
            ball.velocity = vector(vx, vy, 0)
            t = 0
            while ball.pos.y >= 0 and motion_var.get() == "拋物線":
                rate(100)
                ball.pos.x = -15 + ball.velocity.x * t
                ball.pos.y = ball.velocity.y * t - 0.5 * g * t**2
                ball.velocity.y = vy - g * t
                scene.center = ball.pos
                t += 0.01

        elif selected_motion == "自由落體":
            ball.pos = vector(0, 20, 0)
            t = 0
            while ball.pos.y >= 0 and motion_var.get() == "自由落體":
                rate(100)
                ball.pos.y = 20 - 0.5 * g * t**2
                scene.center = ball.pos
                t += 0.01

        elif selected_motion == "圓周運動":
            radius = 5
            omega = v / radius
            t = 0
            while t <= 2 * math.pi / omega and motion_var.get() == "圓周運動":
                rate(100)
                ball.pos = vector(radius * math.cos(omega * t),
                                  radius * math.sin(omega * t) + 5, 0)
                scene.center = ball.pos
                t += 0.01

    except ValueError:
        print("輸入錯誤，請檢查數值！")

def start():
    selected_motion = motion_var.get()
    if selected_motion == "雙狹縫干涉":
        open_double_slit_gui()
    else:
        threading.Thread(target=run_simulation).start()
def compute_pattern(wavelength, slit_width, slit_sep, L):
    x = np.linspace(-10e-3, 10e-3, 1000)
    y = np.linspace(-5e-3, 5e-3, 500)
    X, Y = np.meshgrid(x, y)
    alpha = np.pi * slit_sep * X / (wavelength * L)
    beta = np.pi * slit_width * X / (wavelength * L)
    I = (np.cos(alpha) ** 2) * (np.sinc(beta / np.pi) ** 2)
    I /= I.max()
    return x, y, I

def update_plot(event=None):
    wavelength = wavelength_var.get() * 1e-9
    slit_width = width_var.get() * 1e-6
    slit_sep   = sep_var.get() * 1e-6
    L          = L_var.get()
    x, y, I = compute_pattern(wavelength, slit_width, slit_sep, L)
    ax.clear()
    ax.imshow(I, extent=[x.min()*1e3, x.max()*1e3, y.min()*1e3, y.max()*1e3],
              cmap="inferno", aspect="auto", origin="lower")
    ax.set_title("雙狹縫干涉模擬")
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    canvas.draw()

def open_double_slit_gui():
    top = tk.Toplevel(rt)
    top.title("雙狹縫干涉模擬 (滑桿版)")

    frame = ttk.Frame(top)
    frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    global wavelength_var, width_var, sep_var, L_var, fig, ax, canvas
    wavelength_var = tk.DoubleVar(value=500)
    width_var = tk.DoubleVar(value=20)
    sep_var = tk.DoubleVar(value=200)
    L_var = tk.DoubleVar(value=1.0)

    ttk.Label(frame, text="波長 λ (nm)").pack()
    tk.Scale(frame, from_=300, to=700, orient="horizontal",
             variable=wavelength_var, command=update_plot).pack(fill="x")

    ttk.Label(frame, text="狹縫寬度 a (μm)").pack()
    tk.Scale(frame, from_=5, to=100, orient="horizontal",
             variable=width_var, command=update_plot).pack(fill="x")

    ttk.Label(frame, text="狹縫間距 d (μm)").pack()
    tk.Scale(frame, from_=50, to=500, orient="horizontal",
             variable=sep_var, command=update_plot).pack(fill="x")

    ttk.Label(frame, text="螢幕距離 L (m)").pack()
    tk.Scale(frame, from_=0.1, to=5.0, resolution=0.1, orient="horizontal",
             variable=L_var, command=update_plot).pack(fill="x")

    fig, ax = plt.subplots(figsize=(6, 3.5))
    canvas = FigureCanvasTkAgg(fig, master=top)
    canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    update_plot()


rt = tk.Tk()
rt.title("運動模擬選擇")

ttk.Label(rt, text="初速 (m/s)").grid(row=0, column=0, padx=10, pady=10)
ev = ttk.Entry(rt)
ev.grid(row=0, column=1, padx=10, pady=10)

angle_frame = ttk.Frame(rt)
ttk.Label(angle_frame, text="發射角度").grid(row=0, column=0, padx=10, pady=10)
ea = ttk.Entry(angle_frame)
ea.grid(row=0, column=1, padx=10, pady=10)

motion_var = tk.StringVar()
motion_var.set("拋物線")
motion_menu = ttk.Combobox(rt, textvariable=motion_var,
                           values=["拋物線", "自由落體", "圓周運動", "雙狹縫干涉"])
motion_menu.grid(row=2, column=0, columnspan=2, pady=10)
motion_var.trace("w", lambda *args: update_inputs())

ttk.Button(rt, text="開始", command=start).grid(row=3, column=0, columnspan=2, pady=20)

scene = canvas(title="運動過程", width=1000, height=800)
scene.background = color.black
scene.range = 20
scene.center = vector(0, 5, 0)

ball = sphere(radius=0.5, color=color.white, make_trail=True)
ground = box(pos=vector(0, -0.5, 0), size=vector(80, 1, 1), color=color.green)

def update_inputs(*args):
    selected_motion = motion_var.get()
    if selected_motion == "拋物線":
        
        ev.grid(row=0, column=1, padx=10, pady=10)
        angle_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
    elif selected_motion in ["自由落體", "圓周運動"]:
       
        ev.grid(row=0, column=1, padx=10, pady=10)
        angle_frame.grid_remove()
    elif selected_motion == "雙狹縫干涉":
       
        ev.grid_remove()
        angle_frame.grid_remove()

update_inputs()
rt.mainloop()