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
        self.my_socket = socket.socket()
        self.username = ''
       

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
        self.label_chat.place(relwidth = 0.70, relheight = 0.9999, relx = 0.30, rely = 0.0)


        """Entrys"""
        #Contacts Chat
        self.entry_contacts = Entry(self.label_contacts, font=('Arial', 15))
        self.entry_contacts.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        self.entry_contacts.place(relwidth = 0.9999, relheight = 0.05, relx = 0.0, rely = 0.0)

        #Chat Entry
        self.entry_chat = Entry(self.label_chat, font=('Arial', 15))
        self.entry_chat.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        self.entry_chat.place(relwidth = 0.75, relheight = 0.06, relx = 0.02, rely = 0.92)


        """Buttons"""
        #Chat Button
        self.button_chat = Button(self.label_chat, text='Enviar')
        self.button_chat.place(relwidth = 0.10, relheight = 0.05, relx = 0.78, rely = 0.92)

        #Image Button
        self.button_sendimg = Button(self.label_chat, text='Imagen')
        self.button_sendimg.place(relwidth = 0.10, relheight = 0.05, relx = 0.89, rely = 0.92)


        """Messages"""
        self.widget_messages = Message(self.label_chat, text='Prueba')
        #self.widget_messages.place(relwidth = 0.10, relheight = 0.05, relx = 0.50, rely = 0.50)


        """Chat"""
        #Chat Frame
        self.frame_chat = Frame(self.label_chat)
        self.frame_chat.configure(background='#1F1F1F', relief=SOLID, borderwidth=2)
        self.frame_chat.place(relwidth = 0.9998, relheight = 0.91, relx = 0.0, rely = 0.0)

        #Chat Canvas
        self.canvas_chat = Canvas(self.frame_chat)
        self.canvas_chat.configure(background='gray', relief=SOLID, borderwidth=0, highlightbackground='#1F1F1F')
        self.canvas_chat.place(relwidth = 0.9998, relheight = 0.9999, relx = 0.0, rely = 0.0)
        
        #Chat Scrollbar
        self.scrollbar_chat = Scrollbar(self.frame_chat, orient=VERTICAL, command=self.canvas_chat.yview)
        self.scrollbar_chat.configure()
        self.scrollbar_chat.place(relwidth = 0.05, relheight = 0.996, relx = 0.92, rely = 0)
        
        #Configure Chat Canvas with Chat Scrollbar
        self.canvas_chat.configure(yscrollcommand=self.scrollbar_chat.set)
        self.canvas_chat.bind('<Configure>', lambda e: self.canvas_chat.configure(scrollregion=self.canvas_chat.bbox('all'))) 

        #Helper Frame
        self.frame_helper = Frame(self.canvas_chat)
        self.canvas_chat.create_window((0,0), window=self.frame_helper, anchor=NW)

        for messages in range(100):
            Message(self.frame_helper, text=f'Nakuru {messages}').grid()
            
    
        

if __name__ == '__main__':
    WindowT = Tk()
    application = App(WindowT)
    WindowT.mainloop()