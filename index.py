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
        

if __name__ == '__main__':
    WindowT = Tk()
    application = Product(WindowT)
    WindowT.mainloop()