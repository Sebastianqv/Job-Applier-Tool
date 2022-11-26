# TODO:
# - Add error handlers for the login

import sys
import threading
from tkinter import *
from tkinter import ttk
from Frames.applier import ApplierInstance
from Frames.login import FrameLogin
from Frames.selection import FrameSelection

class ApplyController(Tk):
    
    container:Frame
    applier:ApplierInstance
    frameCurrent:Frame
    frameLogin:FrameLogin
    frameSelection:FrameSelection
    frameQuery:Frame
    frameLoading:Frame

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.wm_title("ApplyTool")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.container = Frame(self)
        self.container.pack(side= TOP, fill= BOTH, expand = True)
        self.container.grid_rowconfigure(0, weight = 1)
        self.container.grid_columnconfigure(0, weight = 1)
        self.frameLoading = self.getLoading()

        self.frameLogin = FrameLogin(self.container, self)

    def login(self, username:str, password:str, field:str):
        self.frameLoading.tkraise()
        self.frameCurrent = self.frameLoading
        self.frameLogin.destroy()
        self.applier = ApplierInstance(username, password, field)
        applier_start_thread = threading.Thread(target = self.applier.start, daemon = True)
        applier_start_thread.start()
        self.frameSelection = FrameSelection(self.container, self, self.applier)
        self.frameTransition(self.frameSelection)

    #Transitions to the passed frame
    def frameTransition(self, frameNext:Frame):
        self.frameCurrent.grid_remove()
        frameNext.grid()
        self.frameCurrent = frameNext
    
    def getLoading(self):
        loadingFrame = Frame(self.container)
        loadingLabel = ttk.Label(loadingFrame, text = "Loading...")
        loadingLabel.grid(row = 0,column = 0)
        loadingFrame.grid(row = 0, column = 0)
        return loadingFrame

    def on_close(self):
        if self.applier:
            self.applier.exit()
        self.destroy()
        sys.exit()

app = ApplyController()
app.mainloop()