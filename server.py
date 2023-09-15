import socket 
import threading

HEADER = 4064
PORT = 8009
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = []
server.listen()

def broadcast_clients(message, conn):
    global clients
    for client in clients:
        client.send(message.encode(FORMAT))


def messages_clients(client):
     global clients

     while True:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            msg_length = int(msg_length)
            msg = client.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                broadcast_clients(f"Se desconecto Jesus \n", client)
                clients.remove(client)
                client.close()
            else:
                broadcast_clients(msg, client)

        except:
            break 

def handle_clients(conn, addr):
    global clients

    while True:
        clients.append(conn)
        wel_message = "Jesus se unio al chat \n"
        broadcast_clients(wel_message, conn)
        conn.send("Conectado al server \n".encode(FORMAT))

        messages_thread = threading.Thread(target=messages_clients, args=(conn,))
        messages_thread.start()

        


def start():
    print(f"[LISTENING] Server is listening on {SERVER}")
    conn, addr = server.accept()
    handle_thread = threading.Thread(target=handle_clients, args=(conn, addr))
    handle_thread.start()
    print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
    
print("[STARTING] server is starting....")
start()