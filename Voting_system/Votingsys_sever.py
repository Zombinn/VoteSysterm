from tkinter import *
import socket
import threading
from tkinter.messagebox import showinfo
import time
import traceback

this_votecal=[0,0,0,0,0,0]  # 各选项得票计数
# 锁


def NotifyAll(xx):
    global msg
    if con.acquire():
        msg = xx
        con.notifyAll()
        con.release()


con = threading.Condition()  # 条件
msg = ""
mysk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 发送


def CTout(conn,connaddr):
    global msg
    while True:
        if con.acquire():
            con.wait()
            if msg:
                try:
                    conn.send(msg.encode())
                    NotifyAll("")
                    con.release()
                except:
                    con.release()
                    return
# 接收


def CTin(conn,connaddr):
    global this_votecal
    while True:
        try:
            data = conn.recv(1024).decode()
            if not data:
                conn.close()
                return
            else:
                if data == "1" or \
                        data == "2" or \
                        data == "3" or \
                        data == "4" or \
                        data == "5" or \
                        data == "6":
                    this_votecal[int(data)-1] += 1
                else:
                    InfoWin(data)
                    writetxt = open("e:\\vote.txt", "a")
                    writetxt.write(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + "\n" +data)
                    writetxt.close()
        except:
            InfoWin("异常!!!"+"\n"+traceback.format_exc())
            return
# 发布投票


def Dealoutvote():
    myconn = int((threading.activeCount()) / 2)
    if myconn == 0:
        InfoWin("没有客户端连接！")
    else:
        if str(topictext.get()) == "":
            InfoWin("请输入投票主题！")
        else:
            if str(c1text.get()) == "" or str(c2text.get()) == "":
                InfoWin("请至少输入选项1和2")
            else :
                msg = "投票主题：\n" + str(topictext.get()) + "\n" + \
                      "选项1：" + str(c1text.get()) + "\n" + \
                      "选项2：" + str(c2text.get()) + "\n" + \
                      "选项3：" + str(c3text.get()) + "\n" + \
                      "选项4：" + str(c4text.get()) + "\n" + \
                      "选项5：" + str(c5text.get()) + "\n" + \
                      "选项6：" + str(c6text.get())
                InfoWin("投票已发送（主题：" + str(topictext.get()) + "）")
                NotifyAll(msg)
# 发布结果


def Dealoutres():
    myconn = int((threading.activeCount()) / 2)
    if myconn == 0:
        InfoWin("没有客户端连接！")
    else:
        temp = "投票主题：\n" + str(topictext.get()) + "\n" + \
                 "选项1：" + str(c1text.get()) + "\n" + str(this_votecal[0]) + \
                 "票\n选项2：" + str(c2text.get()) + "\n" + str(this_votecal[1]) + \
                 "票\n选项3：" + str(c3text.get()) + "\n" + str(this_votecal[2]) + \
                 "票\n选项4：" + str(c4text.get()) + "\n" + str(this_votecal[3]) + \
                 "票\n选项5：" + str(c5text.get()) + "\n" + str(this_votecal[4]) + \
                 "票\n选项6：" + str(c6text.get()) + "\n" + str(this_votecal[5]) + \
                 "票\n"
        NotifyAll(temp)
        InfoWin("投票结果已发布！")
        writetxt = open("e:\\finallvote.txt", "a")
        writetxt.write(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + "\n" + temp)
        writetxt.close()
# 启动服务器


def StartSever():
    global mysk
    ip_port = (str(ipinput.get()), int(portinput.get()))
    mysk.bind(ip_port)
    InfoWin("服务器开启")
    mysk.listen(5)
    InfoWin("等待...")
    threading.Thread(target=ConnW, args=(mysk,)).start()


def ConnW(mysk):
    global msg
    while True:
        conn, address = mysk.accept()
        connaddr = conn.recv(2048).decode()
        InfoWin(connaddr + "连接")
        InfoWin("当前连接数：" + str(int((threading.activeCount()) / 2)))
        threading.Thread(target=CTin, args=(conn, connaddr)).start()
        threading.Thread(target=CTout, args=(conn, connaddr)).start()
# 帮助信息


def MyHelp():
    showinfo(title="帮助信息", message="应用程序使用说明：1）输入端口和ip以启动服务器。2）等待各个客户端连接后，输入投票主题和选项（至少要输入选项一选项二）"+
                                        "3)等待客户端投票（投票情况可按刷新键实时查看），后可按需求停止投票。4）发布结果，后可重置投票，以开始新的投票。")
# 信息


def InfoWin(msg):
    wininfo = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + "\n" + msg + "\n"
    InfoText.config(state=NORMAL)
    InfoText.insert(END, wininfo)
    InfoText.config(state=DISABLED)
# 投票计数


def  VoteCal(i):
    global this_votecal
    return this_votecal[i-1]
# 刷新


def ResShow():
    c1R["text"] = "1: " + str(VoteCal(1)) + "票"
    c2R["text"] = "2: " + str(VoteCal(2)) + "票"
    c3R["text"] = "3: " + str(VoteCal(3)) + "票"
    c4R["text"] = "4: " + str(VoteCal(4)) + "票"
    c5R["text"] = "5: " + str(VoteCal(5)) + "票"
    c6R["text"] = "6: " + str(VoteCal(6)) + "票"
