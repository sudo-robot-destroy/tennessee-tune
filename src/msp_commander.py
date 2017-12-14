#!/usr/bin/env python

from pymultiwii import MultiWii
import time

serialPort = "socket://127.0.0.1:5761"
board = MultiWii(serialPort)

while True:
    print board.getData(MultiWii.ATTITUDE)
    data = [1500, 1500, 2000, 2000,0,0,0,0]
    board.sendCMD(16, MultiWii.SET_RAW_RC, data)
    time.sleep(.5)
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
