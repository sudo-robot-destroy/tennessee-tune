#!/usr/bin/env python


import serial, time

serialPort = "socket://127.0.0.1:5762"
ser = serial.serial_for_url(serialPort, do_not_open = True)

ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 0
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 2
"""Time to wait until the board becomes operational"""
wakeup = 2
try:
    ser.open()
    print "Waking up board on " + ser.port + "..."
    for i in range(1, wakeup):
        print wakeup - i
        time.sleep(1)
except Exception, error:
    print "\n\nError opening " + ser.port + " port.\n" + str(error) + "\n\n"



"""
from MultiWii import MultiWii

serialPort = "socket://127.0.0.1:5762"
mw = MultiWii()
connect = mw.connect(serialPort, 115200)

if connect:
    print "MSP connection made to " + serialPort
else:
    print "MSP connection failed. "

"""
"""
from pymultiwii import MultiWii
import time
import struct

serialPort = "socket://127.0.0.1:5762"
board = MultiWii(serialPort)
time.sleep(.5)
board.arm()
while True:
    print board.getData(MultiWii.ATTITUDE)
    #  SET_RAW_RC is like this ROLL/PITCH/THROTTLE/YAW/AUX1/AUX2/AUX3/AUX4
    #  Range is 1000 to 2000
    data = [1500, 1500, 1500, 1500, 2000, 2000, 2000, 2000]
    #set_raw_rc_packet = struct.pack("8H", 1500, 1500, 1500, 2000, 2000, 2000, 2000, 2000)
    board.sendCMD(16, MultiWii.SET_RAW_RC, data)
    time.sleep(.1)
"""


"""
try:
    #board.arm()
    #board.SET_RAW_RC()
    print "Calibrate Accel"
    board.sendCMD(0, MultiWii.ACC_CALIBRATION, [])
    time.sleep(1)
    print "Calibrate Mag"
    board.sendCMD(0, MultiWii.MAG_CALIBRATION, [])
    time.sleep(1)
    print "send motor commands"
    data = [1500, 1500, 2000, 2000]
    board.sendCMD(8, MultiWii.SET_RAW_RC, data)
    time.sleep(3)
    #board.disarm()

except Exception, error:
    print "Error on Main: "+str(error)

"""

"""
import serial
serPort = "socket://127.0.0.1:5761"
ser = serial.serial_for_url(serPort)
ser.port = serPort
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.timeout = 0
ser.xonxoff = False
ser.rtscts = False
ser.dsrdtr = False
ser.writeTimeout = 2


ser.open()
"""
"""
#!/usr/bin/env python

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2017 Altax.net"

__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

from pymultiwii import MultiWii
from sys import stdout

if __name__ == "__main__":

    #board = MultiWii("/dev/ttyUSB0")
    board = MultiWii("socket://127.0.0.1:5761")
    try:
        while True:
            board.getData(MultiWii.ATTITUDE)
            #print board.attitude #uncomment for regular printing

            # Fancy printing (might not work on windows...)
            message = "angx = {:+.2f} \t angy = {:+.2f} \t heading = {:+.2f} \t elapsed = {:+.4f} \t".format(float(board.attitude['angx']),float(board.attitude['angy']),float(board.attitude['heading']),float(board.attitude['elapsed']))
            stdout.write("\r%s" % message )
            stdout.flush()
            # End of fancy printing
    except Exception,error:
        print "Error on Main: "+str(error)
"""
