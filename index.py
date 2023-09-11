from tkinter import ttk
from tkinter import * 

class Product:

    def __init__(self, WindowT):
        #Window Attributes
        self.wind = WindowT
        self.wind.title('Chat')
        self.wind.geometry('900x700')
        self.wind.configure(bg='#1F1F1F')

        #Variables
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
        self.label_chat = Label(self.wind, text='three')
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

        """Chat"""
        self.widget_chat = Text(self.label_chat, font=('Arial', 15))
        self.widget_chat.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
        self.widget_chat.place(relwidth = 0.9999, relheight = 0.91, relx = 0.00, rely = 0.0)


if __name__ == '__main__':
    WindowT = Tk()
    application = Product(WindowT)
    WindowT.mainloop()