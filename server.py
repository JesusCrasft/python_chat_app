import socket 
import threading

HEADER = 1024
PORT = 8080
SERVER = socket.gethostbyname(socket.gethostname)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


