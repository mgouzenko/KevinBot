import serial
import pygame

pygame.init()

joystick_count = pygame.joystick.get_count()
print ("There is ", joystick_count, "joystick/s")
if joystick_count == 0:
    print ("Error, I did not find any joysticks")
else:
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()

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

    xAxis = my_joystick.get_axis(0) 
    yAxis = my_joystick.get_axis(1) * -1
    aAxis = my_joystick.get_axis(2)
    bAxis = my_joystick.get_axis(3) * -1

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

    return [xAxis, yAxis, aAxis, bAxis, j.get_button(0), j.get_button(1), \
    j.get_button(2),j.get_button(3),j.get_button(4)]

s=serial.Serial(port="COM4", baudrate=38400)
while(1):
    j_read=joy()
    out = [int(j_read[0]*124)+128, int(j_read[1]*124)+128, \
    int(j_read[2]*124)+128, int(j_read[3]*124)+128, j_read[4], j_read[5], \
    j_read[6], j_read[7], j_read[8]]
    writePacket(out)
    if (s.inWaiting()>=5 and s.read()=='\xFF'):
        print readPacket()
    pygame.time.wait(20)