from tkinter import ttk
from tkinter import * 

class Product:

    def __init__(self, WindowT):
        #Window Attributes
        self.wind = WindowT
        self.wind.title('Chat')
        self.wind.geometry('1000x800')
        self.wind.configure(bg='#1F1F1F')

        #Variables
        self.username = ''

        """Labels"""
        #Label Username
        self.label_username = Label(self.wind, text='one')
        self.label_username.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_username.place(relwidth = 0.10, relheight = 0.09, relx = 0.0, rely = 0.0)

        #Label Contacts
        self.label_contacts = Label(self.wind, text='two')
        self.label_contacts.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_contacts.place(relwidth = 0.10, relheight = 0.09, relx = 0.25, rely = 0.50)


        #Label Chat
        self.label_chat = Label(self.wind, text='three')
        self.label_chat.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
        self.label_chat.place(relwidth = 0.10, relheight = 0.09, relx = 0.70, rely = 0.0)


if __name__ == '__main__':
    WindowT = Tk()
    application = Product(WindowT)
    WindowT.mainloop()