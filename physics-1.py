import math
from vpython import *
import tkinter as tk
from tkinter import ttk
import threading #在執行過程不卡住介面

def update_input(*args):
    # 根據選擇的運動方式，決定是否顯示角度輸入欄
    if motion_var.get() == '拋物線':
        label_angle.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ea.grid(row=1, column=1, padx=10, pady=10, sticky="w")
    else:
        label_angle.grid_remove()
        ea.grid_remove()

def run_simulation():
    try:
        v = float(ev.get())  # 初速度
        a = float(ea.get()) if motion_var.get() == "拋物線" else 0
        a = math.radians(a)  # 角度轉弧度
        g = 9.8
        select_motion = motion_var.get()
        ball.clear_trail()  # 清除軌跡
        t = 0

        if select_motion == "拋物線":
            vx = v * math.cos(a)
            vy = v * math.sin(a)
            ball.pos = vector(-15, 0, 0)
            ball.velocity = vector(vx, vy, 0)
            while ball.pos.y >= 0:
                rate(100)
                ball.pos.x = -15 + ball.velocity.x * t
                ball.pos.y = ball.velocity.y * t - 0.5 * g * t ** 2
                ball.velocity.y = vy - g * t
                scene.center = ball.pos
                t += 0.01

        elif select_motion == "自由落體":
            ball.pos = vector(0, 20, 0)
            while ball.pos.y >= 0:
                rate(100)
                ball.pos.y = 20 - 0.5 * g * t ** 2
                scene.center = ball.pos
                t += 0.01

        elif select_motion == "圓周運動":
            radius = 5
            omega = v / radius
            while t <= 2 * math.pi / omega:
                rate(100)
                ball.pos = vector(radius * math.cos(omega * t),
                                  radius * math.sin(omega * t) + 5,
                                  0)
                scene.center = ball.pos
                t += 0.01

    except ValueError:
        print("輸入錯誤")

def start():
    threading.Thread(target=run_simulation).start()

# --- Tkinter GUI ---
rt = tk.Tk()
rt.title("物理運動模擬視覺化")

# 初速度輸入
ttk.Label(rt, text="初速度 (m/s)").grid(row=0, column=0, padx=10, pady=10, sticky="e")
ev = ttk.Entry(rt)
ev.grid(row=0, column=1, padx=10, pady=10, sticky="w")

# 發射角度輸入（預設會隱藏，拋物線時才出現）
label_angle = ttk.Label(rt, text="發射角度 (度)")
label_angle.grid(row=1, column=0, padx=10, pady=10, sticky="e")
ea = ttk.Entry(rt)
ea.grid(row=1, column=1, padx=10, pady=10, sticky="w")

# 運動類型選單
motion_var = tk.StringVar()
motion_var.set("拋物線")
motion_menu = ttk.Combobox(rt, textvariable=motion_var,
                           values=["拋物線", "自由落體", "圓周運動"])
motion_menu.grid(row=2, column=0, columnspan=2, pady=10)
motion_var.trace("w", update_input)

# 開始按鈕
ttk.Button(rt, text="開始", command=start).grid(row=3, column=0, columnspan=2, pady=20)

# VPython 畫面
scene = canvas(title="運動過程", width=1000, height=800)
scene.background = color.black
scene.range = 20
scene.center = vector(0, 5, 0)

ball = sphere(radius=0.5, color=color.white, make_trail=True)
ground = box(pos=vector(0, -0.5, 0), size=vector(80, 1, 1), color=color.green)

update_input()
rt.mainloop()