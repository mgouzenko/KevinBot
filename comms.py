import pygame as pg
import Tkinter as tk
import controller

def init(gui):
    pg.init()
    js = pg.joystick.Joystick(0)
    js.init()
    update(js, gui)

def update(js, gui):
    #Amir do things here using the js joystick object and controller library.
    #read and write method calls
    gui.after(100, update(js,gui))