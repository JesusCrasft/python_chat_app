import socket 
import threading
import pickle
import time

HEADER = 4064
PORT = 8005
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = {}
groups = {}


#Function to handle messages to a group
def handle_megroup(sender, group_name, message):
    global clients
    global groups
    
    #Get the integrants
    integrants = groups.get(group_name)

    #Message
    message = f"{sender}: {message}"

    #Encode the data
    type_data = ["group_message", group_name, message]
    type_data = pickle.dumps(type_data)

    #Send the information to the integrants
    for i in integrants:
        if i != sender:
            reciever = clients.get(i)
            reciever.send(type_data)


#Function to handle the direct msg
def handle_dms(sender, reciever, message):
    global clients
    global groups

    #Get the reciever conn
    reciever = clients.get(reciever)
    
    #Message
    message = f"{sender}: {message}"

    #Encode the data
    type_data = ["dm_message", sender, message]
    type_data = pickle.dumps(type_data)
    
    #Send the type and data
    reciever.send(type_data)


#Function to handle send files
def handle_images(conn, sender, receiver):
    global clients
    global groups

    #Get the connection from the sender of the image
    receiver = clients.get(receiver)

    #Create an image with the data recv from the sender
    file = open('server_image.jpg', 'wb')
    file_data = conn.recv(4080)
    
    while file_data:
        file.write(file_data)
        file_data = conn.recv(4080)
    
    file.close()

    #Encode the data with pickle to send
    type_data = ["send_image", sender]
    type_data = pickle.dumps(type_data)
    
    #Send the type and data
    receiver.send(type_data)

    #Send the image data to the receiver
    #Open the file and read 
    file = open("server_image.png.jpg", 'rb')
    file_data = file.read(4080)

    while file_data:
        receiver.send(file_data)
        file_data = file.read(4080)

    file.close()


#Function to create groups
def create_gruop(name, integrants):
    global clients
    global groups

    #Add the group to the groups list
    groups.update({name: integrants})

    #Encode the information with pickle
    type_data = ["create_group", name, integrants]
    type_data = pickle.dumps(type_data)

    #Send the information to the integrants
    for i in integrants:
        reciever = clients.get(i)
        reciever.send(type_data)


#Function to check if the username is available
def check_user(conn, addr, username):
    global clients
    global groups

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
        typeco_thread = threading.Thread(target=manage_recv, args=(conn, addr))
        typeco_thread.start()


#Function to send the users online to the clients        
def users_online(req=None, reciever=None):
    global clients
    global groups
    print(list(clients.keys()), "users online")
    

    #Validation
    if req == True:
        #Send the users online to a single user
        reciever = clients.get(reciever)
        type_data = ["online_users", list(clients.keys())]
        type_data = pickle.dumps(type_data)
        reciever.send(type_data)

    else:
        #Send the users online to all the users
        for client in clients.values():
            #Send the type of conn
            type_data = ["online_users", list(clients.keys())]
            type_data = pickle.dumps(type_data)
            client.send(type_data)


#Function to handle the disconnection from a client
def handle_disc(conn, addr, username=None, useroff=None):
    global clients
    global groups

    #Remove the user and client from the lists
    conn.close()
    if useroff != None:
        clients.pop(pickle.loads(username))  
        users_online() 


#Function to know what type of connection the users wants
def manage_recv(conn=None, addr=None):
    while True:
        global clients
        global groups

        try:
            type_data = conn.recv(HEADER)
            
            #Type connection
            if type_data != b'':
                type_data = pickle.loads(type_data)
                
                #Recieve message
                if type_data[0] == "dm_message":
                    sender = type_data[1]
                    reciever = type_data[2]
                    message = type_data[3]
                    handle_dms(sender, reciever, message)

                #Recieve group message
                if type_data[0] == "group_message":
                    sender = type_data[1]
                    group_name = type_data[2]
                    message = type_data[3]
                    handle_megroup(sender, group_name, message)

                #Recieve image
                if type_data[0] == "send_image":
                    handle_images(conn, type_data[1], type_data[2])

                #Create group
                if type_data[0] == "create_group":
                    create_gruop(type_data[1], type_data[2])

                ##Disconnect client
                if type_data[0] == "disconnect_user":       
                    handle_disc(conn, addr, pickle.dumps(type_data[1]), useroff=True)
                    break

                if type_data[0] == "disconnect_nouser":
                    handle_disc(conn, addr, useroff=None)
                    break
                
                #Request Online Users
                if type_data[0] == "req_online_users":
                    users_online(req=True, reciever=type_data[1])

        except Exception as ex: 
            print(ex)
            break
                
                                  
#Main function to handle the clients
def handle_client():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        global clients
        global groups

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