from tkinter import *
from socket import *
import _thread

clients = []  # List to store all connected clients

def sendmsg():
    global textbox, conn
    msg = textbox.get("0.0", END)
    update_chat(msg, 0)
    broadcast(msg.encode('ascii'), conn)
    textbox.delete("0.0", END)

def initialize_server():
    global conn
    s = socket(AF_INET, SOCK_STREAM)
    host = 'localhost'
    port = 3000
    s.bind((host, port))
    s.listen(5)  # Can handle up to 5 clients
    print('Server on, waiting for clients...')
    
    while True:
        conn, addr = s.accept()
        clients.append(conn)  # Add the new client to the list
        print('Client connected:', addr)
        _thread.start_new_thread(client_thread, (conn,))  # Start a new thread for each client

def broadcast(msg, sender_conn):
    """Send the message to all clients except the sender"""
    for client in clients:
        if client != sender_conn:
            try:
                client.send(msg)  # Send message to all other clients
            except:
                pass  # If an error occurs (e.g., client disconnected), ignore it

def update_chat(msg, state):
    global chatlog
    chatlog.config(state=NORMAL)
    if state == 0:
        chatlog.insert(END, 'you: ' + msg)
    else:
        chatlog.insert(END, 'other: ' + msg)
    chatlog.config(state=DISABLED)
    chatlog.yview(END)

def recivemsg(conn):
    while 1:
        try:
            data = conn.recv(1024)  # Receive message from client
            if data:
                msg = data.decode('ascii')
                update_chat(msg, 1)  # Display received message
        except:
            pass

def client_thread(conn):
    """Thread for each client to listen for incoming messages"""
    _thread.start_new_thread(recivemsg, (conn,))

def GUI():
    global chatlog, textbox
    gui = Tk()
    gui.title("Server Chat")
    gui.geometry("500x300")

    chatlog = Text(gui, bg='white', height=15, width=50)
    chatlog.config(state=DISABLED)

    sendbutton = Button(gui, bg='red', fg='grey', text='send', command=sendmsg)

    textbox = Text(gui, bg='white', height=3, width=30)

    chatlog.place(x=6, y=6, height=240, width=380)
    textbox.place(x=6, y=250, height=30, width=260)
    sendbutton.place(x=300, y=250, height=30, width=40)

    gui.mainloop()

if __name__ == '__main__':
    conn = None
    _thread.start_new_thread(initialize_server, ())  # Start server in a new thread
    GUI()
