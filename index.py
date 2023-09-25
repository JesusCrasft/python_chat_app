from tkinter import ttk
from tkinter import * 

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
        self.PORT = 8011
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
        self.entry_user.insert(END, "jesus")


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
        self.responses_stop = threading.Event()
        self.Eventks()
        
    def Eventks(self):
        self.wind.protocol("WM_DELETE_WINDOW", self.closing_window)

    #Function to manage the closing window
    def closing_window(self):
        self.disconnect_client()
        self.responses_stop.set()
        self.wind.destroy()
        
    #Function to select username 
    def select_username(self):
        self.client.connect(self.ADDR)
        self.username_client = self.entry_user.get()
        self.username_client = pickle.dumps(self.username_client)
    

        self.responses_thread = threading.Thread(target=self.recieve_responses)
        self.responses_thread.start()

        self.chat_stage()

        self.client.send(self.username_client)

    #Function to send the message and username
    def send_message(self):
        #Get the username and message
        username = self.entry_user.get()
        message = self.entry_chat.get()
        
        #Use pickle to encode the data
        data_list = [username, message]
        data = pickle.dumps(data_list)

        #Extract the length
        send_length = self.length_message(str(data))

        #Sending the message and the length
        self.client.send(send_length)
        self.client.send(data)

        
    #Recieve message
    def recieve_responses(self):  
        while True:
            try:  
                if self.responses_stop.is_set():
                    break

                else:
                    #Pickle method    
                    #self.client.settimeout(1)
                    type_conn = self.client.recv(self.HEADER) 

                    #Type connection
                    if type_conn != b'':
                        type_conn = pickle.loads(type_conn)

                        #Users online
                        if type_conn == "online_users":
                            data = self.client.recv(self.HEADER)
                            if data != b'':
                                print(pickle.loads(data), "data") 
                                
                                #self.textbox_chat.insert(END, f"{username} : {message} \n")

            except TimeoutError:
                continue

            except Exception as ex:
                print(ex, "recieve responses")
                break
        
    
    #Function to disconnect from server
    def disconnect_client(self):   
        self.client.send(pickle.dumps("disconnect"))
        self.client.send(self.username_client)


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

    def chat_stage(self):
        self.entry_chat.place_forget()
        self.button_user.place_forget()
        self.label_user.place_forget()

        self.wind.geometry("900x700")
        self.wind.title("Chat")

        self.label_username.place(relwidth = 0.30, relheight = 0.09, relx = 0.0, rely = 0.0)
        self.label_contacts.place(relwidth = 0.30, relheight = 0.91, relx = 0.0, rely = 0.09)
        self.label_chat.place(relwidth = 0.70, relheight = 0.90, relx = 0.30, rely = 0.0)
        #self.label_wchat.place(relwidth = 0.70, relheight = 0.10, relx = 0.30, rely = 0.90)
        self.entry_contacts.place(relwidth = 0.9999, relheight = 0.05, relx = 0.0, rely = 0.0)
        #self.entry_chat.place(relwidth = 0.75, relheight = 0.65, relx = 0.02, rely = 0.08)
        #self.button_chat.place(relwidth = 0.10, relheight = 0.65, relx = 0.78, rely = 0.08)
        #self.button_sendimg.place(relwidth = 0.10, relheight = 0.65, relx = 0.89, rely = 0.08)
        #self.textbox_chat.place(relwidth = 0.95, relheight = 0.999, relx = 0.0, rely = 0.0)
        #self.scrollbar_chat.place(relwidth = 0.05, relheight = 0.999, relx = 0.95, rely = 0)

if __name__ == '__main__':
    WindowT = Tk()
    application = App(WindowT)
    WindowT.mainloop()