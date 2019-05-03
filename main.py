from player_and_bullet import *
from pygame import K_w, K_a, K_s, K_d, K_UP, \
    K_DOWN, K_LEFT, K_RIGHT, key, time, init, K_ESCAPE
from display import display, do_exit
import serial
import re

b_A = K_w
b_B = K_s
b_L = K_a
b_R = K_d

r_A = K_UP
r_B = K_DOWN
r_L = K_RIGHT
r_R = K_LEFT


# 获取手柄数据
def getValue(ser):
    temp = str(ser.read(50000))[2:-1]  # 去掉开头的b'和结尾的’
    values = temp.split('\\n')
    for i in range(0, len(values)):
        v = values[-i - 1]  # 从后往前匹配
        if re.match(r"\(-?\d+, -?\d+\)&\(\d, \d, \d, \d, \d\)&\(-?\d+, -?\d+\)&\(\d, \d, \d, \d, \d\)", v):
            r_joypadStick = tuple(map(int, re.findall(r"-?\d+", v.split('&')[0])))  # x，y
            r_joypadKey = tuple(map(int, filter(str.isdigit, v.split('&')[1])))  # 手柄，上，下，左，右
            b_joypadStick = tuple(map(int, re.findall(r"-?\d+", v.split('&')[2])))  # x，y
            b_joypadKey = tuple(map(int, filter(str.isdigit, v.split('&')[3])))  # 手柄，上，下，左，右
            print(str(r_joypadStick) + '&' + str(r_joypadKey) + '&' + str(b_joypadStick) + '&' + str(b_joypadKey))  # for test
            return r_joypadStick, r_joypadKey, b_joypadStick, b_joypadKey
    joypadKey = (0, 0, 0, 0, 0)
    joypadStick = (0, 0)
    return joypadStick, joypadKey, joypadStick, joypadKey


# ----------------------------MAIN--------------------------------
def main():
    player_red = Player(20, 90)
    player_blue = Player(550, 270)  # 地图高度这个参数
    bullet_list_red = []
    bullet_list_blue = []

    r_A_down = False
    b_A_down = False

    init()

    FPSclock = time.Clock()
    ser = serial.Serial('COM3', 9600, timeout=0)

    while player_blue.is_alive() and player_red.is_alive():
        time_passed = FPSclock.tick() / 1000
        # 接受指令
        key_pressed = key.get_pressed()
        if key_pressed[K_ESCAPE]:
            break

        # 读取手柄指令
        r_joypadStick, r_joypadKey, b_joypadStick, b_joypadKey = getValue(ser)

        # 人物射击
        if r_joypadKey[3]:
            r_A_down = True
            player_red.power.update()
        else:
            if r_A_down:
                for bullet in player_red.attack():
                    bullet_list_red.append(bullet)
            r_A_down = False

        if b_joypadKey[3]:
            b_A_down = True
            player_blue.power.update()
        else:
            if b_A_down:
                for bullet in player_blue.attack():
                    bullet_list_blue.append(bullet)
            b_A_down = False

        #  移动
        player_red.setDir(r_joypadStick)
        player_blue.setDir(b_joypadStick)

        for i in range(time_passed):
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


# 当前程序为主程序时调用
if __name__ == "__main__":
    main()
