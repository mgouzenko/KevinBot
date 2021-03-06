import pygame as pg
import Tkinter as tk
import serial
import controller

class Comm():

    PACKET_START = '\xFF'
    CHECK_MOD = 240

    def __init__(self, parent):
        port=parent.comStr
        self.ser=serial.Serial(port=port, baudrate = 38400, timeout=.05)

    def update(self,buttons, axes):
        #Amir do things here using the js joystick object and controller library.
        #read and write method calls
        self.writePacket(axes, buttons)
        return self.readPacket()

    def scaleaxis(self, axis, center):
        axis *= center
        axis += center
        if(axis > center*2-2):
            axis = center*2-2
        elif(axis < 0):
            axis = 0
        return int(axis)


    def writePacket(self, axesDict, buttonDict):
        y1=self.scaleaxis(axesDict['Y-Axis1'],128)
        y2=self.scaleaxis(axesDict['Y-Axis2'],128)
        x1=self.scaleaxis(axesDict['X-Axis1'],128)
        x2=self.scaleaxis(axesDict['X-Axis2'],128)
        self.ser.write(self.PACKET_START)                                           #bit0 - Packet start
        self.ser.write(chr(y1))                                                     #bit1 - Walking info
        self.ser.write(chr(x1))                                                     #bit2 - Walking info
        self.ser.write(chr(y2))                                                     #bit3 - Turret Info
        self.ser.write(chr(x2))                                                     #bit4 - Turret Info
        indicatorByte = self.makeIndicatorByte(buttonDict)
        self.ser.write(chr(indicatorByte))                                          #bit5 - misc button indicators
        self.ser.write(chr(self.makeCheckSum([y1, y2, x1, x2, indicatorByte])))     #bit6 - checksum

    def makeIndicatorByte(self, buttonDict):
        indicatorByte = 0
        indicatorIndex = 1
        #input = [Filler, Filler, Laser Toggle, Robot Enabled Toggle, Right Hip Pos, Left Hip Pos, Smoothwalk Toggle, Fire]
        roboInput = [0, 0, buttonDict['leftBumper'], buttonDict['startButton'], buttonDict['rightTrigger'], buttonDict['leftTrigger'], buttonDict['xButton'], buttonDict['rightBumper']]

        for n in roboInput:
            indicatorByte += n*indicatorIndex
            indicatorIndex *= 2

        return indicatorByte

    def makeCheckSum(self, vals):
        checkSum = sum(vals)
        checkSum = checkSum % self.CHECK_MOD

        return checkSum

    def readPacket(self):
        if(self.ser.inWaiting>=8 and self.ser.read() == self.PACKET_START):
                #populate input[leftMotorPos, rightMotorPos, turretInfo, turretInfo, batteryInfo, indicatorBits]
                read=[int(self.ser.read().encode('hex'),16) for x in range(7)]
                #get checksum & check it
                checksum=sum(read[0:6])%240
                if (checksum==read[6]):
                    return read[0:6]
                else:
                    return -1
        else:
            return -2

    def stop(self):
        self.ser.close()