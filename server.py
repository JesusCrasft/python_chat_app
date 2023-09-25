import socket 
import threading
import pickle
import time

HEADER = 4064
PORT = 8084
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = []
usernames = []
data = ''
data_str = ''
data_length = ''

#Function to extract the length
def length_convert(length):
    length = pickle.loads(length)
    length = str(length)
    length = int(length)
    return length

#Function to extract the length
def length_data(length):
    length = str(length)
    data_length = len(length)
    send_length = str(data_length)
    send_length = pickle.dumps(send_length)
    send_length += b' ' * (HEADER - len(send_length))
    return send_length
    
def broadcast_clients(length=None, data=None, conn=None):
    global clients
    for client in clients:
        client.send(length)
        client.send(data)

def handle_messages(client):
    global clients
    global data
    global data_str
    global data_length

    while True:
            pass
    

def handle_disc(conn, addr, username):
    global clients
    global usernames
    
    print(usernames)
    print(pickle.loads(username))
    usernames.remove(pickle.loads(username))
    print(usernames)
    conn.close()
    clients.remove(conn)
            
def users_online():
    global clients
    global usernames
    while True:
        for client in clients:
            client.send(pickle.dumps("online_users"))
            for user in usernames:
                time.sleep(1)
                client.send(pickle.dumps(user))
                print(user)


def type_connect(conn, addr):
    global usernames
    while True:
        type_conn = conn.recv(HEADER)
        if type_conn != b'':
            type_conn = pickle.loads(type_conn)
            
            if type_conn == "username":
                username = conn.recv(HEADER)
                usernames.append(pickle.loads(username))
                continue

            if type_conn == "disconnect":
                username = conn.recv(HEADER)
                handle_disc(conn, addr, username)
                continue
                                  

def handle_client():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    global clients
    while True:
        conn, addr = server.accept()

        clients.append(conn)

        #messages_thread = threading.Thread(target=handle_messages, args=(conn,))
        #messages_thread.start()

        typeco_thread = threading.Thread(target=type_connect, args=(conn, addr))
        typeco_thread.start()

        #userson_thread = threading.Thread(target=users_online)
        #userson_thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

print("[STARTING] server is starting....")
handle_client()