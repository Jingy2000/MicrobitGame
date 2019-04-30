import serial
import time

ser = serial.Serial('COM3', 9600, timeout=0)
while True:
    time.sleep(0.2)
    temp = str(ser.read(1000))
    values = temp.split('\\n')
    if len(values) == 1 or len(temp) < 10:
        continue
    values = values[-2]
    print(values)
# hello = ser.read(10)
# hello2 = ser.read(10)
