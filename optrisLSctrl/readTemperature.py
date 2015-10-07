#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
Created on Oct 6, 2015-8:29:14 PM

@author: Ling Wang<LingWangNeuralEng@gmail.com>
'''
import time, serial
#SERIAL_INTERFACE_PARAMs
class SERIAL_INTERFACE_PARAMs(object):
    models = ['OPTRIS MSpro', 'OPTRIS LS']
    baudRate = 115200
    byteSize = serial.EIGHTBITS
    stopBits = serial.STOPBITS_ONE
    parity = serial.PARITY_NONE
    flowControl = None # for some devices it can be XON/XOFF or other
    xonxoff = False #disable software flow control
    rtscts = False #disable hardware (RTS/CTS) flow control
    dsrdtr = False #disable hardware (DSR/DTR) flow control
    writeTimeout = 1. # default is to wait 1 sec.
    readTimeout = 1. # default is to wait 1 sec. None for block read, 0 for non-block read, x>0 for timeout block read
    
    def __init__(self, writeTimeout = 1., readTimeout = 1., *args, **kwargs):
        self.writeTimeout = writeTimeout
        self.readTimeout = readTimeout
        self.bitRate = self.baudRate # because serial port is 1-bit baud
        self.byteRate = self.bitRate/8.
        self.timePerByte = 1./self.byteRate
        object.__init__(self, *args, **kwargs)
        


def initSerialConnection(portName, portParams = SERIAL_INTERFACE_PARAMs()):
    
    ser = serial.Serial(port = portName, baudrate = portParams.baudRate, parity = portParams.parity, stopbits = portParams.stopBits, bytesize = portParams.byteSize)
#     ser.open() #the serial port is automatically opened when it is explicitly defined as you have done with ser
    if not ser.isOpen():
        raise IOError("I cannot open serial port %s"%(portName))
    else:
        ser.flushInput() #flush input buffer, discarding all its contents
        ser.flushOutput()#flush output buffer, aborting current output and discard all that is in buffer
        
        
    return ser

import optrisLSCMDlist
from checksum import checkData

def get_value(ser, cmd_obj, dispStr, debug = False):
    
    ser.write(cmd_obj.cmd_cs)
    print dispStr,
    data = ser.read(size = cmd_obj.data_size_cs)
    if not checkData(bytearray(data), debug = debug):
        return None
    data = data[:cmd_obj.data_size]
    print data
    return data

    
def get_model_code(ser, debug = False):
    return get_value(ser, optrisLSCMDlist.device.model_code, "model code is ", debug)

def get_general_status(ser, debug = False):
    return get_value(ser, optrisLSCMDlist.data.status_general, "general status is ", debug)

import struct
def get_Float_T(data, bytePackType):
    
    return (struct.unpack(bytePackType, data) - 1000.)/10
    
    
def lazyRead_IRtemperature(ser, debug = False):
    """
    get one T_obj data
    """
    get_model_code(ser, debug)
    get_general_status(ser, debug)
    ser.write(optrisLSCMDlist.data.T_obj.cmd_cs)
    print "T_obj is ",
    data = ser.read(size = optrisLSCMDlist.data.T_obj.data_size_cs)
    if not checkData(bytearray(data), debug = debug):
        return None
    data = data[:optrisLSCMDlist.data.T_obj.data_size]
    _T_obj = get_Float_T(data, optrisLSCMDlist.data.T_obj.bytePackType)
    print _T_obj
    return _T_obj

def main():
    import sys
    portName = sys.argv[1]
    readTimeout = sys.argv[2]
    writeTimeout = sys.argv[3]
    N_points = sys.argv[4]
    
    readTimeout = float(readTimeout)
    writeTimeout = float(writeTimeout)
    N_points = int(N_points)
    
    portParams = SERIAL_INTERFACE_PARAMs(writeTimeout, readTimeout)
    
    ser = initSerialConnection(portName, portParams)
    try:
        if N_points >0:
            for _i in xrange(0, N_points):
                
                lazyRead_IRtemperature(ser, debug = True)
        else:
            while True:
                lazyRead_IRtemperature(ser, debug = True)
                time.sleep(1./10)
    except (KeyboardInterrupt, SystemExit):
        ser.close()
        print "Done!"
    except:
        ser.close()
        import traceback
        traceback.print_exc(file = sys.stderr)
        
    

if __name__ == '__main__':
    main()
    