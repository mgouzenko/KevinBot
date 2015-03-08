'''
***************************************************************************
Kully Kekaula

Description: A GUI to run the Mech Warfare robot code.
***************************************************************************
''' 
import pygame, sys, math
from pygame.locals import *
import Tkinter as tk
from Tkinter import Menu, Frame, Toplevel
import tkMessageBox as tkm
import controller, XboxPane
from PS3Controller import PS3Controller
from XboxController import XboxController
import comms

class robotGUI():
    def __init__(self):

        self.createMainWindow()

    def createMainWindow(self):
        #Configurations and program settings are determined here
        controllers = []
        controllers = self.retrieveControllers()

        #Initialize the master window 
        self.main = tk.Tk()
        self.main.title("Robot Interface v0.24")
        print controllers
        if len(controllers) == 1:
            self.main.geometry("850x650+160+10")
        elif len(controllers) == 2:
            self.main.geometry("980x650+160+10")
        self.main.resizable(width=False, height=False)

        menubar = Menu(self.main)
        self.main.config(menu=menubar)
        
        preferenceMenu = Menu(menubar)
        preferenceMenu.add_command(label="Controller Settings", \
            command = self.createControllerWindow)
        helpMenu = Menu(menubar)
        helpMenu.add_command(label="Help...")
        comMenu = Menu(menubar)
        comMenu.add_command(label="Communication Settings", \
            command = self.createCommunicationWindow)
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Data Files...")

        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Preferences", menu=preferenceMenu)
        menubar.add_cascade(label="COM Port", menu=comMenu)
        menubar.add_cascade(label="Help", menu=helpMenu)

        #Initialize frame sections of the window
        self.titleFrame = tk.Frame()

        self.robotPane()

        PS3Pane = getattr(PS3Controller(), 'createPS3Pane')
        createXboxPane = getattr(XboxController(), 'createXbox360Pane')
        if 'PS3 PowerA' in self.controllers:
            PS3Pane(self.controllers)
        if 'Xbox 360 Afterglow' in self.controllers:
            createXboxPane(self.controllers)
        
        #Initalize Axis Labels
        self.title_label = tk.Label(self.titleFrame, text='Mech Warfare GUI',\
            font=("Helvetica", 20),bg='blue',fg='white', width = 90) 

        self.title_label.pack()

        #Package frames and create the window
        self.titleFrame.pack()

        #Start commlunications and begin looping
        comms.init(self.main)

        tk.mainloop()

    def robotPane(self):
        self.enableDisableFrame = tk.Frame()
        self.ps3 = PS3Controller()

        #Frame partitions (subframes) go here
        self.enableDisable=tk.Frame(self.enableDisableFrame,width=129,height=87)
        self.enableDisable.pack_propagate(0)

        #Initialize buttons
        self.remote_Label = tk.Label(self.enableDisable, text='Robot',\
            font=("Helvetica", 13), fg='black', anchor = tk.CENTER, width = 12)
        self.remote_Label.pack(side = "top")

        self.initBut = tk.Button(self.enableDisable, text ="Enable", \
            command= lambda: self.ps3.runController(1), width = 15)
        self.initBut.pack()

        self.stopBut = tk.Button(self.enableDisable, text ="Disable", \
            command= lambda: self.stopController(1), width = 15)
        self.stopBut.pack()

        self.enableDisable.pack()
        self.enableDisableFrame.pack()

        self.enableDisableFrame.place(x=5, y=42)
        self.enableDisable.config(highlightbackground="black", borderwidth= 5, \
            relief = "ridge")

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

    def createCommunicationWindow(self):

        #Creation of the main window
        self.communicationWindow = Toplevel()
        self.communicationWindow.title("Communication Settings")
        self.communicationWindow.geometry("400x310+450+200")
        self.communicationWindow.resizable(width=False, height=False)

        #Frame for the manual controller options
        self.k_controllerFrame = tk.Frame(self.communicationWindow)
        self.c_controllerFrame = tk.Frame(self.communicationWindow)
        self.instructionFrame = tk.Frame(self.communicationWindow)

        self.knownJsFrame=tk.Frame(self.k_controllerFrame,width=150,height=120)
        self.knownJsFrame.pack_propagate(0)
        self.chosenJsFrame=tk.Frame(self.c_controllerFrame,width=150,height=120)
        self.chosenJsFrame.pack_propagate(0)

        self.instrLabel = tk.Label(self.instructionFrame, text="Please select a " \
            "communication port from the list below.  This port will be used to" \
            "communicate with the robot.", anchor=tk.W, justify=tk.LEFT, wraplength = 400)
        self.instrLabel.pack()
        self.l1 = tk.Label(self.knownJsFrame, text="Communication Ports")
        self.l1.pack()
        self.l2 = tk.Label(self.chosenJsFrame, text="Selected Ports")
        self.l2.pack()
        self.knownListbox = tk.Listbox(self.knownJsFrame, height = 15, width = 29)
        self.knownListbox.insert(tk.END)

        for item in ["COM 1", "COM 2", "COM 3", "COM 4", "COM 5", "COM 6", "COM 7", \
        "COM 8", "COM 9", "COM 1"]:
            self.knownListbox.insert(tk.END, item)

        self.chosenListbox = tk.Listbox(self.chosenJsFrame, height = 15, width = 29)
        self.chosenListbox.insert(tk.END)
        
        self.comStr = self.retrieveComPort()

        self.chosenListbox.insert(tk.END, self.comStr)

        self.closeBtn = tk.Button(self.communicationWindow, text ="Close", \
            command = self.communicationWindow.destroy, width = 12)

        self.applyBtn = tk.Button(self.communicationWindow, text ="Apply Changes", \
            width = 16, command = self.selectedComBoxWriteout)

        self.addBtn = tk.Button(self.communicationWindow, text ="Add", \
            width = 10, command = self.addListBoxIndex)

        self.rmvBtn = tk.Button(self.communicationWindow, text ="Remove", \
            width = 10, command = self.rmvListBoxIndex)

        self.knownListbox.pack()
        self.chosenListbox.pack()
        self.knownJsFrame.pack()
        self.chosenJsFrame.pack()
        self.instructionFrame.pack()
        self.k_controllerFrame.pack()
        self.c_controllerFrame.pack()
        self.closeBtn.pack()
        self.applyBtn.pack()
        self.addBtn.pack()
        self.rmvBtn.pack()

        self.k_controllerFrame.place(x = 20, y = 85)
        self.c_controllerFrame.place(x = 210, y = 85)

        self.closeBtn.place(x = 300, y = 275)
        self.applyBtn.place(x = 20, y = 275)
        self.addBtn.place(x = 40, y = 210)
        self.rmvBtn.place(x = 240, y = 210)

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

    def selectedComBoxWriteout(self):

        self.tempStr = ""
        self.comStr = ""
        self.success = 0
        if self.chosenListbox.size() == 0:
            tkm.showerror("Error", "No communication port selected.")
        
        elif self.chosenListbox.size() == 1:
            self.comStr = self.chosenListbox.get(0)
            self.tempStr = "communications{" + self.comStr + "}\n"
            self.success = 1
            self.data = []
            with open('config.txt', 'r') as file:
                # read a list of lines into data
                self.data = file.readlines()

            for x in range (0, len(self.data)):
                if self.data[x].find("communications") != -1:
                    self.data[x] = self.tempStr
                    print self.data[x]

            with open('config.txt', 'w') as file:
                file.writelines(self.data)

            self.communicationWindow.destroy

    def retrieveControllers(self):

        #Used to determine previous setting for selected controller listBox
        self.tempInt = 0
        self.tempStr = ""
        self.contrlStr1 = ""
        self.contrlStr2 = ""
        self.controllers = []
        with open('config.txt', 'r') as file:
                # read a list of lines into data
                self.data = file.readlines()

        for x in range (0, len(self.data)):
            if self.data[x].find("controllerdata") != -1:
                self.tempStr = self.data[x]
                if self.data[x].find(",") == -1:
                    self.tempInt = self.tempStr.find("}")
                    self.contrlStr1 = self.tempStr[15:self.tempInt]
                    self.contrlStr1 = self.contrlStr1.replace ("_", " ")

                    self.controllers.append(self.contrlStr1)

                elif self.data[x].find(",") != -1:
                    self.tempInt = self.tempStr.find(",")
                    self.contrlStr1 = self.tempStr[15:self.tempInt]
                    self.contrlStr2 = self.tempStr[self.tempInt + 1:self.tempStr.find("}")]

                    self.contrlStr1 = self.contrlStr1.replace ("_", " ")
                    self.contrlStr2 = self.contrlStr2.replace ("_", " ")

                    self.controllers.append(self.contrlStr1)
                    self.controllers.append(self.contrlStr2)

        return self.controllers

    def retrieveComPort(self):

        #Used to determine previous setting for selected communication port
        self.tempInt = 0
        self.tempStr = ""
        self.portStr = ""
        with open('config.txt', 'r') as file:
                # read a list of lines into data
                self.data = file.readlines()

        for x in range (0, len(self.data)):
            if self.data[x].find("communications") != -1:
                self.tempStr = self.data[x]

                self.tempInt = self.tempStr.find("}")
                self.portStr = self.tempStr[15:self.tempInt]
        return self.portStr

robotGUI = robotGUI()