# 停止投票


def StopVote():
    mysk.close()
    InfoWin("投票已停止！")
# 重置投票


def NewVote():
    global this_votecal
    i = 0
    while i < 6:
        this_votecal[i] = 0
        i += 1
    topictext["text"] = ""
    c1text["text"] = ""
    c2text["text"] = ""
    c3text["text"] = ""
    c4text["text"] = ""
    c5text["text"] = ""
    c6text["text"] = ""
    c1R["text"] = "1: " + str(VoteCal(1)) + "票"
    c2R["text"] = "2: " + str(VoteCal(2)) + "票"
    c3R["text"] = "3: " + str(VoteCal(3)) + "票"
    c4R["text"] = "4: " + str(VoteCal(4)) + "票"
    c5R["text"] = "5: " + str(VoteCal(5)) + "票"
    c6R["text"] = "6: " + str(VoteCal(6)) + "票"
    InfoWin("投票已重置！")

# 窗体GUI


win1 = Tk()
win1.title("V_sever")
win1.geometry("500x400")
TopTlitle = Label(win1, text="欢迎使用投票系统！", font=("楷体", 16, "normal"))
TopTlitle.place(x=280, y=10)
# 信息窗
Infoframe = Frame(win1, height=300, width=160, )
InfoText = Text(Infoframe, fg="white", bg="black")
InfoText.config(state=DISABLED)
InfoText.grid()
Infoframe.grid(row=0, column=0, columnspan=2, padx=30, pady=80)
Infoframe.grid_propagate(0)
# 设置端口
btn = Button(win1, text="启动服务器", command=StartSever)
btn.place(x=160, y=40)
port = Label(win1, text="端口号：")
port.place(x=30, y=20)
ip = Label(win1, text="ip：")
ip.place(x=30, y=50)
portinput = Entry(win1, width=4)
portinput.insert(INSERT, "")
portinput.place(x=88, y=20)
ipinput = Entry(win1, width=8)
ipinput.insert(INSERT, "")
ipinput.place(x=60, y=50)
# 设置投票
Topic = Label(win1, text="投票主题：")
Topic.place(x=220, y=80)
topictext = Entry(win1, width=8)
topictext.place(x=220, y=100)
topictext.insert(INSERT, "")
c1 = Label(win1, text="选项1：")
c1.place(x=220, y=120)
c1text = Entry(win1, width=8)
c1text.place(x=220, y=140)
c1text.insert(INSERT, "")
c2 = Label(win1, text="选项2：")
c2.place(x=220, y=160)
c2text = Entry(win1, width=8)
c2text.place(x=220, y=180)
c2text.insert(INSERT, "")
c3 = Label(win1, text="选项3：")
c3.place(x=220, y=200)
c3text = Entry(win1, width=8)
c3text.place(x=220, y=220)
c3text.insert(INSERT, "")
c4 = Label(win1, text="选项4：")
c4.place(x=220, y=240)
c4text = Entry(win1, width=8)
c4text.place(x=220, y=260)
c4text.insert(INSERT, "")
c5 = Label(win1, text="选项5：")
c5.place(x=220, y=280)
c5text = Entry(win1, width=8)
c5text.place(x=220, y=300)
c5text.insert(INSERT, "")
c6 = Label(win1, text="选项6：")
c6.place(x=220, y=320)
c6text = Entry(win1, width=8)
c6text.place(x=220, y=340)
c6text.insert(INSERT, "")
# 投票情况
Res = Label(win1, text="当前投票情况:")
c1R = Label(win1, text="1: " + str(VoteCal(1)) + "票")
c2R = Label(win1, text="2: " + str(VoteCal(2)) + "票")
c3R = Label(win1, text="3: " + str(VoteCal(3)) + "票")
c4R = Label(win1, text="4: " + str(VoteCal(4)) + "票")
c5R = Label(win1, text="5: " + str(VoteCal(5)) + "票")
c6R = Label(win1, text="6: " + str(VoteCal(6)) + "票")
Res.place(x=330, y=210)
c1R.place(x=330, y=230)
c2R.place(x=390, y=230)
c3R.place(x=330, y=260)
c4R.place(x=390, y=260)
c5R.place(x=330, y=290)
c6R.place(x=390, y=290)
c1R["text"] = win1.update()
# 功能键
SendVote = Button(win1, text="发起投票", command=Dealoutvote)
StopVote = Button(win1, text="停止投票", command=StopVote)
ReVote = Button(win1, text="重置投票", command=NewVote)
Reashow = Button(win1, text=" 刷 新 ", command=ResShow)
SendResult = Button(win1, text="发布结果", command=Dealoutres)
SendVote.place(x=330, y=100)
StopVote.place(x=330, y=140)
ReVote.place(x=330, y=180)
Reashow.place(x=330, y=330)
SendResult.place(x=390, y=330)
# 菜单
Mymenu = Menu(win1)
Mymenu.add_command(label=" 帮 助 ", command=MyHelp)
win1["menu"] = Mymenu

win1.update_idletasks()
win1.mainloop()