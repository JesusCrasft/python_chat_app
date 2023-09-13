import socket

my_socket = socket.socket()

my_socket.bind(('localhost', 8000))

my_socket.listen(5)

while True:
    connection, adrr = my_socket.accept()
    
    request = connection.recv(2)
    print(request)
    connection.close()
    
