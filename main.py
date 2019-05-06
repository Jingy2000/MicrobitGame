from player_and_bullet import *
from pygame import K_w, K_a, K_s, K_d, K_UP, \
    K_DOWN, K_LEFT, K_RIGHT, key, time, init, K_ESCAPE
from display import display, do_exit
import serial
import re

SEP = bytes([9])

b_A = K_w
b_B = K_s
b_L = K_a
b_R = K_d

r_A = K_UP
r_B = K_DOWN
r_L = K_RIGHT
r_R = K_LEFT


# 获取手柄数据
def conv(data):
    if len(data) != 9:
        return None, None
    x, y = data[5] + data[6] / 256, data[7] + data[8] / 256
    x = round(x - 8)
    y = round(8 - y)
    return [x, y], data[:5]


def getValue(ser):
    temp = ser.read(100)  # 开始的时候mb一定要重启，避免垃圾数据的残留，就要卡很久了....
    valueList = temp.split(b'\n')[:-1]  # 舍弃最后一个残缺的
    if not valueList:  # 如果是空的，说明数据get的少了
        return
    values = valueList[-1]
    if not SEP in values:
        return
    data1 = list(values.split(SEP)[0])
    data2 = list(values.split(SEP)[1])
    r_joypadStick, r_joypadKey = conv(data1)
    b_joypadStick, b_joypadKey = conv(data2)
    if None in (r_joypadStick, r_joypadKey, b_joypadStick, b_joypadKey):
        print("Bad")
        return None
    print(r_joypadStick, r_joypadKey, b_joypadStick, b_joypadKey)
    return r_joypadStick, r_joypadKey, b_joypadStick, b_joypadKey


# ----------------------------MAIN--------------------------------
def main():
    player_red = P_Square(20, 90)
    player_blue = P_Round(580, 270)  # 地图高度这个参数
    player_red.set_enemy(player_blue)
    player_blue.set_enemy(player_red)

    player_red.cards.append(C_flower(player_red))
    player_blue.cards.append(C_chain(player_blue))

    bullet_list_red = []
    bullet_list_blue = []

    r_A_down = False
    b_A_down = False

    init()

    FPSclock = time.Clock()
    ser = serial.Serial('COM3', baudrate=19200, timeout=0)

    last = [[0, 0], [0, 0, 0, 0, 0], [0, 0], [0, 0, 0, 0, 0]]

    while player_blue.is_alive() and player_red.is_alive():
        FPSclock.tick(10)
        # 接受指令
        key_pressed = key.get_pressed()
        if key_pressed[K_ESCAPE]:
            break

        # 读取手柄指令
        values = getValue(ser)
        if values == None:
            values = last
        r_joypadStick, r_joypadKey, b_joypadStick, b_joypadKey = values
        last = values

        # 人物射击
        if r_joypadKey[3]:
            r_A_down = True
            bs = player_red.power_up()
            if bs != None:
                for bullet in bs:
                    bullet_list_red.append(bullet)
        else:
            if r_A_down:
                bs = player_red.attack()
                if bs != None:
                    for bullet in bs:
                        bullet_list_red.append(bullet)
            r_A_down = False

        if b_joypadKey[3]:
            b_A_down = True
            bs = player_blue.power_up()
            if bs != None:
                for bullet in bs:
                    bullet_list_blue.append(bullet)
        else:
            if b_A_down:
                bs = player_blue.attack()
                if bs != None:
                    for bullet in bs:
                        bullet_list_blue.append(bullet)
            b_A_down = False

        #  移动
        player_red.setDir(r_joypadStick)
        player_blue.setDir(b_joypadStick)

        player_red.move()
        player_blue.move()

        # 子弹的运动
        for bullet in bullet_list_red:
            bullet.move()
        for bullet in bullet_list_blue:
            bullet.move()

        # 子弹出屏判定
        for bullet in bullet_list_blue:
            x = bullet.getPos()[0]
            y = bullet.getPos()[1]
            if x > 400 or x < 0 or y < 0 or y > 800:
                bullet_list_blue.remove(bullet)
        for bullet in bullet_list_red:
            x = bullet.getPos()[0]
            y = bullet.getPos()[1]
            if x > 400 or x < 0 or y < 0 or y > 800:
                bullet_list_red.remove(bullet)

        # *子弹之间的碰撞判定
        pass

        # *子弹存活判定(?)
        pass

        # 子弹与人物的碰撞判定
        for bullet in bullet_list_red:
            if bullet.hit(player_blue):
                bullet_list_red.remove(bullet)
        for bullet in bullet_list_blue:
            if bullet.hit(player_red):
                bullet_list_blue.remove(bullet)

        # 调用绘图
        display(player_red, player_blue, bullet_list_red, bullet_list_blue)
        do_exit()

    if not player_blue.is_alive():
        print('blue die!')
    if not player_red.is_alive():
        print('red die!')


# 当前程序为主程序时调用
if __name__ == "__main__":
    main()
