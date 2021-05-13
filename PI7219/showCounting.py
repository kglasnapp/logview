# Example for seven segment displays to display date and time on a 8 digit 7 segment display with a max7219 chip

import time
import sys
import Display
def main():
    # create seven segment device
    print("Start Test Display")
    print("Ensure that self._spi.max_speed_hz = 1000000 is set in led.py")
    print("Ensure that spi is enabled in sudo raspi-config")
    disp = Display.Display()
    disp.message(0, "HELLO")
    time.sleep(2)
    disp.clear(0)
    while(True):
      for i in range(0,9999):
        disp.showInt(0,1,i)
        disp.showInt(0,5,9999-i)

if __name__ == '__main__':
    main()

