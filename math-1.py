import numpy as np #產生數值範圍(連續x)
import matplotlib.pyplot as plt #繪製
import sympy as sp #x,y代數積分的運算符號
import tkinter as tk
from tkinter import messagebox #跳出錯誤訊息
#plt.rcParams['font.family']='Microsoft JhengHei'
plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
plt.rcParams['axes.unicode_minus']=False

#定義主要函式，接收引入的函數區間後繪圖
def plot_integral(equation,a,b,variable='x'):
    x=sp.Symbol(variable) #定義x給sympy
    try:
        f=sp.sympify(equation) #把字串轉成sympy讀懂的函式
    except sp.SympifyError: #如sympy字串轉換失敗
        messagebox.showerror("錯誤，請輸入正確的多項式")
        return
    F=sp.integrate(f,x) #計算不定積分
    func=sp.lambdify(x,f,'numpy') #轉換成可計算函式
    integral_func=sp.lambdify(x,F,'numpy')
    
    xx=np.linspace(a-2,b+2,400) #產生範圍
    yy=func(xx) #計算f(x)的y值
    integral_values=integral_func(xx) #不定積分F(x)的y值
    
    
    plt.figure(figsize=(8,6)) #建立視窗，尺寸8*6
    plt.plot(xx,yy,label=f'f(x)={f}',color='blue') #輸出函式，標籤為函式本身
    plt.plot(xx,integral_values,label=f'∫f(x)dx={F}+C',color='green',linestyle='dotted') #畫出不定積分
    
    definite_integral=sp.integrate(f,(x,a,b)) #計算定積分
    
    x_fill=np.linspace(a,b,100) #填色區的x
    y_fill=func(x_fill) #填色區的y
    round_area=round(definite_integral.evalf(),2) #取到小數點第二位
    plt.fill_between(x_fill,y_fill,color='gray',alpha=0.3,label=f'面積大小={round_area:.2f}') #填充上下限
    
    plt.axhline(0,color='black',linewidth=1) #垂直x軸
    plt.axvline(0,color='black',linewidth=1) #垂直y軸
    plt.grid(True,linestyle='--',alpha=0.6) #顯示格線，alpha表示透明度
    plt.legend() #顯示圖例
    plt.title("函式與定積分圖")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
    
#使用者按下繪製圖形時執行
def on_plot():
    eq=entry_func.get()
    try:
        a=float(entry_a.get()) #取得積分下限
        b=float(entry_b.get()) #取得積分上限
    except ValueError: #如果型態錯誤
        messagebox.showerror("上下限輸入型態不正確")
        return
    plot_integral(eq,a,b) #呼叫主要圖表函式
    
#建立tkinter介面
root=tk.Tk() #主視窗
root.title("定積分視覺化圖表")

tk.Label(root,text="輸入函數f(x):").grid(row=0,column=0,sticky='e') #函數標籤、位置
entry_func=tk.Entry(root,width=30) #輸入欄位(函數的欄位)
entry_func.grid(row=0,column=1) #設定位置

#輸入欄、標籤...
tk.Label(root,text="下限:").grid(row=1,column=0,sticky='e') #下限a的標籤
entry_a=tk.Entry(root) #輸入欄位(下限的欄位a)
entry_a.grid(row=1,column=1) #設定位置
tk.Label(root,text="上限:").grid(row=2,column=0,sticky='e') #上限b的標籤
entry_b=tk.Entry(root) #輸入欄位(上限欄位b)
entry_b.grid(row=2,column=1) #設定位置

#建立可生成圖表的按鈕
btn_plot=tk.Button(root,text="繪製圖表",command=on_plot) #生成圖表按鈕
btn_plot.grid(row=3,column=0,columnspan=2,pady=10) #顯示位置


root.mainloop() #讓tkinter在執行時保持顯示部關閉，直到主程式互動