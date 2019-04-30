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


def getValue(ser):
    joypadKey = (0, 0, 0, 0, 0)
    joypadStick = (0, 0)
    temp = str(ser.read(500))
    values = temp.split('\\n')
    if len(values) == 1 or len(temp) < 30:  # 传输的值要足够长才有效！
        return joypadStick, joypadKey
    values = values[-2]  # 最后一个不是想要的
    joypadStick = re.findall(r"-?\d+", values.split('&')[0])  # x，y
    joypadStick = tuple(map(int, joypadStick))
    joypadKey = filter(str.isdigit, values.split('&')[1])  # 手柄，上，下，左，右
    joypadKey = tuple(map(int, joypadKey))
    return joypadStick, joypadKey


# ----------------------------MAIN--------------------------------
def main():
    player_red = Player(20, 90)
    player_blue = Player(580, 270)  # 地图高度这个参数
    bullet_list_red = []
    bullet_list_blue = []

    r_A_down = False
    b_A_down = False

    init()

    FPSclock = time.Clock()
    ser = serial.Serial('COM3', 9600, timeout=0)

    while player_blue.is_alive() and player_red.is_alive():
        FPSclock.tick(50)
        # 接受指令
        key_pressed = key.get_pressed()
        if key_pressed[K_ESCAPE]:
            break

        # 读取手柄指令
        joypadStick, joypadKey = getValue(ser)

        # 人物射击
        if joypadKey[3]:
            r_A_down = True
            player_red.power.update()
        else:
            if r_A_down:
                for bullet in player_red.attack():
                    bullet_list_red.append(bullet)
            r_A_down = False

        #  移动
        player_red.setDir(joypadStick)

        # if key_pressed[b_A]:
        #     b_A_down = True
        #     player_blue.power.update()
        # else:
        #     if b_A_down:
        #         for bullet in player_blue.attack():
        #             bullet_list_blue.append(bullet)
        #     b_A_down = False
        #
        # if key_pressed[b_L]:
        #     player_blue.state = 'l'
        # if key_pressed[b_R]:
        #     player_blue.state = 'r'
        # if (key_pressed[b_L] and key_pressed[b_R]) or (not key_pressed[b_L] and not key_pressed[b_R]):
        #     player_blue.state = 's'

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
