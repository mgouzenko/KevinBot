import pygame as pg
import Tkinter as tk
import controller

def init(gui, buttons, axes):

    update(js, gui)

def update(js, gui):
    #Amir do things here using the js joystick object and controller library.
    #read and write method calls
    gui.after(100, update(js,gui))