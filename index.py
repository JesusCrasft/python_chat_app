from tkinter import ttk
from tkinter import * 

import time
import threading
import socket

class App:

    def __init__(self, WindowT):
        #Window Attributes
        self.wind = WindowT
        self.wind.title('Select Username')
        self.wind.geometry('400x200')
        #self.wind.geometry('900x700')
        self.wind.configure(bg='#1F1F1F')

        #Constants
        self.HEADER = 4064
        self.PORT = 8022
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = "!DISCONNECT".encode(self.FORMAT)
        self.SERVER = "192.168.1.205"
        self.ADDR = (self.SERVER, self.PORT)

        #Variables
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        self.username = ''
        self.x = 0.80
        self.y = 0
        self.arrived_message = "False"
        self.recieve_length = 4064
       

        """Labels"""
        #Username Label
        self.label_username = Label(self.wind, text='one')
        self.label_username.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        #self.label_username.place(relwidth = 0.30, relheight = 0.09, relx = 0.0, rely = 0.0)
        
        #Contacts Label
        self.label_contacts = Label(self.wind, text='two')
        self.label_contacts.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        #self.label_contacts.place(relwidth = 0.30, relheight = 0.91, relx = 0.0, rely = 0.09)
        
        #Chat Label
        self.label_chat = Label(self.wind)
        self.label_chat.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        #self.label_chat.place(relwidth = 0.70, relheight = 0.90, relx = 0.30, rely = 0.0)
        
        #Widget Chat Label
        self.label_wchat = Label(self.wind)
        self.label_wchat.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        #self.label_wchat.place(relwidth = 0.70, relheight = 0.10, relx = 0.30, rely = 0.90)
        
        #Select Username Label
        self.label_user = Label(self.wind)
        self.label_user.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_user.place(relwidth = 0.9999, relheight = 0.9999, relx = 0.0, rely = 0.0)

        """Entrys"""
        #Contacts Chat
        self.entry_contacts = Entry(self.label_contacts, font=('Arial', 15))
        self.entry_contacts.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        #self.entry_contacts.place(relwidth = 0.9999, relheight = 0.05, relx = 0.0, rely = 0.0)
        
        #Chat Entry
        self.entry_chat = Entry(self.label_wchat, font=('Arial', 15))
        self.entry_chat.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        #self.entry_chat.place(relwidth = 0.75, relheight = 0.65, relx = 0.02, rely = 0.08)
        
        #Select Username Entry
        self.entry_user = Entry(self.label_user, font=('Arial', 15))
        self.entry_user.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        self.entry_user.place(relwidth = 0.70, relheight = 0.18, relx = 0.16, rely = 0.25)
        self.entry_user.insert(END, "       Enter Username")


        """Buttons"""
        #Chat Button
        self.button_chat = Button(self.label_wchat, text='Enviar', command=self.send_message)
        #self.button_chat.place(relwidth = 0.10, relheight = 0.65, relx = 0.78, rely = 0.08)
        
        #Image Button
        self.button_sendimg = Button(self.label_wchat, text='Imagen')
        #self.button_sendimg.place(relwidth = 0.10, relheight = 0.65, relx = 0.89, rely = 0.08)
        
        #Accept User Button
        self.button_user = Button(self.label_user, text='Aceptar', command=self.select_username)
        self.button_user.place(relwidth = 0.25, relheight = 0.18, relx = 0.39, rely = 0.55)


        """Chat"""
        #Textbox
        self.textbox_chat = Text(self.label_chat, font=('Arial', 15))
        self.textbox_chat.configure(exportselection=False, bg='white', fg='gray', highlightbackground='gray')
        #self.textbox_chat.place(relwidth = 0.95, relheight = 0.999, relx = 0.0, rely = 0.0)
        
        #ScrollBar
        self.scrollbar_chat = Scrollbar(self.label_chat, command=self.textbox_chat.yview)
        self.textbox_chat.configure(yscrollcommand=self.scrollbar_chat.set)
        self.scrollbar_chat.configure(background='#444444', activebackground='gray')
        #self.scrollbar_chat.place(relwidth = 0.05, relheight = 0.999, relx = 0.95, rely = 0)
        
        #Threads
        self.request_thread = threading.Thread(target=self.recieve_message, args=(True,))
        self.request_stop = threading.Event()
        #self.response_thread = threading.Thread(target=self.send_message)
        self.request_thread.start()
        self.Eventks()

    def Eventks(self):
        self.wind.protocol("WM_DELETE_WINDOW", self.closing_window)

    #Function to manage the closing window
    def closing_window(self): 
        self.request_stop.set()
        self.wind.destroy()
        self.client.close()

    #Function to select username 
    def select_username(self):
        self.chat_stage()

        """#Get the username
        self.username = self.entry_user.get().encode(self.FORMAT)

        #Type connection
        send_length = self.length_message("username")#Username
        self.client.send(send_length)
        self.client.send("username".encode(self.FORMAT))#Username
        self.recieve_length = send_length

        #Extract the length and encode the message
        send_length = self.length_message(self.username)
        self.recieve_length = send_length"""

        

    def chat_stage(self):
        self.entry_chat.place_forget()
        self.button_user.place_forget()
        self.label_user.place_forget()

        self.wind.geometry("900x700")
        self.wind.title("Chat")

        self.label_username.place(relwidth = 0.30, relheight = 0.09, relx = 0.0, rely = 0.0)
        self.label_contacts.place(relwidth = 0.30, relheight = 0.91, relx = 0.0, rely = 0.09)
        self.label_chat.place(relwidth = 0.70, relheight = 0.90, relx = 0.30, rely = 0.0)
        self.label_wchat.place(relwidth = 0.70, relheight = 0.10, relx = 0.30, rely = 0.90)
        self.entry_contacts.place(relwidth = 0.9999, relheight = 0.05, relx = 0.0, rely = 0.0)
        self.entry_chat.place(relwidth = 0.75, relheight = 0.65, relx = 0.02, rely = 0.08)
        self.button_chat.place(relwidth = 0.10, relheight = 0.65, relx = 0.78, rely = 0.08)
        self.button_sendimg.place(relwidth = 0.10, relheight = 0.65, relx = 0.89, rely = 0.08)
        self.textbox_chat.place(relwidth = 0.95, relheight = 0.999, relx = 0.0, rely = 0.0)
        self.scrollbar_chat.place(relwidth = 0.05, relheight = 0.999, relx = 0.95, rely = 0)
        

    #Function to send the message and username
    def send_message(self):
        #Get the username
        self.username = self.entry_user.get().encode(self.FORMAT)

        #Sending the message and the length
        self.client.send(send_length)
        self.client.send(self.username)

        #Get the message
        message = self.entry_chat.get()
        message = message.encode(self.FORMAT)

        #Extract the length and encode the message
        send_length = self.length_message(message)
        self.recieve_length = send_length

        #Sending the message and the length
        self.client.send(send_length)
        self.client.send(message)

    #Recieve message
    def recieve_message(self, connected):  
        while connected:
            try:
                if self.request_stop.is_set():
                    break
                else:
                    self.client.settimeout(1)
                    self.recieve_length = int(self.recieve_length)
                    msg = self.client.recv(self.recieve_length * 90).decode(self.FORMAT)
                    self.textbox_chat.insert(END, f"{self.username} : {msg} \n")
                    
            except Exception as ex:
                continue
       

    #Function to extract the length
    def length_message(self, msg):
        msg_length = len(msg)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        return send_length

if __name__ == '__main__':
    WindowT = Tk()
    application = App(WindowT)
    WindowT.mainloop()