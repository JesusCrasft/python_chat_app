import socket 
import threading

HEADER = 64
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
new_message = False
message = "No hay mensajes por ahora"
clients = []

def broadcast_clients(message, clients):
    for client in clients:
        client.send(message.encode(FORMAT))


def messages_clients(client):
     while True:
          try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
               
     

def  handle_clients(conn, addr):
    global new_message
    global message
    global clients

    while True:
            clients.append(conn)

            wel_message = f"Jesus se unio al chat"
            broadcast_clients(wel_message, clients)
            conn.send("Conectado al server".encode(FORMAT))


            messages_thread = threading.Thread(target=messages_clients, args=(addr))
            messages_thread.start()

            """#Request Server
            if msg == 'request_server':
                if new_message == True:
                    for client in clients:
                        client.send(message.encode(FORMAT)) 
           
            #Response Client
            if msg == 'response_client':
                print(f"[NEW RESPONSE CONNECTION] {addr} connected.") 
                new_message = True
                print(new_message)
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    message = msg """  


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        handle_thread = threading.Thread(target=handle_clients, args=(conn, addr))
        handle_thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting....")
start()