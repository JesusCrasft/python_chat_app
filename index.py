from tkinter import ttk
from tkinter import * 

import socket

class App:

    def __init__(self, WindowT):
        #Window Attributes
        self.wind = WindowT
        self.wind.title('Chat')
        self.wind.geometry('900x700')
        self.wind.configure(bg='#1F1F1F')

        #Variables
        self.username = 'jesus'
        self.x = 0.80
        self.y = 0
       

        """Labels"""
        #Username Label
        self.label_username = Label(self.wind, text='one')
        self.label_username.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_username.place(relwidth = 0.30, relheight = 0.09, relx = 0.0, rely = 0.0)

        #Contacts Label
        self.label_contacts = Label(self.wind, text='two')
        self.label_contacts.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_contacts.place(relwidth = 0.30, relheight = 0.91, relx = 0.0, rely = 0.09)

        #Chat Label
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
        self.button_chat = Button(self.label_wchat, text='Enviar', command=self.place_mymessage)
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

    #Function to place the message that the user wrote
    def place_mymessage(self):
        #Get the message
        message = self.entry_chat.get()

        #Insert the message in the chat
        self.listbox_chat.insert(END, f'{self.username} : {message} \n')
        
        #Encode the message
        message_encode = message.encode()

        #Sending message
        self.send_mymessage(message_encode)

    def send_mymessage(self, message):
        sender = self.username.encode()
        request = (sender, message)

        #Create the socket
        self.my_socket = socket.socket()

        #Connect to host
        self.my_socket.connect(('localhost', 8000))

        #Send the message and sender
        self.my_socket.sendall()

        self.my_socket.close()


    def place_hismessage(self):
        pass



if __name__ == '__main__':
    WindowT = Tk()
    application = App(WindowT)
    WindowT.mainloop()