'''
***************************************************************************
Kully Kekaula

Description: Methods to create and manage the controller settings window.
***************************************************************************
''' 
from pygame.locals import *
import Tkinter as tk
from Tkinter import Menu, Frame, Toplevel
import tkMessageBox as tkm
import main

class controllerSettings():

    def createControllerWindow(self):

        #Creation of the main window
        self.controllerWindow = Toplevel()
        self.controllerWindow.title("Controller Settings")
        self.controllerWindow.geometry("400x310+450+200")
        self.controllerWindow.resizable(width=False, height=False)

        #Frame for the manual controller options
        self.k_controllerFrame = tk.Frame(self.controllerWindow)
        self.c_controllerFrame = tk.Frame(self.controllerWindow)
        self.instructionFrame = tk.Frame(self.controllerWindow)

        self.knownJsFrame=tk.Frame(self.k_controllerFrame,width=150,height=120)
        self.knownJsFrame.pack_propagate(0)
        self.chosenJsFrame=tk.Frame(self.c_controllerFrame,width=150,height=120)
        self.chosenJsFrame.pack_propagate(0)

        self.instrLabel = tk.Label(self.instructionFrame, text="Please select up " \
            "to two remote controllers from the recognized controller list. Alter" \
            "natively, scan for existing controllers and automatically add the " \
            "controller to the software.", anchor=tk.W, justify=tk.LEFT, wraplength = 400)
        self.instrLabel.pack()
        self.l1 = tk.Label(self.knownJsFrame, text="Recognized Controllers")
        self.l1.pack()
        self.l2 = tk.Label(self.chosenJsFrame, text="Selected Controller/s")
        self.l2.pack()
        self.knownListbox = tk.Listbox(self.knownJsFrame, height = 15, width = 29)
        self.knownListbox.insert(tk.END)

        for item in ["PS3 PowerA", "Xbox 360 Afterglow"]:
            self.knownListbox.insert(tk.END, item)

        self.chosenListbox = tk.Listbox(self.chosenJsFrame, height = 15, width = 29)
        self.chosenListbox.insert(tk.END)

        self.controllers = []
        self.controllers = self.retrieveControllers()

        if len(self.controllers) == 1:
            self.chosenListbox.insert(tk.END, self.controllers[0])
        elif len(self.controllers) == 2:
            self.chosenListbox.insert(tk.END, self.controllers[0])
            self.chosenListbox.insert(tk.END, self.controllers[1])

        self.closeBtn = tk.Button(self.controllerWindow, text ="Close", \
            command = self.controllerWindow.destroy, width = 12)

        self.okBtn = tk.Button(self.controllerWindow, text ="Okay", \
            width = 12)

        self.applyBtn = tk.Button(self.controllerWindow, text ="Apply Changes", \
            width = 16, command = self.selectedListBoxWriteout)

        self.addBtn = tk.Button(self.controllerWindow, text ="Add", \
            width = 10, command = self.addListBoxIndex)

        self.rmvBtn = tk.Button(self.controllerWindow, text ="Remove", \
            width = 10, command = self.rmvListBoxIndex)

        self.scanBtn = tk.Button(self.controllerWindow, text ="Scan for controllers...", \
            width = 16)

        self.knownListbox.pack()
        self.chosenListbox.pack()
        self.knownJsFrame.pack()
        self.chosenJsFrame.pack()
        self.instructionFrame.pack()
        self.k_controllerFrame.pack()
        self.c_controllerFrame.pack()
        self.closeBtn.pack()
        self.okBtn.pack()
        self.applyBtn.pack()
        self.addBtn.pack()
        self.rmvBtn.pack()
        self.scanBtn.pack()

        self.k_controllerFrame.place(x = 20, y = 85)
        self.c_controllerFrame.place(x = 210, y = 85)

        self.closeBtn.place(x = 300, y = 275)
        self.okBtn.place(x = 200, y = 275)
        self.applyBtn.place(x = 20, y = 275)
        self.addBtn.place(x = 40, y = 210)
        self.rmvBtn.place(x = 240, y = 210)
        self.scanBtn.place(x = 230, y = 50)

    def addListBoxIndex(self):

        self.chosenInt = 0
        self.chosenInt = self.chosenListbox.size()

        if self.chosenInt >= 2:
            tkm.showerror("Error", "You can only add up to two controllers.")
        else:
            self.listBoxStr = ""
            self.listBoxStr = self.knownListbox.get(tk.ACTIVE)

            self.chosenListbox.insert(tk.END, self.listBoxStr)

    def rmvListBoxIndex(self):

        self.chosenInt = 0
        self.chosenInt = self.chosenListbox.index(tk.ACTIVE)

        self.chosenListbox.delete(self.chosenInt)

    def selectedListBoxWriteout(self):

        self.tempStr = ""
        self.contrlStr1 = ""
        self.contrlStr2 = ""
        self.success = 0
        if self.chosenListbox.size() == 0:
            tkm.showerror("Error", "No controllers selected.")
        
        elif self.chosenListbox.size() == 1:
            self.contrlStr1 = self.chosenListbox.get(0)
            self.tempStr = "controllerdata{" + self.contrlStr1 + "}\n"
            self.tempStr = self.tempStr.replace (" ", "_")
            self.success = 1

        elif self.chosenListbox.size() == 2:
            self.contrlStr1 = self.chosenListbox.get(0)
            self.contrlStr2 = self.chosenListbox.get(1)
            self.tempStr = "controllerdata{" + self.contrlStr1 + ","\
            + self.contrlStr2 + "}\n"
            self.tempStr = self.tempStr.replace (" ", "_")
            self.success = 1

        if self.success == 1:
            self.data = []
            with open('config.txt', 'r') as file:
                # read a list of lines into data
                self.data = file.readlines()

            for x in range (0, len(self.data)):
                if self.data[x].find("controllerdata") != -1:
                    self.data[x] = self.tempStr
                    print self.data[x]

            with open('config.txt', 'w') as file:
                file.writelines(self.data)

        self.main.destroy()
        self.createMainWindow()