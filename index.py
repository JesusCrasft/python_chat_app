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
        self.PORT = 8006
        self.SERVER = "192.168.1.205"
        self.ADDR = (self.SERVER, self.PORT)

        #Variables
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username_client = ''
        self.check_conn = [False, False]
       

        """Labels"""
        #Username Label
        self.label_username = Label(self.wind)
        self.label_username.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        #self.label_username.place(relwidth = 0.30, relheight = 0.09, relx = 0.0, rely = 0.0)
        
        #Contacts Label
        self.label_contacts = Label(self.wind)
        self.label_contacts.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        #self.label_contacts.place(relwidth = 0.30, relheight = 0.95, relx = 0.0, rely = 0.09)
        
        #Chat Label
        self.label_chat = Label(self.wind, text="Seleccione un Chat para comenzar a chatear")
        self.label_chat.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray', font=('Arial', 15))
        #self.label_chat.place(relwidth = 0.70, relheight = 0.90, relx = 0.30, rely = 0.0)
        
        #Widget Chat Label
        self.label_wchat = Label(self.wind)
        self.label_wchat.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        #self.label_wchat.place(relwidth = 0.70, relheight = 0.10, relx = 0.30, rely = 0.90)
        
        #Select Username Label
        self.label_user = Label(self.wind)
        self.label_user.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_user.place(relwidth = 0.9999, relheight = 0.9999, relx = 0.0, rely = 0.0)

        #Chat Type
        self.label_chatype = Label(self.label_contacts, text='Online Users')
        self.label_chatype.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')

        """Entrys"""
        #Chat Entry
        self.entry_chat = Entry(self.label_wchat, font=('Arial', 15))
        self.entry_chat.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        #self.entry_chat.place(relwidth = 0.75, relheight = 0.65, relx = 0.02, rely = 0.08)
        
        #Select Username Entry
        self.entry_user = Entry(self.label_user, font=('Arial', 15))
        self.entry_user.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        self.entry_user.place(relwidth = 0.70, relheight = 0.18, relx = 0.16, rely = 0.25)

        """Buttons"""
        #Chat Button
        self.button_chat = Button(self.label_wchat, text='Enviar', command=self.send_dm)
        #self.button_chat.place(relwidth = 0.10, relheight = 0.65, relx = 0.78, rely = 0.08)
        
        #Image Button
        self.button_sendimg = Button(self.label_wchat, text='Imagen')
        #self.button_sendimg.place(relwidth = 0.10, relheight = 0.65, relx = 0.89, rely = 0.08)
        
        #DM Button
        self.button_seldms = Button(self.label_contacts, text='Messages', font=('Arial', 10), command=lambda m="": self.manage_send("req_online_users"))
        self.button_seldms.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='white')

        #Groups Button
        self.button_selgroups = Button(self.label_contacts, text='Groups', font=('Arial', 10))
        self.button_selgroups.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='white')

        #Accept User Button
        self.button_user = Button(self.label_user, text='Aceptar', command=self.check_client, state='disabled')
        self.button_user.place(relwidth = 0.25, relheight = 0.18, relx = 0.39, rely = 0.55)

        """Others"""
        self.listbox_userson = Listbox(self.label_contacts)
        self.listbox_userson.configure(bg='#1F1F1F', font=('Arial', 17), fg='white', highlightbackground='gray', borderwidth=1)

        """Chat"""
        #Textbox
        self.textbox_chat = Text(self.label_chat, font=('Arial', 15), state='disabled')
        self.textbox_chat.configure(exportselection=False, bg='white', fg='gray', highlightbackground='gray')
        
        #ScrollBar
        self.scrollbar_chat = Scrollbar(self.label_chat, command=self.textbox_chat.yview)
        self.textbox_chat.configure(yscrollcommand=self.scrollbar_chat.set)
        self.scrollbar_chat.configure(background='#444444', activebackground='gray')
        
        #Functions
        self.responses_stop = threading.Event()  
        self.Eventks()
    
    #Function to catch the events from tkinter
    def Eventks(self):

        #Window close event
        self.wind.protocol("WM_DELETE_WINDOW", self.closing_window)

        #Listbox select
        self.listbox_userson.bind('<<ListboxSelect>>', self.select_chat)

        #Button release
        self.entry_user.bind("<KeyRelease>", self.validate_buttons)


    #Function to select username 
    def check_client(self):
        #Check if client is already connected
        try:
            self.client.connect(self.ADDR)

        except socket.error:
            pass

        #Get the username
        self.username_client = self.entry_user.get()

        #Send the username
        self.client.send(pickle.dumps(self.username_client))
        
        #Update check conn
        self.check_conn[0] = True

        #Active responses thread
        self.responses_thread = threading.Thread(target=self.manage_recv)
        self.responses_thread.start()


    #Function to manage all the recvs
    def manage_recv(self):  
        while True:
            #Flag to stop the while
            if self.responses_stop.is_set():
                break

            try:   
                type_data = self.client.recv(self.HEADER) 
        
                #Type connection
                if type_data != b'':  
                    type_data = pickle.loads(type_data)

                    #Handle Other Messages
                    if type_data[0] == "dm_message":
                        sender = type_data[1]
                        message = type_data[2]
                        
                        #Manage the chat file
                        self.chats_files(sender, message, type="write")

                        if sender == self.listbox_userson.get(ANCHOR):
                            self.refresh_chat()
                            
                    #Users online
                    if type_data[0] == "online_users":
                        self.listbox_userson.delete(0, END)
                        print("blink")
                        for user in  type_data[1]:
                            if user != self.username_client:
                                self.listbox_userson.insert(0, user)
        

                    #Check invalid user
                    if type_data == "invalid_user":
                        label_message = Message(self.label_user, text="The user is already online")
                        label_message.place(relwidth = 0.70, relheight = 0.25, relx = 0.16, rely = 0.10)
                        self.check_conn[1] = False
                        break

                    #Check valid user
                    if type_data == "valid_user":
                        self.chat_stage()
                        self.check_conn[1] = True
                    

            except Exception as ex:
                print(ex, "recieve responses")
                break

    
    #Function to manage a few sends
    def manage_send(self, *args):
        for value in args:
            
            #Request Online Users
            if value == "req_online_users":
                type_data = ["req_online_users", self.username_client]
                type_data = pickle.dumps(type_data)
                self.client.send(type_data)
                print("data req")


    #Function to send the message and username
    def send_dm(self):
        #Get the username and message
        message = self.entry_chat.get()
        receiver = self.listbox_userson.get(ANCHOR)

        #Use pickle to encode the data
        data_list = ["dm_message", self.username_client, receiver, message]
        data_list = pickle.dumps(data_list)

        #Sending the message and the length
        self.client.send(data_list)

        #Message
        message = f"{self.username_client}: {message}"

        #Manage the chat file
        self.chats_files(receiver, message, type="write")
        
        #Refresh the chat
        self.refresh_chat()
    
    
    #Function to manage the chat data from json
    def chats_files(self, chat, message_str=None, type=None):
        messages = []
        message = []
        message.append(message_str)
        
        #Try to open the file if exists
        try:
            #Extract the chat data
            with open(f"chats/{chat}_chat.json") as file:
                chat_data = json.load(file)

            #Write method
            if type == "write":
                messages = chat_data + message
                                    
                #Save the messages in the chat data
                with open(f"chats/{chat}_chat.json", "w") as file:
                    json.dump(messages, file)

            #Open method
            if type == "open":
                return chat_data

        #Create the chat if not exists
        except Exception as ex:

            #Write method
            if type == "write":
                with open(f"chats/{chat}_chat.json", "w") as file:
                    json.dump(message, file)

            #Open method
            if type == "open":
                return None


    #Function to refresh a chat
    def refresh_chat(self):
        #Chat the textbox state
        self.textbox_chat.configure(state='normal')

        #Get the chat user and the messages from the chat file
        chat_user = self.listbox_userson.get(ANCHOR)
        chat_data = self.chats_files(chat_user, type="open")
        
        #Delete the textbox
        self.textbox_chat.delete("1.0", END)

        #Validate if the chat file has messages
        if chat_data != None:
            for message in chat_data:
                self.textbox_chat.insert(END, f"{message} \n")

        #Change the textbox state
        self.textbox_chat.configure(state='disabled')


    #Function to disconnect from server
    def disconnect_client(self):   
        if self.check_conn[0] == False:
            self.wind.destroy()

        elif self.check_conn[0] == True and self.check_conn[1] == False:
            self.client.send(pickle.dumps("disconnect_nouser"))
            self.client.close()
            self.wind.destroy()

        elif self.check_conn[0] == True and self.check_conn[1] == True:
            type_data = ["disconnect_user", self.username_client]
            type_data = pickle.dumps(type_data)
            self.client.send(type_data)
            self.client.close()
            self.wind.destroy()


    #Function to manage the closing window
    def closing_window(self):
        self.responses_stop.set()
        self.disconnect_client()
        

    #Function to select a chat
    def select_chat(self, key):
        if self.listbox_userson.get(ANCHOR) != "":
            #Mount the select chat
            self.label_chat.place(relheight=0.90)
            self.label_wchat.place(relwidth = 0.70, relheight = 0.10, relx = 0.30, rely = 0.90)

            #Chat
            self.textbox_chat.place(relwidth = 0.95, relheight = 0.999, relx = 0.0, rely = 0.0)
            
            self.scrollbar_chat.place(relwidth = 0.05, relheight = 0.999, relx = 0.95, rely = 0)
        
            #Entry and Buttons
            self.entry_chat.place(relwidth = 0.75, relheight = 0.65, relx = 0.02, rely = 0.08)
            self.button_chat.place(relwidth = 0.10, relheight = 0.65, relx = 0.78, rely = 0.08)
            self.button_sendimg.place(relwidth = 0.10, relheight = 0.65, relx = 0.89, rely = 0.08)

            self.refresh_chat()


    #Function to validate buttons
    def validate_buttons(self, key):
        username = self.entry_user.get()

        while username != '' and username.isspace() == False:
            self.button_user.configure(state='normal')
            break
        else:
            self.button_user.configure(state='disabled')


    #Function to mount the chat stage
    def chat_stage(self):
        self.entry_chat.place_forget()
        self.button_user.place_forget()
        self.label_user.place_forget()

        self.wind.geometry("900x700")
        self.wind.title("Chat")

        #Labels
        self.label_contacts.place(relwidth = 0.30, relheight = 0.95, relx = 0.0, rely = 0.05)
        self.label_username.place(relwidth = 0.30, relheight = 0.05, relx = 0.0, rely = 0.0)
        self.label_chat.place(relwidth = 0.70, relheight = 0.999, relx = 0.30, rely = 0.0)
        self.label_username.configure(text=self.username_client)
        
        #Buttons
        self.button_seldms.place(relwidth=0.50, relheight=0.05, relx=0, rely=0)
        self.button_selgroups.place(relwidth=0.50, relheight=0.05, relx=0.50, rely=0)
        
        #Other
        self.listbox_userson.place(relwidth = 0.999, relheight = 0.90, relx = 0, rely = 0.10)
        self.label_chatype.place(relwidth = 0.999, relheight = 0.05, relx = 0, rely = 0.05)




if __name__ == '__main__':
    WindowT = Tk()
    application = App(WindowT)
    WindowT.mainloop()