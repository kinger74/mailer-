from tkinter import *
from socket import *
import _thread

def login():
    global menu 
    username = textbox.get("0.0", END)
    password = textbox.get("0.100", END)
    register = Button("0.200", END)
    

def sendmsg():
    global textbox
    msg = textbox.get("0.0", END)
    update_chat(msg, 0)
    s.send(msg.encode('ascii'))
    textbox.delete("0.0", END)

def initialize_client():
    global s
    s = socket(AF_INET, SOCK_STREAM)
    host = 'localhost'
    port = 3000
    s.connect((host, port))
    print('Connected to server')

def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)
    if state == 0:
        chatlog.insert(END, 'you: ' + msg)
    else:
        chatlog.insert(END, 'other: ' + msg)
    chatlog.config(state=DISABLED)
    chatlog.yview(END)

def recivemsg():
    while 1:
        try:
            data = s.recv(1024)  # Receive message from server
            msg = data.decode('ascii')
            if msg != "":
                update_chat(msg, 1)  # Display received message
        except:
            pass

def GUI():
    global chatlog, textbox
    gui = Tk()
    gui.title("Client Chat")
    gui.geometry("500x300")

    chatlog = Text(gui, bg='white', height=15, width=50)
    chatlog.config(state=DISABLED)

    sendbutton = Button(gui, bg='red', fg='grey', text='send', command=sendmsg)

    textbox = Text(gui, bg='white', height=3, width=30)

    chatlog.place(x=6, y=6, height=240, width=380)
    textbox.place(x=6, y=250, height=30, width=260)
    sendbutton.place(x=300, y=250, height=30, width=40)

    _thread.start_new_thread(recivemsg, ())  # Start receiving messages from server

    gui.mainloop()

if __name__ == '__main__':
    initialize_client()
    GUI()
