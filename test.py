import serial
import time
import re

ser = serial.Serial('COM3', 9600, timeout=0)
while True:
    time.sleep(0.2)
    temp = str(ser.read(10000))[2:-1]  # 去掉开头的b'和结尾的’
    values = temp.split('\\n')
    for i in range(len(values)):
        v = values[-i - 1]  # 从后往前匹配
        if re.match(r"\(-?\d+, -?\d+\)&\(\d, \d, \d, \d, \d\)&\(-?\d+, -?\d+\)&\(\d, \d, \d, \d, \d\)", v):
            r_joypadStick = tuple(map(int, re.findall(r"-?\d+", v.split('&')[0])))  # x，y
            r_joypadKey = tuple(map(int, filter(str.isdigit, v.split('&')[1])))  # 手柄，上，下，左，右
            b_joypadStick = tuple(map(int, re.findall(r"-?\d+", v.split('&')[2])))  # x，y
            b_joypadKey = tuple(map(int, filter(str.isdigit, v.split('&')[3])))  # 手柄，上，下，左，右
            print(str(r_joypadStick) + '&' + str(r_joypadKey) + '&' + str(b_joypadStick) + '&' + str(b_joypadKey))  # for test
        else:
            print("?")

    print(values)
# hello = ser.read(10)
# hello2 = ser.read(10)
