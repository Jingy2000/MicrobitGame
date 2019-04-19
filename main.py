from player_and_bullet import *
from pygame import K_w, K_a, K_s, K_d, K_UP, K_DOWN, K_LEFT, K_RIGHT, key
from display import display

r_A = K_w
r_B = K_s
r_L = K_a
r_R = K_d

b_A = K_UP
b_B = K_DOWN
b_L = K_LEFT
b_R = K_RIGHT


# ----------------------------MAIN--------------------------------
def main():
    player_red = Player(0)
    player_blue = Player(600)  # 地图高度这个参数
    bullet_list_red = []
    bullet_list_blue = []

    r_A_down = False
    b_A_down = False

    while player_blue.is_alive() and player_red.is_alive():
        # 接受指令
        key_pressed = key.get_pressed()

        # 人物移动和射击
        if key_pressed[r_A]:
            r_A_down = True
            player_red.power.update()
        else:
            if r_A_down:
                for bullet in player_red.attack():
                    bullet_list_red.append(bullet)
            r_A_down = False

        if key_pressed[r_L]:
            player_red.state = 'l'
        if key_pressed[r_R]:
            player_red.state = 'r'
        if (key_pressed[r_L]) and (key_pressed[r_R]):
            player_red.state = 's'

        player_red.move()

        # 子弹的运动
        for bullet in bullet_list_red:
            bullet.move()
        for bullet in bullet_list_blue:
            bullet.move()

        # 子弹出屏判定
        pass

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


# 当前程序为主程序时调用
if __name__ == "__main__":
    main()
