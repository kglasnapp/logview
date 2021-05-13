import time
from datetime import datetime
import max7219.led as led
#     print("Ensure that self._spi.max_speed_hz = 1000000 is set in led.py")

print("Imported Display - OK")

class Display:
    # create seven segment device

    def __init__(self):
        print("Init Display")
        self.device = led.sevensegment(cascaded=1)
          
    def clock(self, deviceId):
        self.message(deviceId, time.strftime("%H_%M_%S"))
        
    def date(self, deviceId):
        self.message(deviceId, time.strftime("%m-%d-%y"))
        
    # show pipeline result on the display
    def showResult(self, pipeline):
        self.showFloat(0, 1, pipeline.angle)
        self.showInt(0, 5, pipeline.contours)

    def showNoData(self):
        self.message("--------")
                               
    def showFloat(self, id, position, number):
        s = '{: 3.1f}'.format(number)
        if(len(s) <= 4):
            s += ' '
        #print('|' + s  + '|')
        self.showNumber(id, position, s, 4)
                                                    
    def showInt(self, id, position, number):
        self.showNumber(id,position,'{:4d}'.format(number), 4)
    
    def showNumber(self, id, position, message, length):
        for i in range(0, len(message)):
            if message[i] == '.':
                self.device.letter(id, position - 1, message[i-1], dot=True)
            else:    
                self.device.letter(id, position, message[i])
                position += 1
  
    def showChar(self, id, postion, len, char):
        for i in range(0, len - 1):
            self.device.letter(id, position + i, char)
            
    def message(self, id, message):
        self.device.clear()
        for i in range(1,len(message)+1):
            self.device.letter(id, i, message[i-1])
            
    def clear(self,id):
        self.device.clear()
    