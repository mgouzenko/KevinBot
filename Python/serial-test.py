import serial
import pygame

pygame.init()

pygame.joystick.init()
j=pygame.joystick.Joystick(0)
j.init()

def writePacket(values):
    s.write('\xFF')
    checksum=0;
    for val in values:
        s.write(chr(val))
        checksum=checksum+val
    s.write(chr(checksum%240))

def readPacket():
    read=[int(s.read().encode('hex'),16) for x in range(4)]
    checksum=sum(read[0:3])%256%240
    if (checksum==read[3]%240):
        return read[0:3]
    else:
        return -1

def joy():
    pygame.event.pump()
    return [j.get_axis(0),j.get_axis(1), j.get_button(0)]

s=serial.Serial(port="COM5", baudrate=38400)
while(1):
    j_read=joy()
    out = [int(j_read[0]*124)+128, int(j_read[1]*124)+128, j_read[2]]
    writePacket(out)
    if (s.inWaiting()>=5 and s.read()=='\xFF'):
        print readPacket()
    pygame.time.wait(20)