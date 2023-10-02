from tkinter import ttk
from tkinter import * 

import json 
import threading
import socket
import pickle
import time
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
        self.PORT = 8016
        self.FORMAT = 'utf-8'
        self.DISCONNECT_MESSAGE = pickle.dumps("!DISCONNECT")
        self.SERVER = "192.168.1.205"
        self.ADDR = (self.SERVER, self.PORT)

        #Variables
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.x = 0.80
        self.y = 0
        self.arrived_message = "False"
        self.username_client = ''
        self.check_conn = [False, False]
       

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
        self.entry_user.insert(END, "CSDAW")


        """Buttons"""
        #Chat Button
        self.button_chat = Button(self.label_wchat, text='Enviar', command=self.send_dm)
        #self.button_chat.place(relwidth = 0.10, relheight = 0.65, relx = 0.78, rely = 0.08)
        
        #Image Button
        self.button_sendimg = Button(self.label_wchat, text='Imagen')
        #self.button_sendimg.place(relwidth = 0.10, relheight = 0.65, relx = 0.89, rely = 0.08)
        
        #Accept User Button
        self.button_user = Button(self.label_user, text='Aceptar', command=self.check_client)
        self.button_user.place(relwidth = 0.25, relheight = 0.18, relx = 0.39, rely = 0.55)


        """Chat"""
        #Textbox
        self.textbox_chat = Text(self.label_chat, font=('Arial', 15), state='disabled')
        self.textbox_chat.configure(exportselection=False, bg='white', fg='gray', highlightbackground='gray')
        
        #ScrollBar
        self.scrollbar_chat = Scrollbar(self.label_chat, command=self.textbox_chat.yview)
        self.textbox_chat.configure(yscrollcommand=self.scrollbar_chat.set)
        self.scrollbar_chat.configure(background='#444444', activebackground='gray')
        


        """ListBox"""
        self.listbox_userson = Listbox(self.label_contacts)
        self.listbox_userson.configure(bg='#1F1F1F', font=('Arial', 17), fg='white', highlightbackground='gray', borderwidth=1)
        

        self.responses_stop = threading.Event()  
        self.Eventks()
    
    #Function to catch the events from tkinter
    def Eventks(self):

        #Window close event
        self.wind.protocol("WM_DELETE_WINDOW", self.closing_window)

        #Listbox select
        self.listbox_userson.bind('<<ListboxSelect>>', self.select_chat)


    #Function to manage the closing window
    def closing_window(self):
        self.responses_stop.set()
        self.disconnect_client()
        

    #Function to select username 
    def check_client(self):
        #Check if client is already connected
        try:
            self.client.connect(self.ADDR)

        except socket.error:
            pass

        #Get the username
        self.username_client = self.entry_user.get()
        self.username_client = pickle.dumps(self.username_client)

        #Send the username
        self.client.send(self.username_client)
        
        #Update check conn
        self.check_conn[0] = True

        #Active responses thread
        self.responses_thread = threading.Thread(target=self.manage_recv)
        self.responses_thread.start()


    #Function to send the message and username
    def send_dm(self):
        #Get the username and message
        message = self.entry_chat.get()
        receiver = self.listbox_userson.get(self.listbox_userson.curselection())

        #Use pickle to encode the data
        data_list = [self.username_client, receiver, message]
        data = pickle.dumps(data_list)

        #Sending the message and the length
        self.client.send(pickle.dumps("dm_message"))
        self.client.send(data)

        
    #Recieve message
    def manage_recv(self):  
        while True:
            #Flag to stop the while
            if self.responses_stop.is_set():
                break

            try:   
                type_conn = self.client.recv(self.HEADER) 
        

                #Type connection
                if type_conn != b'':
                    type_conn = pickle.loads(type_conn)

                    #Users online
                    if type_conn == "online_users":
                        users = self.client.recv(self.HEADER)
                        if users != b'':
                            users = pickle.loads(users)
                            self.listbox_userson.delete(0, END)
                            for user in  users:
                                self.listbox_userson.insert(0, user)
                        

                    #Handle Messages
                    if type_conn == "dm_message":
                        data = self.client.recv(self.HEADER)
                        if data != b'':
                            data = pickle.loads(data)
                            sender = data[0]
                            message = data[1]
                            print(sender)
                            print(message)



                    #Check invalid user
                    if type_conn == "invalid_user":
                        label_message = Message(self.label_user, text="The user is already online")
                        label_message.place(relwidth = 0.70, relheight = 0.25, relx = 0.16, rely = 0.10)
                        self.check_conn[1] = False
                        break

                    #Check valid user
                    if type_conn == "valid_user":
                        self.chat_stage()
                        self.check_conn[1] = True
                    

            except Exception as ex:
                print(ex, "recieve responses")
                break
    

    #Function to disconnect from server
    def disconnect_client(self):   
        if self.check_conn[0] == False:
            self.wind.destroy()

        elif self.check_conn[0] == True and self.check_conn[1] == False:
            self.client.send(pickle.dumps("disconnect"))
            self.client.close()
            self.wind.destroy()

        elif self.check_conn[0] == True and self.check_conn[1] == True:
            self.client.send(pickle.dumps("disconnect"))
            self.client.send(self.username_client)
            self.client.close()
            self.wind.destroy()


    #Function to convert the length
    def length_convert(self, length):
        length = pickle.loads(length)
        length = str(length)
        length = int(length)
        return length
    

    #Function to extract the length
    def length_message(self, length):
        length = str(length)
        data_length = len(length)
        send_length = str(data_length)
        send_length = pickle.dumps(send_length)
        send_length += b' ' * (self.HEADER - len(send_length))
        return send_length

    

    #Function to select a chat
    def select_chat(self, key):
        #Mount the select chat
        self.label_wchat.place(relwidth = 0.70, relheight = 0.10, relx = 0.30, rely = 0.90)
        self.textbox_chat.place(relwidth = 0.95, relheight = 0.999, relx = 0.0, rely = 0.0)
        self.textbox_chat.configure(state='normal')
        self.entry_chat.place(relwidth = 0.75, relheight = 0.65, relx = 0.02, rely = 0.08)
        self.scrollbar_chat.place(relwidth = 0.05, relheight = 0.999, relx = 0.95, rely = 0)
        self.button_chat.place(relwidth = 0.10, relheight = 0.65, relx = 0.78, rely = 0.08)
        self.button_sendimg.place(relwidth = 0.10, relheight = 0.65, relx = 0.89, rely = 0.08)



    #Function to mount the chat stage
    def chat_stage(self):
        self.entry_chat.place_forget()
        self.button_user.place_forget()
        self.label_user.place_forget()

        self.wind.geometry("900x700")
        self.wind.title("Chat")

        self.listbox_userson.place(relwidth = 0.999, relheight = 0.90, relx = 0, rely = 0.10)
        self.label_username.place(relwidth = 0.30, relheight = 0.09, relx = 0.0, rely = 0.0)
        self.label_contacts.place(relwidth = 0.30, relheight = 0.91, relx = 0.0, rely = 0.09)
        self.label_chat.place(relwidth = 0.70, relheight = 0.90, relx = 0.30, rely = 0.0)
        #self.label_wchat.place(relwidth = 0.70, relheight = 0.10, relx = 0.30, rely = 0.90)
        self.entry_contacts.place(relwidth = 0.9999, relheight = 0.05, relx = 0.0, rely = 0.0)
        #self.entry_chat.place(relwidth = 0.75, relheight = 0.65, relx = 0.02, rely = 0.08)
        #self.textbox_chat.place(relwidth = 0.95, relheight = 0.999, relx = 0.0, rely = 0.0)
        #self.scrollbar_chat.place(relwidth = 0.05, relheight = 0.999, relx = 0.95, rely = 0)


if __name__ == '__main__':
    WindowT = Tk()
    application = App(WindowT)
    WindowT.mainloop()