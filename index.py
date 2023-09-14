from tkinter import ttk
from tkinter import * 

import threading
import socket

class App:

    def __init__(self, WindowT):
        #Window Attributes
        self.wind = WindowT
        self.wind.title('Chat')
        self.wind.geometry('900x700')
        self.wind.configure(bg='#1F1F1F')

        #Constants
        self.HEADER = 64
        self.PORT = 8082
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT"
        self.SERVER = "192.168.1.205"
        self.ADDR = (self.SERVER, self.PORT)

        #Variables
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.username = 'jesus'
        self.x = 0.80
        self.y = 0
        self.arrived_message = "False"
        self.recieve_length = 64
       

        """Labels"""
        #Username Label
        self.label_username = Label(self.wind, text='one')
        self.label_username.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_username.place(relwidth = 0.30, relheight = 0.09, relx = 0.0, rely = 0.0)

        #Contacts Label
        self.label_contacts = Label(self.wind, text='two')
        self.label_contacts.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_contacts.place(relwidth = 0.30, relheight = 0.91, relx = 0.0, rely = 0.09)

        #Chat Laprint("listo")bel
        self.label_chat = Label(self.wind)
        self.label_chat.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_chat.place(relwidth = 0.70, relheight = 0.90, relx = 0.30, rely = 0.0)

        #Widget Chat Label
        self.label_wchat = Label(self.wind)
        self.label_wchat.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_wchat.place(relwidth = 0.70, relheight = 0.10, relx = 0.30, rely = 0.90)


        """Entrys"""
        #Contacts Chat
        self.entry_contacts = Entry(self.label_contacts, font=('Arial', 15))
        self.entry_contacts.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        self.entry_contacts.place(relwidth = 0.9999, relheight = 0.05, relx = 0.0, rely = 0.0)

        #Chat Entry
        self.entry_chat = Entry(self.label_wchat, font=('Arial', 15))
        self.entry_chat.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        self.entry_chat.place(relwidth = 0.75, relheight = 0.65, relx = 0.02, rely = 0.08)


        """Buttons"""
        #Chat Button
        self.button_chat = Button(self.label_wchat, text='Enviar', command=self.place_message)
        self.button_chat.place(relwidth = 0.10, relheight = 0.65, relx = 0.78, rely = 0.08)

        #Image Button
        self.button_sendimg = Button(self.label_wchat, text='Imagen')
        self.button_sendimg.place(relwidth = 0.10, relheight = 0.65, relx = 0.89, rely = 0.08)


        """Chat"""
        #ListBox
        self.listbox_chat = Text(self.label_chat, font=('Arial', 15))
        self.listbox_chat.configure(exportselection=False, bg='white', fg='gray', highlightbackground='gray')
        self.listbox_chat.place(relwidth = 0.95, relheight = 0.999, relx = 0.0, rely = 0.0)

        #ScrollBar
        self.scrollbar_chat = Scrollbar(self.label_chat, command=self.listbox_chat.yview)
        self.listbox_chat.configure(yscrollcommand=self.scrollbar_chat.set)
        self.scrollbar_chat.configure(background='#444444', activebackground='gray')
        self.scrollbar_chat.place(relwidth = 0.05, relheight = 0.999, relx = 0.95, rely = 0)
        
        self.request_thread = threading.Thread(target=self.recieve_message)
        self.request_thread.start()

    #Function to place the message
    def place_message(self):
        #Get the message
        message = self.entry_chat.get()

        #Insert the message in the chat
        self.listbox_chat.insert(END, f'{self.username} : {message} \n')

        #Sending message
        message = message.encode(self.FORMAT)
        self.send_message(message)


    #Function to send the message and username
    def send_message(self, msg):
        #Type of connection
        self.client.send(self.length_message("response_client".encode(self.FORMAT))[0])
        self.client.send(self.length_message("response_client".encode(self.FORMAT))[1])

        #Extract the length and encode the message
        send_length = self.length_message(msg)[0]
        message = self.length_message(msg)[1]
        self.recieve_length = int(send_length)

        #Sending the message and the length
        self.client.send(send_length)
        self.client.send(message)

        self.recieve_message()

    #Recieve message
    def recieve_message(self):  
        #Type of connection
        self.client.send(self.length_message("request_server".encode(self.FORMAT))[0])
        self.client.send(self.length_message("request_server".encode(self.FORMAT))[1])
        while True:
            try:
                msg = self.client.recv(int(self.recieve_length)).decode(self.FORMAT)
                #self.listbox_chat.insert(END, "prueba")
                print(msg)
                break
                
            except Exception as ex:
                print("An error ocurred")
                self.client.close()
                print(ex)
                break
                   
    
    #Function to extract the length
    def length_message(self, msg):
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        return [send_length, msg]

if __name__ == '__main__':
    WindowT = Tk()
    application = App(WindowT)
    WindowT.mainloop()