import serial
import re
from enum import Enum
import codecs


# SMS receiver using SIM900 GSM Module

class SmsModem():

    def __init__(self, serial_device):
        self.ser = serial_device
        self.owing = None 
        if serial_device is not None:
            self.ser.write(b'ATE0+CMGDA="DEL ALL"\r')    # echo off, clear all messages on SIM900 
            self.owing = Indication.OK
        
    def writeline(self, text):
        text = text + '\r'
        b = bytearray(text,"ascii")
        self.ser.write(b)

    def receive(self):
        line = self.ser.readline()
        return line.decode('utf-8')


class Indication(Enum):
    UNKNOWN = 0
    RX_SMS = 1
    TEXT = 2
    CONNECTED = 3
    OK = 4
    ERROR = 5
    POWEROFF = 6
    

def message_type( message ):
    if message != "":
        m = re.match(r'\+(C\w+):(.+)', message)
        if m:
                if m.group(1) == "CMTI":
                    n = re.search( "(\d+)", m.group(2) )
                    return Indication.RX_SMS, n.group(1)
                elif m.group(1) == "CMGR":
                    sections = re.findall(r'"(.*?)"', m.group(2))
                    return Indication.TEXT, sections 
                    
        m = re.match("OK", message)
        if m:
            return Indication.OK, None
        
        m = re.match("ERROR", message)
        if m:
            return Indication.ERROR, None
        
        m = re.match("NORMAL POWER DOWN", message)
        if m:
            return Indication.POWEROFF, None

    return Indication.UNKNOWN, message



def main():
    ser = serial.Serial(
        port='com3',    # for Windows ( on Linux it will be something like /dev/ttyS0 )
        baudrate=9600,
        timeout=1 )

    sms = SmsModem(ser)

    text_owing = False
    ok_owing = False

    while True:
        line = sms.receive()
        if len(line)>0:
            indication, param = message_type(line)
            if  indication == Indication.RX_SMS:
                print("Receive SMS, # {}".format(param))
                sms.writeline("AT+CMGR={}".format(param))
            elif indication == Indication.TEXT:
                text_owing = True
                header_sections = param
            elif indication == Indication.UNKNOWN and text_owing:
                print("SMS => {} : {}".format(header_sections,param))
                text_owing = False
                ok_owing = True
                header_sections = None
            elif indication == Indication.OK and ok_owing:
                ok_owing = False
                print("Operation completed")
        

if __name__ == "__main__":
    main()

