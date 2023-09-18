import socket 
import threading
import pickle

HEADER = 4064
PORT = 8022
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = []
usernames = []
server.listen()

def broadcast_clients(message, username, conn):
    global clients
    for client in clients:
        client.send(username.encode(FORMAT))
        client.send(message.encode(FORMAT))


def handle_messages(client):
    global clients
    while True:
        try:
            #Get the user
            user_length = client.recv(HEADER).decode(FORMAT)
            user_length = int(user_length)
            user = client.recv(user_length).decode(FORMAT)

            #Get the message
            msg_length = client.recv(HEADER).decode(FORMAT)
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)

            #Send the user and message
            broadcast_clients(msg, user, client)
                

        except:
            broadcast_clients(f"Se desconecto Jesus \n", client)
            clients.remove(client)
            client.close()
            break 


def handle_client(conn, addr):
    global clients
    clients.append(conn)
    
    wel_message = "Jesus se unio al chat \n"
    broadcast_clients(wel_message, conn)
    conn.send("Conectado al server \n".encode(FORMAT))

    messages_thread = threading.Thread(target=messages_clients, args=(conn,))
    messages_thread.start()

def start():
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_thread = threading.Thread(target=handle_client, args=(conn, addr))
        handle_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] server is starting....")
start()