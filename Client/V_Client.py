from tkinter import *
import socket
import os
import time
import threading
from tkinter.messagebox import showinfo

myclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msgout = ""
votepass = 0
con = threading.Condition()


def NotifyAll(xx):
    global msgout
    if con.acquire():
        msgout = xx
        con.notifyAll()
        con.release()
# 接收


def DealIn(myclient):
    global votepass
    while True:
        try:
            data = myclient.recv(1024).decode()
            if not data:
                break
            else:
                votepass = 1
                InfoWin(data)
        except:
            break


thin = threading.Thread(target=DealIn, args=(myclient,))
# 发送


def Dealout(myclient):
    global msgout
    while True:
        while True:
            if con.acquire():
                con.wait()
                if msgout:
                    try:
                        myclient.send(msgout.encode())
                        NotifyAll("")
                        con.release()
                    except:
                        con.release()
                        return


thoutvote = threading.Thread(target=Dealout, args=(myclient,))
# 投票


def Getmsgout():
    global votepass
    if votepass == 0:
        InfoWin("现在不能投票！\n")
    else:
        if str(mynametext.get()) == "" or \
                str(mynametext.get()) == "1" or \
                str(mynametext.get()) == "2" or \
                str(mynametext.get()) == "3" or \
                str(mynametext.get()) == "4" or \
                str(mynametext.get()) == "5" or \
                str(mynametext.get()) == "6":
            InfoWin("请正确输入姓名！")
        else:
            msg = "IP:" + get_host_ip() + "\nCPU ID:\n" + str(id) + "\n名字：" + str(mynametext.get()) + "\n投给：" + str(
                v.get())
            NotifyAll(msg)
            InfoWin("Wait.........")
            time.sleep(2)
            msgg = str(v.get())
            NotifyAll(msgg)
            InfoWin("已投给：" + str(v.get()))
            votepass = 0
# 帮助


def MyHelp():
    showinfo(title="帮助信息", message="应用程序使用说明：1)输入对应服务器ip和端口号，进行连接。2）等待服务端发起投票。" +
                                       "3)输入姓名，并选择对应单选框后，点击投票按钮进行投票" +
                                       "4)等待服务器发送结果。\n\n（注：使用过程中会有相应信息提示。）")
# 连接服务器


def ConnSever():
    global myclient
    myclient.connect((str(ipinput.get()), int(portinput.get())))
    myclient.send(get_host_ip().encode())
    InfoWin("连接成功！")
    thin.start()
    thoutvote.start()
# HOST IP利用 UDP 协议来实现的，生成一个UDP包，把自己的 IP 放如到 UDP 协议头中，然后从UDP包中获取本机的IP。


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('1.0.0.4', 4))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip
# CPUID


id = os.popen("wmic cpu get processorid").readlines()[2]
# 消息框显示
def InfoWin(msg):
    wininfo = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) + "\n" + msg + "\n"
    InfoText.config(state=NORMAL)
    InfoText.insert(END, wininfo)
    InfoText.config(state=DISABLED)
# 窗口主体


client = Tk()

client.title("V_Client(欢迎使用投票系统！)")
client.geometry("440x400")
# 信息窗
Infoframe = Frame(client, height=300, width=160, )
InfoText = Text(Infoframe, fg="white", bg="black")
InfoText.config(state=DISABLED)
InfoText.grid()
Infoframe.grid(row=0, column=0, columnspan=2, padx=30, pady=80)
Infoframe.grid_propagate(0)
# 设置端口
btn = Button(client, text="连接服务器", command=ConnSever)
btn.place(x=160, y=40)
port = Label(client, text="端口号：")
port.place(x=30, y=20)
ip = Label(client, text="ip：")
ip.place(x=30, y=50)
portinput = Entry(client, width=4)
portinput.place(x=88, y=20)
ipinput = Entry(client, width=8)
ipinput.place(x=60, y=50)
# 本机信息
myip = Label(client, text="本机IP： " + get_host_ip())
mycpuid = Label(client, text="本机CPU ID： " + str(id))
myip.place(x=220, y=80)
mycpuid.place(x=220, y=100)
# 投票
v = IntVar()
v.set(1)
myname = Label(client, text="姓名：")
mynametext = Entry(client, width=8)
myname.place(x=220, y=130)
mynametext.place(x=260, y=130)
myvote = Label(client, text="投票给：")
myvote.place(x=220, y=160)
votebtn = Button(client, text=" 投 票 ", command=Getmsgout)
votebtn.place(x=220, y=240)
c1 = Radiobutton(client, text="选项1", variable=v, value=1)
c2 = Radiobutton(client, text="选项2", variable=v, value=2)
c3 = Radiobutton(client, text="选项3", variable=v, value=3)
c4 = Radiobutton(client, text="选项4", variable=v, value=4)
c5 = Radiobutton(client, text="选项5", variable=v, value=5)
c6 = Radiobutton(client, text="选项6", variable=v, value=6)
c1.place(x=220, y=180)
c2.place(x=280, y=180)
c3.place(x=340, y=180)
c4.place(x=220, y=210)
c5.place(x=280, y=210)
c6.place(x=340, y=210)
# 菜单
Mymenu = Menu(client)
Mymenu.add_command(label=" 帮 助 ", command=MyHelp)
client["menu"] = Mymenu

client.mainloop()