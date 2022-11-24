# TODO:
# - Reformat for letting users input their Username, Password, and Field
# - Add error handlers for the above
# - Include multithreading to prevent GUI window freeze

from tkinter import *
from tkinter import ttk
from applier import ApplierInstance
import sys
import time
import threading

root = Tk()

applier = ApplierInstance("Username", "Password", "Software Engineer")
applier.start()

def on_close():
    root.destroy()
    applier.exit()
    sys.exit()

jobSelection = []
checkButtons = []
def confirm_selection():
    for selection in jobSelection:
        if selection.get() != "":
            applier.apply(jobList[selection.get()])
    print("Finished Applying")

confirmButton = ttk.Button(root, text = "Submit", command = confirm_selection)

while(not applier.ranThrough):
    time.sleep(1)

jobList = applier.getJobList()

for jobName in jobList:
    var = StringVar()
    checkbutton = ttk.Checkbutton(root, text = jobName, variable = var, onvalue = jobName, offvalue = "")
    
    jobSelection.append(var)
    checkButtons.append(checkbutton)


for button in checkButtons:
    button.pack()
confirmButton.pack()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()