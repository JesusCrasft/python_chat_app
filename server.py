import socket

my_socket = socket.socket()

my_socket.bind(('localhost', 8001))

my_socket.listen(5)

while True:
    connection, adrr = my_socket.accept()
    
    connection.close()
    
