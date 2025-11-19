import tkinter as tk
from tkinter import messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #在tkinter介面裡面嵌入matplotlib圖表
plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus']=False

def plot_graph(): #定義函數，繪製圖型
    expr_input=entry_function.get() #取得輸入框的數值
    try:
        x=sp.Symbol('x')
        f_expr=sp.sympify(expr_input) #輸入字串轉為數學式
        f_lambdified=sp.lambdify(x,f_expr,'numpy')
    except:
        messagebox.showerror("輸入的三角函數錯誤!")
        return
    try:
        A=float(entry_A.get())
        B=float(entry_B.get())
        C=float(entry_C.get())
        D=float(entry_D.get())
    except:
        messagebox.showerror("數值輸入錯誤")
        return
    
    #有關x軸
    x_val=np.linspace(-2*np.pi,2*np.pi,400) #產生從-2pi到2pi的400間距作為x軸數據
    try:
        y_original=f_lambdified(x_val) #計算x_val的y值
        y_transformed=A*f_lambdified(B*x_val+C)+D
    except:
        messagebox.showerror("函數計算錯誤")
        return
    
    
    #畫圖
    ax.clear() #清除當前圖表內容
    ax.plot(x_val,y_original,label="原始函數",color='blue') #繪製原始函數曲線
    ax.plot(x_val,y_transformed,label="改變後函數",color='red') #繪製改變後函數曲線
    ax.set_title("三角函數的伸縮與平移")
    ax.legend()
    ax.grid(True)
    canvas.draw() #把圖表更新在tkinter
    
    #產生變化後的函式
    x_sym=sp.Symbol('x') #定義一個符號x
    inner_expr=B*x_sym+C
    transformed_expr=A*f_expr.subs(x_sym,inner_expr)+D #(bx+c)代替原本的x再乘上a再加d
    label_result.config(text=f"變化後函數: y = {sp.simplify(transformed_expr)}")
    
    
#介面
root=tk.Tk()
root.title("三角函數伸縮與平移視覺化")

#輸入
tk.Label(root,text="輸入函數:").grid(row=0,column=0,sticky='e') #建立標籤並調整位置
entry_function=tk.Entry(root,width=30) #建立輸入框
entry_function.grid(row=0,column=1,columnspan=4) #將函數輸入框放在網格裡，跨越4列
entry_function.insert(0,"sin(x)") #預設函數輸入框內容為""sin(x)"

tk.Label(root,text="A(垂直伸縮)").grid(row=1,column=0) #a參數標籤
entry_A=tk.Entry(root,width=5) #建立a輸入框
entry_A.insert(0,"1")
entry_A.grid(row=1,column=1) #輸入框放在網格裡

tk.Label(root,text="B(水平伸縮)").grid(row=1,column=2) #a參數標籤
entry_B=tk.Entry(root,width=5) #建立a輸入框
entry_B.insert(0,"1")
entry_B.grid(row=1,column=3) #輸入框放在網格裡

tk.Label(root,text="C(水平平移)").grid(row=2,column=0) #a參數標籤
entry_C=tk.Entry(root,width=5) #建立a輸入框
entry_C.insert(0,"1")
entry_C.grid(row=2,column=1) #輸入框放在網格裡

tk.Label(root,text="D(垂直平移)").grid(row=2,column=2) #a參數標籤
entry_D=tk.Entry(root,width=5) #建立a輸入框
entry_D.insert(0,"1")
entry_D.grid(row=2,column=3) #輸入框放在網格裡


tk.Button(root,text="執行",command=plot_graph).grid(row=3,column=0,columnspan=5,pady=10) #設定button位置及參數選項

#畫圖區
fig,ax=plt.subplots(figsize=(6,4)) #建立圖形和子圓
canvas=FigureCanvasTkAgg(fig,master=root) #把物件嵌入到視窗
canvas.get_tk_widget().grid(row=4,column=0,columnspan=5)
#顯示輸出
label_result=tk.Label(root,text="變化後函數:",fg="green",font=("Microsoft JhengHei",12))
label_result.grid(row=5,column=0,columnspan=5,pady=10)

root.mainloop()