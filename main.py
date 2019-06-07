from player_and_bullet import *
from pygame import K_w, K_a, K_s, K_d, K_f, K_g, K_UP, QUIT, \
    K_DOWN, K_LEFT, K_RIGHT, K_PERIOD, K_COMMA, key, time, init, K_ESCAPE, KEYDOWN, KEYUP
from pygame import event
from display import display, do_exit
from pynput import keyboard

# import serial
# import re

SEP = bytes([9])

Player_Maxspeed = 8

# b_A = K_f
# b_B = K_g
# b_L = K_a
# b_R = K_d
# b_U = K_w
# b_D = K_s
#
# r_A = K_COMMA
# r_B = K_PERIOD
# r_L = K_LEFT
# r_R = K_RIGHT
# r_U = K_UP
# r_D = K_DOWN

b_A = 'f'
b_B = 'g'
b_L = 'a'
b_R = 'd'
b_U = 'w'
b_D = 's'

r_A = ','
r_B = '.'
r_L = 'left'
r_R = 'right'
r_U = 'up'
r_D = 'down'

# using_keys = [K_w, K_a, K_s, K_d, K_f, K_g, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_PERIOD, K_COMMA]
using_keys = ['w', 'a', 's', 'd', 'f', 'g', ',', '.', 'up', 'down', 'left', 'right']
pressing = {k: 0 for k in using_keys}


def on_press(key):
    global pressing
    k = None
    if isinstance(key, keyboard.KeyCode):
        k = key.char
    elif isinstance(key, keyboard.Key):
        k = key.name
    pressing[k] = 1


def on_release(key):
    global pressing
    k = None
    if isinstance(key, keyboard.KeyCode):
        k = key.char
    elif isinstance(key, keyboard.Key):
        k = key.name
    pressing[k] = 0


# 获取手柄数据
def conv(data):
    if len(data) != 9:
        print('aaa' + str(data), end='')
        return None, None
    x, y = data[5] + data[6] / 256, data[7] + data[8] / 256
    x = round(x - 8)
    y = round(8 - y)
    r = (x * x + y * y) ** 0.5
    if r <= 4:
        x = 0
        y = 0
    else:
        x = x / r * 8
        y = y / r * 8
    return [x, y], data[:5]


# def getValue(ser):
#     temp = ser.read(100)  # 开始的时候mb一定要重启，避免垃圾数据的残留，就要ka....
#     valueList = temp.split(b'\n')[:-1]  # 舍弃最后一个残缺的
#     if not valueList:  # 如果是空的，说明数据get的少了
#         print('empty valuelist: ' + str(valueList))
#         return
#     values = valueList[-1]
#     if not SEP in values:
#         print('no sep: ' + str(values))
#         return
#     data1 = list(values.split(SEP)[0])
#     data2 = list(values.split(SEP)[1])
#     r_joypadStick, r_joypadKey = conv(data1)
#     b_joypadStick, b_joypadKey = conv(data2)
#     if None in (r_joypadStick, r_joypadKey, b_joypadStick, b_joypadKey):
#         print("Bad")
#         return None
#     print(r_joypadStick, r_joypadKey, b_joypadStick, b_joypadKey)
#     return r_joypadStick, r_joypadKey, b_joypadStick, b_joypadKey


# ----------------------------MAIN--------------------------------
def main():
    player_red = P_Square(20, 90)
    player_blue = P_Square(580, 270)  # 地图高度这个参数
    player_red.set_enemy(player_blue)
    player_blue.set_enemy(player_red)

    player_red.cards.append(C_spark(player_red))
    player_blue.cards.append(C_spark(player_blue))

    bullet_list_red = []
    bullet_list_blue = []

    r_A_down = False
    b_A_down = False

    # r_vx = 0
    # r_vy = 0
    # b_vx = 0
    # b_vy = 0

    init()

    # key.set_repeat(0, 50)

    FPSclock = time.Clock()
    # ser = serial.Serial('COM4', baudrate=19200, timeout=0)
    #
    # last = [[0, 0], [0, 0, 0, 0, 0], [0, 0], [0, 0, 0, 0, 0]]

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        # listener.run()
        while player_blue.is_alive() and player_red.is_alive():
            FPSclock.tick(15)
            key.set_repeat(10, 10)
            # 接受指令
            # pressing = key.get_pressed()
            # if key_pressed[K_ESCAPE]:
            #     break

            # 读取键盘指令
            # for eve in event.get():
            #     print(eve)
            #     if eve.type == KEYDOWN:  # 键被按下
            #         pressing[eve.key] = 1

            # # elif eve.type == KEYUP:
            # #     pressing[eve.key] = 0
            # if eve.type == QUIT:
            #     exit()

            # 移动处理

            r_vx = 0
            r_vy = 0
            b_vx = 0
            b_vy = 0

            if pressing[r_U] and not pressing[r_D]:
                r_vy = -Player_Maxspeed
            elif pressing[r_D] and not pressing[r_U]:
                r_vy = Player_Maxspeed
            if pressing[r_L] and not pressing[r_R]:
                r_vx = -Player_Maxspeed
            elif pressing[r_R] and not pressing[r_L]:
                r_vx = Player_Maxspeed
            if (r_vx != 0) and (r_vy != 0):
                r_vx *= 0.5 ** 0.5
                r_vy *= 0.5 ** 0.5

            if pressing[b_U] and not pressing[b_D]:
                b_vy = -Player_Maxspeed
            elif pressing[b_D] and not pressing[b_U]:
                b_vy = Player_Maxspeed
            if pressing[b_L] and not pressing[b_R]:
                b_vx = -Player_Maxspeed
            elif pressing[b_R] and not pressing[b_L]:
                b_vx = Player_Maxspeed
            if (b_vx != 0) and (b_vy != 0):
                b_vx *= 0.5 ** 0.5
                b_vy *= 0.5 ** 0.5

            # 人物基本攻击和蓄力攻击
            if pressing[r_A]:
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

            if pressing[b_A]:
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

            # card的子弹输出
            bs = player_red.run_card()
            if bs != None:
                for bullet in bs:
                    bullet_list_red.append(bullet)
            bs = player_blue.run_card()
            if bs != None:
                for bullet in bs:
                    bullet_list_blue.append(bullet)

            # card释放
            if pressing[r_B]:
                player_red.use_card(0)
            if pressing[b_B]:
                player_blue.use_card(0)

            #  移动
            # print(pressing)
            player_red.setDir((r_vx, r_vy))
            player_blue.setDir((b_vx, b_vy))

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
            for bullet in bullet_list_red:
                if not bullet.is_alive():
                    bullet_list_red.remove(bullet)
            for bullet in bullet_list_blue:
                if not bullet.is_alive():
                    bullet_list_blue.remove(bullet)

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
        print('red die!')
    if not player_red.is_alive():
        print('blue die!')


# 当前程序为主程序时调用
if __name__ == "__main__":
    main()
