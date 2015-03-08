import pygame as pg
import Tkinter as tk
import serial
import controller

PACKET_START = 255
CHECK_MOD = 240

def init(gui, buttons, axes):

    update(js, gui, buttons, axes)

def update(js, gui, buttons, axes):
    #Amir do things here using the js joystick object and controller library.
    #read and write method calls
    writePacket(axes, buttons)
    gui.after(100, update(js,gui,buttons, axes))

def scaleaxis(axis, center):
    axis *= center
    axis += center
    if(axis > center*2-2):
        axis = center*2-2
    elif(axis < 0):
        axis = 0
    return axis


def writePacket(axesDict, buttonDict):
    Serial.write(PACKET_START)                                                              #bit0 - Packet start
    Serial.write(scaleaxis(axesDict['Y-Axis1'], 128))                                       #bit1 - Walking info
    Serial.write(scaleaxis(axesDict['X-Axis1'], 128))                                       #bit2 - Walking info
    Serial.write(scaleaxis(axesDict['Y-Axis2'], 128))                                       #bit3 - Turret Info
    Serial.write(scaleaxis(axesDict['X-Axis2'], 128))                                       #bit4 - Turret Info
    indicatorByte = makeIndicatorByte(ButtonDict)
    Serial.write(indicatorByte)                                                             #bit5 - misc button indicators
    Serial.write(makeCheckSum(axesDict['Y-Axis1'], axesDict['Y-Axis2'], indicatorByte))     #bit6 - checksum

def makeIndicatorByte(ButtonDict):
    indicatorByte = 0
    indicatorIndex = 1
    #input = [Filler, Filler, Laser Toggle, Robot Enabled Toggle, Right Hip Pos, Left Hip Pos, Smoothwalk Toggle, Fire]
    roboInput = [0, 0, buttonDict['leftTrigger'], buttonDict['startButton'], buttonDict['rightBumper'], buttonDict['leftBumper'], buttonDict['xButton'], buttonDict['rightTrigger']]

    for n in roboInput:
        indicatorByte += roboInput*indicatorIndex
        indicatorIndex *= 2

    return indicatorByte

def makeCheckSum(Axis1, Axis2, indicatorByte):
    checkSum = Axis1 + Axis2 + indicatorByte
    checkSum = checkSum % CHECK_MOD

    return checkSum

def readPacket():
    roboOutput = []
    if(Serial.read() == PACKET_START):
        #populate input[leftMotorPos, rightMotorPos, turretInfo, turretInfo, batteryInfo, indicatorBits]
        for i in range(6):
            roboOutput.append(Serial.read())

        #get checksum & check it
        checksum = Serial.read()
        test = 0;
        for n in roboOutput:
            test += n
        test %= CHECK_MOD
        if(checksum == test):
            return roboOutput
        else:
            return -1