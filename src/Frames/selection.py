import time
import threading
from tkinter import *
from tkinter import ttk
from .applier import ApplierInstance

class FrameSelection(Frame):
    frameController:Tk
    applier:ApplierInstance
    jobSelection = []
    jobList = []
    confirmButton:Button

    def __init__(self, parent:Frame, frameController:Tk, applier:ApplierInstance):
        Frame.__init__(self, parent)

        self.frameController = frameController
        self.applier = applier

        while not applier.ranThrough:
            time.sleep(3)
        
        self.jobList = applier.getJobList()

        rowCount = 0
        for jobName in self.jobList:
            var = StringVar()
            checkbutton = ttk.Checkbutton(self, text = jobName, variable = var, onvalue = jobName, offvalue = "")
            checkbutton.grid(row = rowCount, column = 0)
            rowCount += 1

            self.jobSelection.append(var)

        confirm_selection_thread = threading.Thread(target = self.confirm_selection, daemon = True)
        self.confirmButton = ttk.Button(self, text = "Submit", command = confirm_selection_thread.start)
        self.confirmButton.grid(row = rowCount, column = 0)

        self.grid(row = 0, column = 0, sticky ="nsew")

    def confirm_selection(self):
        self.confirmButton.config(state = DISABLED)
        for selection in self.jobSelection:
            if selection.get() != "":
                self.applier.apply(self.jobList[selection.get()])
        print("Finished Applying")
        self.confirmButton.config(state = NORMAL)
