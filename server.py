import socket 
import threading

HEADER = 4064
PORT = 8902
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
            broadcast_clients(msg, client)

        except:
            broadcast_clients(f"Se desconecto Jesus \n", client)
            clients.remove(client)
            client.close()
            break
            

def start():
    global clients
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
       
        clients.append(conn)

        wel_message = "Jesus se unio al chat \n"
        broadcast_clients(wel_message, conn)
        conn.send("Conectado al server \n".encode(FORMAT))


        messages_thread = threading.Thread(target=messages_clients, args=(conn,))
        messages_thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting....")
start()