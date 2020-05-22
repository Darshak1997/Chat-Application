

import tkinter
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import datetime
now= datetime.datetime.now()


# https://github.com/KetanSingh11/SimpleChatApp/blob/master/multiChatClient.py
# Function to receive all the communication from server socket
def receive():
    """ Handles receiving of messages. """
    while True:
        try:
            msg = sock.recv(1024).decode("utf8")
            print("MSG: ", msg)
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break

# https://github.com/KetanSingh11/SimpleChatApp/blob/master/multiChatClient.py
# Send all the communication and data to the client socket
def send(event=None):
    """ Handles sending of messages. """
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    sock.send(bytes(msg, "utf8"))
    print("Name: ", msg)
    if msg == "#quit":
        sock.close()
        top.quit()

# https://github.com/KetanSingh11/SimpleChatApp/blob/master/multiChatClient.py
# If you wanna close the connection 
def on_closing(event=None):
    """ This function is to be called when the window is closed. """
    my_msg.set("#quit")
    send()

# If client exists, then close the socket
def clientExist():
    print("name taken")
    l1 = tkinter.Label(messages_frame, text = "Client name taken")
    l1.pack()
    sock.close()
    
# If want to send to a specific client
def one_to_one(event = None):
    rec = my_rec.get()
    my_rec.set("")
    sock.send(bytes(rec, "utf8"))
    print("Rec: ", rec)
    
def One_One(event = None):
    client_label = tkinter.Label(top, text="Enter your usename:")
    client_label.pack()
    client_field = tkinter.Entry(top, textvariable=my_username, foreground="Red")
    client_field.bind("<Return>", send)
    client_field.pack()
    client_button = tkinter.Button(top, text="Send", command=send)
    client_button.pack()
    Receipt_label = tkinter.Label(top, text="Enter Receiptent:")
    Receipt_label.pack()
    Receipt_field = tkinter.Entry(top, textvariable=my_rec, foreground="Red")
    Receipt_field.bind("<Return>", send)
    Receipt_field.pack()
    Receipt_button = tkinter.Button(top, text="Send", command=send)
    Receipt_button.pack()
    button_label = tkinter.Label(top, text="Enter Message:")
    button_label.pack()
    entry_field = tkinter.Entry(top, textvariable=my_msg, foreground="Red")
    entry_field.bind("<Return>", send)
    entry_field.pack()
    send_button = tkinter.Button(top, text="Send", command=send)
    send_button.pack()
    
    
# https://github.com/KetanSingh11/SimpleChatApp/blob/master/multiChatClient.py
# Initializing GUI
top = tkinter.Tk()
top.title("Simple Chat Client v1.0")
messages_frame = tkinter.Frame(top)

my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("")
my_rec = tkinter.StringVar() # To enter Receiptent
my_rec.set("")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=70, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

messages_frame.pack()

button_label = tkinter.Label(top, text="Enter Message:")
button_label.pack()
entry_field = tkinter.Entry(top, textvariable=my_msg, foreground="Red")
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()



one_to_one_button = tkinter.Button(top, text="add Rec", command=one_to_one)
one_to_one_button.pack()

entry_field = tkinter.Entry(top, textvariable=my_rec, foreground="Red")
entry_field.bind("<Return>", one_to_one)
entry_field.pack()

quit_button = tkinter.Button(top, text="Quit", command=on_closing)
quit_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
# Creating a socket connection
HOST = "127.0.0.1"
PORT = 5000
BUFSIZ = 1024
ADDR = (HOST, PORT)
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(ADDR)



# Start receiving messages sent from the socket user
receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.








