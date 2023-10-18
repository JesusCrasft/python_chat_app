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
        self.PORT = 8008
        self.SERVER = "192.168.1.205"
        self.ADDR = (self.SERVER, self.PORT)

        #Variables
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username_client = ''
        self.groups = {}
        self.flags = {
            #Connected to server
            "connected": False,
            #Validation user
            "user": False,
            #dms chat type
            "dms": True,
            #groups chat type
            "groups": False
        }
       

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
        self.button_chat = Button(self.label_wchat, text='Enviar', command=self.send_messages, state='disabled')
        #self.button_chat.place(relwidth = 0.10, relheight = 0.65, relx = 0.78, rely = 0.08)
        
        #Image Button
        self.button_sendimg = Button(self.label_wchat, text='Imagen')
        #self.button_sendimg.place(relwidth = 0.10, relheight = 0.65, relx = 0.89, rely = 0.08)
        
        #DM Button
        self.button_seldms = Button(self.label_contacts, text='Messages', font=('Arial', 10), command=lambda m="": self.chat_type("req_online_users", "button_message"))
        self.button_seldms.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='white')

        #Groups Button
        self.button_selgroups = Button(self.label_contacts, text='Groups', font=('Arial', 10),  command=lambda m="": self.chat_type("button_groups"))
        self.button_selgroups.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='white')

        #Accept User Button
        self.button_user = Button(self.label_user, text='Aceptar', command=self.check_client, state='disabled')
        self.button_user.place(relwidth = 0.25, relheight = 0.18, relx = 0.39, rely = 0.55)

        #Create new group Button
        self.button_cregroup = Button(self.label_username, text='+', command=lambda m="": self.create_windowgr(phase="1"))
        self.button_cregroup.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='white')

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
        self.entry_user.bind("<KeyRelease>", lambda m="": self.validate_buttons("button_user"))
        self.entry_chat.bind("<KeyRelease>", lambda m="": self.validate_buttons("button_chat"))

        #Keys
        self.wind.bind("<Return>", lambda m="": self.validate_buttons("enter_key"))


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
        self.flags.update({"connected": True})

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

                    #Handle DMs Recv
                    if type_data[0] == "dm_message":
                        sender = type_data[1]
                        message = type_data[2]
                        
                        #Manage the chat file
                        self.manage_files(req=False, method="write", directory=sender, flag="dms", new_data=message)

                        if sender == self.listbox_userson.get(ANCHOR):
                            self.refresh_chat()
                    
                    #Handle Messages to Groups
                    if type_data[0] == "group_message":
                        group_name = type_data[1]
                        message = type_data[2]
                        print(message)
                        #Manage the chat file
                        self.manage_files(req=False, method="write", directory=group_name, flag="groups", new_data=message)

                        if group_name == self.listbox_userson.get(ANCHOR):
                            self.refresh_chat()

                    #Online Users Recv
                    if type_data[0] == "online_users":
                        #Delete the list
                        self.listbox_userson.delete(0, END)

                        #Validation "dms" flag
                        if self.flags.get("dms") == True:
                            for user in type_data[1]:
                                if user != self.username_client:
                                    self.listbox_userson.insert(0, user)
                        
                        #Validation "groups" flag
                        if self.flags.get("groups") == "Insert":
                            for user in type_data[1]:
                                if user != self.username_client:
                                    self.list_addgr.insert(0, user)
                                    self.flags.update({"groups": True})

                    #Create Group
                    if type_data[0] == "create_group":
                        self.manage_files(req=True, method="write", new_data={type_data[1]: type_data[2]})

                    #Check invalid user Recv
                    if type_data == "invalid_user":
                        label_message = Message(self.label_user, text="The user is already online")
                        label_message.place(relwidth = 0.70, relheight = 0.25, relx = 0.16, rely = 0.10)
                        self.flags.update({"user": False})
                        break

                    #Check valid user Recv
                    if type_data == "valid_user":
                        self.chat_stage()
                        self.flags.update({"user": True})
                    

            except Exception as ex:
                print(ex, "recieve responses")
                break

    
    #Function to manage the type of the chat
    def chat_type(self, *args):
        #Forget the textbox
        self.textbox_chat.place_forget()

        #Chat Type manage
        for value in args:
            
            """DMs"""
            #Request Online Users
            if value == "req_online_users":
                #Request the data
                type_data = ["req_online_users", self.username_client]
                type_data = pickle.dumps(type_data)
                self.client.send(type_data)

            #Button Messages
            if value == "button_message":
                #flag "dms" True
                self.flags.update({"dms": True})
                self.flags.update({"groups": False})

                #Remove the button 
                self.button_cregroup.place_forget()

            """Groups"""
            #Request Groups
            if value == "button_groups":
                #Delete the list
                self.listbox_userson.delete(0, END)
                
                #List of groups req
                self.groups = self.manage_files(req=True, method="open")
            
                #Update the list with the groups
                for group in list(self.groups.keys()):
                    self.listbox_userson.insert(0, group)
                    
                #Flag "groups" True and "dms" False
                self.flags.update({"groups": True})
                self.flags.update({"dms": False})

                #Place the button
                self.button_cregroup.place(relwidth=0.25, relheight=0.999, relx=0, rely=0)
                

    #Function to send the message and username
    def send_messages(self):
        #Get the username and message
        message = self.entry_chat.get()
        receiver = self.listbox_userson.get(ANCHOR)
        
        #Validate the type of chat
        if self.flags.get("dms") == True:
            flag = "dm_message"
        else:
            flag = "group_message"

        #Use pickle to encode the data
        data_list = [flag, self.username_client, receiver, message]
        data_list = pickle.dumps(data_list)

        #Sending the message and the length
        self.client.send(data_list)

        #Message
        message = f"{self.username_client}: {message}"

        #Manage the chat file
        self.manage_files(req=False, method="write", directory=receiver, new_data=message)
        
        #Refresh the chat
        self.refresh_chat()

        #Delete the entry
        self.entry_chat.delete(0, END)


    #Function to manage the chat data from json
    def manage_files(self, req, method=None, directory=None, new_data=None, flag=None):
        #Validate if the user is requesting the list groups or messages
        if req != True:
            #Validate which directory is going to be use
            if flag != None:
                #If user is in chat dms type and a new group message arrive then save the message in groups
                if self.flags.get("dms") == True:
                    flag = f"chats/groups/{directory}_chat.json"
                else:
                    flag = f"chats/dms/{directory}_chat.json"

            #Validate the type of chat with flag inactive
            else:
                #If the user is in the chat dms type and no new messages arrive the save the message in dms
                if self.flags.get("dms") == True:
                    flag = f"chats/dms/{directory}_chat.json"
                else:
                    flag = f"chats/groups/{directory}_chat.json"
        else:
            flag = "chats/list_groups.json"

        
        #Try to open the file if exists
        try:
            #Get the file data
            with open(flag, "w") as file:
                file_data = json.load(file)

            #Write method
            if method == "write":
                
                if req != True:
                    #Messages method, add the new list to the old list of messages
                    file_data = file_data + new_data
                else:
                    #Group list method, update the file data with the new group dictionary
                    file_data.update(new_data)

                #Save the new data into the file
                with open(flag, "w") as file:
                    json.dump(file_data, file)
                        
            #Open method
            if method == "open":
                return file_data

        #Create the chat if not exists
        except Exception as ex:
            #Write method
            if method == "write":
                with open(flag, "w") as file:
                    json.dump(new_data, file)

            #Open method
            if method == "open":
                if req != True:
                    return None
                else:
                    return {}


    #Function to refresh a chat
    def refresh_chat(self):
        #Chat the textbox state
        self.textbox_chat.configure(state='normal')

        #Get the chat user and the messages from the chat file
        name = self.listbox_userson.get(ANCHOR)
        data = self.manage_files(req=False, method="open", directory=name)
            
        #Delete the textbox
        self.textbox_chat.delete("1.0", END)

        #Validate if the chat file has messages
        if data != None:
            for message in data:
                self.textbox_chat.insert(END, f"{message} \n")

        #Change the textbox state
        self.textbox_chat.configure(state='disabled')


    #Function to manage the closing window
    def closing_window(self):
        self.responses_stop.set()
        self.disconnect_client()
        

    #Function to disconnect from server
    def disconnect_client(self):   
        #Validate if the user is connected
        if self.flags.get("connected") == False:
            self.wind.destroy()

        #Validate if the user is connected and the user is invalid
        elif self.flags.get("connected") == True and self.flags.get("user") == False:
            self.client.send(pickle.dumps("disconnect_nouser"))
            self.client.close()
            self.wind.destroy()

        #Validate if the user is connected and the user is valid
        elif self.flags.get("connected") == True and self.flags.get("user") == True:
            type_data = ["disconnect_user", self.username_client]
            type_data = pickle.dumps(type_data)
            self.client.send(type_data)
            self.client.close()
            self.wind.destroy()


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
 
            #Refresh chat
            self.refresh_chat()
                 

    #Function to validate buttons
    def validate_buttons(self, *args):
        username = self.entry_user.get()
        entry = self.entry_chat.get()

        for value in args:
            #Entry user validation
            if value == "button_user":
                while username != '' and username.isspace() == False:
                    self.button_user.configure(state='normal')
                    break
                else:
                    self.button_user.configure(state='disabled')

            #Entry chat validation
            if value == "button_chat":
                while entry != '' and entry.isspace() == False:
                    self.button_chat.configure(state='normal')
                    break

                else:
                    self.button_chat.configure(state='disabled')

            #Entry addgr validation
            if value == "button_addgr":
                while entry != '' and entry.isspace() == False:
                    self.send_messages()
                    break
                
                else:
                    self.button_chat.configure(state='disabled')


            #Enter key validation
            if value == "button_addgr":
                entry_group = self.entry_addgr.get()
                while entry_group != '' and entry_group.isspace() == False:
                    self.button_addgr.configure(state='active')
                    break
                
                else:
                    self.button_chat.configure(state='disabled')


    #Function to mount the chat stage
    def chat_stage(self):
        #Remove "Select username" stage
        self.entry_chat.place_forget()
        self.button_user.place_forget()
        self.label_user.place_forget()

        #Change the geometry and title
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


    #Function to create a window for the group creation
    def create_windowgr(self, phase, name=None):
        #Phase 1, select a name
        if phase == "1":
            #Create a toplevel window
            self.wind_addgr = Toplevel()
            self.wind_addgr.configure(bg='#1F1F1F')

            #List label
            self.label_addgr = Label(self.wind_addgr)
            self.label_addgr.configure(background='#1F1F1F', relief=SOLID, borderwidth=2, fg='gray')
            self.label_addgr.place(relwidth=0.999, relheight=0.999, relx=0, rely=0)

            #Window config
            self.wind_addgr.geometry("400x200")
            self.wind_addgr.title("Select a name for the group")

            #Entry Add Group
            self.entry_addgr = Entry(self.label_addgr, font=('Arial', 15))
            self.entry_addgr.configure(exportselection=False, bg='#323232', fg='white', highlightbackground='gray')
            self.entry_addgr.place(relwidth = 0.70, relheight = 0.18, relx = 0.16, rely = 0.25)

            #Button Add Group
            self.button_addgr = Button(self.label_addgr, text='Aceptar', command=lambda m="": self.create_windowgr(name=self.entry_addgr.get(), phase="2"), state='disabled')
            self.button_addgr.place(relwidth = 0.25, relheight = 0.18, relx = 0.39, rely = 0.55)

            #Bind the entry 
            self.entry_addgr.bind("<KeyRelease>", lambda m="": self.validate_buttons("button_addgr"))
            
        #Phase 2, select users
        elif phase == "2":
            #Forget the Entry and Button
            self.entry_addgr.place_forget()
            self.button_addgr.place_forget()

            #Window config
            self.wind_addgr.geometry("260x400")
            self.wind_addgr.title("Select the integrants")

            #Listbox Add Group
            self.list_addgr = Listbox(self.label_addgr, selectmode=MULTIPLE)
            self.list_addgr.configure(bg='#1F1F1F', font=('Arial', 17), fg='white', highlightbackground='gray', borderwidth=1)
            self.list_addgr.place(relwidth=0.999, relheight=0.90, relx=0, rely=0)

            #Button Add Group
            self.button_addgr = Button(self.label_addgr, text='Aceptar', command=lambda m="": self.create_group(name, self.list_addgr), state='active')
            self.button_addgr.place(relwidth = 0.25, relheight = 0.10, relx = 0.39, rely = 0.90)

            #Call the function to print this list in the list users
            self.flags.update({"groups": "Insert"})
            self.chat_type("req_online_users")


    #Function to create a group
    def create_group(self, group_name, integrant):
        #Hide the window
        self.wind_addgr.withdraw()

        #list of integrants
        integrants = []

        #Get the list of integrants
        for i in integrant.curselection():
            integrants.append(integrant.get(i))

        #Encode the data
        type_data = ["create_group", group_name, integrants]
        type_data = pickle.dumps(type_data)

        #Add the group to the list of groups and update the listbox
        self.manage_files(req=True, method="write", new_data={group_name: integrants})
        self.chat_type("button_groups")

        #Send the information
        self.client.send(type_data)

        #Destroy the window
        self.wind_addgr.destroy()



if __name__ == '__main__':
    WindowT = Tk()
    application = App(WindowT)
    WindowT.mainloop()