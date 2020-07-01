

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter 
from _thread import *
clients = {}
addresses = {}


# https://www.geeksforgeeks.org/socket-programming-multi-threading-python/
HOST = "127.0.0.1"
PORT = 5000
ADDR = (HOST, PORT)
SOCK = socket(AF_INET, SOCK_STREAM)
SOCK.bind(ADDR)

names_list = []


# https://github.com/KetanSingh11/SimpleChatApp/blob/master/multiChatClient.py
# This function welcomes the incoming connections by storing their addresses and sending them to handle all the clients
def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SOCK.accept()
        print("%s:%s has connected." % client_address)  # Connection Established
        client.send("Greetings from the ChatRoom! ".encode("utf8"))
        client.send("Now type your name and press enter!".encode("utf8")) # Input the username
        addresses[client] = client_address
        
        Thread(target=handle_client, args=(client, client_address)).start()


# https://github.com/KetanSingh11/SimpleChatApp/blob/master/multiChatClient.py
# Takes client socket as argument.
def handle_client(conn, addr):  
    """Handles a single client connection."""
    global names_list
    global name
    name = conn.recv(1024).decode("utf8")  # Receives the username entered by the user
    print("Name: ", name)
    # If name already in use, then stop
    if name in names_list:
        conn.send(str.encode("Undone"))
    # else start sending messages
    else:
        names_list.append(name)
        conn.send(str.encode("Done"))
        print(names_list)
        welcome = 'Welcome %s! If you ever want to quit, type #quit to exit.' % name
        conn.send(bytes(welcome, "utf8"))
        msg = "%s from [%s] has joined the chat!" % (name, "{}:{}".format(addr[0], addr[1]))
        
        clients[name] = conn
        
        # Add the receiptent yoy want to send
        rec = conn.recv(1024).decode("utf8")
        print("Reciptent: ", rec)
            
        # If receiptent is not empty
        if rec:
            print("Single sent")
            msg = conn.recv(1024)
            print("While MSG: ", msg)
            print("RECCC: ", rec + ":")
            if rec in names_list:
#                conn.send(bytes(rec + ":", "utf8") + msg)
                single_client(msg, rec)
        
     
        
# If receiptent is added, then send messages to specific client
def single_client(msg, prefix = ""):
    
    print("Clients in Single: ", clients)
    
    clients[prefix].send(bytes(name + ":", "utf8") + msg)
        
    
#Displaying the Status of the Clients on the GUI
def disp(name):
    top = tkinter.Tk()
    messages_frame = tkinter.Frame(top)
    msg_list = tkinter.Listbox(messages_frame, height=15, width=70)
    msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
    msg_list.pack()
    messages_frame.pack()
    
    msg = name
    msg_list.insert(tkinter.END, msg)
    
    
    
        
        

if __name__ == "__main__":
    null = ""
    SOCK.listen(7)  # Listens for 7 connections at max.
    print("Chat Server has Started !!")
    print("Waiting for connections...")
    name = ""
    # start Accepting connections
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
#    global name
#    start_new_thread(disp,(name,))
    ACCEPT_THREAD.start()  # Starts the infinite loop.
    ACCEPT_THREAD.join()
    SOCK.close()

