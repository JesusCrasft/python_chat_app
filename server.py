import socket 
import threading
import pickle
import time

HEADER = 4064
PORT = 8005
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
def handle_dms(sender, reciever, message):
    global clients

    #Get the reciever conn
    reciever = clients.get(reciever)
    
    #Message
    message = f"{sender}: {message}"

    #Encode the data
    type_data = ["dm_message", sender, message]
    type_data = pickle.dumps(type_data)
    
    #Send the type and data
    reciever.send(type_data)


#Function to check if the username is available
def check_user(conn, addr, username):
    global clients

    if pickle.loads(username) in list(clients.keys()):
        conn.send(pickle.dumps("invalid_user"))
        check = conn.recv(HEADER)
        if check != b'':
            check = pickle.loads(check)
            if check == 'disconnect':
                handle_disc(conn, addr, useroff=False)
            else:
                check_user(conn, addr, username)

    else:
        conn.send(pickle.dumps("valid_user"))
        clients.update({pickle.loads(username): conn})
            
        #Users on thread
        userson_thread = threading.Thread(target=users_online, args=())
        userson_thread.start()

        #Type of connection thread
        typeco_thread = threading.Thread(target=type_connect, args=(conn, addr))
        typeco_thread.start()


#Function to send the users online to the clients        
def users_online():
    global clients
    print(list(clients.keys()), "users online")
    
    #Send the users online
    for client in clients.values():
        #Send the type of conn
        type_data = ["online_users", list(clients.keys())]
        type_data = pickle.dumps(type_data)
        client.send(type_data)


#Function to handle the disconnection from a client
def handle_disc(conn, addr, username=None, useroff=None):
    global clients

    #Remove the user and client from the lists
    conn.close()
    if useroff != None:
        clients.pop(pickle.loads(username))  
        users_online() 


#Function to know what type of connection the users wants
def type_connect(conn=None, addr=None):
    while True:
        global clients
        try:
            type_data = conn.recv(HEADER)
            
            #Type connection
            if type_data != b'':
                type_data = pickle.loads(type_data)
                
                #Recieve message
                if type_data[0] == 'dm_message':
                    sender = type_data[1]
                    reciever = type_data[2]
                    message = type_data[3]
                    handle_dms(sender, reciever, message)

                ##Disconnect client
                if type_data[0] == "disconnect_user":       
                    handle_disc(conn, addr, pickle.dumps(type_data[1]), useroff=True)
                    break

                if type_data[0] == "disconnect_nouser":
                    handle_disc(conn, addr, useroff=None)
                    break

        except Exception as ex: 
            print(ex)
            break
                
                                  
#Main function to handle the clients
def handle_client():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        global clients

        conn, addr = server.accept()
        
        #Recieve the username and append with the client in lists
        username = conn.recv(HEADER)
        check_thread = threading.Thread(target=check_user, args=(conn, addr, username))
        check_thread.start()

        #messages_thread = threading.Thread(target=handle_messages, args=(conn,))
        #messages_thread.start()

        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")
        
  

print("[STARTING] server is starting....")
handle_client()