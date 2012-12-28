#-------------------------------------------------------------------------------
# Name:        CheerLights
# Purpose:     uses the thingspeak api to read the current color from
#              the cheerlights api, then sends a command to an attached
#              Arduino which controls three color channels of LED lighting
#
# Author:      John
#
# Created:     16/12/2012
# Copyright:   (c) John 2012
#-------------------------------------------------------------------------------

import httplib
import serial
import binascii
import time

class getColor:

    def __init__(self):
        self.connection = httplib.HTTPConnection('api.thingspeak.com')
        self.color = ''

    def lookup(self):
        self.connection.request('GET','/channels/1417/field/1/last.txt')
        self.color = self.connection.getresponse().read()
        return self.color

class translateColor:
    _colorSpace = dict(red=['FF','00','00'],
                       green=['00','FF','00'],
                       blue=['00','00','FF'],
                       cyan=['00','FF','FF'],
                       white=['FF','FF','FF'],
                       warmwhite=['FF','F0','F0'],
                       purple=['7F','00','FF'],
                       magenta=['FF','00','FF'],
                       yellow=['CF','FF','00'],
                       orange=['FF','7F','00'])

    def translate(self, color, default):
        return self._colorSpace.get(color, default)

class protocol:

    _header = ['AA', '55', 'AA']
    _serialLink = serial.Serial()

    def __init__(self):
        self._serialLink.port = 3
        self._serialLink.baudrate = 9600
        self._serialLink.parity = 'N'
        self._serialLink.bytesize = 8
        self._serialLink.stopbits = 1
        self._serialLink.open()

    def write(self, data):
        for char in self._header:
            self._serialLink.write(binascii.unhexlify(char))
        for char in data:
            self._serialLink.write(binascii.unhexlify(char))

class delay:

    def sleep(self, length):
        startTime = time.clock()
        while ((time.clock() - startTime) < length):
            pass

def main():
    oldcommand = [0, 0, 0]
    cheerlights = getColor()
    toRGB = translateColor()
    Arduino = protocol()
    timer = delay()

    while True:
        newcolor = cheerlights.lookup()
        print newcolor
        command = toRGB.translate(newcolor, oldcommand)
        oldcommand = command
        Arduino.write(command)
        timer.sleep(20.0)

if __name__ == '__main__':
    main()
