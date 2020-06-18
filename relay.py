# 16 Relay board 
#  https://techiesms.com/iot-projects/esp32-projects/16-appliances-home-automation-using-esp32-over-internet/

import machine
import time

map1 = [15,2,4,18,19,21,22,23,32,33,25,26,27,14,12,13]
map = [26,27,14,12,13, 21,19,18,4,2, 15,22,23,32,33, 25]
#p0 = machine.Pin(13, machine.Pin.OUT)
#p1 = machine.Pin(2, machine.Pin.OUT)
# while True:
	# p0.value(0)
	# p1.value(0)
	# time.sleep(.5)
	# p0.value(1)
	# p1.value(1)
	# time.sleep(.5)
	# print("Loop")

pin = []
j = 0
print("Start")
for i in map:
	pin.append(machine.Pin(i, machine.Pin.OUT))
	pin[j].value(0)
	print(j,i)
	j += 1
while True:
	for i in map:
		print(i, "on")
		time.sleep(.1)
		pin[i].value(1)
	for i in map:
		print(i, "off")
		time.sleep(.5)
		pin[i].value(0)

