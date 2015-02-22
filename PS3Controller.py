'''
***************************************************************************
Kully Kekaula

Description: Methods to create and manage the PS3 controller pane
***************************************************************************
''' 
import pygame, sys, math
from pygame.locals import *
import Tkinter as tk
from Tkinter import Menu, Frame, Toplevel
import tkMessageBox as tkm
import controller

class PS3Controller():
    def __init__(self):
        #Initialize the variables
        self.xAxisVar = tk.StringVar(value = "xAxis is: N/A")
        self.yAxisVar = tk.StringVar(value = "yAxis is: N/A")
        self.aAxisVar = tk.StringVar(value = "aAxis is: N/A")
        self.bAxisVar = tk.StringVar(value = "bAxis is: N/A")

        self.labelFrame = tk.Frame()

        self.buttonLabels=tk.Frame(self.labelFrame,width=130,height=374)
        self.buttonLabels.pack_propagate(0)

        self.xLabel = tk.Label(self.buttonLabels, text=' X ',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER) 

        self.cirLabel = tk.Label(self.buttonLabels, text=' Circle ',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER) 

        self.triLabel = tk.Label(self.buttonLabels, text=' Triangle ',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER) 

        self.squLabel = tk.Label(self.buttonLabels, text=' Square ',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER) 

        self.leftTrigLabel = tk.Label(self.buttonLabels, text='Left Trigger',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER)

        self.rightTrigLabel = tk.Label(self.buttonLabels, text='Right Trigger',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER)

        self.leftBumpLabel = tk.Label(self.buttonLabels, text='Left Bumper',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER)

        self.rightBumpLabel = tk.Label(self.buttonLabels, text='Right Bumper',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER)

        self.selectLabel = tk.Label(self.buttonLabels, text='Select',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER)

        self.startLabel = tk.Label(self.buttonLabels, text='Start',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER)

        self.rightTogLabel = tk.Label(self.buttonLabels, text='Right Toggle',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER)

        self.leftTogLabel = tk.Label(self.buttonLabels, text='Left Toggle',\
            font=("Helvetica", 12), fg='black', bg='red', width = 30, \
            anchor=tk.CENTER)

    def createPS3Pane(self, controllers):

        enableDisableFrame = tk.Frame()

        #Frame partitions (subframes) go here
        enableDisable=tk.Frame(enableDisableFrame,width=129,height=87)
        enableDisable.pack_propagate(0)
        axisLabels=tk.Frame(self.labelFrame,width=130,height=143)
        axisLabels.pack_propagate(0)


        #Initialize buttons
        remote_Label = tk.Label(enableDisable, text='PS3 Controller',\
            font=("Helvetica", 13), fg='black', anchor = tk.CENTER, width = 12)
        remote_Label.pack(side = "top")

        initBut = tk.Button(enableDisable, text ="Enable", \
            command= lambda: self.runController(controllers), width = 15)
        initBut.pack()

        stopBut = tk.Button(enableDisable, text ="Disable", \
            command= lambda: self.stopController(), width = 15)
        stopBut.pack()

        axisTitle = tk.Label(axisLabels, text='Axes',\
            font=("Helvetica", 13), fg='black', width = 40, \
            anchor=tk.CENTER) 

        xAxisLabel = tk.Label(axisLabels, fg="black", \
            textvariable=self.xAxisVar, width=40, font=("Helvetica", 12), \
            anchor=tk.W)

        yAxisLabel = tk.Label(axisLabels, fg="black", \
            textvariable=self.yAxisVar, width=40, font=("Helvetica", 12), \
            anchor=tk.W)

        aAxisLabel = tk.Label(axisLabels, fg="black", \
            textvariable=self.aAxisVar, width=40, font=("Helvetica", 12), \
            anchor=tk.W)

        bAxisLabel = tk.Label(axisLabels, fg="black", \
            textvariable=self.bAxisVar, width=40, font=("Helvetica", 12), \
            anchor=tk.W)

        #Initalize Button Labels
        buttonTitle = tk.Label(self.buttonLabels, text='Buttons',\
            font=("Helvetica", 13), fg='black', width = 40, \
            anchor=tk.CENTER) 

        axisTitle.pack()
        xAxisLabel.pack()
        yAxisLabel.pack()
        aAxisLabel.pack()
        bAxisLabel.pack()
        buttonTitle.pack()
        self.xLabel.pack()
        self.cirLabel.pack()
        self.triLabel.pack()
        self.squLabel.pack()
        self.leftTrigLabel.pack()
        self.rightTrigLabel.pack()
        self.leftBumpLabel.pack()
        self.rightBumpLabel.pack()
        self.rightTogLabel.pack()
        self.leftTogLabel.pack()
        self.selectLabel.pack()
        self.startLabel.pack()

        #Package subframes go here
        axisLabels.pack()
        self.buttonLabels.pack()
        enableDisable.pack()
        enableDisableFrame.pack()
        self.labelFrame.pack()

        if controllers == 1:
            enableDisableFrame.place(x=720, y=42)
            self.labelFrame.place(x=719, y=129)
        else:
            if controllers[0] == 'PS3 PowerA':
                enableDisableFrame.place(x=720, y=42)
                self.labelFrame.place(x=719, y=129)
            elif controllers[1] == 'PS3 PowerA':
                enableDisableFrame.place(x=850, y=42)
                self.labelFrame.place(x=850, y=129)

        axisLabels.config(highlightbackground="black", borderwidth= 5, \
            relief = "ridge")
        self.buttonLabels.config(highlightbackground="black", borderwidth= 5, \
            relief = "ridge")
        enableDisable.config(highlightbackground="black", borderwidth= 5, \
            relief = "ridge")

    def initController(self, controllers):

        pygame.init()

        ### Tells the number of joysticks/error detection
        joystick_count = pygame.joystick.get_count()
        print ("There is ", joystick_count, "joystick/s")
        if joystick_count == 0:
            print ("Error, I did not find any joysticks")
            tkm.showerror("Error", "Please connect a remote controller.")
        else:
            if controllers == 2:
                if joystick_count == 1:
                    tkm.showerror("Error", "Current controller setting is set to two controllers." \
                        " Please connect another controller.")
            #Create one controller object
            my_joystick = pygame.joystick.Joystick(0)
            jsName = my_joystick.get_name
            print(jsName)
            my_joystick.init()
            self.js = my_joystick
            print 'this is working, yay'


    def stopController(self):
        
        self.js.quit()

    def runController(self, controllers):
        
        self.initController(controllers)

        while True:
            pygame.event.pump()
            axes = controller.updateAxes(self.js)
            buttons = controller.updateButtons(self.js)

            self.xAxisVar.set(value="xAxis is: %(xaxis)s" %{'xaxis':str(axes['X-Axis1'])})
            self.yAxisVar.set(value="yAxis is: %(xaxis)s" %{'xaxis':str(axes['Y-Axis1'])})
            self.aAxisVar.set(value="aAxis is: %(xaxis)s" %{'xaxis':str(axes['X-Axis2'])})
            self.bAxisVar.set(value="bAxis is: %(xaxis)s" %{'xaxis':str(axes['Y-Axis2'])})

            if buttons['xButton'] == 1:
                self.xLabel.configure(bg = 'green')
            elif buttons['xButton'] == 0:
                self.xLabel.configure(bg = 'red')

            if buttons['circleButton'] == 1:
                self.cirLabel.configure(bg = 'green')
            elif buttons['circleButton'] == 0:
                self.cirLabel.configure(bg = 'red')

            if buttons['triangleButton'] == 1:
                self.triLabel.configure(bg = 'green')
            elif buttons['triangleButton'] == 0:
                self.triLabel.configure(bg = 'red')

            if buttons['squareButton'] == 1:
                self.squLabel.configure(bg = 'green')
            elif buttons['squareButton'] == 0:
                self.squLabel.configure(bg = 'red')

            if buttons['leftTrigger'] == 1:
                self.leftTrigLabel.configure(bg = 'green')
            elif buttons['leftTrigger'] == 0:
                self.leftTrigLabel.configure(bg = 'red')

            if buttons['rightTrigger'] == 1:
                self.rightTrigLabel.configure(bg = 'green')
            elif buttons['rightTrigger'] == 0:
                self.rightTrigLabel.configure(bg = 'red')

            if buttons['leftBumper'] == 1:
                self.leftBumpLabel.configure(bg = 'green')
            elif buttons['leftBumper'] == 0:
                self.leftBumpLabel.configure(bg = 'red')

            if buttons['rightBumper'] == 1:
                self.rightBumpLabel.configure(bg = 'green')
            elif buttons['rightBumper'] == 0:
                self.rightBumpLabel.configure(bg = 'red')

            if buttons['selectButton'] == 1:
                self.selectLabel.configure(bg = 'green')
            elif buttons['selectButton'] == 0:
                self.selectLabel.configure(bg = 'red')

            if buttons['startButton'] == 1:
                self.startLabel.configure(bg = 'green')
            elif buttons['startButton'] == 0:
                self.startLabel.configure(bg = 'red')

            if buttons['rightToggle'] == 1:
                self.rightTogLabel.configure(bg = 'green')
            elif buttons['rightToggle'] == 0:
                self.rightTogLabel.configure(bg = 'red')

            if buttons['leftToggle'] == 1:
                self.leftTogLabel.configure(bg = 'green')
            elif buttons['leftToggle'] == 0:
                self.leftTogLabel.configure(bg = 'red')

            self.labelFrame.update()

            pygame.time.wait(100)