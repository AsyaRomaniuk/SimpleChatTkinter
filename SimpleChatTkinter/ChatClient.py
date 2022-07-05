import socket
import threading
from tkinter import *
from tkinter.messagebox import showinfo


def receive(sock):
    while True:
        try:
            message = sock.recv(1024).decode('utf-8')
            if message == 'NICK':
                sock.send(nickname.encode('utf-8'))
            else:
                print(message)
                if text1.__ne__(None):
                    text1.configure(state="normal")
                    ci = text1.index("insert")
                    text1.insert("end", message)
                    text1.yview("end")
                    text1.configure(state="disabled")
                    if ":" in message:
                        text1.configure(state="normal")
                        text1.tag_add("color", ci, "{}.{}".format(ci[:ci.find(".")],
                                                                  message.find(":")))
                        text1.configure(state="disabled")
        except:
            print("Error has ocured!")
            sock.close()
            break


def connect():
    global nickname
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1", 50284))
        nickname = edit1.get()
        win.destroy()
        thread = threading.Thread(target=receive, args=(client,))
        thread.start()
        chat_init(client)
    except ConnectionRefusedError:
        showinfo("Error", "Unable to connect to server")


def send(client, txt2):
    message = '{}: {}'.format(nickname, txt2.get("1.0", "end"))
    client.send(message.encode('utf-8'))
    txt2.delete("1.0", "end")


def chat_init(client):
    global text1
    chat = Tk()
    chat.title("Чат")
    chat.resizable(0, 0)
    chat.config(bg="#16171b")
    chat.protocol("WM_DELETE_WINDOW", lambda: (client.close(), chat.destroy()))
    chat.geometry("438x630")
    fr1 = Frame(chat)
    text1 = Text(fr1, height=28, state="disabled", width=45, bg="#202125", fg="#feffff",
                 highlightthickness=2, highlightbackground="#323337", selectbackground="#4b4c50",
                 insertbackground="#00b175", font=("", 12))
    text1.tag_config("color", foreground="red")
    text1.pack(side="left")
    sb1 = Scrollbar(fr1, orient="vertical", command=text1.yview)
    sb1.pack(side="right", fill="y")
    text1.config(yscrollcommand=sb1.set)
    fr1.pack(padx=4, pady=4)
    fr2 = Frame(chat, bg="#16171b")
    text2 = Text(fr2, height=4, width=20, bg="#202125", fg="#feffff",
                 highlightcolor="#01b075", highlightbackground="#323337",
                 highlightthickness=4, selectbackground="#4b4c50",
                 insertbackground="#00b175", font=("", 12), undo=True)
    text2.focus()
    text2.pack(side="left", fill="x", padx=8, pady=8)
    sb2 = Scrollbar(fr2, orient="vertical", command=text2.yview)
    sb2.pack(side="right", fill="y")
    text2.config(yscrollcommand=sb2.set)
    sendbtn = Button(fr2, text=">", command=lambda: send(client, text2),
                     font=("", 10, "bold"), bg="#00b175", fg="#feffff")
    sendbtn.pack(side="right", padx=4, pady=4, fill="y")
    fr2.pack(anchor="e", padx=4, pady=4)
    chat.mainloop()


if __name__ == "__main__":
    text1 = None
    nickname = "Nickname1"
    win = Tk()
    win.title("PyChat")
    win.geometry("400x300")
    win.config(bg="#16171b")
    win.resizable(0, 0)
    lab1 = Label(win, text="Enter your name!", font=("Times", 20), width=16, bg="#16171b", fg="#feffff")
    edit1 = Entry(win, font=("Times", 20), width=17, justify="center", bg="#00b175", fg="#feffff",
                  selectbackground="#4b4c50")
    edit1.insert(0, nickname)
    btn1 = Button(win, text="Join", font=("Times", 20), width=16,
                  command=connect, bg="#00b175", fg="#feffff")
    btn2 = Button(win, text="Exit", font=("Times", 20), width=16,
                  command=lambda: win.destroy(), bg="#00b175", fg="#feffff")
    lab1.place(relx=0.2, rely=0.05)
    edit1.place(relx=0.21, rely=0.2)
    btn1.place(relx=0.2, rely=0.4)
    btn2.place(relx=0.2, rely=0.6)
    win.mainloop()
