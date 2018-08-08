import time
import os


# =====================================
# Convenient function
# =====================================

def broadcastMsg(msg):
    server4left.send(msg)
    server4right.send(msg)
    server4centre.send(msg)
def createFolder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
def limitValue(n, minn, maxn):
    return max(min(maxn, n), minn)

# =====================================
# SERVO & SERIES
# =====================================
#  Polotu
import maestro
servo = maestro.Controller()
import maestro
servo = maestro.Controller('/dev/ttyACM0')
servo.setRange(0, 1000 * 4, 2000 * 4)
servo.setSpeed(0, 45)
servo.setRange(1, 1000 * 4, 2500 * 4)
#  Arduino
import serial
ser = serial.Serial(port='/dev/ttyTHS2', baudrate=115200)  # open serial port
ser.flushInput()
ser.flushOutput()
# =====================================
# Global setting
# =====================================

record_FPS = 10
frequence = 1 / record_FPS
speed_range = [1250, 1750]
steer_range = [976, 1976]
camera_left = '/media/nvidia/Files/Left/'
camera_right = '/media/nvidia/Files/Right/'
camera_centre = '/media/nvidia/Files/Centre/'
createFolder(camera_left)
createFolder(camera_right)
createFolder(camera_centre)
# =====================================
# CSV
# =====================================
import csv
f = open('/media/nvidia/Files/data_c.csv', 'w')
fnames = ['name', 'steering', 'speed', 'category']
writer = csv.DictWriter(f, fieldnames=fnames)
writer.writeheader()
# =====================================
# Init value
# =====================================

start_time = time.time()
end_time = time.time()
iter_num = 0
ch3_pre = 1000
flag=0
situation=0

# =====================================
# Network Configuration
# =====================================
from multiprocessing.connection import Listener
print('Left----centre----Right')
print('Waiting for left')
server4left = Listener(('', 25000), authkey=b'peekaboo').accept()
print('Connected to Left')
print('Waiting for Right')
server4right = Listener(('', 25001), authkey=b'peekaboo').accept()
print('Connected to Right')
print('Waiting for Centre')
server4centre = Listener(('', 25002), authkey=b'peekaboo').accept()
print('Connected to Centre')
ch1, ch2, ch3=1476,1500,976
try:
    while True:
        # ======  Get command  ====== #
        try:
            command =ser.readline().decode('utf-8').rstrip().split('x')
            ch1, ch2, ch3 = int(command[0].strip('\x00')), int(command[1].strip('\x00')), int(command[2].strip('\x00'))
        except UnicodeDecodeError:
            print('hehe')
            pass
            
        dis=ch3-ch3_pre
        if dis>500 and situation==0:situation=1
        elif dis<-500 and situation==1:situation,flag=0,0

        end_time = time.time()
        if end_time-start_time>0.1:
            if situation==1 and flag==0:
                flag=1
                print('enter')
                iter_num = iter_num + 1
                broadcastMsg('Iter:' + str(iter_num))
                time.sleep(0.1)
            if ch3_pre > 1500 and flag==1:
                data = {'name': iter_num,'steering': ch1,'speed': ch2,'category': 0}
                broadcastMsg('Save')
                writer.writerow(data)
            else:
                broadcastMsg('Waiting')
            start_time=time.time()
        # ======  Send command  ====== #
        ch1 = limitValue(ch1, steer_range[0], steer_range[1])
        ch2 = limitValue(ch2, speed_range[0], speed_range[1])
        servo.setTarget(0, ch1 * 4)  #set servo to move to centre position
        servo.setTarget(1, ch2 * 4)  #set servo to move to centre position
        # ============================ #
        ch3_pre = ch3
finally:
    servo.setTarget(0, 1476 * 4)  #set servo to move to centre position
    servo.setTarget(1, 1500 * 4)  #set servo to move to centre position
    f.close()
    servo.close()
    ser.close()
    print('finished')
