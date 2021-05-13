#!/usr/bin/env python

"""
Example for seven segment displays to display date and time on a 8 digit 7 segment display with a max7219 chip
"""

import time
import random
from datetime import datetime

import max7219.led as led


def date(device, deviceId):
    """
    Display current date on device.
    """
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year - 2000

    # Set day
    device.letter(deviceId, 5, int(day / 10))     # Tens
    device.letter(deviceId, 4, day % 10)          # Ones
    device.letter(deviceId, 6, '-')               # dash
    # Set month
    device.letter(deviceId, 8, int(month / 10))   # Tens
    device.letter(deviceId, 7, month % 10)        # Ones
    device.letter(deviceId, 3, '-')               # dash
    # Set year
    device.letter(deviceId, 2, int(year / 10))    # Tens
    device.letter(deviceId, 1, year % 10)         # Ones


def clock(device, deviceId, seconds):
    """
    Display current time on device.
    """
    for _ in range(seconds):
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        dot = second % 2 == 0                # calculate blinking dot
        # Set hours
        device.letter(deviceId, 4, int(hour / 10))     # Tens
        device.letter(deviceId, 3, hour % 10, dot)     # Ones
        # Set minutes
        device.letter(deviceId, 2, int(minute / 10))   # Tens
        device.letter(deviceId, 1, minute % 10)        # Ones
        device.letter(deviceId, 8, ' ')
        device.letter(deviceId, 7, ' ')
        device.letter(deviceId, 6, ' ')
        device.letter(deviceId, 5, ' ')
        time.sleep(1)


def main():
    # create seven segment device
    device = led.sevensegment(cascaded=1)
    for i in range(1,9):
        device.letter(0,i,str(i))
    time.sleep(10)
    # Digit futzing
    #for x in range(0, 4):
    #    date(device, 0)
    #    time.sleep(5)
    #    clock(device, 0, seconds=5)
    print('Clear device...')
    device.clear()
    time.sleep(1)

if __name__ == '__main__':
    main()
