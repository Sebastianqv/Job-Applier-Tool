import threading
from tkinter import *
from tkinter import ttk

class FrameLogin(Frame):
    frameController:Tk
    username:str
    usernameInput:Entry
    password:str
    passwordInput:Entry
    field:str
    fieldInput:Entry

    def __init__(self, parent:Frame, frameController:Tk):
        Frame.__init__(self, parent)

        self.frameController = frameController

        usernameLabel = ttk.Label(self, text = "Username")
        usernameLabel.grid(row = 0, column = 0)
        self.usernameInput = ttk.Entry(self)
        self.usernameInput.grid(row = 1, column = 0)

        passwordLabel = ttk.Label(self, text = "Password")
        passwordLabel.grid(row = 2, column = 0)
        self.passwordInput = ttk.Entry(self)
        self.passwordInput.grid(row = 3, column = 0)

        fieldLabel = ttk.Label(self, text = "Field")
        fieldLabel.grid(row = 4, column = 0)
        self.fieldInput = ttk.Entry(self)
        self.fieldInput.grid(row = 5, column = 0)

        confirm_login_thread = threading.Thread(target = self.confirm_login, daemon = True)

        loginConfirm = ttk.Button(self, text = "Start", command = confirm_login_thread.start)
        loginConfirm.grid(row = 6, column = 0)

        self.grid(row = 0, column = 0, sticky ="nsew")
    
    def confirm_login(self):
        self.updateParameters()
        self.frameController.login(self.username, self.password, self.field)

    def updateParameters(self):
        self.username = self.usernameInput.get()
        self.password = self.passwordInput.get()
        self.field = self.fieldInput.get()
