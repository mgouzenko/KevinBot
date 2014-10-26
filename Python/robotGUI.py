'''
***************************************************************************
Kully Kekaula-Basque
knk2116
Description: A GUI to run the Mech Warfare robot code.
***************************************************************************
''' 
import pygame, sys, math
from pygame.locals import *
import Tkinter as tk
import tkMessageBox as tkm

class robotGUI():
    def __init__(self):
        
        pygame.init()

        ### Tells the number of joysticks/error detection
        joystick_count = pygame.joystick.get_count()
        print ("There is ", joystick_count, "joystick/s")
        if joystick_count == 0:
            print ("Error, I did not find any joysticks")
        else:
            my_joystick = pygame.joystick.Joystick(0)
        
        my_joystick.init()
        self.js = my_joystick
        window = tk.Tk()
        window.title("Robot GUI")
        window.geometry("300x280+300+300")

        window.labelFrame = tk.Frame()
        
        #Create three levels of bottom frame and turn of their propagation.
        window.leftLabels = tk.Frame(window.labelFrame, width=200, height=200)
        window.leftLabels.pack_propagate(0)
        window.leftLabels.pack()

        B = tk.Button(window, text ="Run Remote Controller", command = self.runController())
        B.pack()

        xAxisLabel = tk.Label(window.labelFrame, fg="black", text="xAxis is: ")
        xAxisLabel.pack()
        yAxisLabel = tk.Label(window.labelFrame, fg="black", text="yAxis is: ")
        yAxisLabel.pack()
        aAxisLabel = tk.Label(window.labelFrame, fg="black", text="aAxis is: ")
        aAxisLabel.pack()
        bAxisLabel = tk.Label(window.labelFrame, fg="black", text="bAxis is: ")
        bAxisLabel.pack()

        window.mainloop()

    def runController(self):
        while True:
            pygame.event.pump()
            axes = self.updateAxes()

            xAxisLabel.config(text="xAxis is: %(xaxis)s" %{'xaxis':str(axes['X-Axis1'])})
            yAxisLabel.config(text="yAxis is: %(yaxis)s" %{'yaxis':str(axes['Y-Axis1'])})
            aAxisLabel.config(text="aAxis is: %(aaxis)s" %{'aaxis':str(axes['X-Axis2'])})
            bAxisLabel.config(text="bAxis is: %(baxis)s" %{'baxis':str(axes['Y-Axis2'])})

            window.update()

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

code = robotGUI()