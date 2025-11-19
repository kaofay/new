import tkinter as tk
from tkinter import messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus'] = False

root = tk.Tk()
root.title("數學圖形視覺化工具")

def show_frame(frame):
    frame.tkraise()

root.geometry("700x600")#主畫面尺寸
root.rowconfigure(0, weight=1)#讓row可以隨視窗放大縮小
root.columnconfigure(0, weight=1)#讓column可以隨視窗放大縮小

frame_menu = tk.Frame(root)#建立主選單
frame_trig = tk.Frame(root)#第二專案變換畫面
frame_integral = tk.Frame(root)#第一" " "

for frame in (frame_menu, frame_trig, frame_integral):#重複遍歷每個畫面
    frame.grid(row=0, column=0, sticky='nsew')#將每個畫面放在同一個位置方便切換

tk.Label(frame_menu, text="請選擇功能", font=("Microsoft JhengHei", 18)).pack(pady=40)#主畫面標題，pady 調整文字位置

tk.Button(frame_menu, text="三角函數圖形變換", font=("Microsoft JhengHei", 14), width=25,
          command=lambda: show_frame(frame_trig)).pack(pady=20) #功能鍵按鈕

tk.Button(frame_menu, text="定積分圖形繪製", font=("Microsoft JhengHei", 14), width=25,
          command=lambda: show_frame(frame_integral)).pack(pady=20)#功能鍵按鈕

def plot_trig():
    expr_input = entry_function.get()
    try:
        x = sp.Symbol('x')
        f_expr = sp.sympify(expr_input)
        f_lambdified = sp.lambdify(x, f_expr, 'numpy')
    except:
        messagebox.showerror("錯誤", "請輸入正確的三角函數（如 sin(x), cos(x)）")
        return

    try:
        A = float(entry_A.get())
        B = float(entry_B.get())
        C = float(entry_C.get())
        D = float(entry_D.get())
    except:
        messagebox.showerror("錯誤", "請輸入有效的 A, B, C, D 值")
        return

    x_vals = np.linspace(-2 * np.pi, 2 * np.pi, 400)
    try:
        y_original = f_lambdified(x_vals)
        y_transformed = A * f_lambdified(B * x_vals + C) + D
    except:
        messagebox.showerror("錯誤", "函數計算錯誤")
        return

    ax1.clear()
    ax1.plot(x_vals, y_original, label="原始函數", color='blue')
    ax1.plot(x_vals, y_transformed, label="變換後函數", color='red')
    ax1.set_title("三角函數伸縮與平移")
    ax1.legend()
    ax1.grid(True)
    canvas1.draw()

    inner_expr = B * x + C
    transformed_expr = A * f_expr.subs(x, inner_expr) + D
    label_result.config(text=f"變換後函數：y = {sp.simplify(transformed_expr)}")

tk.Label(frame_trig, text="輸入 f(x)：").grid(row=0, column=0)
entry_function = tk.Entry(frame_trig, width=20)
entry_function.insert(0, "sin(x)")
entry_function.grid(row=0, column=1, columnspan=4)

tk.Label(frame_trig, text="A（垂直伸縮）").grid(row=1, column=0)
entry_A = tk.Entry(frame_trig, width=5)
entry_A.insert(0, "1")
entry_A.grid(row=1, column=1)

tk.Label(frame_trig, text="B（水平伸縮）").grid(row=1, column=2)
entry_B = tk.Entry(frame_trig, width=5)
entry_B.insert(0, "1")
entry_B.grid(row=1, column=3)

tk.Label(frame_trig, text="C（水平平移）").grid(row=2, column=0)
entry_C = tk.Entry(frame_trig, width=5)
entry_C.insert(0, "0")
entry_C.grid(row=2, column=1)

tk.Label(frame_trig, text="D（垂直平移）").grid(row=2, column=2)
entry_D = tk.Entry(frame_trig, width=5)
entry_D.insert(0, "0")
entry_D.grid(row=2, column=3)

tk.Button(frame_trig, text="繪圖", command=plot_trig).grid(row=3, column=0, columnspan=5, pady=10)

fig1, ax1 = plt.subplots(figsize=(6, 4))
canvas1 = FigureCanvasTkAgg(fig1, master=frame_trig)
canvas1.get_tk_widget().grid(row=4, column=0, columnspan=5)

label_result = tk.Label(frame_trig, text="變換後函數：", fg="green", font=("Microsoft JhengHei", 12))
label_result.grid(row=5, column=0, columnspan=5, pady=10)

tk.Button(frame_trig, text="返回主選單", command=lambda: show_frame(frame_menu)).grid(row=6, column=0, columnspan=5, pady=10)

def plot_integral(eq, a, b, variable='x'):
    x = sp.Symbol(variable)
    try:
        f = sp.sympify(eq)
    except:
        messagebox.showerror("錯誤", "請輸入正確多項式")
        return

    F = sp.integrate(f, x)
    func = sp.lambdify(x, f, 'numpy')
    integral_func = sp.lambdify(x, F, 'numpy')

    xx = np.linspace(a - 2, b + 2, 400)
    yy = func(xx)
    yy_int = integral_func(xx)

    ax2.clear()
    ax2.plot(xx, yy, label=f'f(x) = {f}', color='blue')
    ax2.plot(xx, yy_int, label=f'∫f(x)dx = {F} + C', color='green', linestyle='dotted')

    x_fill = np.linspace(a, b, 100)
    y_fill = func(x_fill)
    definite_integral = sp.integrate(f, (x, a, b))
    area = definite_integral.evalf()
    ax2.fill_between(x_fill, y_fill, color='gray', alpha=0.3,
                     label=f'面積大小 = {area:.2f}')

    ax2.axhline(0, color='black')
    ax2.axvline(0, color='black')
    ax2.set_title("函數與定積分圖")
    ax2.grid(True)
    ax2.legend()
    canvas2.draw()

def on_plot_integral():
    eq = entry_func.get()
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
    except:
        messagebox.showerror("錯誤", "請輸入有效數值作為上下限")
        return
    plot_integral(eq, a, b)

tk.Label(frame_integral, text="輸入函數 f(x):").grid(row=0, column=0)
entry_func = tk.Entry(frame_integral, width=30)
entry_func.grid(row=0, column=1)

tk.Label(frame_integral, text="積分下限 a:").grid(row=1, column=0)
entry_a = tk.Entry(frame_integral)
entry_a.grid(row=1, column=1)

tk.Label(frame_integral, text="積分上限 b:").grid(row=2, column=0)
entry_b = tk.Entry(frame_integral)
entry_b.grid(row=2, column=1)

tk.Button(frame_integral, text="繪製圖形", command=on_plot_integral).grid(row=3, column=0, columnspan=2, pady=10)

fig2, ax2 = plt.subplots(figsize=(6, 4))
canvas2 = FigureCanvasTkAgg(fig2, master=frame_integral)
canvas2.get_tk_widget().grid(row=4, column=0, columnspan=3)

tk.Button(frame_integral, text="返回主選單", command=lambda: show_frame(frame_menu)).grid(row=5, column=0, columnspan=3, pady=10)#因為有兩個畫面，所以兩個畫面都要補上返回主選單按鈕才能都有功能返回主畫面

show_frame(frame_menu)
root.mainloop()
