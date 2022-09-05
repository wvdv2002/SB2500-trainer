import pyvesc
from pyvesc import *
import serial
import serial.tools.list_ports
import binascii
import threading
import time
#do something
import socket


class ControllerCommunicationThread(threading.Thread):
    def __init__(self,port,baudrate):
        self.setComPort('COM0')
        self.baudrate = baudrate
        self.count = 0
        self.doSerial = False
        self.doTcp = False
        self.port = 0;
        threading.Thread.__init__(self)

    def run(self):
        while 1:
            if self.isConnected():
                if(self.doSerial):
                    self.ser.write(0)
                self.serialCommunication()
            else:
               time.sleep(0.2)


    def setCallback(self,cb):
        self.cb = cb

    def setComPort(self,port):
        self.port = port

    def connect(self):
        if(self.port):
            print('Connecting with: ' + self.port + ' baud:' + str(self.baudrate))
            self.ser = serial.Serial(self.port, self.baudrate, timeout=0.2)
            self.doSerial = True
            if self.isConnected():
                print('Made serial connection')
            else:
                self.doSerial = False
        else:
            print('Select com port first')

    def tcpConnect(self,aPort):
        self.port = aPort
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(self.socket)
        self.socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print(self.socket)
        print(self.socket.connect(('127.0.0.1',aPort)))
        self.doTcp = True

    def isSerial(self):
        return self.doSerial

    def isConnected(self):
        isOpen = False
        if (self.doTcp):
            isOpen = True
        if(self.doSerial):
            try:
                isOpen = self.ser.isOpen()
            except AttributeError:
                isOpen = False
        return isOpen

    def stopSerial(self):
        self.doSerial = False
        if(self.ser):
            self.ser.close()

    def setCommandReceivedCallback(self,cb):
        self.cb = cb

    def sendCommand(self,command):
        self.lastCommand = command
        data = pyvesc.encode_request(command)
        print(str(self.count) + ' ' + str(len(data)) + ' ' + str(binascii.hexlify(data)))
        self.count = self.count+1
        if(self.doSerial):
            self.ser.write(data)
        if(self.doTcp):
            self.socket.sendall(data)

    def sendSetCommand(self,command):
        self.lastCommand = command
        data = pyvesc.encode(command)
        print(str(self.count) + ' ' + str(len(data)) + ' ' + str(binascii.hexlify(data)))
        self.count = self.count+1
        if(self.doSerial):
            self.ser.write(data)
        if(self.doTcp):
            self.socket.sendall(data)


    def serialCommunication(self):
        while self.doSerial:
            rec_data = bytearray()
            st = time.time()
            while time.time() - st < 0.1:
                # Check if there is enough data back for a measurement
                if (self.ser.in_waiting > 0):
                    st = time.time()
                rec_data = rec_data + self.ser.read()
                lastRecLen = len(rec_data)
            if(len(rec_data)):
                print("data: " + str(binascii.hexlify(rec_data)))
            while len(rec_data) > 0:
                consumed = 0
                try:
                    (response, consumed) = pyvesc.decode(bytes(rec_data))
                except KeyError:
                    pass

                rec_data = rec_data[consumed:]
                recLen = len(rec_data)
                if (recLen == lastRecLen):  # if no packages can be decoded.
                    rec_data = []
                else:
                    lastRecLen = recLen
                if(response):
                    try:
                     self.cb(response)
                    except AttributeError:
                        pass
        while self.doTcp:
            rec_data = self.socket.recv(1024)
            if rec_data == b'':
                print("Connection Broken")
#                time.sleep(0.2)
                self.doTcp = False
                break
            consumed = 0
            print("data: " + str(binascii.hexlify(rec_data)))
            lastRecLen = len(rec_data)
            while len(rec_data) > 0:
                try:
                    (response, consumed) = pyvesc.decode(bytes(rec_data))
                except KeyError:
                    pass
                print("received %i %i %i" % (consumed,len(rec_data),lastRecLen))

                rec_data = rec_data[consumed:]
                recLen = len(rec_data)
                if ((recLen == lastRecLen) or (recLen == 1)):  # if no packages can be decoded.
                    rec_data = []
                else:
                    lastRecLen = recLen
                if (response):
                    try:
                        self.cb(response)
                    except AttributeError:
                        pass



def listPorts():
    return serial.tools.list_ports.comports()



if __name__ == "__main__":
    serialCommunication('COM16',115200)