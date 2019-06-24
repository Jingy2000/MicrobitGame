from player_and_bullet import *
from pygame import K_w, K_a, K_s, K_d, K_f, K_g, K_UP, QUIT, \
    K_DOWN, K_LEFT, K_RIGHT, K_PERIOD, K_COMMA, key, time, init, K_ESCAPE, KEYDOWN, KEYUP
from pygame import event
from display import display, do_exit, display_init
from pynput import keyboard
from functools import reduce
import socket

# import serial
# import re

line_mode = True
is_server = True

Smooth_Multi = 1
Player_Maxspeed = 10 / Smooth_Multi

if line_mode:
    b_A = 'z'
    b_B = 'x'
    b_L = 'left'
    b_R = 'right'
    b_U = 'up'
    b_D = 'down'
    b_S = 'shift'

    r_A = 'RA'
    r_B = 'RB'
    r_L = 'RL'
    r_R = 'RR'
    r_U = 'RU'
    r_D = 'RD'
    r_S = 'RS'

else:
    b_A = 'f'
    b_B = 'g'
    b_L = 'a'
    b_R = 'd'
    b_U = 'w'
    b_D = 's'
    b_S = 'c'

    r_A = ','
    r_B = '.'
    r_L = 'left'
    r_R = 'right'
    r_U = 'up'
    r_D = 'down'
    r_S = '/'

# l_A = 'z'
# l_B = 'x'
# l_L = 'left'
# l_R = 'right'
# l_U = 'up'
# l_D = 'down'
# l_S = 'shift'



l_keys = {'z': 0, 'x': 1, 'left': 2, 'right': 3, 'up': 4, 'down': 5, 'shift': 6}

# using_keys = [K_w, K_a, K_s, K_d, K_f, K_g, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_PERIOD, K_COMMA]

using_keys = ['w', 'a', 's', 'd', 'f', 'g', ',', '.', 'up', 'down', 'left', 'right', 'c', '/', 'shift', 'z', 'x']
now_pressing = {k: 0 for k in using_keys}


def line_link():
    if is_server:
        s = socket.socket()  # 创建 socket 对象
        port = 21001  # 设置端口
        s.bind(('10.3.160.107', port))  # 绑定端口
        s.listen(1)  # 等待客户端连接
        print('waiting for connection...')
        c, addr = s.accept()  # 建立客户端连接
        print('connection created!', addr)
        c.send(b'welcome!')
        return c
    else:
        port = 47338  # 设置端口号
        s = socket.socket()
        s.connect(('memento.51vip.biz', port))
        s.recv(1024)
        print('connection created!')
        return s


def getbit(n, i):
    return (n % 2 ** (i + 1)) // 2 ** i


def key_to_byte(my_keys):
    ktb = [b_A, b_B, b_L, b_R, b_U, b_D, b_S]
    b_lst = [my_keys[k] for k in ktb]
    n = reduce(lambda x, y: x * 2 + y, b_lst)
    return bytes([n])


def byte_to_key(enemy_bytes):
    btk = [r_A, r_B, r_L, r_R, r_U, r_D, r_S]
    enemy_keys = {}
    n = ord(enemy_bytes.decode())
    for i in range(7):
        enemy_keys[btk[i]] = getbit(n, i)
    return enemy_keys


def update_by_net(link, my_keys):
    my_bytes = key_to_byte(my_keys)
    link.send(my_bytes)
    enemy_bytes = link.recv(1024)
    enemy_keys = byte_to_key(enemy_bytes)
    enemy_keys.update(my_keys)
    return enemy_keys


def on_press(key):
    global now_pressing
    k = None
    if isinstance(key, keyboard.KeyCode):
        k = key.char
    elif isinstance(key, keyboard.Key):
        k = key.name
    now_pressing[k] = 1


def on_release(key):
    global now_pressing
    k = None
    if isinstance(key, keyboard.KeyCode):
        k = key.char
    elif isinstance(key, keyboard.Key):
        k = key.name
    now_pressing[k] = 0


# 获取手柄数据
# def conv(data):
#     if len(data) != 9:
#         print('aaa' + str(data), end='')
#         return None, None
#     x, y = data[5] + data[6] / 256, data[7] + data[8] / 256
#     x = round(x - 8)
#     y = round(8 - y)
#     r = (x * x + y * y) ** 0.5
#     if r <= 4:
#         x = 0
#         y = 0
#     else:
#         x = x / r * 8
#         y = y / r * 8
#     return [x, y], data[:5]


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
    player_red = P_Shield(20, 90)
    player_blue = P_Square(580, 270)  # 地图高度这个参数
    player_red.set_enemy(player_blue)
    player_blue.set_enemy(player_red)

    player_red.cards.append(C_lock(player_red))
    player_blue.cards.append(C_spark_aim(player_blue))

    bullet_list_red = []
    bullet_list_blue = []

    r_A_down = False
    b_A_down = False

    # r_vx = 0
    # r_vy = 0
    # b_vx = 0
    # b_vy = 0
    link = None
    if line_mode:
        link = line_link()

    init()
    display_init()

    # key.set_repeat(0, 50)

    FPSclock = time.Clock()
    # ser = serial.Serial('COM4', baudrate=19200, timeout=0)
    #
    # last = [[0, 0], [0, 0, 0, 0, 0], [0, 0], [0, 0, 0, 0, 0]]

    max_buffer = 3
    pressing_buffer = []

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        # listener.run()
        while player_blue.is_alive() and player_red.is_alive():
            FPSclock.tick(30 * Smooth_Multi)
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

            if line_mode:
                # 这里交换信息
                link_pressing = update_by_net(link)

                pressing_buffer.append(link_pressing)
                for i in range(max_buffer):
                    if i == len(pressing_buffer) - 1:
                        break
                    pressing_buffer[i] = pressing_buffer[i + 1].copy()
                if len(pressing_buffer) == max_buffer + 1:
                    pressing_buffer.pop()
                pressing = pressing_buffer[0]
            else:
                pressing = now_pressing

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
            if pressing[r_S]:
                r_vx *= 0.5
                r_vy *= 0.5

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
            if pressing[b_S]:
                b_vx *= 0.5
                b_vy *= 0.5

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

            # 移动
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
                if x > 400 or x < 0 or y < 0 or y > 600:
                    bullet_list_blue.remove(bullet)
            for bullet in bullet_list_red:
                x = bullet.getPos()[0]
                y = bullet.getPos()[1]
                if x > 400 or x < 0 or y < 0 or y > 600:
                    bullet_list_red.remove(bullet)

            # *子弹之间的碰撞判定
            pass

            # 消弹圈

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

    # 把这个改成更科学一点的显示
    if not player_blue.is_alive():
        print('red die!')
    if not player_red.is_alive():
        print('blue die!')


# 当前程序为主程序时调用
if __name__ == "__main__":
    main()
