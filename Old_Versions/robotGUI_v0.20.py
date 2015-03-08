'''
***************************************************************************
Kully Kekaula

Description: A GUI to run the Mech Warfare robot code.
***************************************************************************
''' 
import pygame, sys, math
from pygame.locals import *
import Tkinter as tk
import tkMessageBox as tkm

class robotGUI():
    def __init__(self):

        #Initialize the master window 
        self.main = tk.Tk()
        self.main.title("Robot Interface v0.2")
        self.main.geometry("850x600+300+300")
        self.main.resizable(width=False, height=False)

        #Initialize frame sections of the window
        self.titleFrame = tk.Frame()
        self.topFrame = tk.Frame()
        self.labelFrame = tk.Frame()

        #Frame partitions (subframes) go here
        self.axisLabels=tk.Frame(self.labelFrame,width=130,height=124)
        self.axisLabels.pack_propagate(0)
        self.buttonLabels=tk.Frame(self.labelFrame,width=130,height=360)
        self.buttonLabels.pack_propagate(0)

        #Initialize the variables
        self.xAxisVar = tk.StringVar(value = "xAxis is: N/A")
        self.yAxisVar = tk.StringVar(value = "yAxis is: N/A")
        self.aAxisVar = tk.StringVar(value = "aAxis is: N/A")
        self.bAxisVar = tk.StringVar(value = "bAxis is: N/A")
        self.xColor = tk.StringVar()
        self.xColor.set("red")

        #Initialize buttons
        self.initBut = tk.Button(self.topFrame, text ="Run Remote Controller", \
            command = self.runController)
        self.initBut.pack()

        self.stopBut = tk.Button(self.topFrame, text ="Stop Remote Controller", \
            command = self.stopController)
        self.stopBut.pack()

        #Initalize Axis Labels
        self.title_label = tk.Label(self.titleFrame, text='Mech Warfare GUI',\
            font=("Helvetica", 20),bg='blue',fg='white', width = 53) 

        self.axisTitle = tk.Label(self.axisLabels, text='     Axes',\
            font=("Helvetica", 13), fg='black', width = 40, \
            anchor=tk.W) 

        self.xAxisLabel = tk.Label(self.axisLabels, fg="black", \
            textvariable=self.xAxisVar, width=40, font=("Helvetica", 12), \
            anchor=tk.W)

        self.yAxisLabel = tk.Label(self.axisLabels, fg="black", \
            textvariable=self.yAxisVar, width=40, font=("Helvetica", 12), \
            anchor=tk.W)

        self.aAxisLabel = tk.Label(self.axisLabels, fg="black", \
            textvariable=self.aAxisVar, width=40, font=("Helvetica", 12), \
            anchor=tk.W)

        self.bAxisLabel = tk.Label(self.axisLabels, fg="black", \
            textvariable=self.bAxisVar, width=40, font=("Helvetica", 12), \
            anchor=tk.W)

        #Initalize Button Labels
        self.buttonTitle = tk.Label(self.buttonLabels, text='   Buttons',\
            font=("Helvetica", 13), fg='black', width = 40, \
            anchor=tk.W) 

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

        self.title_label.pack()
        self.axisTitle.pack()
        self.xAxisLabel.pack()
        self.yAxisLabel.pack()
        self.aAxisLabel.pack()
        self.bAxisLabel.pack()
        self.buttonTitle.pack()
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
        self.axisLabels.pack(side='top')
        self.buttonLabels.pack(side='bottom')

        #Package frames and create the window
        self.titleFrame.pack()
        self.topFrame.pack()
        self.labelFrame.pack()

        self.topFrame.place(x=5, y=45)
        self.labelFrame.place(x=5, y=100)

        tk.mainloop()

    def initController(self):

        pygame.init()

        ### Tells the number of joysticks/error detection
        joystick_count = pygame.joystick.get_count()
        print ("There is ", joystick_count, "joystick/s")
        if joystick_count == 0:
            print ("Error, I did not find any joysticks")
            tkm.showerror("Error", "Please connect a remote controller.")
        else:
            my_joystick = pygame.joystick.Joystick(0)
        my_joystick.init()
        self.js = my_joystick

    def stopController(self):

        self.js.quit()

    def runController(self):
        self.initController()
        while True:
            pygame.event.pump()
            axes = self.updateAxes()
            buttons = self.updateButtons()

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

    def updateAxes(self):

        controllerDict = {'X-Axis1': 0, 'Y-Axis2': 0, 'X-Axis2': 0, 'Y-Axis2': 0};

        xAxis = self.js.get_axis(0) 
        yAxis = self.js.get_axis(1) * -1
        aAxis = self.js.get_axis(2)
        bAxis = self.js.get_axis(3) * -1

        if xAxis < 0.1 and xAxis > -0.1:
            xAxis = 0
        if yAxis < 0.1 and yAxis > -0.1:
            yAxis = 0
        if aAxis < 0.1 and aAxis > -0.1:
            aAxis = 0
        if bAxis < 0.1 and bAxis > -0.1:
            bAxis = 0

        xAxis = math.ceil(xAxis*10000)/10000
        yAxis = math.ceil(yAxis*10000)/10000
        aAxis = math.ceil(aAxis*10000)/10000
        bAxis = math.ceil(bAxis*10000)/10000

        print 'X-Axis 1: ' + str(xAxis) + '  Y-Axis 1: ' + str(yAxis)
        print 'X-Axis 2: ' + str(aAxis) + '  Y-Axis 2: ' + str(bAxis)

        controllerDict['X-Axis1'] = xAxis;
        controllerDict['Y-Axis1'] = yAxis;
        controllerDict['X-Axis2'] = aAxis;
        controllerDict['Y-Axis2'] = bAxis;

        print "dict['X-Axis1']: ", controllerDict['X-Axis1'];

        return controllerDict

    def updateButtons(self):

        buttonDict = {'xButton': 0, 'circleButton': 0, 'triangleButton': 0, 'squareButton': 0,
        'leftBumper': 0, 'rightBumper': 0, 'leftTrigger': 0, 'rightTrigger': 0,
        'selectButton': 0, 'startButton': 0, 'leftToggle': 0, 'rightToggle': 0,};

        xButton = self.js.get_button(1)
        circleButton = self.js.get_button(2)
        triangleButton = self.js.get_button(3)
        squareButton = self.js.get_button(0)
        leftBumper = self.js.get_button(4)
        rightBumper = self.js.get_button(5)
        leftTrigger = self.js.get_button(6)
        rightTrigger = self.js.get_button(7)
        selectButton = self.js.get_button(8)
        startButton = self.js.get_button(9)
        leftToggle = self.js.get_button(10)
        rightToggle = self.js.get_button(11)

        print 'X Button is: ' + str(xButton) + '  Circle Button is: ' + str(circleButton)
        print 'Triangle Button is: ' + str(triangleButton) + '  Square Button is: ' + str(squareButton)
        print 'Left Bumper is: ' + str(leftBumper) + '  Right Bumper is: ' + str(rightBumper)
        print 'Left Trigger is: ' + str(leftTrigger) + '  Right Trigger is: ' + str(rightTrigger)
        print 'Select Button is: ' + str(selectButton) + '  Start Button is: ' + str(startButton)
        print 'Left Toggle is: ' + str(leftToggle) + '  Right Toggle is: ' + str(rightToggle)

        buttonDict['xButton'] = xButton;
        buttonDict['circleButton'] = circleButton;
        buttonDict['triangleButton'] = triangleButton;
        buttonDict['squareButton'] = squareButton;
        buttonDict['leftBumper'] = leftBumper;
        buttonDict['rightBumper'] = rightBumper;
        buttonDict['leftTrigger'] = leftTrigger;
        buttonDict['rightTrigger'] = rightTrigger;
        buttonDict['selectButton'] = selectButton;
        buttonDict['startButton'] = startButton;
        buttonDict['leftToggle'] = leftToggle;
        buttonDict['rightToggle'] = rightToggle;

        print "dict['xButton']: ", buttonDict['xButton'];

        return buttonDict

robotGUI = robotGUI()