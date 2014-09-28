import pygame as pg
import sys
import serial

'''
Event types
    7 - Axes motion
        Axis 2: right
        Axis 3

'''

pg.init()
size = [500, 700]
screen = pg.display.set_mode(size)
pg.display.set_caption("Kevin")
done = False
clock = pg.time.Clock()
joystick = pg.joystick.Joystick(0)
joystick.init()
while True:
    axis1 = joystick.get_axis(1)
    if abs(axis1)>.1:
        print axis1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()


