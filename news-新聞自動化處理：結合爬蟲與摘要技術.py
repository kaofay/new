import tkinter as tk
from tkinter import messagebox
import requests #請求訪問網站的模組
from bs4 import BeautifulSoup #匯入bs4 用來解析HTML的模組
from transformers import pipeline #用於ai摘要
import threading #多線程優化，在執行過程不卡住介面
import time #時間模組

#summarizer=pipeline("summarization",model="facebook/bart-large-cnn")
summarizer = pipeline("summarization",model ="facebook/bart-large-cnn")#transformers 提供的summeruzation,載入模型做摘要

def safe_request(url,retries=3): #請求函數(設次數為3,增加請求成功率)
    headers={"User-Agent":"Mozilla/2.5"} #代理瀏覽器
    for _ in range(retries):
        try:
            res=requests.get(url,headers=headers,timeout=10) #發送get請求,最多10秒
            res.raise_for_status() #如果狀態碼不是200,就拋出異常
            return res #成功回傳response物件
        except:
            time.sleep(1) #如果錯誤,等1秒再試
    raise Exception("爬取資料失敗") #三次都失敗後跳錯誤訊息


def fetch_new_list():
    url="https://news.ltn.com.tw/list/breakingnews" #自由時報網址
    res=safe_request(url) #使用安全函數取得網頁資料
    soup=BeautifulSoup(res.text,"html.parser") #解析HTML的內容
    articles=soup.select('ul.list > li a')[:10] #抓取前10篇文章的標題
    
    new_list=[] #空新聞清單
    for a in articles:
        title=a.text.strip() #取得標題文字(去除空白)
        link=a['href'] #取得連結網址
        if not link.startswith('http'):
            link='https'+link #補上http
        new_list.append(title,link) #將標題和連結加入清單
    return new_list #回傳新聞清單
    
def summarize_news(link):
    res=safe_request(link) #安全請求新聞全文網頁
    soup=BeautifulSoup(res.text,"html.parser") #解析HTML的內容
    content_div=soup.select_one("div.text") #找出class="text"的區域,一般是新聞正文
    if not content_div: #如果找不到
        return "找不到新聞內容" #回傳錯誤訊息
    
    paragraphs=content_div.find_all('p') #取得所有段落
    full_text="".join(p.text for p in paragraphs) #將段落文字合併成一串
    trimmed_text="".join(full_text.split()[:900]) #取前900字避免ai出錯
    
    summary=summarizer(trimmed_text,max_length=100,min_length=30,do_sample=False) #ai摘要 30~100
    
    return summary[0]['summary_text'] #回傳摘要文字

def loading_animation():
    dots=0 #初始化點點數量
    while loading_flag: #當loading_flag=true 時持續執行
        text_area.insert(tk.END) #在文字區新增一個點
        text_area.see(tk.END) #滾動視窗顯示最新文字
        dots+=1 #點點數量加一
        if dots%5==0:
            text_area.delete("end-5c",tk.END) #清除前5個字元/點
        time.sleep(0.5) #控制畫面速度
        
def fetch_and_display(title,link):
    global loading_flag
    try:
        summary=summarize_news(link) #取得新聞摘要
        loading_flag=False
        text_area.delete("1.0",tk.END) #清空文字區
        text_area.insert(tk.END,f"標題:{title}\n連結:{link}\n\n摘要:\n{summary}")
        
    except Exception as e:
        loading_flag=False
        text_area.insert(tk.END,f"\錯誤:{str(e)}") #錯誤訊息
        
def on_select(event):
    global loading_flag
    selection=listbox.curselection()
    if not selection:
        return
    index=selection[0] #取出索引值
    title,link=news_items[index] #取得新聞標題和連結
    
    text_area.delete("1.0",tk.END)
    text_area.insert(tk.END,f"標題:{title}\n連結:{link}\n\n正在抓取摘要") #顯示載入訊息
    loading_flag=True #啟動讀取動畫
    
    #多線程優化
    threading.Thread(target=loading_animation,daemon=True).start() #開啟讀取動畫背景執行緒
    threading.Thread(target=fetch_and_display,args=(title,link),daemon=True).start() #開啟背景執行序並顯示摘要

def refresh_news():
    global news_items
    try:
        new_items=fetch_new_list() #重新取得最新新聞
        listbox.delete(0,tk.END)
        for title,link in new_items:#把新聞標題一個一個放到listbox裡
            listbox.insert(tk.END,title)
        text_area.delete("1.0",tk.END) #清空文字區
        text_area.insert(tk.END,"更新後的新聞列表") #顯示更新完成的訊息
    except Exception as e:
        messagebox.showerror("錯誤",str(e)) #錯誤訊息
        
root=tk.Tk()
root.title("最新新聞")
root.geometry("1000x600") #設定視窗大小
frame_left=tk.Frame(root)
frame_left.pack(side="left",fill="y",padx=10,pady=10) #設定左邊框

btn_refresh=tk.Button(frame_left,text="重新整理新聞",font=("Arial",12),command=refresh_news) #建立按鈕
btn_refresh.pack(pady=(0,5))
tk.Label(frame_left,text="最新新聞",font=("Arial",14)).pack()
listbox=tk.Listbox(frame_left,width=45,font=("Arial",12))
listbox.pack(fill="y",expand=True) #垂直方向填滿,可擴張

frame_right=tk.Frame(root) #右框架
frame_right.pack(side="right",fill="both",expand=True,padx=10,pady=10)

text_area=tk.Text(frame_right,font=("Arial",12),wrap="word") #建立文字輸入框,顯示新聞摘要,文字自動換行
text_area.pack(fill="both",expand=True)
news_items=fetch_new_list() #程式啟動時先抓一次新聞清單
for title,link in news_items:
    listbox.insert(tk.END,title)
listbox.bind("<<ListboxSelect>>",on_select) #綁定listbox的選取事件
root.mainloop()
