import socket 
import threading
import pickle

HEADER = 4064
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = []
usernames = []

def broadcast_clients(length, data, conn):
    global clients
    for client in clients:
        print(client)
        client.send(length)
        client.send(data)
        #client.send(username.encode(FORMAT))
        #client.send(message.encode(FORMAT))
        


def handle_messages(client):
    global clients
    while True:
        try:
            #Get the length
            data_length = client.recv(HEADER)
            data_two = data_length

            if data_length:
                #Get the message and username
                data_length = int(data_length)
                data_str = client.recv(data_length)
                if pickle.loads(data_str) == DISCONNECT_MESSAGE:
                    raise Exception("Client disconnect")
                
                send_data = pickle.dumps(data_str)
                broadcast_clients(data_two, send_data, client)


                #Eval method
                #data = eval(data_str)
                #print(data)
                #data_length = str(data_length).encode(FORMAT)
                
                #Send the username, message and length
                #broadcast_clients(data_length, data_str, client)
                
        except Exception as ex:
            print(ex, "messages")
            #broadcast_clients(f"Se desconecto Jesus \n", client)
            clients.remove(client)
            client.close()
            break 


def handle_client():
    while True:
        server.listen()
        print(f"[LISTENING] Server is listening on {SERVER}")

        global clients

        conn, addr = server.accept()
        clients.append(conn)
        
        wel_message = "Jesus se unio al chat \n"
        #broadcast_clients(wel_message, conn)
        #conn.send("Conectado al server \n".encode(FORMAT))

        messages_thread = threading.Thread(target=handle_messages, args=(conn,))
        messages_thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting....")
handle_client()