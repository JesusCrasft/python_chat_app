import socket 
import threading

HEADER = 64
PORT = 8082
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
new_message = False
message = "No hay mensajes por ahora"


def  handle_client(conn, addr):
    global new_message
    global message

    clients = []
    clients.append(conn)

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            #Type of connection

            #Request Server
            if msg == 'request_server':
                print(msg)
                if new_message == True:
                    for conns in clients:
                        conns.send(message.encode(FORMAT)) 
           
            #Response Client
            if msg == 'response_client':
                print(f"[NEW RESPONSE CONNECTION] {addr} connected.") 
                new_message = True
                print(new_message)
                msg_length = conn.recv(HEADER).decode(FORMAT)
                if msg_length:
                    msg_length = int(msg_length)
                    msg = conn.recv(msg_length).decode(FORMAT)
                    message = msg   


def start():
    print(new_message)
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting....")
start()