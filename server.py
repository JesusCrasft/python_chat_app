import socket 
import threading
import pickle
import time

HEADER = 4064
PORT = 8011
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = {}
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

#Function to handle messages to a group
def handle_megroup():
    global clients

    pass

#Function to handle the direct msg
def handle_dms():
    global clients
     
    pass


#Function to send the users online to the clients        
def users_online():
    global clients
    print(list(clients.keys()), "Users online")

    for client in clients.values():
        client.send(pickle.dumps("online_users"))
        time.sleep(2)
        client.send(pickle.dumps(list(clients.keys())))


#Function to handle the disconnection from a client
def handle_disc(conn, addr, username):
    global clients

    #Remove the user and client from the lists
    clients.pop(pickle.loads(username))  
    conn.close()
    users_online() 

#Function to know what type of connection the users wants
def type_connect(conn, addr):
    global clients
    while True:
        try:
            type_conn = conn.recv(HEADER)

            #Type connection
            if type_conn != b'':
                type_conn = pickle.loads(type_conn)

                #Disconnect client
                if type_conn == "disconnect":
                    username = conn.recv(HEADER) 
                    if username != b'':       
                        handle_disc(conn, addr, username)

        #Bad file descriptor catch
        except socket.error:
            pass

        except Exception as ex:
            print(ex)
            break
                
                                  
#Main function to handle the clients
def handle_client():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    global clients
    while True:
        conn, addr = server.accept()

        #Recieve the username and append with the client in lists
        username = conn.recv(HEADER)
        clients.update({pickle.loads(username): conn})

        #messages_thread = threading.Thread(target=handle_messages, args=(conn,))
        #messages_thread.start()

        #Type of connection thread
        typeco_thread = threading.Thread(target=type_connect, args=(conn, addr))
        typeco_thread.start()

        #Users on thread
        userson_thread = threading.Thread(target=users_online, args=())
        userson_thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")

print("[STARTING] server is starting....")
handle_client()